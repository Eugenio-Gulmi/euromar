"""Control de calidad de fotos: rasgos de la ficha, especie, defectos de IA y texto visible (OCR).

Uso: python3 fotos/control.py <salida.json> <imagen>[=<archivo de prompts.py>] ...
Si no se indica el archivo, se usa el nombre de la imagen (sin _v1/_v2). Sin ficha, solo revisa
defectos y texto visible. Revisor: gemini-3.1-pro-preview (clave GEMINI_API_KEY_LIBROS).
"""
import base64, io, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

sys.path.insert(0, os.path.expanduser("~/dev/eugenio/consulting/ricardo-gulminelli-libros/scripts"))
sys.path.insert(0, os.path.dirname(__file__))
from video_ia import post          # noqa: E402
from prompts import FOTOS          # noqa: E402

MODELO = "gemini-3.1-pro-preview"
FICHA = {os.path.splitext(f["archivo"])[0]: f for f in FOTOS}
# Fotos viejas de la web con nombre distinto al del reemplazo
ALIAS = {"langostinos": "langostinos-inicio",
         "productos-empanados-mar-02-bastones-merluza-1-960x640": "apanado-bastones",
         "productos-empanados-mar-03-rabas-960x640": "apanado-rabas",
         "productos-empanados-mar-06-filet-merluza-a-la-romana-960x640": "apanado-romana",
         "productos-empanados-mar-05-formitas-de-merluza-960x640": "apanado-formitas"}

INSTRUCCION = """You are a strict ichthyologist and photo-quality reviewer for a seafood exporter's website.
Customers are professional fish buyers: any anatomical error is unacceptable.

EXPECTED SUBJECT (from the FishBase-based brief):
{ficha}

Review the image and answer in JSON with these keys (write values in Spanish):
- "rasgos": list of objects {{"rasgo": short trait from the brief, "estado": "ok" | "mal" | "no se ve", "nota": short}}.
  Include EVERY diagnostic trait in the brief (fins, mouth, tail shape, colours, spots/stripes, size, composition).
- "especie_reconocible": true/false — would a fish buyer recognise it as the stated species?
- "parece_otra": name of the species it looks like instead, or "".
- "defectos_ia": list of anatomical or physical errors typical of AI images (extra/missing/duplicated fins,
  fused bodies, wrong number of eyes, deformed mouth or gills, impossible shapes, melted or floating objects,
  inconsistent lighting), or [].
- "texto_visible": transcribe EVERY visible text, number, logo, watermark, brand or boat name (OCR), or [].
- "veredicto": "OK" (publishable as is), "REVISAR" (minor issue) or "MAL" (wrong species or clear error).
- "motivo": one sentence in Spanish explaining the verdict.
Be strict: if a trait in the brief is wrong or missing, it cannot be "OK"."""

SIN_FICHA = ("No species brief: this is a general website photo (people, port, landscape or product). "
             "Only check for AI defects, visible text/logos/watermarks and overall photographic quality.")


def b64(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((1280, 1280))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()


def revisar(arg):
    path, _, clave = arg.partition("=")
    base = clave or re.sub(r"_v\d+$", "", os.path.splitext(os.path.basename(path))[0])
    base = ALIAS.get(base, base)
    f = FICHA.get(base)
    texto = INSTRUCCION.format(ficha=f["prompt"] if f else SIN_FICHA)
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": b64(path)}},
                                    {"text": texto}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    try:
        r = post(f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent", body)
        txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"])
        out = json.loads(txt)
    except BaseException as e:
        out = {"veredicto": "ERROR", "motivo": str(e)[:200]}
    out.update(imagen=path, ficha=base if f else None)
    return out


if __name__ == "__main__":
    salida, args = sys.argv[1], sys.argv[2:]
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(revisar, args))
    json.dump(res, open(salida, "w"), ensure_ascii=False, indent=1)
    for r in res:
        print(f"{r['veredicto']:8} {os.path.basename(r['imagen']):60} {r.get('motivo', '')[:150]}")
