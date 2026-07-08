"""
Regenerate species images with dark-background realistic style.
Also upscale meluza negra.jpeg.
"""
import requests, base64, os, time
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

API_KEY = os.environ["XAI_API_KEY"]
OUT = Path("public/images")

# Style reference: dark slate/black surface, crushed ice, natural cold light,
# muted colors, real fish market/restaurant photography, NOT studio, NOT CGI
STYLE = (
    "on crushed ice on a dark black slate surface, dramatic natural side lighting, "
    "muted desaturated colors, real food photography, authentic fish market quality, "
    "gritty realistic texture, no artificial saturation, no CGI glow, "
    "shot on 35mm film camera, natural grain, dark moody background. No text."
)

SPECIES = [
    (
        "merluza.jpg",
        f"Three whole fresh Argentine Hake (Merluccius hubbsi) fish laid parallel {STYLE}"
    ),
    (
        "hoki.jpg",
        f"Two whole fresh Hoki fish (Macruronus magellanicus), elongated slender silver body {STYLE}"
    ),
    (
        "pescadilla.jpg",
        f"Two whole fresh Striped Weakfish (Cynoscion striatus / Pescadilla), silver fish with faint lateral stripes {STYLE}"
    ),
    (
        "pez-palo.jpg",
        f"One whole fresh Brazilian Flathead fish (Percophis brasiliensis / Pez Palo), elongated flattened body, pointed snout {STYLE}"
    ),
    (
        "salmon-blanco.jpg",
        f"One whole fresh Argentine Sandperch (Pseudopercis semifasciata / Salmon Blanco), elongated silver-white body {STYLE}"
    ),
    (
        "white-drum.jpg",
        f"One whole fresh White Drum fish (Plagioscion squamosissimus / Cuca), large silver fish with big scales {STYLE}"
    ),
    (
        "rape.jpg",
        f"Fresh Monkfish tail (Lophius gastrophysus / Rape) and thick white fillet showing firm white flesh {STYLE}"
    ),
    (
        "abadejo.jpg",
        f"One whole fresh Pink Cusk-eel (Genipterus blacodes / Abadejo), elongated pinkish-brown spotted eel-like fish {STYLE}"
    ),
    (
        "langostino.jpg",
        f"Pile of fresh wild Argentine Red Shrimp (Pleoticus muelleri / Langostinos Patagonicos), vivid coral-red color {STYLE}"
    ),
    (
        "calamar.jpg",
        f"Fresh Patagonian Squid (Illex argentinus / Calamar), two whole squid and cleaned white tubes {STYLE}"
    ),
    (
        "merluza-negra.jpg",
        f"Whole fresh Patagonian Toothfish (Dissostichus eleginoides / Merluza Negra), dark grey-black skin, large scaled deep-sea fish {STYLE}"
    ),
    (
        "atun.jpg",
        f"Two thick Yellowfin Tuna steaks (Thunnus albacares / Atun) showing deep ruby-red flesh, sashimi grade {STYLE}"
    ),
    (
        "salmon-atlantico.jpg",
        f"Whole Atlantic Salmon (Salmo salar) and one cross-section steak showing vivid orange-pink flesh {STYLE}"
    ),
    (
        "trucha.jpg",
        f"Two whole Rainbow Trout (Oncorhynchus mykiss / Trucha Arcoiris), iridescent pink-silver stripe along body {STYLE}"
    ),
    (
        "mahi-mahi.jpg",
        f"Fresh Mahi-Mahi / Dolphinfish (Coryphaena hippurus) fillet showing golden-green iridescent skin and white-pink flesh {STYLE}"
    ),
    (
        "corvina.jpg",
        f"Two whole fresh Whitemouth Croaker (Micropogonias furnieri / Corvina), silver fish with golden sheen {STYLE}"
    ),
    (
        "besugo.jpg",
        f"One whole fresh Red Porgy (Pagrus sedicem / Besugo), pinkish-red compact fish with spiny dorsal fin {STYLE}"
    ),
    (
        "raya.jpg",
        f"Fresh Skate Ray (Raja spp / Raya) displayed flat, top-down view showing diamond wing shape and mottled skin {STYLE}"
    ),
]

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def generate(filename, prompt):
    r = requests.post(
        "https://api.x.ai/v1/images/generations",
        headers=headers,
        json={"model": "grok-imagine-image", "prompt": prompt, "n": 1, "response_format": "b64_json"},
        timeout=60
    )
    if r.status_code == 429:
        print("  Rate limited, waiting 15s...")
        time.sleep(15)
        r = requests.post("https://api.x.ai/v1/images/generations", headers=headers,
                          json={"model": "grok-imagine-image", "prompt": prompt, "n": 1, "response_format": "b64_json"}, timeout=60)
    r.raise_for_status()
    return base64.b64decode(r.json()["data"][0]["b64_json"])

# --- 1. Upscale meluza negra.jpeg ---
print("Upscaling meluza negra.jpeg...")
src = Path("public/images/meluza negra.jpeg")
img = Image.open(src).convert("RGB")
# 3x upscale with LANCZOS
w, h = img.size
img_up = img.resize((w * 3, h * 3), Image.LANCZOS)
# Sharpen + contrast boost
img_up = ImageEnhance.Sharpness(img_up).enhance(2.0)
img_up = ImageEnhance.Contrast(img_up).enhance(1.2)
img_up = img_up.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
img_up.save(OUT / "merluza-negra-real.jpg", "JPEG", quality=92)
print(f"  OK -> merluza-negra-real.jpg ({(OUT / 'merluza-negra-real.jpg').stat().st_size // 1024} KB)")

# --- 2. Regenerate all species ---
total = len(SPECIES)
for i, (filename, prompt) in enumerate(SPECIES, 1):
    print(f"[{i}/{total}] {filename}")
    try:
        img_bytes = generate(filename, prompt)
        (OUT / filename).write_bytes(img_bytes)
        print(f"  OK ({len(img_bytes)//1024} KB)")
    except Exception as e:
        print(f"  ERROR: {e}")
    if i < total:
        time.sleep(2)

print("\nDone.")
