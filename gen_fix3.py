"""Fix: reduce shine, add water droplets to 5 images"""
import requests, base64, os, time
from pathlib import Path

API_KEY = os.environ["XAI_API_KEY"]
OUT = Path("public/images")

STYLE = (
    "on crushed ice on a dark black slate surface, dramatic natural side lighting, "
    "muted desaturated colors, real food photography, authentic fish market quality, "
    "matte wet skin with small water droplets, gritty realistic texture, "
    "no artificial saturation, no CGI glow, no iridescent sheen, "
    "shot on 35mm film camera, natural grain, dark moody background. No text."
)

FIXES = [
    (
        "mahi-mahi.jpg",
        f"Fresh Mahi-Mahi / Dolphinfish (Coryphaena hippurus) whole fish, "
        f"muted golden-green skin, NO iridescent metallic glow, NO blue shimmer, "
        f"matte damp skin, small water droplets on body, realistic market fish color, "
        f"desaturated natural tones {STYLE}"
    ),
    (
        "corvina.jpg",
        f"Two whole fresh Whitemouth Croaker (Micropogonias furnieri / Corvina), "
        f"silver-grey matte scales, NO golden metallic sheen, NO nacreous glow on gills, "
        f"small water droplets on skin, slightly different sizes, realistic fish market {STYLE}"
    ),
    (
        "salmon-atlantico.jpg",
        f"Whole Atlantic Salmon (Salmo salar) and one cross-section steak beside it, "
        f"matte grey-silver skin with small dark spots, muted orange-pink flesh visible in steak, "
        f"small water droplets on fish skin, NO CGI clean skin, natural imperfections {STYLE}"
    ),
    (
        "salmon-blanco.jpg",
        f"One whole fresh Argentine Sandperch (Pseudopercis semifasciata / Salmon Blanco), "
        f"matte silver-white scales, NOT overly shiny, small water droplets on skin, "
        f"natural wet fish texture, realistic fish market display {STYLE}"
    ),
    (
        "white-drum.jpg",
        f"One whole fresh White Drum fish (Plagioscion squamosissimus / Cuca), "
        f"matte silver-white scales, NOT glossy or overly prominent scales, "
        f"small water droplets on skin, natural wet texture, realistic market fish {STYLE}"
    ),
]

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

for i, (filename, prompt) in enumerate(FIXES, 1):
    print(f"[{i}/{len(FIXES)}] {filename}...")
    r = requests.post(
        "https://api.x.ai/v1/images/generations",
        headers=headers,
        json={"model": "grok-imagine-image", "prompt": prompt, "n": 1, "response_format": "b64_json"},
        timeout=60
    )
    r.raise_for_status()
    img = base64.b64decode(r.json()["data"][0]["b64_json"])
    (OUT / filename).write_bytes(img)
    print(f"  OK ({len(img)//1024} KB)")
    if i < len(FIXES):
        time.sleep(2)

print("Done.")
