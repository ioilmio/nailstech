#!/usr/bin/env python3
"""
Script di automazione per raccolta contatti centri unghie e servizi unghie
Area: Catania e dintorni (max 40km)
Fonti: PagineGialle, Treatwell, Fresha, Google Maps
Versione 2: Usa Playwright per siti JavaScript-heavy
"""

import json
import re
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright, Page, Browser


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
    note_attrezzature: str = ""
    fonte: str = ""
    data_raccolta: str = ""

    def to_dict(self) -> Dict:
        return {
            "nome_salone": self.nome_salone,
            "responsabile": self.responsabile,
            "cellulare": self.cellulare,
            "indirizzo": self.indirizzo,
            "categoria": self.categoria,
            "email": self.email,
            "social": {
                "instagram": self.instagram,
                "facebook": self.facebook
            },
            "sito_web": self.sito_web,
            "note_attrezzature": self.note_attrezzature,
            "fonte": self.fonte,
            "data_raccolta": self.data_raccolta
        }


class ValidatoreContatti:
    """Valida e normalizza i contatti raccolti"""

    @staticmethod
    def normalizza_cellulare(numero: str) -> Optional[str]:
        """Normalizza numero cellulare italiano, rimuove fissi"""
        if not numero:
            return None

        # Rimuovi spazi, trattini, parentesi, punti
        numero_pulito = re.sub(r'[\s\-\.\(\)\/]', '', numero)

        # Rimuovi prefisso internazionale se presente
        if numero_pulito.startswith('+39'):
            numero_pulito = numero_pulito[3:]
        elif numero_pulito.startswith('0039'):
            numero_pulito = numero_pulito[4:]

        # Verifica che sia un numero italiano valido (deve iniziare con 3 e avere 10 cifre)
        if not re.match(r'^3\d{9}$', numero_pulito):
            return None  # Esclude numeri fissi e non validi

        return f"+39{numero_pulito}"

    @staticmethod
    def deduplica_contatti(contatti: List[Contatto]) -> List[Contatto]:
        """Rimuove duplicati basati su cellulare + nome"""
        visti: Set[str] = set()
        unici: List[Contatto] = []

        for c in contatti:
            chiave = f"{c.cellulare}|{c.nome_salone.lower().strip()}"
            if chiave not in visti and c.cellulare:
                visti.add(chiave)
                unici.append(c)

        return unici

    @staticmethod
    def estrai_telefoni_da_testo(testo: str) -> List[str]:
        """Estrae tutti i numeri di telefono da un testo"""
        if not testo:
            return []

        # Pattern per numeri italiani
        pattern = r'(?:\+39|0039)?[\s\-\.]?3\d{2}[\s\-\.]?\d{3}[\s\-\.]?\d{4}'
        trovati = re.findall(pattern, testo)

        normalizzati = []
        for num in trovati:
            norm = ValidatoreContatti.normalizza_cellulare(num)
            if norm:
                normalizzati.append(norm)

        return list(set(normalizzati))


class ScraperPagineGialle:
    """Scraper per PagineGialle.it usando Playwright"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca(self, page: Page, query: str, localita: str = "Catania", max_pagine: int = 3) -> List[Contatto]:
        """Cerca attività su PagineGialle"""
        print(f"[PagineGialle] Ricerca: '{query}' a {localita}")

        for pagina in range(1, max_pagine + 1):
            try:
                url = f"https://www.paginegialle.it/ricerca/{quote(query)}%20{quote(localita)}/p-{pagina}"
                print(f"  Navigazione: {url}")

                await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)

                # Accetta cookie se presente
                try:
                    cookie_btn = await page.query_selector('button[data-testid="cookie-accept"], .cookie-accept, #accept-cookies')
                    if cookie_btn:
                        await cookie_btn.click()
                        await asyncio.sleep(1)
                except:
                    pass

                # Estrai risultati
                contatti_pagina = await self._estrai_contatti_da_pagina(page)
                self.contatti.extend(contatti_pagina)
                print(f"  Pagina {pagina}: {len(contatti_pagina)} contatti")

                # Verifica se ci sono più pagine
                next_btn = await page.query_selector('a.next, [aria-label="Next"], .pagination-next')
                if not next_btn:
                    break

                await asyncio.sleep(2)

            except Exception as e:
                print(f"  Errore pagina {pagina}: {e}")
                continue

        return self.contatti

    async def _estrai_contatti_da_pagina(self, page: Page) -> List[Contatto]:
        """Estrae contatti dalla pagina caricata"""
        contatti = []

        # Selettori per risultati PagineGialle
        selettori_card = [
            'article.search-result',
            '.item-list .item',
            '[data-testid="search-result"]',
            '.result-item'
        ]

        cards = []
        for selettore in selettori_card:
            cards = await page.query_selector_all(selettore)
            if cards:
                break

        for card in cards[:10]:
            try:
                contatto = Contatto()
                contatto.fonte = "paginegialle.it"
                contatto.data_raccolta = datetime.now().isoformat()

                # Nome
                nome_elem = await card.query_selector('h2 a, .title a, [data-testid="business-name"]')
                if nome_elem:
                    contatto.nome_salone = await nome_elem.inner_text()

                # Indirizzo
                addr_elem = await card.query_selector('.address, [data-testid="address"], .indirizzo')
                if addr_elem:
                    contatto.indirizzo = await addr_elem.inner_text()

                # Telefono - cerca in vari posti
                tel_elem = await card.query_selector('a[href^="tel:"], .telefono, [data-testid="phone"]')
                if tel_elem:
                    tel_href = await tel_elem.get_attribute('href') or ""
                    tel_testo = await tel_elem.inner_text()

                    # Prova href tel:
                    if 'tel:' in tel_href:
                        telefono = tel_href.replace('tel:', '').strip()
                    else:
                        telefono = tel_testo

                    contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

                # Categoria
                cat_elem = await card.query_selector('.category, .categoria, [data-testid="category"]')
                if cat_elem:
                    contatto.categoria = await cat_elem.inner_text()

                # Se non ha telefono, prova a cliccare per dettagli
                if not contatto.cellulare:
                    try:
                        link_elem = await card.query_selector('a[href*="/catania/"]')
                        if link_elem:
                            href = await link_elem.get_attribute('href')
                            if href:
                                telefono = await self._estrai_telefono_da_dettaglio(page, href)
                                if telefono:
                                    contatto.cellulare = telefono
                    except:
                        pass

                if contatto.nome_salone:
                    contatti.append(contatto)

            except Exception as e:
                continue

        return contatti

    async def _estrai_telefono_da_dettaglio(self, page: Page, path: str) -> Optional[str]:
        """Visita pagina dettaglio per estrarre telefono"""
        try:
            url = f"https://www.paginegialle.it{path}" if path.startswith('/') else path
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1)

            # Cerca telefono
            tel_elem = await page.query_selector('a[href^="tel:"]')
            if tel_elem:
                href = await tel_elem.get_attribute('href') or ""
                telefono = href.replace('tel:', '').strip()
                return ValidatoreContatti.normalizza_cellulare(telefono)

        except:
            pass
        return None


class ScraperTreatwell:
    """Scraper per Treatwell.it"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca_saloni_catania(self, page: Page) -> List[Contatto]:
        """Cerca saloni a Catania con servizi unghie"""
        print("[Treatwell] Ricerca saloni a Catania...")

        servizi_unghie = [
            ("manicure", "https://www.treatwell.it/salone/manicure/catania-ct"),
            ("pedicure", "https://www.treatwell.it/salone/pedicure/catania-ct"),
            ("ricostruzione-unghie", "https://www.treatwell.it/salone/ricostruzione-unghie/catania-ct"),
            ("smalto-semipermanente", "https://www.treatwell.it/salone/smalti-semipermanenti/catania-ct"),
        ]

        for servizio, url in servizi_unghie:
            try:
                print(f"  Servizio: {servizio}")
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(3)

                # Accetta cookie
                try:
                    cookie_btn = await page.query_selector('button[data-testid="accept-cookies"], #onetrust-accept-btn-handler')
                    if cookie_btn:
                        await cookie_btn.click()
                        await asyncio.sleep(1)
                except:
                    pass

                contatti = await self._estrai_saloni_da_pagina(page, servizio)
                self.contatti.extend(contatti)
                print(f"    Trovati: {len(contatti)} contatti")

                await asyncio.sleep(3)

            except Exception as e:
                print(f"    Errore {servizio}: {e}")

        return self.contatti

    async def _estrai_saloni_da_pagina(self, page: Page, servizio: str) -> List[Contatto]:
        """Estrae saloni dalla pagina Treatwell"""
        contatti = []

        # Scrolla per caricare tutti i risultati
        for _ in range(3):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(1)

        # Selettori per card salone
        selettori = [
            '[data-testid="venue-card"]',
            '.venue-card',
            'article[class*="venue"]'
        ]

        cards = []
        for sel in selettori:
            cards = await page.query_selector_all(sel)
            if cards:
                break

        for card in cards[:20]:
            try:
                contatto = Contatto()
                contatto.fonte = "treatwell.it"
                contatto.data_raccolta = datetime.now().isoformat()
                contatto.categoria = f"centro estetico - {servizio}"

                # Nome
                nome_sel = await card.query_selector('h3, .venue-name, [data-testid="venue-name"]')
                if nome_sel:
                    contatto.nome_salone = await nome_sel.inner_text()

                # Indirizzo
                addr_sel = await card.query_selector('.address, [data-testid="venue-address"]')
                if addr_sel:
                    contatto.indirizzo = await addr_sel.inner_text()

                # Link dettaglio
                link_sel = await card.query_selector('a[href*="/salone/"]')
                if link_sel:
                    href = await link_sel.get_attribute('href')
                    if href:
                        telefono = await self._estrai_telefono_dettaglio(page, href)
                        if telefono:
                            contatto.cellulare = telefono

                if contatto.nome_salone:
                    contatti.append(contatto)

            except:
                continue

        return contatti

    async def _estrai_telefono_dettaglio(self, page: Page, path: str) -> Optional[str]:
        """Estrae telefono da pagina dettaglio"""
        try:
            url = f"https://www.treatwell.it{path}" if path.startswith('/') else path

            # Apri in nuova tab temporanea
            new_page = await page.context.new_page()
            await new_page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(2)

            # Cerca telefono
            tel_sel = await new_page.query_selector('a[href^="tel:"], .phone-number, [data-testid="phone"]')
            telefono = None

            if tel_sel:
                href = await tel_sel.get_attribute('href') or ""
                testo = await tel_sel.inner_text()

                if 'tel:' in href:
                    telefono = ValidatoreContatti.normalizza_cellulare(href.replace('tel:', ''))
                else:
                    telefono = ValidatoreContatti.normalizza_cellulare(testo)

            await new_page.close()
            return telefono

        except:
            return None


class ScraperFresha:
    """Scraper per Fresha.com"""

    def __init__(self):
        self.contatti: List[Contatto] = []

    async def cerca_saloni_catania(self, page: Page) -> List[Contatto]:
        """Cerca saloni a Catania"""
        print("[Fresha] Ricerca saloni a Catania...")

        url = "https://www.fresha.com/it/explore?query=Catania&category=beauty-salon&country=it"

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Scrolla per caricare
            for _ in range(3):
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            contatti = await self._estrai_da_pagina(page)
            self.contatti.extend(contatti)
            print(f"  Trovati: {len(contatti)} contatti")

        except Exception as e:
            print(f"  Errore Fresha: {e}")

        return self.contatti

    async def _estrai_da_pagina(self, page: Page) -> List[Contatto]:
        """Estrae saloni da pagina Fresha"""
        contatti = []

        selettori = [
            '[data-testid="business-card"]',
            '.business-card',
            'a[href*="/business/"]'
        ]

        cards = []
        for sel in selettori:
            cards = await page.query_selector_all(sel)
            if cards:
                break

        for card in cards[:20]:
            try:
                contatto = Contatto()
                contatto.fonte = "fresha.com"
                contatto.data_raccolta = datetime.now().isoformat()
                contatto.categoria = "salone bellezza"

                # Nome
                nome_sel = await card.query_selector('h3, h4, .business-name')
                if nome_sel:
                    contatto.nome_salone = await nome_sel.inner_text()

                # Indirizzo
                addr_sel = await card.query_selector('.address, .location')
                if addr_sel:
                    contatto.indirizzo = await addr_sel.inner_text()

                # Link
                href = await card.get_attribute('href')
                if href and not href.startswith('http'):
                    href = f"https://www.fresha.com{href}"

                if href and contatto.nome_salone:
                    contatti.append(contatto)

            except:
                continue

        return contatti


# Funzione per codificare stringhe URL
def quote(s: str) -> str:
    """Codifica stringa per URL"""
    return s.replace(' ', '%20')


def salva_contatti(contatti: List[Contatto], filename: str = "contatti_catania.json"):
    """Salva contatti in file JSON"""
    data = {
        "data_generazione": datetime.now().isoformat(),
        "totale_contatti": len(contatti),
        "area": "Catania e dintorni (40km)",
        "servizio_target": "noleggio stampante unghie",
        "fonti": ["paginegialle.it", "treatwell.it", "fresha.com"],
        "contatti": [c.to_dict() for c in contatti]
    }

    filepath = f"/home/ioilmio/quadro/nailstech/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ Salvati {len(contatti)} contatti in:")
    print(f"  {filepath}")
    print(f"{'='*60}")


async def main():
    """Funzione principale"""
    print("=" * 60)
    print("RACCOLTA CONTATTI - CENTRI UNGHIE CATANIA")
    print("Versione 2 - Con Playwright (JavaScript rendering)")
    print("=" * 60)
    print()

    tutti_contatti: List[Contatto] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 800}
        )

        # 1. Pagine Gialle
        print("FASE 1: Pagine Gialle")
        print("-" * 40)
        page = await context.new_page()
        pg = ScraperPagineGialle()

        queries_pg = ["centri unghie", "manicure", "ricostruzione unghie", "centri estetici", "nail bar"]
        for query in queries_pg:
            contatti = await pg.cerca(page, query, pagine=2)
            tutti_contatti.extend(contatti)
            await asyncio.sleep(3)

        await page.close()
        print(f"Totale da Pagine Gialle: {len(tutti_contatti)}\n")

        # 2. Treatwell
        print("FASE 2: Treatwell")
        print("-" * 40)
        page = await context.new_page()
        tw = ScraperTreatwell()
        contatti_tw = await tw.cerca_saloni_catania(page)
        tutti_contatti.extend(contatti_tw)
        await page.close()
        print(f"Totale da Treatwell: {len(contatti_tw)}\n")

        # 3. Fresha
        print("FASE 3: Fresha")
        print("-" * 40)
        page = await context.new_page()
        fr = ScraperFresha()
        contatti_fr = await fr.cerca_saloni_catania(page)
        tutti_contatti.extend(contatti_fr)
        await page.close()
        print(f"Totale da Fresha: {len(contatti_fr)}\n")

        await browser.close()

    # 4. Validazione e deduplicazione
    print("FASE 4: Validazione e Deduplicazione")
    print("-" * 40)
    print(f"Contatti prima deduplicazione: {len(tutti_contatti)}")

    # Filtra solo contatti con cellulare valido
    contatti_validi = [c for c in tutti_contatti if c.cellulare]
    print(f"Contatti con cellulare valido: {len(contatti_validi)}")

    # Deduplica
    contatti_unici = ValidatoreContatti.deduplica_contatti(contatti_validi)
    print(f"Contatti unici: {len(contatti_unici)}")

    # 5. Salvataggio
    print()
    salva_contatti(contatti_unici)

    print()
    print("=" * 60)
    print("RACCOLTA COMPLETATA!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
