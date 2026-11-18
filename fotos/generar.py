"""Genera variantes de las fotos de fotos/prompts.py con Nano Banana (gemini-3.1-flash-image).

Uso: python3 fotos/generar.py <carpeta_salida> [variantes=2] [archivo1,archivo2,...]
Reusa video_ia.imagen() de ricardo-gulminelli-libros/scripts (clave GEMINI_API_KEY_LIBROS).
"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.expanduser("~/dev/eugenio/consulting/ricardo-gulminelli-libros/scripts"))
sys.path.insert(0, os.path.dirname(__file__))
from video_ia import imagen          # noqa: E402
import video_ia                      # noqa: E402
from prompts import FOTOS, ESTILO, ESTILO_PRODUCTO, ESTILO_REAL  # noqa: E402

# REAL=1: Nano Banana Pro + estilo de foto sin retocar (las tandas con flash se veían "de IA")
REAL = os.environ.get("REAL") == "1"
if REAL:
    video_ia.IMG_MODEL = "gemini-3-pro-image"
PRODUCTO_REAL = ESTILO_PRODUCTO + (" Unretouched photograph with a DSLR, soft window light, natural imperfections "
                                   "(uneven crumb, a few loose crumbs, light frost), fine sensor grain, no CGI look.")

salida = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
solo = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
os.makedirs(salida, exist_ok=True)

trabajos = [(f, v) for f in FOTOS if not solo or f["archivo"] in solo for v in range(1, n + 1)]


def uno(t):
    f, v = t
    base = os.path.splitext(f["archivo"])[0]
    destino = os.path.join(salida, f"{base}_v{v}.png")
    try:
        p = f["prompt"]
        if REAL:
            p = p.replace(ESTILO, ESTILO_REAL).replace(ESTILO_PRODUCTO, PRODUCTO_REAL)
        imagen(destino, p, "3:2")
        return f"ok    {destino}"
    except BaseException as e:          # imagen() puede hacer sys.exit
        return f"FALLO {base}_v{v}: {e}"


with ThreadPoolExecutor(4) as ex:
    for r in ex.map(uno, trabajos):
        print(r, flush=True)
print(f"{len(trabajos)} pedidos")
