"""
Scraper Seafood Expo Global 2026 - MODO 100% MANUAL

División estricta de roles:
  - TÚ cargas las tarjetas a mano (scroll + Load More en Chrome) a tu ritmo.
  - EL SCRIPT solo cuenta las que haya y las procesa.

No hay Load More automático. No hay detección anti-bot por scroll.
Solo tú clicando a ritmo humano. Cuando tengas todas (o las que te deje),
pulsas ENTER y el script coge lo que haya.

USO:
  python scraper_manual.py

Salida: Expositores_Manual.xlsx
"""

import time
import re
import os
import random
import sys
import shutil
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# ============ CONFIG ============
LIST_URL          = "https://www.seafoodexpo.com/global/exhibitor-lists/"
OUTPUT_FILE       = "Expositores_Manual.xlsx"

PAGE_WAIT         = 3.0
SAVE_EVERY        = 25
JITTER            = 1.0
LONG_BREAK_EVERY  = 50
LONG_BREAK_SEC    = (20, 40)

REVERSE_ORDER     = True   # True = última→primera, False = primera→última
LIMIT             = None
# ================================


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().\-]{7,}\d")
STAND_RE = re.compile(r"\b([0-9][A-Z]{1,3}[0-9]{3,4}[A-Z]?)\b")

CAPTCHA_MARKERS = [
    "Enter the characters seen in the image",
    "Download audio CAPTCHA",
    "captcha", "CAPTCHA",
    "I'm not a robot",
    "Verify you are human",
    "unusual traffic",
]


def build_driver():
    profile = os.path.join(os.getcwd(), "chrome_profile_manual")
    if os.path.exists(profile):
        try:
            shutil.rmtree(profile)
        except Exception:
            pass

    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(f"--user-data-dir={profile}")
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


def beep():
    try:
        import winsound
        for _ in range(3):
            winsound.Beep(880, 200)
            time.sleep(0.1)
    except Exception:
        for _ in range(5):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.2)


def has_captcha(driver):
    try:
        driver.switch_to.default_content()
        body = driver.find_element(By.TAG_NAME, "body").text
    except Exception:
        return False
    return any(m.lower() in body.lower() for m in CAPTCHA_MARKERS)


def handle_captcha(driver, context=""):
    beep()
    print("\n" + "!" * 70)
    print("!! CAPTCHA " + context)
    print("!! Resuélvelo en Chrome y vuelve aquí.")
    print("!" * 70)
    input(">>> ENTER cuando lo resuelvas... ")
    time.sleep(2)


CARD_LINK_SELECTORS = [
    "a[href*='/exhibitor/']",
    "a[href*='/widget/event/']",
]


def count_cards_anywhere(driver):
    """Cuenta tarjetas en default + cada iframe."""
    best = 0
    try:
        driver.switch_to.default_content()
        for sel in CARD_LINK_SELECTORS:
            best = max(best, len(driver.find_elements(By.CSS_SELECTOR, sel)))
    except Exception:
        pass
    try:
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)
                for sel in CARD_LINK_SELECTORS:
                    best = max(best, len(driver.find_elements(By.CSS_SELECTOR, sel)))
            except Exception:
                continue
    except Exception:
        pass
    driver.switch_to.default_content()
    return best


def collect_urls_all_frames(driver):
    urls, seen = [], set()

    def here(label):
        before = len(urls)
        for sel in CARD_LINK_SELECTORS:
            try:
                for a in driver.find_elements(By.CSS_SELECTOR, sel):
                    href = a.get_attribute("href") or ""
                    if "/exhibitor/" in href and href not in seen:
                        seen.add(href)
                        urls.append(href)
            except Exception:
                pass
        added = len(urls) - before
        if added > 0:
            print(f"  {label}: +{added} (total {len(urls)})")

    driver.switch_to.default_content()
    here("default")

    for i, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe)
            here(f"iframe[{i}]")
        except Exception:
            pass

    driver.switch_to.default_content()
    return urls


# --- Parseo ficha ---
SECTION_PATTERNS = {
    "Informacion":  r"^(?:Información|Information|About)$",
    "Products":     r"^Products?$",
    "Address":      r"^(?:Address|Dirección|Direccion)$",
    "Redes":        r"^(?:Redes sociales|Social networks)$",
    "Contacto":     r"^(?:Datos de contacto|Contact details|Contact info|Contact)$",
    "Profiles":     r"^Product Profiles(?:\s*\(.+\))?$",
    "Documentos":   r"^(?:Documentos y enlaces|Documents and links)$",
}

CATEGORY_SUBHEADERS = ("Seafood Product Categories", "Processing Product Categories",
                      "Aquaculture Product Categories")


def split_sections(text):
    secs = {"_pre": []}
    current = "_pre"
    for ln in text.split("\n"):
        s = ln.strip()
        m = None
        for k, p in SECTION_PATTERNS.items():
            if re.match(p, s):
                m = k
                break
        if m:
            current = m
            if current not in secs:
                secs[current] = []
        else:
            if current not in secs:
                secs[current] = []
            secs[current].append(ln)
    return {k: "\n".join(v).strip() for k, v in secs.items()}


def clean_products(text):
    return "\n".join([l for l in text.split("\n")
                      if l.strip() not in CATEGORY_SUBHEADERS]).strip()


def parse_addr(text):
    d = {"City": "", "State": "", "Country": ""}
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    mp = {"city": "City", "state": "State", "state/province": "State",
          "province": "State", "country": "Country", "país": "Country",
          "pais": "Country"}
    i = 0
    while i < len(lines):
        low = lines[i].lower().rstrip(":")
        if low in mp and i + 1 < len(lines):
            d[mp[low]] = lines[i + 1]
            i += 2
        else:
            i += 1
    return d


def scrape_detail(driver, url, max_retries=2):
    data = {
        "URL": url, "Nombre": "", "Stand": "",
        "Descripcion": "", "Productos": "", "Categorias": "",
        "Address_Raw": "", "City": "", "State": "", "Country": "",
        "Redes_Sociales": "", "Contacto": "",
        "Product_Profiles": "", "Documentos": "",
        "Website": "", "Email": "", "Telefono": "",
        "Texto_Completo": "",
    }

    for attempt in range(max_retries + 1):
        try:
            driver.get(url)
        except WebDriverException as e:
            data["Texto_Completo"] = f"ERROR navegando: {e}"
            return data

        wait_jitter(PAGE_WAIT)

        if has_captcha(driver):
            handle_captcha(driver, f"ficha {url[:60]}")
            if attempt < max_retries:
                continue

        try:
            body = driver.find_element(By.TAG_NAME, "body").text
        except NoSuchElementException:
            body = ""
        data["Texto_Completo"] = body[:5000]

        if has_captcha(driver):
            data["Texto_Completo"] = "CAPTCHA persistente"
            return data

        for tag in ("h1", "h2"):
            try:
                n = driver.find_element(By.TAG_NAME, tag).text.strip()
                if n and len(n) > 2:
                    data["Nombre"] = n
                    break
            except NoSuchElementException:
                continue

        m = STAND_RE.search(body)
        if m:
            data["Stand"] = m.group(1)

        secs = split_sections(body)
        g = lambda k: secs.get(k, "")

        data["Descripcion"]      = g("Informacion")[:3000]
        data["Productos"]        = clean_products(g("Products"))[:2000]
        data["Categorias"]       = data["Productos"][:1000]
        data["Address_Raw"]      = g("Address")
        data["Redes_Sociales"]   = g("Redes")[:500]
        data["Contacto"]         = g("Contacto")[:500]
        data["Product_Profiles"] = g("Profiles")[:2000]
        data["Documentos"]       = g("Documentos")[:1000]
        if data["Address_Raw"]:
            data.update(parse_addr(data["Address_Raw"]))

        emails = set(EMAIL_RE.findall(body))
        for a in driver.find_elements(By.XPATH, "//a[starts-with(@href,'mailto:')]"):
            emails.add((a.get_attribute("href") or "").replace("mailto:", "").split("?")[0])
        emails = {e for e in emails if "swapcard" not in e and "divcom" not in e
                  and "seafoodexpo" not in e}
        data["Email"] = "; ".join(sorted(emails))

        phones = set(m.strip() for m in PHONE_RE.findall(body))
        data["Telefono"] = "; ".join(sorted(phones)[:3])

        skip = ("seafoodexpo.com", "swapcard", "divcom", "google.com",
                "divcomevents", "connectglobal")
        soc_d = ("facebook.", "linkedin.", "twitter.", "x.com",
                 "instagram.", "youtube.", "tiktok.")
        webs, socs = set(), set()
        for a in driver.find_elements(By.TAG_NAME, "a"):
            href = (a.get_attribute("href") or "").strip()
            if not href.startswith("http") or "mailto:" in href:
                continue
            low = href.lower()
            if any(s in low for s in skip):
                continue
            if any(s in low for s in soc_d):
                socs.add(href)
            else:
                webs.add(href)
        data["Website"] = "; ".join(sorted(webs)[:3])
        if socs:
            data["Redes_Sociales"] = ((data["Redes_Sociales"] + " | ") if data["Redes_Sociales"] else "") + "; ".join(sorted(socs))

        return data

    return data


def load_progress(path):
    if not os.path.exists(path):
        return set(), []
    try:
        df = pd.read_excel(path)

        def val(row):
            if pd.isna(row.get("Nombre")) or not str(row.get("Nombre", "")).strip():
                return False
            t = str(row.get("Texto_Completo", ""))
            if t.startswith("ERROR") or "CAPTCHA persistente" in t:
                return False
            return True

        df_ok = df[df.apply(val, axis=1)].copy()
        urls = set(df_ok["URL"].dropna().astype(str).tolist())
        print(f"[RESUME] {len(urls)} ya hechas")
        return urls, df_ok.to_dict("records")
    except Exception as e:
        print(f"[WARN] {e}")
        return set(), []


def save(rows, path):
    if rows:
        pd.DataFrame(rows).to_excel(path, index=False)


def fmt(s):
    return str(timedelta(seconds=int(s)))


def main():
    driver = build_driver()
    urls_done, all_rows = load_progress(OUTPUT_FILE)

    try:
        print(f"Abriendo {LIST_URL} ...")
        driver.get(LIST_URL)

        print("\n" + "=" * 70)
        print("MODO MANUAL - tú cargas, yo scrapeo")
        print("=" * 70)
        print("""
En la ventana de Chrome que acabo de abrir:

  1) Acepta las cookies.
  2) Si sale captcha, resuélvelo.
  3) Haz scroll hacia abajo y click en "Load More" MUCHAS veces.
     - Puedes tardar 10, 20, 30 minutos, lo que necesites.
     - Si sale captcha durante la carga, resuélvelo y sigue.
     - Cuando NO aparezca más el botón "Load More", has llegado al final.
  4) Cuando NO puedas cargar más tarjetas, vuelve aquí y pulsa ENTER.

Cuantas más tarjetas cargues, más expositores procesaré.
""")
        input(">>> ENTER cuando tengas las tarjetas cargadas... ")

        if has_captcha(driver):
            handle_captcha(driver, "antes de contar")

        print("\n=== CONTANDO TARJETAS CARGADAS ===")
        total = count_cards_anywhere(driver)
        print(f"Tarjetas detectadas: {total}")

        if total == 0:
            print("[!!] 0 tarjetas. ¿Seguro que cargaste en la VENTANA QUE ABRIÓ ESTE SCRIPT?")
            input(">>> ENTER para cerrar")
            return

        if total < 100:
            print(f"[WARN] Solo {total} tarjetas - ¿seguro que cargaste todas?")
            r = input(f"¿Procesar las {total} que hay? (s/n): ").strip().lower()
            if r != 's':
                print("Carga más tarjetas en Chrome y relanza el script.")
                return

        print("\n=== RECOGIENDO URLs ===")
        urls = collect_urls_all_frames(driver)

        if not urls:
            print("[!!] Sin URLs.")
            input(">>> ENTER")
            return

        print(f"\n[OK] {len(urls)} URLs únicas")

        if REVERSE_ORDER:
            urls = list(reversed(urls))
            print("[REVERSE] Procesando de la última a la primera")

        pendientes = [u for u in urls if u not in urls_done]
        saltadas = len(urls) - len(pendientes)
        if saltadas:
            print(f"[RESUME] {saltadas} saltadas. Pendientes: {len(pendientes)}")

        if LIMIT:
            pendientes = pendientes[:LIMIT]

        if not pendientes:
            print("[OK] Nada que hacer")
            return

        eta = len(pendientes) * (PAGE_WAIT + 1.5)
        print(f"Estimación: {fmt(eta)} | fin ~{(datetime.now() + timedelta(seconds=eta)).strftime('%H:%M')}\n")

        t0 = time.time()
        errs = 0
        MAX_ERRS = 5

        for i, url in enumerate(pendientes, 1):
            if i > 1 and i % LONG_BREAK_EVERY == 0:
                p = random.uniform(*LONG_BREAK_SEC)
                print(f"\n   ...descanso {p:.0f}s...")
                time.sleep(p)

            try:
                print(f"\n[{i}/{len(pendientes)}] {url[:90]}")
                row = scrape_detail(driver, url)

                t = str(row.get("Texto_Completo", ""))
                if t.startswith("ERROR navegando") or "ERR_" in t or "net::" in t:
                    errs += 1
                    print(f"  !! red ({errs}/{MAX_ERRS})")
                else:
                    errs = 0
                    all_rows.append(row)
                    print(f"  {row['Nombre'][:55]} | {row['Stand']} | {row['Country']}")

                if errs >= MAX_ERRS:
                    beep()
                    print("\n!! Muchos errores. ¿Internet caído?")
                    input(">>> ENTER cuando vuelva... ")
                    errs = 0

            except Exception as e:
                print(f"  !! {e}")
                errs += 1

            if i % SAVE_EVERY == 0:
                save(all_rows, OUTPUT_FILE)
                print(f"  [checkpoint]")

        save(all_rows, OUTPUT_FILE)
        print(f"\n[OK] {len(all_rows)} filas en {OUTPUT_FILE}")
        print(f"Tiempo: {fmt(time.time() - t0)}")
        input(">>> ENTER para cerrar")

    except KeyboardInterrupt:
        save(all_rows, OUTPUT_FILE)
        print(f"\nInterrumpido. Parcial en {OUTPUT_FILE}")
    except Exception as e:
        print(f"\n!! {e}")
        save(all_rows, OUTPUT_FILE)
        input(">>> ENTER")
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
