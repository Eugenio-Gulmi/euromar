"""Quita el 'brillo de IA': comprime luces, baja saturación y microcontraste, suaviza apenas y agrega grano real.
Uso: python3 fotos/desai.py <entrada> <salida.jpg>   (o importar desai())"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def desai(entrada, salida, ancho=1400, semilla=7):
    im = Image.open(entrada).convert("RGB")
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    # 1) microcontraste: mezclar 25% con versión suavizada (quita el "HDR")
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(2.2))).astype(np.float32) / 255
    a = a * 0.75 + blur * 0.25
    # 2) luces: curva que aplasta los reflejos especulares por encima de 0.72
    luz = a.mean(axis=2, keepdims=True)
    k = np.clip((luz - 0.72) / 0.28, 0, 1)
    a = a - k * (a - (0.72 + (a - 0.72) * 0.45)) * (a > 0.72)
    # 3) saturación -12% y negros apenas levantados (película / sensor)
    gris = a.mean(axis=2, keepdims=True)
    a = gris + (a - gris) * 0.88
    a = 0.025 + a * 0.965
    # 4) grano de luminancia
    rng = np.random.default_rng(semilla)
    g = rng.normal(0, 0.018, a.shape[:2])[..., None]
    a = np.clip(a + g * (0.6 + 0.4 * (1 - luz)), 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8))
    out = out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=35, threshold=2))
    out.save(salida, "JPEG", quality=82, optimize=True, progressive=True)
    return salida


if __name__ == "__main__":
    desai(sys.argv[1], sys.argv[2])
