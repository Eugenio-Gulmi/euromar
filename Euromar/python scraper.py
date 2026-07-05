"""
Scraper de expositores - Seafood Expo Global / Seafood Processing Global
Plataforma: Small World Labs (acceso público, SIN login)

USO:
  1) pip install selenium webdriver-manager pandas openpyxl
  2) python scraper_seafood.py
  3) Se abre Chrome. Acepta cookies. Vuelve a la terminal y pulsa ENTER.
  4) El script hace el resto solo. Genera Expositores_Seafood.xlsx.

Pensado para ~2.600 fichas por lista. Tiempo estimado: ~2h por lista a 3s/ficha.
"""

import time
import re
import os
import random
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# =========== CONFIGURACIÓN ===========
LISTAS = {
    "Seafood_Expo_Global":       "https://seg2025.smallworldlabs.com/exhibitors",
    "Seafood_Processing_Global": "https://spg2025.smallworldlabs.com/exhibitors",
}

OUTPUT_FILE       = "Expositores_Seafood.xlsx"
PAGE_WAIT         = 3        # segundos tras cargar cada ficha (sube si la red va lenta)
SCROLL_PAUSE      = 2.5      # pausa entre scrolls para cargar más en la lista
MAX_SCROLL_STABLE = 5        # nº de scrolls consecutivos sin cambios antes de parar
SAVE_EVERY        = 50       # guarda checkpoint cada N fichas
LIMIT             = None     # pon un número (ej. 20) para probar; None = todos
JITTER            = 0.6      # segundos aleatorios añadidos a cada espera (anti-bot)
# =====================================


# ---------- Regex ----------
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().\-]{7,}\d")


# ---------- Setup ----------
def build_driver():
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_seafood")
    opts.add_argument(f"--user-data-dir={profile_dir}")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


def wait_jitter(base):
    time.sleep(base + random.uniform(0, JITTER))


def wait_for_user(msg):
    print("\n" + "=" * 70)
    print(msg)
    print("=" * 70)
    input(">>> Cuando estés listo, pulsa ENTER para continuar... ")


# ---------- Listado ----------
def scroll_to_load_all(driver):
    print("Haciendo scroll para cargar todos los expositores...")
    last_count, stable = 0, 0
    while stable < MAX_SCROLL_STABLE:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        count = len(driver.find_elements(By.CSS_SELECTOR, 'a[href*="/co/"]'))
        print(f"   ...enlaces cargados: {count}")
        if count == last_count:
            stable += 1
        else:
            stable = 0
            last_count = count
    print(f"[OK] Scroll terminado. Total: {last_count}")


def collect_exhibitor_urls(driver):
    urls, seen = [], set()
    for el in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/co/"]'):
        href = el.get_attribute("href")
        if href and "/co/" in href and href not in seen:
            seen.add(href)
            urls.append(href)
    return urls


# ---------- Ficha ----------
def extract_exhibitor(driver, url):
    data = {
        "URL": url, "Nombre": "", "Stand": "", "Pais": "",
        "Website": "", "Email": "", "Telefono": "",
        "Descripcion": "", "Productos_Categorias": "",
        "Permisos_Exportacion": "", "Certificaciones": "",
        "Redes_Sociales": "", "Texto_Completo": "",
    }

    try:
        driver.get(url)
    except WebDriverException as e:
        data["Texto_Completo"] = f"ERROR navegando: {e}"
        return data

    wait_jitter(PAGE_WAIT)

    try:
        data["Nombre"] = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except NoSuchElementException:
        pass

    try:
        body_text = driver.find_element(By.TAG_NAME, "main").text
    except NoSuchElementException:
        body_text = driver.find_element(By.TAG_NAME, "body").text
    data["Texto_Completo"] = body_text[:3000]

    # Emails
    emails = set(EMAIL_RE.findall(body_text))
    for a in driver.find_elements(By.XPATH, "//a[starts-with(@href,'mailto:')]"):
        href = a.get_attribute("href") or ""
        emails.add(href.replace("mailto:", "").split("?")[0])
    emails = {e for e in emails
              if "divcom.com" not in e and "smallworldlabs" not in e}
    data["Email"] = "; ".join(sorted(emails))

    # Teléfonos
    phones = set(m.strip() for m in PHONE_RE.findall(body_text))
    data["Telefono"] = "; ".join(sorted(phones)[:3])

    # Websites y redes
    social_doms = ("facebook.", "linkedin.", "twitter.", "x.com",
                   "instagram.", "youtube.", "tiktok.")
    skip_doms = ("smallworldlabs.com", "divcom.com", "seafoodexpo.com",
                 "seafoodsource.com", "divcomevents", "google.com",
                 "mya2zevents.com")
    websites, socials = set(), set()
    for a in driver.find_elements(By.TAG_NAME, "a"):
        href = (a.get_attribute("href") or "").strip()
        if not href.startswith("http") or "mailto:" in href:
            continue
        low = href.lower()
        if any(s in low for s in skip_doms):
            continue
        if any(s in low for s in social_doms):
            socials.add(href)
        else:
            websites.add(href)
    data["Website"]        = "; ".join(sorted(websites)[:3])
    data["Redes_Sociales"] = "; ".join(sorted(socials))

    # Stand
    m = re.search(r"Stand\s*#?\s*([A-Z0-9,\s]+)", body_text)
    if m:
        data["Stand"] = m.group(1).strip().split("\n")[0][:60]

    # Secciones (heurístico — ajustable tras ver una ficha real)
    secciones = {
        "Pais":                 r"(?:Country|País|Pais)\s*[:\n]+\s*(.+?)(?:\n\n|\n[A-Z][a-z]+\s*[:\n])",
        "Descripcion":          r"(?:About|Description|Descripci[oó]n)\s*[:\n]+\s*(.+?)(?:\n\n|\n[A-Z][a-z]+\s*[:\n])",
        "Productos_Categorias": r"(?:Products?|Categor(?:y|ies|ías?))\s*[:\n]+\s*(.+?)(?:\n\n|\n[A-Z][a-z]+\s*[:\n])",
        "Permisos_Exportacion": r"(?:Export(?:\s+Markets|\s+Countries|\s+Permits)?|Exportaci[oó]n|Mercados)\s*[:\n]+\s*(.+?)(?:\n\n|\n[A-Z][a-z]+\s*[:\n])",
        "Certificaciones":      r"(?:Certifications?|Certificaciones?)\s*[:\n]+\s*(.+?)(?:\n\n|\n[A-Z][a-z]+\s*[:\n])",
    }
    for campo, patron in secciones.items():
        m = re.search(patron, body_text, re.IGNORECASE | re.DOTALL)
        if m:
            data[campo] = m.group(1).strip()[:1000]

    return data


# ---------- Guardado ----------
def save_excel(rows, path):
    if not rows:
        return
    df = pd.DataFrame(rows)
    if "Fuente" in df.columns and df["Fuente"].nunique() > 1:
        with pd.ExcelWriter(path, engine="openpyxl") as xl:
            for fuente, sub in df.groupby("Fuente"):
                sub.to_excel(xl, sheet_name=fuente[:31], index=False)
    else:
        df.to_excel(path, index=False)


def fmt(seconds):
    return str(timedelta(seconds=int(seconds)))


# ---------- Main ----------
def main():
    driver = build_driver()
    all_rows = []

    try:
        primera = next(iter(LISTAS.values()))
        print(f"Abriendo {primera} ...")
        driver.get(primera)

        wait_for_user(
            "Acepta el BANNER DE COOKIES (y cierra cualquier popup).\n"
            "NO necesitas hacer login. Cuando veas la tabla de expositores, vuelve aquí."
        )

        for nombre_fuente, url_listado in LISTAS.items():
            print(f"\n========== {nombre_fuente} ==========")
            driver.get(url_listado)
            wait_jitter(PAGE_WAIT)

            scroll_to_load_all(driver)
            urls = collect_exhibitor_urls(driver)
            print(f"[{nombre_fuente}] {len(urls)} expositores encontrados")

            if LIMIT:
                urls = urls[:LIMIT]
                print(f"[LIMIT activo] procesaré solo {len(urls)}")

            eta = len(urls) * (PAGE_WAIT + 1.5)
            print(f"[{nombre_fuente}] Estimación: {fmt(eta)} (hh:mm:ss) | "
                  f"fin previsto: {(datetime.now() + timedelta(seconds=eta)).strftime('%H:%M')}")

            t0 = time.time()
            for i, url in enumerate(urls, 1):
                try:
                    row = extract_exhibitor(driver, url)
                    row["Fuente"] = nombre_fuente
                    all_rows.append(row)

                    if i % 10 == 0 or i == len(urls):
                        elapsed = time.time() - t0
                        rate = i / elapsed if elapsed else 0
                        remaining = (len(urls) - i) / rate if rate else 0
                        print(f"   [{i}/{len(urls)}] {row.get('Nombre','')[:40]:<40} | "
                              f"{rate*60:.1f}/min | faltan ~{fmt(remaining)}")
                except Exception as e:
                    print(f"   [{i}/{len(urls)}] !! error en {url}: {e}")
                    all_rows.append({"URL": url, "Fuente": nombre_fuente,
                                     "Texto_Completo": f"ERROR: {e}"})

                if i % SAVE_EVERY == 0:
                    save_excel(all_rows, OUTPUT_FILE)
                    print(f"      [checkpoint guardado en {OUTPUT_FILE}]")

        save_excel(all_rows, OUTPUT_FILE)
        print(f"\n[OK] Terminado. {len(all_rows)} filas en {OUTPUT_FILE}")

    except KeyboardInterrupt:
        print("\nInterrumpido. Guardando progreso...")
        save_excel(all_rows, OUTPUT_FILE)
        print(f"Guardado parcial en {OUTPUT_FILE}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()