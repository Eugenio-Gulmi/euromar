"""Fix: atun - whole fish + steak cross-section beside it"""
import requests, base64, os
from pathlib import Path

API_KEY = os.environ["XAI_API_KEY"]
OUT = Path("public/images")

STYLE = (
    "on crushed ice on a dark black slate surface, dramatic natural side lighting, "
    "muted desaturated colors, real food photography, authentic fish market quality, "
    "matte wet skin with small water droplets, gritty realistic texture, "
    "no artificial saturation, no CGI glow, "
    "shot on 35mm film camera, natural grain, dark moody background. No text."
)

prompt = (
    f"One whole fresh Yellowfin Tuna (Thunnus albacares) lying on its side, "
    f"and beside it one thick cross-section steak cut showing deep ruby-red flesh with fine grain, "
    f"tuna skin dark blue-grey with yellow fins visible, natural imperfections, "
    f"small water droplets on fish skin, realistic fish market display {STYLE}"
)

print("Generating atun.jpg...")
r = requests.post(
    "https://api.x.ai/v1/images/generations",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"model": "grok-imagine-image", "prompt": prompt, "n": 1, "response_format": "b64_json"},
    timeout=60
)
r.raise_for_status()
img = base64.b64decode(r.json()["data"][0]["b64_json"])
(OUT / "atun.jpg").write_bytes(img)
print(f"  OK ({len(img)//1024} KB)")
