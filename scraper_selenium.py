#!/usr/bin/env python3
"""
Raccolta Contatti - Centri Unghie Catania
Google Places API + Selenium per scraping directory

Fonti:
- Google Places API (primaria)
- PagineGialle.it (Selenium)
- Treatwell.it (Selenium)
- Fresha.com (Selenium)

Output: contatti_catania.json
"""

import csv
import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass, asdict
from urllib.parse import quote_plus

# Carica variabili d'ambiente da .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import requests
try:
    import pandas as pd
except ImportError:
    pd = None
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# ============================================================================
# CONFIGURAZIONE
# ============================================================================

CATANIA_COORDS = {"lat": 37.5079, "lng": 15.0830}
RAGGIO_KM = 40
RAGGIO_METRI = RAGGIO_KM * 1000

QUERY_RICERCA = [
    # === CATANIA CENTRO E ZONE ===
    "centro unghie Catania",
    "nail bar Catania",
    "manicure Catania",
    "ricostruzione unghie Catania",
    "centro estetico unghie Catania",
    "salone bellezza unghie Catania",
    "spa manicure Catania",
    "nail art Catania",
    "pedicure Catania",
    "smalto semipermanente Catania",
    "nails studio Catania",
    "unghie gel Catania",
    "refill unghie Catania",
    "extension ciglia unghie Catania",
    "beauty center nails Catania",
    # === QUARTIERI CATANIA ===
    "centro estetico Via Etnea Catania",
    "nail bar Piazza Dante Catania",
    "centro unghie Via dei Crociferi Catania",
    "salone bellezza Borgo Catania",
    "manicure San Giovanni Galermo Catania",
    "nail art Nesima Catania",
    "centro estetico Picanello Catania",
    "unghie Monte Po Catania",
    # === CITTA' VICINE (entro 40km) ===
    "centro unghie Acireale",
    "nail bar Acireale",
    "manicure Acireale",
    "centro estetico Acireale",
    "centro unghie Misterbianco",
    "nail bar Misterbianco",
    "manicure Misterbianco",
    "centro estetico Misterbianco",
    "centro unghie Paternò",
    "nail bar Paternò",
    "manicure Paternò",
    "centro unghie Belpasso",
    "nail bar Belpasso",
    "manicure Belpasso",
    "centro unghie Aci Castello",
    "nail bar Aci Castello",
    "manicure Aci Castello",
    "centro unghie Aci Catena",
    "nail bar Aci Catena",
    "centro unghie San Giovanni La Punta",
    "nail bar San Giovanni La Punta",
    "centro unghie Tremestieri Etneo",
    "centro unghie Gravina di Catania",
    "centro unghie San Gregorio di Catania",
    "centro unghie Mascalucia",
    "centro unghie Nicolosi",
    # === TERMINI ALTERNATIVI ===
    "salone parrucchiere unghie Catania",
    "centro benessere unghie Catania",
    "salone estetico manicure Catania",
    "salone manicure pedicure Catania",
    "centro nails e bellezza Catania",
    "nail spa Catania",
    "beauty nails Catania",
    "nail designer Catania",
    "tecnico unghie Catania",
    "onycotecnia Catania",
    "manicure russa Catania",
    "nail art design Catania",
    "gel unghie Catania",
    "acrilico unghie Catania",
    "copertura unghie Catania",
    "sostituzione unghie Catania",
    "manicure spa Catania",
    "pedicure spa Catania",
]

# Termini da escludere (centri formazione, corsi, etc.)
TERMINI_ESCLUSI = [
    "corso", "corsi", "formazione", "scuola", "academy", "lezioni",
    "insegnamento", "training", "diploma", "certificazione", "master",
    "professionale", "stage", "tirocinio", "apprendistato"
]


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Contatto:
    nome_salone: str = ""
    responsabile: str = ""
    cellulare: str = ""
    indirizzo: str = ""
    categoria: str = ""
    email: str = ""
    instagram: str = ""
    facebook: str = ""
    sito_web: str = ""
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    place_id: str = ""
    note_attrezzature: str = ""
    fonte: str = ""
    data_raccolta: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome_salone": self.nome_salone,
            "responsabile": self.responsabile,
            "cellulare": self.cellulare,
            "indirizzo": self.indirizzo,
            "categoria": self.categoria,
            "email": self.email,
            "social": {"instagram": self.instagram, "facebook": self.facebook},
            "sito_web": self.sito_web,
            "rating": self.rating,
            "user_ratings_total": self.user_ratings_total,
            "place_id": self.place_id,
            "note_attrezzature": self.note_attrezzature,
            "fonte": self.fonte,
            "data_raccolta": self.data_raccolta,
        }


# ============================================================================
# VALIDAZIONE
# ============================================================================

class ValidatoreContatti:
    @staticmethod
    def normalizza_cellulare(numero: str) -> Optional[str]:
        if not numero:
            return None
        pulito = re.sub(r"[^\d]", "", numero)
        if pulito.startswith("0039") and len(pulito) > 10:
            pulito = pulito[4:]
        elif pulito.startswith("39") and len(pulito) == 12:
            pulito = pulito[2:]
        if len(pulito) != 10 or not pulito.startswith("3"):
            return None
        return f"+39{pulito}"

    @staticmethod
    def deduplica(contatti: List[Contatto]) -> List[Contatto]:
        visti: Set[str] = set()
        unici: List[Contatto] = []
        for c in contatti:
            if not c.cellulare:
                continue
            chiave = f"{c.cellulare}|{c.nome_salone.lower().strip()}"
            if chiave not in visti:
                visti.add(chiave)
                unici.append(c)
        return unici

    @staticmethod
    def filtra_formazione(contatti: List[Contatto]) -> List[Contatto]:
        """Filtra via contatti che sono centri di formazione/corsi"""
        filtrati: List[Contatto] = []
        for c in contatti:
            nome_lower = c.nome_salone.lower()
            # Controlla se contiene termini esclusi
            if any(term in nome_lower for term in TERMINI_ESCLUSI):
                print(f"    [FILTRO] Escluso (formazione): {c.nome_salone}")
                continue
            filtrati.append(c)
        return filtrati


# ============================================================================
# GOOGLE PLACES API (da ava/lib/tools/google-maps.ts)
# ============================================================================

class GooglePlacesScraper:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            print("⚠️  GOOGLE_PLACES_API_KEY non trovata. Google Places API disabilitata.")

    def _call_api(self, endpoint: str, params: Dict) -> Dict:
        base_url = "https://maps.googleapis.com/maps/api/place"
        url = f"{base_url}/{endpoint}/json"
        params["key"] = self.api_key
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"  Errore API: {e}")
            return {"status": "ERROR", "error_message": str(e)}

    def text_search(self, query: str) -> List[Dict]:
        if not self.api_key:
            return []
        print(f"  [Google Places] Text Search: '{query}'")
        params = {
            "query": query,
            "location": f"{CATANIA_COORDS['lat']},{CATANIA_COORDS['lng']}",
            "radius": RAGGIO_METRI,
        }
        data = self._call_api("textsearch", params)
        if data.get("status") not in ["OK", "ZERO_RESULTS"]:
            print(f"    Errore: {data.get('status')}")
            return []
        results = data.get("results", [])
        print(f"    Trovati: {len(results)} risultati")
        return results

    def place_details(self, place_id: str) -> Optional[Dict]:
        if not self.api_key:
            return None
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,types",
        }
        data = self._call_api("details", params)
        if data.get("status") != "OK":
            return None
        return data.get("result")

    def cerca_tutti(self) -> List[Contatto]:
        if not self.api_key:
            print("  (Saltato - richiede GOOGLE_PLACES_API_KEY)")
            return []
        print("\n[Google Places API]")
        print("-" * 50)
        tutti_contatti: List[Contatto] = []
        place_ids_visti: Set[str] = set()
        for query in QUERY_RICERCA:
            results = self.text_search(query)
            for place in results:
                place_id = place.get("place_id")
                if place_id in place_ids_visti:
                    continue
                place_ids_visti.add(place_id)
                contatto = Contatto(
                    nome_salone=place.get("name", ""),
                    indirizzo=place.get("formatted_address", ""),
                    place_id=place_id,
                    fonte="google_places",
                    data_raccolta=datetime.now().isoformat(),
                    categoria=", ".join(place.get("types", [])[:2]),
                    rating=place.get("rating"),
                    user_ratings_total=place.get("user_ratings_total"),
                )
                details = self.place_details(place_id)
                if details:
                    telefono = details.get("formatted_phone_number", "")
                    contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""
                    contatto.sito_web = details.get("website", "")
                if contatto.nome_salone:
                    tutti_contatti.append(contatto)
            time.sleep(0.5)
        validi = [c for c in tutti_contatti if c.cellulare]
        print(f"\n  Totale contatti validi: {len(validi)}/{len(tutti_contatti)}")
        return validi


# ============================================================================
# SELENIUM BASE SCRAPER
# ============================================================================

class SeleniumScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None

    def setup(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
        except Exception as e:
            print(f"  Errore setup Chrome: {e}")
            # Fallback a chromedriver di sistema
            self.driver = webdriver.Chrome(options=options)

    def teardown(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def accetta_cookie(self):
        """Cerca e accetta banner cookie"""
        selectors = [
            "#onetrust-accept-btn-handler",
            "button[data-testid='cookie-accept']",
            ".cookie-accept",
            "#accept-cookies",
            "button[contains(text(), 'Accetta')]",
        ]
        for selector in selectors:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                btn.click()
                time.sleep(1)
                return True
            except:
                continue
        return False


# ============================================================================
# PAGINE GIALLE SCRAPER
# ============================================================================

class PagineGialleScraper(SeleniumScraper):
    def cerca(self, query: str, max_pagine: int = 2) -> List[Contatto]:
        contatti: List[Contatto] = []
        print(f"  Ricerca: '{query}'")
        for pagina in range(1, max_pagine + 1):
            try:
                url = f"https://www.paginegialle.it/ricerca/{quote_plus(query)}%20Catania/p-{pagina}"
                self.driver.get(url)
                time.sleep(3)
                self.accetta_cookie()
                time.sleep(2)

                cards = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "article.search-result, .item-list .item, [data-testid='search-result']"
                )

                for card in cards[:10]:
                    try:
                        contatto = self._estrai_contatto(card)
                        if contatto and contatto.cellulare:
                            contatti.append(contatto)
                    except:
                        continue

                print(f"    Pagina {pagina}: {len(cards)} risultati")

                # Controlla se c'è pagina successiva
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, "a.next:not(.disabled)")
                    if not next_btn.is_displayed():
                        break
                except:
                    break

                time.sleep(2)
            except Exception as e:
                print(f"    Errore pagina {pagina}: {e}")
                continue
        return contatti

    def _estrai_contatto(self, card) -> Optional[Contatto]:
        try:
            contatto = Contatto()
            contatto.fonte = "paginegialle.it"
            contatto.data_raccolta = datetime.now().isoformat()

            # Nome
            try:
                nome_elem = card.find_element(By.CSS_SELECTOR, "h2 a, .title a")
                contatto.nome_salone = nome_elem.text.strip()
            except:
                pass

            # Indirizzo
            try:
                addr_elem = card.find_element(By.CSS_SELECTOR, ".address, [data-testid='address']")
                contatto.indirizzo = addr_elem.text.strip()
            except:
                pass

            # Telefono
            try:
                tel_elem = card.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
                href = tel_elem.get_attribute("href") or ""
                telefono = href.replace("tel:", "").strip()
                contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""
            except:
                pass

            # Categoria
            try:
                cat_elem = card.find_element(By.CSS_SELECTOR, ".category")
                contatto.categoria = cat_elem.text.strip()
            except:
                pass

            return contatto if contatto.nome_salone else None
        except:
            return None

    def cerca_tutti(self) -> List[Contatto]:
        print("\n[PagineGialle.it]")
        print("-" * 50)
        self.setup()
        try:
            queries = [
                "centri unghie",
                "manicure",
                "ricostruzione unghie",
                "centri estetici",
                "nail bar",
            ]
            tutti: List[Contatto] = []
            for query in queries:
                contatti = self.cerca(query, max_pagine=2)
                tutti.extend(contatti)
                time.sleep(3)
            unici = ValidatoreContatti.deduplica(tutti)
            validi = [c for c in unici if c.cellulare]
            print(f"\n  Totale contatti validi: {len(validi)}/{len(tutti)}")
            return validi
        finally:
            self.teardown()


# ============================================================================
# TREATWELL SCRAPER
# ============================================================================

class TreatwellScraper(SeleniumScraper):
    def cerca_servizio(self, servizio: str, url: str) -> List[Contatto]:
        print(f"  Servizio: {servizio}")
        contatti: List[Contatto] = []
        try:
            self.driver.get(url)
            time.sleep(4)
            self.accetta_cookie()
            time.sleep(2)

            # Scroll per caricare
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            cards = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='venue-card'], .venue-card"
            )

            for card in cards[:15]:
                try:
                    contatto = Contatto()
                    contatto.fonte = "treatwell.it"
                    contatto.data_raccolta = datetime.now().isoformat()
                    contatto.categoria = f"centro estetico - {servizio}"

                    try:
                        nome_elem = card.find_element(By.CSS_SELECTOR, "h3, [data-testid='venue-name']")
                        contatto.nome_salone = nome_elem.text.strip()
                    except:
                        continue

                    try:
                        addr_elem = card.find_element(By.CSS_SELECTOR, ".address, [data-testid='venue-address']")
                        contatto.indirizzo = addr_elem.text.strip()
                    except:
                        pass

                    # Cerca link per telefono
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, "a[href*='/salone/']")
                        href = link_elem.get_attribute("href")
                        if href:
                            telefono = self._estrai_telefono_dettaglio(href)
                            if telefono:
                                contatto.cellulare = telefono
                    except:
                        pass

                    if contatto.nome_salone:
                        contatti.append(contatto)
                except:
                    continue

            print(f"    Trovati: {len(contatti)} contatti")
            return contatti
        except Exception as e:
            print(f"    Errore: {e}")
            return []

    def _estrai_telefono_dettaglio(self, url: str) -> Optional[str]:
        try:
            # Apri in nuova tab
            original_window = self.driver.current_window_handle
            self.driver.execute_script(f"window.open('{url}', '_blank')")
            time.sleep(3)

            # Switch a nuova tab
            new_window = [w for w in self.driver.window_handles if w != original_window][0]
            self.driver.switch_to.window(new_window)
            time.sleep(2)

            telefono = None
            try:
                tel_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
                href = tel_elem.get_attribute("href") or ""
                telefono = ValidatoreContatti.normalizza_cellulare(href.replace("tel:", ""))
            except:
                pass

            # Chiudi tab e torna
            self.driver.close()
            self.driver.switch_to.window(original_window)
            return telefono
        except:
            return None

    def cerca_tutti(self) -> List[Contatto]:
        print("\n[Treatwell.it]")
        print("-" * 50)
        self.setup()
        try:
            servizi = [
                ("manicure", "https://www.treatwell.it/salone/manicure/catania-ct"),
                ("pedicure", "https://www.treatwell.it/salone/pedicure/catania-ct"),
                ("ricostruzione-unghie", "https://www.treatwell.it/salone/ricostruzione-unghie/catania-ct"),
                ("semipermanente", "https://www.treatwell.it/salone/smalti-semipermanenti/catania-ct"),
            ]
            tutti: List[Contatto] = []
            for servizio, url in servizi:
                contatti = self.cerca_servizio(servizio, url)
                tutti.extend(contatti)
                time.sleep(3)
            unici = ValidatoreContatti.deduplica(tutti)
            validi = [c for c in unici if c.cellulare]
            print(f"\n  Totale contatti validi: {len(validi)}/{len(tutti)}")
            return validi
        finally:
            self.teardown()


# ============================================================================
# FRESHA SCRAPER
# ============================================================================

class FreshaScraper(SeleniumScraper):
    def cerca_tutti(self) -> List[Contatto]:
        print("\n[Fresha.com]")
        print("-" * 50)
        self.setup()
        try:
            url = "https://www.fresha.com/it/explore?query=Catania&category=beauty-salon&country=it"
            self.driver.get(url)
            time.sleep(4)

            # Scroll
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            cards = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='business-card'], a[href*='/business/']"
            )

            contatti: List[Contatto] = []
            for card in cards[:20]:
                try:
                    contatto = Contatto()
                    contatto.fonte = "fresha.com"
                    contatto.data_raccolta = datetime.now().isoformat()
                    contatto.categoria = "salone bellezza"

                    try:
                        nome_elem = card.find_element(By.CSS_SELECTOR, "h3, h4")
                        contatto.nome_salone = nome_elem.text.strip()
                    except:
                        continue

                    try:
                        addr_elem = card.find_element(By.CSS_SELECTOR, ".address, .location")
                        contatto.indirizzo = addr_elem.text.strip()
                    except:
                        pass

                    if contatto.nome_salone:
                        contatti.append(contatto)
                except:
                    continue

            validi = [c for c in contatti if c.cellulare]
            print(f"\n  Trovati: {len(contatti)} saloni ({len(validi)} con telefono)")
            print("  Nota: Fresha spesso richiede login per vedere telefoni")
            return contatti
        finally:
            self.teardown()


# ============================================================================
# MAIN
# ============================================================================

def salva_contatti_json(contatti: List[Contatto], filename: str = "contatti_catania.json"):
    """Salva contatti in formato JSON"""
    data = {
        "metadata": {
            "data_generazione": datetime.now().isoformat(),
            "totale_contatti": len(contatti),
            "area": "Catania e dintorni (40km)",
            "servizio_target": "noleggio stampante unghie",
            "fonti": ["google_places", "paginegialle.it", "treatwell.it", "fresha.com"],
        },
        "contatti": [c.to_dict() for c in contatti],
    }
    filepath = f"/home/ioilmio/quadro/nailstech/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ JSON: {filepath}")
    return filepath


def salva_contatti_csv(contatti: List[Contatto], filename: str = "contatti_catania.csv"):
    """Salva contatti in formato CSV (ottimale per importazioni)"""
    filepath = f"/home/ioilmio/quadro/nailstech/{filename}"

    # Campi per CSV (semplificati per importazione)
    fieldnames = [
        "nome_salone", "cellulare", "indirizzo", "categoria",
        "sito_web", "rating", "fonte"
    ]

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in contatti:
            writer.writerow({
                "nome_salone": c.nome_salone,
                "cellulare": c.cellulare,
                "indirizzo": c.indirizzo,
                "categoria": c.categoria,
                "sito_web": c.sito_web,
                "rating": c.rating,
                "fonte": c.fonte,
            })

    print(f"  ✓ CSV: {filepath}")
    return filepath


def salva_contatti_excel(contatti: List[Contatto], filename: str = "contatti_catania.xlsx"):
    """Salva contatti in formato Excel"""
    if pd is None:
        print("  ⚠️  Pandas non installato, salto Excel")
        return None

    filepath = f"/home/ioilmio/quadro/nailstech/{filename}"

    # Prepara dati per DataFrame
    data = []
    for c in contatti:
        data.append({
            "Nome Salone": c.nome_salone,
            "Cellulare": c.cellulare,
            "Indirizzo": c.indirizzo,
            "Categoria": c.categoria,
            "Sito Web": c.sito_web,
            "Rating": c.rating,
            "Recensioni": c.user_ratings_total,
            "Fonte": c.fonte,
            "Data Raccolta": c.data_raccolta,
        })

    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False, sheet_name="Contatti Catania")
    print(f"  ✓ Excel: {filepath}")
    return filepath


def salva_tutti_formati(contatti: List[Contatto]):
    """Salva contatti in tutti i formati disponibili"""
    print(f"\n{'='*60}")
    print(f"SALVATAGGIO CONTATTI - {len(contatti)} trovati")
    print(f"{'='*60}")

    salva_contatti_json(contatti)
    salva_contatti_csv(contatti)
    salva_contatti_excel(contatti)

    print(f"{'='*60}")


def main():
    print("=" * 60)
    print("RACCOLTA CONTATTI - CENTRI UNGHIE CATANIA")
    print("Google Places API + Selenium Scraping")
    print("=" * 60)

    tutti_contatti: List[Contatto] = []

    # 1. Google Places API
    google = GooglePlacesScraper()
    tutti_contatti.extend(google.cerca_tutti())

    # 2. Pagine Gialle
    pg = PagineGialleScraper()
    tutti_contatti.extend(pg.cerca_tutti())

    # 3. Treatwell
    tw = TreatwellScraper()
    tutti_contatti.extend(tw.cerca_tutti())

    # 4. Fresha
    fr = FreshaScraper()
    tutti_contatti.extend(fr.cerca_tutti())

    # Deduplicazione e filtro formazione
    print("\n" + "=" * 60)
    print("VALIDAZIONE, DEDUPLICAZIONE E FILTRO")
    print("=" * 60)
    print(f"Contatti totali raccolti: {len(tutti_contatti)}")

    # Filtro formazione
    senza_formazione = ValidatoreContatti.filtra_formazione(tutti_contatti)
    print(f"Dopo filtro formazione: {len(senza_formazione)}")

    # Deduplicazione
    unici = ValidatoreContatti.deduplica(senza_formazione)
    print(f"Contatti unici finali: {len(unici)}")

    # Statistiche
    per_fonte: Dict[str, int] = {}
    for c in unici:
        per_fonte[c.fonte] = per_fonte.get(c.fonte, 0) + 1
    print("\nBreakdown per fonte:")
    for fonte, count in sorted(per_fonte.items(), key=lambda x: -x[1]):
        print(f"  - {fonte}: {count}")

    # Salva in tutti i formati
    salva_tutti_formati(unici)

    print("\n" + "=" * 60)
    print("RACCOLTA COMPLETATA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
