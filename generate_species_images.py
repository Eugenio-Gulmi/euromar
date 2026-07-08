"""
Euromar SA — Grok Image Generator
Generates professional frozen seafood product photography for each species.
Usage: python generate_species_images.py
Requires: XAI_API_KEY environment variable (or set it in the script below)
"""

import os
import base64
import time
import requests
from pathlib import Path

API_KEY = os.environ.get("XAI_API_KEY", "YOUR_GROK_API_KEY_HERE")
API_URL = "https://api.x.ai/v1/images/generations"
IMAGE_MODEL = "aurora"  # xAI image generation model
OUTPUT_DIR = Path(__file__).parent / "public" / "images"

CAMERA_SUFFIX = (
    "Shot on Canon EOS R5, 85mm f/2.8, soft studio lighting, "
    "clean white or pale blue background, professional commercial food photography, "
    "sharp focus, photojournalistic editorial style, no text, no labels."
)

# Species list: (filename, english_name, scientific_name, prompt_description)
SPECIES = [
    # ── White Fish ──────────────────────────────────────────────────────────
    (
        "hoki.jpg",
        "Hoki",
        "Macruronus magellanicus",
        "A whole fresh Hoki fish (Macruronus magellanicus) displayed on crushed ice, "
        "showing its elongated silvery body with a tapered tail. Elegant presentation."
    ),
    (
        "corvina.jpg",
        "Whitemouth Croaker",
        "Micropogonias furnieri",
        "A fresh Whitemouth Croaker (Corvina) fish displayed on crushed ice, "
        "silvery scales with subtle golden sheen, clean professional seafood photography."
    ),
    (
        "pescadilla.jpg",
        "Striped Weakfish",
        "Cynoscion striatus",
        "A whole fresh Striped Weakfish (Pescadilla) on crushed ice, "
        "showing its distinctive striped pattern along the body, silver scales, clean cut."
    ),
    (
        "besugo.jpg",
        "Red Porgy",
        "Pagrus sedicem",
        "A whole fresh Red Porgy (Besugo) fish on crushed ice, "
        "pinkish-red scales, compact body, bright eye — premium seafood presentation."
    ),
    (
        "pez-palo.jpg",   # NEW — missing entirely
        "Brazilian Flathead",
        "Percophis brasiliensis",
        "A whole fresh Brazilian Flathead fish (Pez Palo / Percophis brasiliensis) "
        "on crushed ice, elongated and slightly flattened silver body, clearly showing "
        "the distinctive flathead shape. Clean professional seafood photography."
    ),
    (
        "raya.jpg",
        "Skate / Ray",
        "Raja spp.",
        "A fresh Skate Ray (Raya) displayed flat on crushed ice, "
        "showing its characteristic wing shape and diamond-patterned skin, "
        "top-down view, professional seafood market photography."
    ),
    (
        "salmon-blanco.jpg",
        "Argentine Sandperch",
        "Pseudopercis semifasciata",
        "A whole fresh Argentine Sandperch (Salmón Blanco) on crushed ice, "
        "silvery-white fish with firm body, clean professional frozen seafood photography."
    ),
    (
        "white-drum.jpg",
        "Cuca / White Drum",
        "Plagioscion squamosissimus",
        "A whole fresh White Drum fish (Plagioscion squamosissimus) on crushed ice, "
        "large silver-white scales, robust body, professional seafood photography."
    ),
    (
        "rape.jpg",
        "Monkfish",
        "Lophius gastrophysus",
        "Fresh Monkfish (Rape / Lophius) tail section and cross-section fillet "
        "displayed on crushed ice, showing the white firm flesh, premium restaurant-quality presentation."
    ),
    # ── Shellfish & Mollusks ─────────────────────────────────────────────────
    (
        "langostino.jpg",
        "Argentine Red Shrimp",
        "Pleoticus muelleri",
        "A pile of fresh wild Argentine Red Shrimp (Langostinos Patagónicos) "
        "with characteristic vivid coral-orange color, displayed on crushed ice, "
        "some whole and some split showing the firm white-pink flesh inside."
    ),
    (
        "calamar.jpg",
        "Patagonian Squid",
        "Illex argentinus",
        "Fresh Patagonian Squid (Calamar Illex argentinus) displayed on crushed ice, "
        "whole squid and cleaned tubes, white-translucent flesh, purple-spotted mantle."
    ),
    # ── Premium Species ──────────────────────────────────────────────────────
    (
        "merluza-negra.jpg",
        "Patagonian Toothfish",
        "Dissostichus eleginoides",
        "A thick premium Patagonian Toothfish (Merluza Negra / Chilean Sea Bass) fillet "
        "on crushed ice, showing its white buttery flesh with fine flake, "
        "luxury restaurant-quality seafood presentation."
    ),
    (
        "salmon-atlantico.jpg",
        "Atlantic Salmon",
        "Salmo salar",
        "A fresh whole Atlantic Salmon and a cross-section fillet showing the vivid "
        "pink-orange flesh, displayed on crushed ice, premium aquaculture product."
    ),
    (
        "atun.jpg",
        "Yellowfin Tuna",
        "Thunnus albacares",
        "A premium Yellowfin Tuna loin and steak cross-section on crushed ice, "
        "deep ruby-red flesh, clean sashimi-grade cut, professional seafood photography."
    ),
    (
        "trucha.jpg",
        "Rainbow Trout",
        "Oncorhynchus mykiss",
        "A whole fresh Rainbow Trout (Trucha Arcoíris) displayed on crushed ice, "
        "iridescent pink-silver skin with characteristic rainbow stripe, "
        "and a fillet showing the pale orange flesh."
    ),
    (
        "mahi-mahi.jpg",
        "Dolphinfish / Mahi-Mahi",
        "Coryphaena hippurus",
        "A fresh Mahi-Mahi (Dolphinfish / Dorado) fillet on crushed ice, "
        "showing the golden-green iridescent skin and firm white-pinkish flesh inside."
    ),
    # ── Breaded Products ─────────────────────────────────────────────────────
    (
        "productos-empanados-mar-02-bastones-merluza-1-960x640.jpg",
        "Hake Fish Sticks",
        "Merluccius hubbsi — processed",
        "Frozen breaded Hake fish sticks (Bastones de Merluza) arranged neatly "
        "on a white surface, golden-brown crispy coating, one broken open to show "
        "the white flaky fish inside. Commercial food photography."
    ),
    (
        "productos-empanados-mar-03-rabas-960x640.jpg",
        "Breaded Squid Rings",
        "Illex argentinus — processed",
        "Frozen breaded Patagonian Squid rings (Rabas / Calamar Apanado) "
        "displayed on a white surface, golden coating, rings and strips mixed, "
        "commercial frozen seafood product photography."
    ),
    (
        "productos-empanados-mar-06-filet-merluza-a-la-romana-960x640.jpg",
        "Breaded Hake Fillet",
        "Merluccius hubbsi — processed",
        "Frozen breaded Hake fillets (Filet Apanado de Merluza) on a white surface, "
        "rectangular portion-sized pieces with golden crispy breadcrumb coating, "
        "one broken open showing the white fish inside."
    ),
    (
        "productos-empanados-mar-05-formitas-de-merluza-960x640.jpg",
        "Hake Portions",
        "Merluccius hubbsi — processed",
        "Frozen breaded Hake portions (Formitas de Merluza) in various shapes "
        "displayed on white background, golden coating, child-friendly shapes, "
        "commercial frozen food product photography."
    ),
]


def generate_image(species_name: str, prompt: str) -> bytes | None:
    full_prompt = f"{prompt} {CAMERA_SUFFIX}"
    payload = {
        "model": IMAGE_MODEL,
        "prompt": full_prompt,
        "n": 1,
        "response_format": "b64_json",
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code == 429:
            print(f"  Rate limited — waiting 15s...")
            time.sleep(15)
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        b64 = data["data"][0]["b64_json"]
        return base64.b64decode(b64)
    except Exception as e:
        print(f"  ERROR for {species_name}: {e}")
        return None


def main():
    if API_KEY == "YOUR_GROK_API_KEY_HERE":
        print("❌ Set your XAI_API_KEY first:\n   export XAI_API_KEY=xai-...")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(SPECIES)
    generated = 0

    for i, (filename, name, scientific, prompt) in enumerate(SPECIES, 1):
        out_path = OUTPUT_DIR / filename
        # Change extension to .png for AI-generated images if original is .jpg
        # (Grok returns PNG; rename to match expected path)
        print(f"[{i}/{total}] {name} ({scientific})")

        img_bytes = generate_image(name, prompt)
        if img_bytes:
            out_path.write_bytes(img_bytes)
            print(f"  ✅ Saved → {out_path.name}  ({len(img_bytes)//1024} KB)")
            generated += 1
        else:
            print(f"  ⚠️  Skipped")

        # Brief pause between requests
        if i < total:
            time.sleep(2)

    print(f"\nDone: {generated}/{total} images generated → {OUTPUT_DIR}")
    if generated < total:
        print("Re-run to retry failed ones — existing files are overwritten.")


if __name__ == "__main__":
    main()
