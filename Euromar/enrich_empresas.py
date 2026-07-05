"""
Enrichment Expositores Seafood - 100% gratis

Para cada empresa del Excel MASTER que no tenga datos de contacto:
  1. Busca su website en DuckDuckGo (no necesita API key)
  2. Entra al website y páginas de contacto
  3. Extrae: email, teléfono, dirección, actividad principal, redes sociales
  4. Escribe todo en nuevas columnas del Excel

Características:
  - Pausas aleatorias entre búsquedas (anti-bloqueo)
  - Rotación de User-Agents
  - Checkpoints cada 25 empresas
  - RESUME automático: si lo relanzas, continúa donde lo dejaste
  - Solo procesa empresas que aún no tengan website

USO:
  pip install requests beautifulsoup4 pandas openpyxl lxml
  python enrich_empresas.py

INPUT:  Expositores_MASTER.xlsx
OUTPUT: Expositores_ENRIQUECIDO.xlsx
"""

import os
import re
import time
import random
import sys
from urllib.parse import urlparse, urljoin, quote_plus
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ============ CONFIG ============
INPUT_FILE   = "Expositores_MASTER.xlsx"
OUTPUT_FILE  = "Expositores_ENRIQUECIDO.xlsx"

DELAY_BETWEEN_SEARCHES = (2.0, 5.0)     # segundos entre búsquedas Google/DDG
DELAY_BETWEEN_SCRAPES  = (1.0, 2.5)     # segundos entre scrapes de web
TIMEOUT                = 12             # timeout por petición
SAVE_EVERY             = 25
LIMIT                  = None           # None = todas; pon 10 para probar
# ================================


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
EMAIL_OBFUSCATED_RE = re.compile(
    r'([A-Za-z0-9._%+\-]+)\s*(?:\[|\()?\s*(?:at|AT|arroba|ARROBA|@)\s*(?:\]|\))?\s*([A-Za-z0-9.\-]+)\s*(?:\[|\()?\s*(?:dot|DOT|punto|PUNTO|\.)\s*(?:\]|\))?\s*([A-Za-z]{2,})'
)
PHONE_RE = re.compile(r'\+?\d[\d\s().\-]{7,}\d')

# Dominios que NO son websites oficiales de empresas
BLACKLIST_DOMAINS = {
    'facebook.com', 'linkedin.com', 'twitter.com', 'x.com',
    'instagram.com', 'youtube.com', 'tiktok.com', 'pinterest.com',
    'wikipedia.org', 'wikidata.org',
    'duckduckgo.com', 'google.com', 'bing.com', 'yahoo.com',
    'amazon.com', 'alibaba.com', 'europages.com',
    'opencorporates.com', 'dnb.com', 'bloomberg.com',
    'crunchbase.com', 'glassdoor.com', 'indeed.com',
    'seafoodsource.com', 'seafoodexpo.com',
    'yelp.com', 'yellowpages.com',
    'youtu.be', 't.co',
}

SOCIAL_DOMAINS = (
    'facebook.com', 'linkedin.com', 'twitter.com', 'x.com',
    'instagram.com', 'youtube.com', 'tiktok.com',
)


def ua():
    return random.choice(USER_AGENTS)


def sleep_range(rng):
    time.sleep(random.uniform(*rng))


def headers_base():
    return {
        "User-Agent": ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5,es;q=0.3",
        "Connection": "keep-alive",
    }


# ---------- Búsqueda de website ----------
def search_duckduckgo(query):
    """
    Busca en DuckDuckGo (HTML version, sin API key).
    Devuelve lista de URLs candidatas, filtrando redes sociales y directorios.
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        r = requests.get(url, headers=headers_base(), timeout=TIMEOUT)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, "lxml")
        results = []
        for a in soup.select("a.result__a, a.result__url"):
            href = a.get("href") or ""
            if not href.startswith("http"):
                continue
            # DDG a veces envuelve con /l/?uddg=...
            if "duckduckgo.com/l/" in href:
                m = re.search(r'uddg=([^&]+)', href)
                if m:
                    from urllib.parse import unquote
                    href = unquote(m.group(1))
            try:
                dom = urlparse(href).netloc.lower().replace("www.", "")
                if any(bd in dom for bd in BLACKLIST_DOMAINS):
                    continue
                if href not in results:
                    results.append(href)
            except Exception:
                continue
        return results[:5]
    except Exception as e:
        print(f"      [DDG error] {e}")
        return []


def find_website(empresa, pais=""):
    """Intenta encontrar el website oficial. Devuelve (url, confianza 0-1)."""
    # Limpiar nombre: quitar sufijos tipo "S.L", "Ltd", "PVT LTD"
    clean_name = re.sub(r'\b(s\.?l\.?u?\.?|s\.?r\.?l\.?|ltd\.?|gmbh|bv|pvt|inc\.?|co\.?|corp\.?|limited|private|&|and)\b',
                        '', empresa, flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'\s+', ' ', clean_name)

    queries = [
        f'"{empresa}" {pais} official website',
        f'{clean_name} {pais} site',
        f'{empresa} contact',
    ]

    best_url, best_conf = "", 0.0

    for q in queries:
        results = search_duckduckgo(q)
        if not results:
            sleep_range(DELAY_BETWEEN_SEARCHES)
            continue

        # Mirar los primeros 3 resultados
        for url in results[:3]:
            try:
                dom = urlparse(url).netloc.lower().replace("www.", "")
                conf = 0.3  # base

                # Bonus si el nombre aparece en el dominio
                # (quitando espacios y mayúsculas)
                name_for_match = re.sub(r'[^a-z0-9]', '', clean_name.lower())
                if len(name_for_match) >= 4:
                    dom_clean = re.sub(r'[^a-z0-9]', '', dom)
                    # Coincidencia parcial del nombre en dominio
                    # (5+ caracteres consecutivos)
                    for size in range(min(len(name_for_match), 12), 4, -1):
                        for i in range(len(name_for_match) - size + 1):
                            frag = name_for_match[i:i + size]
                            if frag in dom_clean:
                                conf += 0.3
                                break
                        if conf > 0.3:
                            break

                if conf > best_conf:
                    best_conf = conf
                    best_url = url
                    if conf >= 0.6:  # suficiente, no seguimos
                        return best_url, min(best_conf, 1.0)
            except Exception:
                continue
        sleep_range(DELAY_BETWEEN_SEARCHES)

    return best_url, min(best_conf, 1.0)


# ---------- Scrape del website ----------
def fetch(url):
    try:
        r = requests.get(url, headers=headers_base(), timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
            return r.text, r.url
    except Exception:
        pass
    return None, None


def find_contact_pages(base_url, html):
    """Encuentra URLs de páginas /contact, /about, /contacto dentro del site."""
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        return []
    base_dom = urlparse(base_url).netloc.lower()
    found, seen = [], set()
    keywords = ['contact', 'contacto', 'about', 'acerca', 'quienes', 'empresa',
                'impressum', 'legal', 'company', 'nosotros']
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        text = a.get_text(strip=True).lower()[:80]
        if not href:
            continue
        full = urljoin(base_url, href)
        try:
            dom = urlparse(full).netloc.lower()
        except Exception:
            continue
        if dom != base_dom:
            continue
        if full in seen:
            continue
        # Match por URL o por texto del enlace
        if any(kw in full.lower() or kw in text for kw in keywords):
            seen.add(full)
            found.append(full)
    return found[:4]


def extract_contact_info(html, base_url):
    """Extrae emails, teléfonos, dirección, actividad, redes del HTML."""
    info = {
        "emails": set(),
        "phones": set(),
        "socials": set(),
        "address": "",
        "description": "",
    }
    if not html:
        return info

    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        return info

    # Quitar script/style para sacar texto limpio
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)

    # Emails
    for m in EMAIL_RE.findall(text):
        if not any(x in m.lower() for x in ['example.', 'domain.', 'yoursite', 'yourdomain',
                                              'sentry.', 'wixpress', 'wordpress.com',
                                              '.png', '.jpg', '.gif']):
            info["emails"].add(m.lower())

    # Emails ofuscados ("info [at] empresa [dot] com")
    for m in EMAIL_OBFUSCATED_RE.findall(text):
        email = f"{m[0]}@{m[1]}.{m[2]}".lower()
        info["emails"].add(email)

    # Links mailto
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if href.startswith("mailto:"):
            e = href.replace("mailto:", "").split("?")[0].strip().lower()
            if "@" in e:
                info["emails"].add(e)

    # Teléfonos (limitado)
    for m in PHONE_RE.findall(text)[:30]:
        clean = re.sub(r'[^\d+]', '', m)
        if 8 <= len(clean) <= 16:
            info["phones"].add(m.strip())

    # Redes sociales
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if href.startswith("http"):
            low = href.lower()
            if any(sd in low for sd in SOCIAL_DOMAINS):
                info["socials"].add(href.split("?")[0])

    # Dirección: buscar meta address o texto con código postal
    addr_meta = soup.find("meta", attrs={"property": "business:contact_data:street_address"})
    if addr_meta:
        info["address"] = addr_meta.get("content", "")[:200]
    else:
        # Heurística: texto con calle + ciudad + código postal
        addr_patterns = [
            r'([A-Za-zÀ-ÿ0-9\.\-\s,]{5,50}\s+\d{4,6}\s+[A-Za-zÀ-ÿ\.\-\s]{3,30})',
        ]
        for pat in addr_patterns:
            m = re.search(pat, text)
            if m:
                info["address"] = m.group(1).strip()[:200]
                break

    # Descripción (meta description)
    for key in [("name", "description"), ("property", "og:description")]:
        tag = soup.find("meta", attrs={key[0]: key[1]})
        if tag and tag.get("content"):
            info["description"] = tag.get("content").strip()[:500]
            break

    # Actividad principal (keywords)
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if kw_tag and kw_tag.get("content"):
        info["keywords"] = kw_tag.get("content").strip()[:300]
    else:
        info["keywords"] = ""

    return info


def enrich_website(url):
    """Scrape completo de un website: home + páginas de contacto."""
    combined = {
        "emails": set(), "phones": set(), "socials": set(),
        "address": "", "description": "", "keywords": "",
    }

    html, final_url = fetch(url)
    if not html:
        return combined, None

    info_home = extract_contact_info(html, final_url)
    for k in ["emails", "phones", "socials"]:
        combined[k] |= info_home[k]
    for k in ["address", "description", "keywords"]:
        if info_home.get(k):
            combined[k] = info_home[k]

    # Visitar páginas de contacto
    contact_pages = find_contact_pages(final_url, html)
    for cp in contact_pages[:3]:
        sleep_range(DELAY_BETWEEN_SCRAPES)
        chtml, _ = fetch(cp)
        if chtml:
            info_c = extract_contact_info(chtml, cp)
            for k in ["emails", "phones", "socials"]:
                combined[k] |= info_c[k]
            if info_c.get("address") and not combined["address"]:
                combined["address"] = info_c["address"]

    return combined, final_url


# ---------- Main ----------
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No encuentro {INPUT_FILE}. Ponlo en la misma carpeta.")
        return

    # Cargar input
    df_in = pd.read_excel(INPUT_FILE, sheet_name='Expositores')
    print(f"[OK] {len(df_in)} empresas cargadas de {INPUT_FILE}")

    # Preparar columnas de enrichment
    new_cols = ['Website_Auto', 'Website_Confianza', 'Email_Auto',
                'Telefono_Auto', 'Direccion_Auto', 'Descripcion_Auto',
                'Keywords_Auto', 'Redes_Auto', 'Status_Enrichment']

    # Reanudar desde OUTPUT si existe
    if os.path.exists(OUTPUT_FILE):
        try:
            df = pd.read_excel(OUTPUT_FILE, sheet_name='Expositores')
            print(f"[RESUME] {OUTPUT_FILE} existe, continuaré donde iba")
        except Exception:
            df = df_in.copy()
            for c in new_cols:
                df[c] = ""
    else:
        df = df_in.copy()
        for c in new_cols:
            df[c] = ""

    # Asegurar columnas
    for c in new_cols:
        if c not in df.columns:
            df[c] = ""

    # Identificar pendientes
    # Pendiente: Status_Enrichment vacío
    mask_pendientes = df['Status_Enrichment'].astype(str).str.strip().isin(['', 'nan', 'None'])
    pendientes_idx = df[mask_pendientes].index.tolist()

    print(f"\nPendientes de enrichment: {len(pendientes_idx)} / {len(df)}")

    if LIMIT:
        pendientes_idx = pendientes_idx[:LIMIT]
        print(f"[LIMIT] solo procesaré {len(pendientes_idx)}")

    if not pendientes_idx:
        print("[OK] Todas enriquecidas.")
        return

    print(f"\nEstimación: ~{len(pendientes_idx) * 10 / 60:.0f} minutos"
          f" ({len(pendientes_idx) * 10 / 3600:.1f} horas)")
    print("Pulsa Ctrl+C cuando quieras parar; se guarda checkpoint.\n")

    processed = 0
    try:
        for i, idx in enumerate(pendientes_idx, 1):
            empresa = str(df.at[idx, 'Empresa']) if 'Empresa' in df.columns else str(df.at[idx, 'Nombre'])
            pais = str(df.at[idx, 'País']) if 'País' in df.columns else str(df.at[idx, 'Country'])
            web_existente = str(df.at[idx, 'Website']) if 'Website' in df.columns else ""

            print(f"\n[{i}/{len(pendientes_idx)}] {empresa[:50]} ({pais})")

            # Si ya hay web original, saltar búsqueda y usarla
            if web_existente and web_existente.strip() not in ('', 'nan'):
                web = web_existente.split(";")[0].split("|")[0].strip()
                conf = 1.0
                print(f"  usa web existente: {web[:60]}")
            else:
                # Buscar web
                web, conf = find_website(empresa, pais)
                print(f"  web encontrada: {web[:60] if web else '(nada)'} (conf {conf:.2f})")

            df.at[idx, 'Website_Auto'] = web
            df.at[idx, 'Website_Confianza'] = round(conf, 2)

            if web and conf >= 0.3:
                # Scrape del website
                try:
                    info, final_url = enrich_website(web)
                    df.at[idx, 'Email_Auto']        = "; ".join(sorted(info['emails'])[:5])
                    df.at[idx, 'Telefono_Auto']     = "; ".join(sorted(info['phones'])[:3])
                    df.at[idx, 'Redes_Auto']        = "; ".join(sorted(info['socials'])[:5])
                    df.at[idx, 'Direccion_Auto']    = info.get('address', '')
                    df.at[idx, 'Descripcion_Auto']  = info.get('description', '')
                    df.at[idx, 'Keywords_Auto']     = info.get('keywords', '')
                    df.at[idx, 'Status_Enrichment'] = 'OK'
                    print(f"  emails: {len(info['emails'])} | tel: {len(info['phones'])} | socials: {len(info['socials'])}")
                except Exception as e:
                    df.at[idx, 'Status_Enrichment'] = f'ERR_SCRAPE: {str(e)[:60]}'
                    print(f"  !! error scrape: {e}")
            else:
                df.at[idx, 'Status_Enrichment'] = 'NO_WEB'

            processed += 1

            if processed % SAVE_EVERY == 0:
                df.to_excel(OUTPUT_FILE, sheet_name='Expositores', index=False)
                print(f"  [checkpoint → {OUTPUT_FILE}]")

            sleep_range(DELAY_BETWEEN_SEARCHES)

    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Guardando...")

    df.to_excel(OUTPUT_FILE, sheet_name='Expositores', index=False)

    # Stats finales
    ok = (df['Status_Enrichment'] == 'OK').sum()
    con_email = df['Email_Auto'].astype(str).str.strip().ne('').sum()
    print(f"\n{'=' * 60}")
    print(f"TERMINADO")
    print(f"{'=' * 60}")
    print(f"Total empresas         : {len(df)}")
    print(f"Enriquecidas con éxito : {ok}")
    print(f"Con email encontrado   : {con_email}")
    print(f"Archivo final          : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()