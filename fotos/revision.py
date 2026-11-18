"""Cadena de revisores para las fotos de la web: cada foto pasa por 5 revisores independientes;
si alguno la rechaza, se corrige con sus notas y se vuelve a revisar (hasta 3 rondas).

Revisores (cada uno con su rol y modelo):
  taxonomo      gemini-3.1-pro-preview  rasgos de la ficha FishBase uno por uno
  comparador    gemini-3.1-pro-preview  contra una foto real de control (Wikimedia Commons, licencia libre)
  detector_ia   gemini-3.8-flash        ¿se nota que es IA? (piel plástica, hielo repetido, reflejos falsos)
  comprador     gemini-3.5-flash        comprador mayorista: ¿confiaría en esta foto? ¿sirve como tarjeta 3:2?
  ocr           gemini-3.1-pro-preview  texto/logos/marcas de agua y defectos anatómicos

Uso:
  python3 fotos/revision.py <carpeta_trabajo> <carpeta_candidatos> [archivo1,archivo2,...]
      candidatos = <base>_v1.png, <base>_v2.png... ; genera rondas nuevas en <carpeta_trabajo>/<base>/
  python3 fotos/revision.py --solo-revisar <salida.json> <imagen> ...   (revisa sin regenerar, p.ej. la web actual)
"""
import base64, glob, io, json, os, re, statistics, sys, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

sys.path.insert(0, os.path.expanduser("~/dev/eugenio/consulting/ricardo-gulminelli-libros/scripts"))
sys.path.insert(0, os.path.dirname(__file__))
import video_ia                                            # noqa: E402
from prompts import FOTOS, ESTILO, ESTILO_PRODUCTO, ESTILO_REAL   # noqa: E402
from desai import desai   # noqa: E402

video_ia.IMG_MODEL = "gemini-3-pro-image"
API = "https://generativelanguage.googleapis.com/v1beta/models"
# Revisores baratos (10-nov-2026): con gemini-3.1-pro + razonamiento la corrida costó ~US$40. Flash + razonamiento bajo.
MODELO_REV = os.environ.get("MODELO_REV", "gemini-3.8-flash")
USO = {"llamadas": 0, "entrada": 0, "salida": 0, "razonamiento": 0}
REFS = json.load(open(os.environ.get("REFS", "/private/tmp/claude-501/-Users-eugeniogulminellibarrau-dev/"
                       "bd72b5d5-9cdb-4e44-ba1e-ef90450c4f3d/scratchpad/refs/refs_multi.json")))
FICHA = {os.path.splitext(f["archivo"])[0]: f for f in FOTOS}
ALIAS = {"langostinos": "langostinos-inicio", "fish-merluza": "fish-merluza",
         "productos-empanados-mar-02-bastones-merluza-1-960x640": "apanado-bastones",
         "productos-empanados-mar-03-rabas-960x640": "apanado-rabas",
         "productos-empanados-mar-06-filet-merluza-a-la-romana-960x640": "apanado-romana",
         "productos-empanados-mar-05-formitas-de-merluza-960x640": "apanado-formitas"}
REF_DE = {"fish-merluza": "merluza", "langostinos-inicio": "langostino"}
PRODUCTO_REAL = ESTILO_PRODUCTO + (" Unretouched photograph with a DSLR, soft window light, natural imperfections "
                                   "(uneven crumb, a few loose crumbs, light frost), fine sensor grain, no CGI look.")

SALIDA = """Answer ONLY with one JSON object with keys:
"aprobado": true/false, "puntaje": 1-10, "problemas": [short strings in Spanish],
"arreglo": one precise instruction in English to fix the problems in a new version of the photo ("" if none).
Be strict: approve only if a demanding professional would publish it as is."""

ROLES = {
    "taxonomo": (MODELO_REV,
        "You are an ichthyologist. Check EVERY diagnostic trait of this brief against the photo (body shape, head, "
        "mouth, every fin, tail shape, colours, spots or stripes, size, composition). Any wrong or missing trait "
        "= not approved.\nBRIEF: {ficha}"),
    "comparador": (MODELO_REV,
        "The first {n} image(s) are verified references of the real species ({especie}): drawings, live or "
        "landed fish; ignore their background, pose and style. The LAST image is a candidate product photo. Is the last image unmistakably the "
        "same species? Compare body proportions, head and mouth, fins and tail, and colour pattern. List every "
        "difference that a fish buyer would notice."),
    "detector_ia": (MODELO_REV,
        "You are a forensic photo editor who spots AI-generated images. Does this look like a real camera "
        "photograph? Look for: plastic or waxy skin, too-perfect symmetry, painterly texture, repeated or melted "
        "ice cubes, impossible reflections, objects merging, inconsistent shadows, over-smooth gradients, "
        "uncanny eyes, too-clean scene. puntaje = realism 1-10; approve only if 8 or more."),
    "comprador": (MODELO_REV,
        "You are a senior frozen-seafood buyer for a Spanish distributor reviewing an Argentine exporter's "
        "website. The photo is shown as a 3:2 card with the product name overlaid at the bottom-left. Would you "
        "trust it as a real photo of this product ({titulo})? Is the product clear, appetising and professional, "
        "the framing right for the card, nothing distracting? Brief: {ficha}"),
    "ocr": (MODELO_REV,
        "Quality control. (1) OCR: put in an extra key \"texto\" a list with EVERY visible text, number, logo, "
        "watermark, label or boat name (empty list if none). (2) Find anatomical or physical defects: extra, missing or "
        "duplicated fins, eyes, legs or antennae; fused bodies; deformed mouth or gills; floating objects; "
        "cut-off product. Subject: {titulo}"),
}


def b64(path, lado=1280):
    im = Image.open(path).convert("RGB"); im.thumbnail((lado, lado))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def llamar(modelo, partes):
    for i in range(4):
        try:
            r = video_ia.post(f"{API}/{modelo}:generateContent", {"contents": [{"parts": partes}],
                    "generationConfig": {"responseMimeType": "application/json", "temperature": 0,
                                         "thinkingConfig": {"thinkingLevel": "low"}}})
            u = r.get("usageMetadata", {})
            USO["llamadas"] += 1; USO["entrada"] += u.get("promptTokenCount", 0)
            USO["salida"] += u.get("candidatesTokenCount", 0); USO["razonamiento"] += u.get("thoughtsTokenCount", 0)
            txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"])
            out = json.loads(txt)
            if isinstance(out, list):
                out = out[0] if out else {}
            return out
        except BaseException as e:
            err = str(e)[:200]; time.sleep(8 * (i + 1))
    return {"aprobado": False, "puntaje": 0, "problemas": [f"error del revisor: {err}"], "arreglo": ""}


def pasa(res):
    """Calibrado con 12 fotos reales (10-nov-2026): una foto real saca 7 de realismo y el control de anatomía
    marca 'defectos' hasta en peces reales. Reglas: especie correcta (taxónomo >= 7 y comparador aprueba),
    realismo >= 7 (como una foto real), comprador >= 6 y cero texto visible."""
    p = lambda k: (res.get(k) or {}).get("puntaje", 0) or 0
    ok = True
    if "taxonomo" in res:
        ok &= p("taxonomo") >= 7
    if "comparador" in res:
        ok &= bool(res["comparador"].get("aprobado"))
    ok &= p("detector_ia") >= 7 and p("comprador") >= 6
    ok &= not (res.get("ocr") or {}).get("texto")
    return bool(ok)


def revisar(path, base):
    f = FICHA.get(base)
    ficha = f["prompt"] if f else "General website photo (people, port or landscape): no species brief."
    titulo = base.replace("-", " ")
    ref = REFS.get(REF_DE.get(base, base))
    trabajos = {}
    for rol, (modelo, texto) in ROLES.items():
        if rol == "taxonomo" and not f:
            continue
        if rol == "comparador":
            if not ref:
                continue
            refs = ref[:4]
            partes = [b64(r["archivo"], 800) for r in refs] + [b64(path), {"text": texto.format(
                n=len(refs), especie=refs[0]["titulo"].split(" (")[0].replace("File:", "")) + "\n" + SALIDA}]
        else:
            partes = [b64(path), {"text": texto.format(ficha=ficha, titulo=titulo) + "\n" + SALIDA}]
        trabajos[rol] = (modelo, partes)
    with ThreadPoolExecutor(5) as ex:
        res = dict(zip(trabajos, ex.map(lambda t: llamar(*t), trabajos.values())))
    pts = [r.get("puntaje", 0) or 0 for r in res.values()]
    return {"imagen": path, "aprobada": pasa(res), "texto": res.get("ocr", {}).get("texto", []),
            "puntaje": round(statistics.mean(pts), 2) if pts else 0, "revisores": res}


def corregir(base, mejor, rev, carpeta, ronda):
    """Dos candidatos nuevos: la mejor editada con las notas y una generada de cero con las notas."""
    f = FICHA[base]
    notas = " ".join(r.get("arreglo", "") for r in rev["revisores"].values() if not r.get("aprobado"))
    prompt = f["prompt"].replace(ESTILO, ESTILO_REAL).replace(ESTILO_PRODUCTO, PRODUCTO_REAL)
    nuevos = []
    a = f"{carpeta}/{base}_r{ronda}_edit.png"
    try:
        video_ia.editar(a, "Edit this photograph so that it is a real, unretouched camera photo and fix these "
                           f"problems, keeping everything else: {notas} Reference brief: {prompt}", [mejor], "3:2")
        nuevos.append(desai(a, a[:-4] + ".jpg"))
    except BaseException as e:
        print("  fallo edición", base, str(e)[:120])
    b = f"{carpeta}/{base}_r{ronda}_nueva.png"
    try:
        video_ia.imagen(b, f"{prompt} MUST ALSO: {notas}", "3:2"); nuevos.append(desai(b, b[:-4] + ".jpg"))
    except BaseException as e:
        print("  fallo generación", base, str(e)[:120])
    return nuevos


def procesar(base, candidatos, trabajo, rondas=3):
    carpeta = f"{trabajo}/{base}"; os.makedirs(carpeta, exist_ok=True)
    historia = []
    for ronda in range(1, rondas + 1):
        with ThreadPoolExecutor(2) as ex:
            revs = list(ex.map(lambda p: revisar(p, base), candidatos))
        for r in revs:
            r["ronda"] = ronda
        historia += revs
        aprobadas = [r for r in historia if r["aprobada"]]
        print(f"{base:22} ronda {ronda}: " + ", ".join(
            f"{os.path.basename(r['imagen'])} {r['puntaje']}{'✓' if r['aprobada'] else '✗'}" for r in revs), flush=True)
        if aprobadas or ronda == rondas:
            break
        mejor = max(historia, key=lambda r: r["puntaje"])
        candidatos = corregir(base, mejor["imagen"], mejor, carpeta, ronda + 1)
        if not candidatos:
            break
    pool = [r for r in historia if r["aprobada"]] or historia
    elegida = max(pool, key=lambda r: r["puntaje"])
    out = {"foto": base, "elegida": elegida["imagen"], "aprobada": elegida["aprobada"], "historia": historia}
    json.dump(out, open(f"{carpeta}/revision.json", "w"), ensure_ascii=False, indent=1)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--solo-revisar":
        salida, imgs = sys.argv[2], sys.argv[3:]
        def una(p):
            b = re.sub(r"_(v\d+|r\d+_(edit|nueva))$", "", os.path.splitext(os.path.basename(p))[0])
            return revisar(p, ALIAS.get(b, b))
        with ThreadPoolExecutor(3) as ex:
            res = list(ex.map(una, imgs))
        json.dump(res, open(salida, "w"), ensure_ascii=False, indent=1)
        print("USO", USO)
        for r in res:
            pp = " ".join(f"{k[:4]}={v.get('puntaje')}" for k, v in r["revisores"].items())
            print(f"{'OK ' if r['aprobada'] else 'NO '} {r['puntaje']:4} {os.path.basename(r['imagen']):48} {pp} texto={r['texto']}")
        sys.exit()
    trabajo, cand = sys.argv[1], sys.argv[2]
    solo = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    bases = [os.path.splitext(f["archivo"])[0] for f in FOTOS if not solo or f["archivo"] in solo]
    os.makedirs(trabajo, exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        res = list(ex.map(lambda b: procesar(b, sorted(glob.glob(f"{cand}/{b}_v*.jpg")), trabajo), bases))
    json.dump([{k: r[k] for k in ("foto", "elegida", "aprobada")} for r in res],
              open(f"{trabajo}/elegidas.json", "w"), ensure_ascii=False, indent=1)
    print(f"\n{sum(r['aprobada'] for r in res)}/{len(res)} aprobadas por los 5 revisores")
