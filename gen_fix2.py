"""Fix: trucha (too shiny) and merluza (too uniform sizes)"""
import requests, base64, os
from pathlib import Path

API_KEY = os.environ["XAI_API_KEY"]
OUT = Path("public/images")

STYLE = (
    "on crushed ice on a dark black slate surface, dramatic natural side lighting, "
    "muted desaturated colors, real food photography, authentic fish market quality, "
    "gritty realistic texture, no artificial saturation, no CGI glow, "
    "shot on 35mm film camera, natural grain, dark moody background. No text."
)

FIXES = [
    (
        "trucha.jpg",
        f"Two whole fresh Rainbow Trout (Oncorhynchus mykiss) fish laid on crushed ice, "
        f"matte grey-silver skin with faint pink lateral stripe, natural wet skin texture, "
        f"NO iridescent sheen, NO glossy highlight, NO pink glow, realistic matte fish skin, "
        f"slightly different sizes, natural irregular positioning {STYLE}"
    ),
    (
        "merluza.jpg",
        f"Three whole fresh Argentine Hake (Merluccius hubbsi), slightly different sizes, "
        f"natural irregular positioning, silver-grey elongated bodies, slightly different angles, "
        f"realistic imperfect fish market arrangement, NOT uniformly aligned, NOT identical size, "
        f"authentic market display {STYLE}"
    ),
]

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

for filename, prompt in FIXES:
    print(f"Generating {filename}...")
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

print("Done.")
