#!/usr/bin/env python3
"""
Raccolta Contatti - Centri Unghie Catania
Basato su approccio Google Places API (inspirato da /home/ioilmio/quadro/ava)

Fonti:
- Google Places API (Text Search + Place Details)
- PagineGialle.it (scraping con Playwright)
- Treatwell.it (scraping con Playwright)
- Fresha.com (scraping con Playwright)

Output: contatti_catania.json con nome, cellulare, indirizzo, categoria
"""

import json
import os
import re
import sys
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass, asdict, field
from urllib.parse import urlencode, quote_plus

import requests
from playwright.async_api import async_playwright, Page


# ============================================================================
# CONFIGURAZIONE
# ============================================================================

CATANIA_COORDS = {"lat": 37.5079, "lng": 15.0830}
RAGGIO_KM = 40
RAGGIO_METRI = RAGGIO_KM * 1000

# Categorie di ricerca per centri che possono avere servizio unghie
QUERY_RICERCA = [
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
]


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Contatto:
    nome_salone: str = ""
    responsabile: str = ""
    cellulare: str = ""  # Solo cellulari, NO fissi
    indirizzo: str = ""
    categoria: str = ""
    email: str = ""
    instagram: str = ""
    facebook: str = ""
    sito_web: str = ""
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    place_id: str = ""  # Google Place ID per riferimento
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
            "social": {
                "instagram": self.instagram,
                "facebook": self.facebook,
            },
            "sito_web": self.sito_web,
            "rating": self.rating,
            "user_ratings_total": self.user_ratings_total,
            "place_id": self.place_id,
            "note_attrezzature": self.note_attrezzature,
            "fonte": self.fonte,
            "data_raccolta": self.data_raccolta,
        }


# ============================================================================
# VALIDAZIONE E UTILITIES
# ============================================================================

class ValidatoreContatti:
    """Valida e normalizza i contatti raccolti"""

    @staticmethod
    def normalizza_cellulare(numero: str) -> Optional[str]:
        """
        Normalizza numero cellulare italiano.
        Ritorna None se è un numero fisso o non valido.
        """
        if not numero:
            return None

        # Rimuovi tutti i caratteri non numerici
        pulito = re.sub(r'[^\d]', '', numero)

        # Se inizia con 0039 o +39, rimuovi il prefisso
        if pulito.startswith('0039') and len(pulito) > 10:
            pulito = pulito[4:]
        elif pulito.startswith('39') and len(pulito) == 12:
            pulito = pulito[2:]

        # Verifica che sia un cellulare italiano (inizia con 3, 10 cifre)
        if len(pulito) != 10:
            return None
        if not pulito.startswith('3'):
            return None  # Non è un cellulare

        return f"+39{pulito}"

    @staticmethod
    def deduplica(contatti: List[Contatto]) -> List[Contatto]:
        """Rimuove duplicati basati su cellulare + nome"""
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


# ============================================================================
# GOOGLE PLACES API (Basato su ava/lib/tools/google-maps.ts)
# ============================================================================

class GooglePlacesScraper:
    """
    Scraper Google Places API
    Implementazione basata su /home/ioilmio/quadro/ava/lib/tools/google-maps.ts
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            print("⚠️  GOOGLE_PLACES_API_KEY non trovata. Google Places API disabilitata.")

    def _call_api(self, endpoint: str, params: Dict) -> Dict:
        """Chiama l'API Google Places"""
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
        """
        Text Search API - cerca luoghi per query testuale
        """
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
            print(f"    Errore: {data.get('status')} - {data.get('error_message', '')}")
            return []

        results = data.get("results", [])
        print(f"    Trovati: {len(results)} risultati")
        return results

    def place_details(self, place_id: str) -> Optional[Dict]:
        """
        Place Details API - ottieni dettagli completi di un luogo
        Include: telefono, sito web, orari, ecc.
        """
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
        """
        Cerca tutti i centri unghie nell'area di Catania
        """
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

                # Crea contatto base
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

                # Ottieni dettagli per telefono e sito web
                details = self.place_details(place_id)
                if details:
                    telefono = details.get("formatted_phone_number", "")
                    contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""
                    contatto.sito_web = details.get("website", "")

                if contatto.nome_salone:
                    tutti_contatti.append(contatto)

            # Rate limiting
            import time
            time.sleep(0.5)

        # Filtra solo contatti con cellulare valido
        validi = [c for c in tutti_contatti if c.cellulare]
        print(f"\n  Totale contatti validi: {len(validi)}/{len(tutti_contatti)}")

        return validi


# ============================================================================
# PAGINE GIALLE SCRAPER (Playwright)
# ============================================================================

class PagineGialleScraper:
    """Scraper per PagineGialle.it"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca(self, page: Page, query: str, max_pagine: int = 2) -> List[Contatto]:
        """Cerca attività su PagineGialle"""
        print(f"  Ricerca: '{query}'")

        for pagina in range(1, max_pagine + 1):
            try:
                url = f"https://www.paginegialle.it/ricerca/{quote_plus(query)}%20Catania/p-{pagina}"
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)

                # Accetta cookie
                try:
                    cookie_btn = await page.query_selector(
                        'button[data-testid="cookie-accept"], '
                        '#onetrust-accept-btn-handler, '
                        '.cookie-banner .accept'
                    )
                    if cookie_btn:
                        await cookie_btn.click()
                        await asyncio.sleep(1)
                except:
                    pass

                # Estrai risultati
                cards = await page.query_selector_all(
                    'article.search-result, '
                    '.item-list .item, '
                    '[data-testid="search-result"]'
                )

                for card in cards[:10]:
                    contatto = await self._estrai_contatto_da_card(card)
                    if contatto and contatto.cellulare:
                        self.contatti.append(contatto)

                print(f"    Pagina {pagina}: {len(cards)} risultati trovati")

                # Controlla se c'è pagina successiva
                next_btn = await page.query_selector('a.next, .pagination-next:not(.disabled)')
                if not next_btn:
                    break

                await asyncio.sleep(2)

            except Exception as e:
                print(f"    Errore pagina {pagina}: {e}")
                continue

        return self.contatti

    async def _estrai_contatto_da_card(self, card) -> Optional[Contatto]:
        """Estrae contatto da una card risultato"""
        try:
            contatto = Contatto()
            contatto.fonte = "paginegialle.it"
            contatto.data_raccolta = datetime.now().isoformat()

            # Nome
            nome_elem = await card.query_selector('h2 a, .title a, [data-testid="business-name"]')
            if nome_elem:
                contatto.nome_salone = (await nome_elem.inner_text()).strip()

            # Indirizzo
            addr_elem = await card.query_selector('.address, [data-testid="address"]')
            if addr_elem:
                contatto.indirizzo = (await addr_elem.inner_text()).strip()

            # Telefono
            tel_elem = await card.query_selector('a[href^="tel:"]')
            if tel_elem:
                href = await tel_elem.get_attribute('href') or ""
                telefono = href.replace('tel:', '').strip()
                contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

            # Categoria
            cat_elem = await card.query_selector('.category, .categoria')
            if cat_elem:
                contatto.categoria = (await cat_elem.inner_text()).strip()

            return contatto if contatto.nome_salone else None

        except:
            return None

    async def cerca_tutti(self, page: Page) -> List[Contatto]:
        """Esegue tutte le ricerche su PagineGialle"""
        print("\n[PagineGialle.it]")
        print("-" * 50)

        queries = [
            "centri unghie",
            "manicure",
            "ricostruzione unghie",
            "centri estetici",
            "nail bar",
        ]

        for query in queries:
            await self.cerca(page, query, max_pagine=2)
            await asyncio.sleep(3)

        # Deduplica interna
        unici = ValidatoreContatti.deduplica(self.contatti)
        validi = [c for c in unici if c.cellulare]

        print(f"\n  Totale contatti validi: {len(validi)}/{len(self.contatti)}")
        return validi


# ============================================================================
# TREATWELL SCRAPER (Playwright)
# ============================================================================

class TreatwellScraper:
    """Scraper per Treatwell.it"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca_servizio(self, page: Page, servizio: str, url: str) -> List[Contatto]:
        """Cerca saloni per un servizio specifico"""
        print(f"  Servizio: {servizio}")

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Accetta cookie
            try:
                cookie_btn = await page.query_selector('#onetrust-accept-btn-handler')
                if cookie_btn:
                    await cookie_btn.click()
                    await asyncio.sleep(1)
            except:
                pass

            # Scroll per caricare tutti
            for _ in range(3):
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            # Estrai cards
            cards = await page.query_selector_all(
                '[data-testid="venue-card"], .venue-card'
            )

            contatti_locali: List[Contatto] = []

            for card in cards[:15]:
                try:
                    contatto = Contatto()
                    contatto.fonte = "treatwell.it"
                    contatto.data_raccolta = datetime.now().isoformat()
                    contatto.categoria = f"centro estetico - {servizio}"

                    # Nome
                    nome_elem = await card.query_selector('h3, [data-testid="venue-name"]')
                    if nome_elem:
                        contatto.nome_salone = (await nome_elem.inner_text()).strip()

                    # Indirizzo
                    addr_elem = await card.query_selector('.address, [data-testid="venue-address"]')
                    if addr_elem:
                        contatto.indirizzo = (await addr_elem.inner_text()).strip()

                    # Link per telefono
                    link_elem = await card.query_selector('a[href*="/salone/"]')
                    if link_elem:
                        href = await link_elem.get_attribute('href')
                        if href:
                            telefono = await self._estrai_telefono_da_dettaglio(page, href)
                            if telefono:
                                contatto.cellulare = telefono

                    if contatto.nome_salone:
                        contatti_locali.append(contatto)

                except:
                    continue

            print(f"    Trovati: {len(contatti_locali)} contatti")
            return contatti_locali

        except Exception as e:
            print(f"    Errore: {e}")
            return []

    async def _estrai_telefono_da_dettaglio(self, page: Page, path: str) -> Optional[str]:
        """Estrae telefono dalla pagina dettaglio"""
        try:
            new_page = await page.context.new_page()
            url = f"https://www.treatwell.it{path}" if path.startswith('/') else path

            await new_page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(2)

            tel_elem = await new_page.query_selector('a[href^="tel:"]')
            telefono = None

            if tel_elem:
                href = await tel_elem.get_attribute('href') or ""
                telefono = ValidatoreContatti.normalizza_cellulare(
                    href.replace('tel:', '')
                )

            await new_page.close()
            return telefono

        except:
            return None

    async def cerca_tutti(self, page: Page) -> List[Contatti]:
        """Esegue tutte le ricerche su Treatwell"""
        print("\n[Treatwell.it]")
        print("-" * 50)

        servizi = [
            ("manicure", "https://www.treatwell.it/salone/manicure/catania-ct"),
            ("pedicure", "https://www.treatwell.it/salone/pedicure/catania-ct"),
            ("ricostruzione-unghie", "https://www.treatwell.it/salone/ricostruzione-unghie/catania-ct"),
            ("semipermanente", "https://www.treatwell.it/salone/smalti-semipermanenti/catania-ct"),
        ]

        for servizio, url in servizi:
            contatti = await self.cerca_servizio(page, servizio, url)
            self.contatti.extend(contatti)
            await asyncio.sleep(3)

        # Deduplica e filtra
        unici = ValidatoreContatti.deduplica(self.contatti)
        validi = [c for c in unici if c.cellulare]

        print(f"\n  Totale contatti validi: {len(validi)}/{len(self.contatti)}")
        return validi


# ============================================================================
# FRESHA SCRAPER (Playwright)
# ============================================================================

class FreshaScraper:
    """Scraper per Fresha.com"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca_tutti(self, page: Page) -> List[Contatto]:
        """Cerca saloni su Fresha"""
        print("\n[Fresha.com]")
        print("-" * 50)

        url = "https://www.fresha.com/it/explore?query=Catania&category=beauty-salon&country=it"

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Scroll
            for _ in range(3):
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            # Estrai business
            cards = await page.query_selector_all(
                '[data-testid="business-card"], a[href*="/business/"]'
            )

            for card in cards[:20]:
                try:
                    contatto = Contatto()
                    contatto.fonte = "fresha.com"
                    contatto.data_raccolta = datetime.now().isoformat()
                    contatto.categoria = "salone bellezza"

                    # Nome
                    nome_elem = await card.query_selector('h3, h4')
                    if nome_elem:
                        contatto.nome_salone = (await nome_elem.inner_text()).strip()

                    # Indirizzo
                    addr_elem = await card.query_selector('.address, .location')
                    if addr_elem:
                        contatto.indirizzo = (await addr_elem.inner_text()).strip()

                    # Telefono (spesso non visibile direttamente, richiederebbe visita)

                    if contatto.nome_salone:
                        self.contatti.append(contatto)

                except:
                    continue

            validi = [c for c in self.contatti if c.cellulare]
            print(f"\n  Trovati: {len(self.contatti)} saloni ({len(validi)} con telefono)")
            print("  Nota: Fresha spesso non mostra telefoni direttamente")

            return self.contatti

        except Exception as e:
            print(f"  Errore: {e}")
            return []


# ============================================================================
# MAIN
# ============================================================================

def salva_contatti(contatti: List[Contatto], filename: str = "contatti_catania.json"):
    """Salva contatti in file JSON"""
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

    print(f"\n{'='*60}")
    print(f"✓ Salvati {len(contatti)} contatti in:")
    print(f"  {filepath}")
    print(f"{'='*60}")


async def main():
    """Funzione principale"""
    print("=" * 60)
    print("RACCOLTA CONTATTI - CENTRI UNGHIE CATANIA")
    print("Google Places API + Scraping Directory")
    print("=" * 60)

    tutti_contatti: List[Contatto] = []

    # 1. Google Places API (se API key disponibile)
    google_scraper = GooglePlacesScraper()
    contatti_google = google_scraper.cerca_tutti()
    tutti_contatti.extend(contatti_google)

    # 2. Scraping con Playwright
    print("\n" + "=" * 60)
    print("SCRAPING DIRECTORY CON PLAYWRIGHT")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1280, "height": 800},
        )

        # Pagine Gialle
        page_pg = await context.new_page()
        pg_scraper = PagineGialleScraper()
        contatti_pg = await pg_scraper.cerca_tutti(page_pg)
        tutti_contatti.extend(contatti_pg)
        await page_pg.close()

        # Treatwell
        page_tw = await context.new_page()
        tw_scraper = TreatwellScraper()
        contatti_tw = await tw_scraper.cerca_tutti(page_tw)
        tutti_contatti.extend(contatti_tw)
        await page_tw.close()

        # Fresha
        page_fr = await context.new_page()
        fr_scraper = FreshaScraper()
        contatti_fr = await fr_scraper.cerca_tutti(page_fr)
        tutti_contatti.extend(contatti_fr)
        await page_fr.close()

        await browser.close()

    # Deduplicazione finale
    print("\n" + "=" * 60)
    print("VALIDAZIONE E DEDUPLICAZIONE")
    print("=" * 60)
    print(f"Contatti totali raccolti: {len(tutti_contatti)}")

    contatti_unici = ValidatoreContatti.deduplica(tutti_contatti)
    print(f"Contatti unici: {len(contatti_unici)}")

    # Statistiche per fonte
    per_fonte: Dict[str, int] = {}
    for c in contatti_unici:
        per_fonte[c.fonte] = per_fonte.get(c.fonte, 0) + 1

    print("\nBreakdown per fonte:")
    for fonte, count in sorted(per_fonte.items(), key=lambda x: -x[1]):
        print(f"  - {fonte}: {count}")

    # Salva
    salva_contatti(contatti_unici)

    print("\n" + "=" * 60)
    print("RACCOLTA COMPLETATA!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
