#!/usr/bin/env python3
"""
Script di automazione per raccolta contatti centri unghie e servizi unghie
Area: Catania e dintorni (max 40km)
Fonti: PagineGialle, Treatwell, Fresha, Google Maps
"""

import json
import re
import time
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote_plus, urljoin
import requests
from dataclasses import dataclass, asdict


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

        # Rimuovi spazi, trattini, parentesi
        numero_pulito = re.sub(r'[\s\-\.\(\)]', '', numero)

        # Rimuovi prefisso internazionale se presente
        if numero_pulito.startswith('+39'):
            numero_pulito = numero_pulito[3:]
        elif numero_pulito.startswith('0039'):
            numero_pulito = numero_pulito[4:]

        # Verifica che sia un numero italiano valido
        if not numero_pulito.startswith('3') or len(numero_pulito) != 10:
            return None  # Esclude numeri fissi e non validi

        return f"+39{numero_pulito}"

    @staticmethod
    def deduplica_contatti(contatti: List[Contatto]) -> List[Contatto]:
        """Rimuove duplicati basati su cellulare + nome"""
        visti = set()
        unici = []

        for c in contatti:
            chiave = f"{c.cellulare.lower()}|{c.nome_salone.lower()}"
            if chiave not in visti and c.cellulare:
                visti.add(chiave)
                unici.append(c)

        return unici


class ScraperPagineGialle:
    """Scraper per PagineGialle.it"""

    BASE_URL = "https://www.paginegialle.it"
    SEARCH_URL = "https://www.paginegialle.it/ricerca"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.contatti: List[Contatto] = []

    def cerca(self, query: str, localita: str = "Catania", pagine: int = 5) -> List[Contatto]:
        """Cerca attività su PagineGialle"""
        print(f"[PagineGialle] Ricerca: {query} a {localita}")

        for pagina in range(1, pagine + 1):
            try:
                params = {
                    'q': query,
                    'where': localita,
                    'page': pagina
                }

                response = self.session.get(self.SEARCH_URL, params=params, timeout=30)

                if response.status_code == 200:
                    contatti_pagina = self._estrai_contatti_da_html(response.text)
                    self.contatti.extend(contatti_pagina)
                    print(f"  Pagina {pagina}: {len(contatti_pagina)} contatti trovati")

                time.sleep(2)  # Rate limiting

            except Exception as e:
                print(f"  Errore pagina {pagina}: {e}")

        return self.contatti

    def _estrai_contatti_da_html(self, html: str) -> List[Contatto]:
        """Estrae contatti dal HTML della pagina di ricerca"""
        contatti = []

        # Pattern per estrarre risultati (struttura base)
        pattern_risultato = r'<article[^>]*class="[^"]*search-result[^"]*"[^>]*>(.*?)</article>'
        risultati = re.findall(pattern_risultato, html, re.DOTALL)

        for risultato in risultati[:10]:  # Limita per pagina
            contatto = Contatto()
            contatto.fonte = "paginegialle.it"
            contatto.data_raccolta = datetime.now().isoformat()

            # Nome attività
            nome_match = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', risultato, re.DOTALL)
            if nome_match:
                contatto.nome_salone = self._pulisci_testo(nome_match.group(1))

            # Indirizzo
            indirizzo_match = re.search(r'class="address[^"]*"[^>]*>(.*?)</span>', risultato, re.DOTALL)
            if indirizzo_match:
                contatto.indirizzo = self._pulisci_testo(indirizzo_match.group(1))

            # Telefono
            tel_match = re.search(r'tel:([\d\s\+]+)', risultato)
            if tel_match:
                telefono = tel_match.group(1).replace(' ', '')
                contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

            # Categoria
            cat_match = re.search(r'class="category[^"]*"[^>]*>(.*?)</', risultato, re.DOTALL)
            if cat_match:
                contatto.categoria = self._pulisci_testo(cat_match.group(1))

            if contatto.nome_salone and contatto.cellulare:
                contatti.append(contatto)

        return contatti

    @staticmethod
    def _pulisci_testo(testo: str) -> str:
        """Pulisce testo HTML"""
        testo = re.sub(r'<[^>]+>', '', testo)
        testo = testo.replace('&nbsp;', ' ').strip()
        return testo


class ScraperTreatwell:
    """Scraper per Treatwell.it"""

    API_URL = "https://www.treatwell.it/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        self.contatti: List[Contatto] = []

    def cerca_saloni_catania(self) -> List[Contatto]:
        """Cerca saloni a Catania con servizi unghie"""
        print("[Treatwell] Ricerca saloni a Catania...")

        # Coordinate Catania centro
        lat, lng = 37.5079, 15.0830

        try:
            # Ricerca per servizi unghie
            servizi_unghie = [
                "manicure", "pedicure", "ricostruzione-unghie",
                "nail-art", "gel-unghie", "semipermanente"
            ]

            for servizio in servizi_unghie:
                url = f"https://www.treatwell.it/salone/{servizio}/catania-ct"
                self._scarica_pagina_saloni(url, servizio)
                time.sleep(3)

        except Exception as e:
            print(f"  Errore Treatwell: {e}")

        return self.contatti

    def _scarica_pagina_saloni(self, url: str, servizio: str):
        """Scarica e analizza pagina saloni"""
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                contatti = self._estrai_da_html_treatwell(response.text, servizio)
                self.contatti.extend(contatti)
                print(f"  Servizio '{servizio}': {len(contatti)} contatti")
        except Exception as e:
            print(f"  Errore URL {url}: {e}")

    def _estrai_da_html_treatwell(self, html: str, servizio: str) -> List[Contatto]:
        """Estrae dati saloni da HTML Treatwell"""
        contatti = []

        # Pattern per card salone
        pattern_salone = r'<div[^>]*class="[^"]*venue-card[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>'
        saloni = re.findall(pattern_salone, html, re.DOTALL)

        for salone in saloni[:15]:
            contatto = Contatto()
            contatto.fonte = "treatwell.it"
            contatto.data_raccolta = datetime.now().isoformat()
            contatto.categoria = f"centro estetico - {servizio}"

            # Nome
            nome_match = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', salone, re.DOTALL)
            if nome_match:
                contatto.nome_salone = self._pulisci_testo(nome_match.group(1))

            # Indirizzo
            addr_match = re.search(r'class="[^"]*address[^"]*"[^>]*>(.*?)</span>', salone, re.DOTALL)
            if addr_match:
                contatto.indirizzo = self._pulisci_testo(addr_match.group(1))

            # Telefono (spesso in pagina dettaglio)
            tel_match = re.search(r'tel[:\s]+([\d\s\+]+)', salone, re.IGNORECASE)
            if tel_match:
                telefono = tel_match.group(1).replace(' ', '')
                contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

            # Link dettaglio per telefono
            link_match = re.search(r'<a[^>]*href="(/salone/[^"]+)"', salone)
            if link_match and not contatto.cellulare:
                telefono = self._estrai_telefono_da_dettaglio(link_match.group(1))
                if telefono:
                    contatto.cellulare = telefono

            if contatto.nome_salone and contatto.cellulare:
                contatti.append(contatto)

        return contatti

    def _estrai_telefono_da_dettaglio(self, path: str) -> Optional[str]:
        """Estrae telefono dalla pagina dettaglio salone"""
        try:
            url = f"https://www.treatwell.it{path}"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                # Cerca numero telefono
                tel_match = re.search(r'tel[:\s]+([\d\s\+]{10,})', response.text, re.IGNORECASE)
                if tel_match:
                    telefono = tel_match.group(1).replace(' ', '').replace('-', '')
                    return ValidatoreContatti.normalizza_cellulare(telefono)
        except:
            pass
        return None

    @staticmethod
    def _pulisci_testo(testo: str) -> str:
        testo = re.sub(r'<[^>]+>', '', testo)
        return testo.strip()


class ScraperFresha:
    """Scraper per Fresha.com"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.contatti: List[Contatto] = []

    def cerca_saloni_catania(self) -> List[Contatto]:
        """Cerca saloni di bellezza a Catania"""
        print("[Fresha] Ricerca saloni a Catania...")

        try:
            url = "https://www.fresha.com/it/explore?query=Catania&category=beauty-salon"
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                contatti = self._estrai_da_html_fresha(response.text)
                self.contatti.extend(contatti)
                print(f"  Trovati {len(contatti)} contatti")

        except Exception as e:
            print(f"  Errore Fresha: {e}")

        return self.contatti

    def _estrai_da_html_fresha(self, html: str) -> List[Contatto]:
        """Estrae dati da HTML Fresha"""
        contatti = []

        # Pattern per business card
        pattern_card = r'<a[^>]*class="[^"]*business-card[^"]*"[^>]*>(.*?)</a>'
        cards = re.findall(pattern_card, html, re.DOTALL)

        for card in cards[:20]:
            contatto = Contatto()
            contatto.fonte = "fresha.com"
            contatto.data_raccolta = datetime.now().isoformat()
            contatto.categoria = "salone bellezza"

            # Nome
            nome_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', card, re.DOTALL)
            if nome_match:
                contatto.nome_salone = self._pulisci_testo(nome_match.group(1))

            # Indirizzo
            addr_match = re.search(r'<p[^>]*class="[^"]*address[^"]*"[^>]*>(.*?)</p>', card, re.DOTALL)
            if addr_match:
                contatto.indirizzo = self._pulisci_testo(addr_match.group(1))

            # Telefono (spesso non visibile direttamente)
            tel_match = re.search(r'tel[:\s]+([\d\s\+]+)', card, re.IGNORECASE)
            if tel_match:
                telefono = tel_match.group(1).replace(' ', '')
                contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

            if contatto.nome_salone:
                contatti.append(contatto)

        return contatti

    @staticmethod
    def _pulisci_testo(testo: str) -> str:
        testo = re.sub(r'<[^>]+>', '', testo)
        return testo.strip()


class GoogleMapsScraper:
    """Scraper per Google Maps (usa Places API o scraping diretto)"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.contatti: List[Contatto] = []

    def cerca_luoghi(self, query: str, location: str = "Catania", radius: int = 40000) -> List[Contatto]:
        """Cerca luoghi su Google Maps"""
        print(f"[Google Maps] Ricerca: {query}")

        if self.api_key:
            return self._cerca_con_api(query, location, radius)
        else:
            print("  API key non fornita, salto Google Maps API")
            return []

    def _cerca_con_api(self, query: str, location: str, radius: int) -> List[Contatto]:
        """Cerca usando Google Places API"""
        # Coordinate Catania
        lat, lng = 37.5079, 15.0830

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f"{query} {location}",
            'location': f"{lat},{lng}",
            'radius': radius,
            'key': self.api_key
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()

            if data.get('status') == 'OK':
                for result in data.get('results', []):
                    contatto = self._converti_place_in_contatto(result)
                    if contatto:
                        self.contatti.append(contatto)

                print(f"  Trovati {len(self.contatti)} risultati")

        except Exception as e:
            print(f"  Errore API: {e}")

        return self.contatti

    def _converti_place_in_contatto(self, place: Dict) -> Optional[Contatto]:
        """Converte risultato Google Places in Contatto"""
        contatto = Contatto()
        contatto.fonte = "google_maps"
        contatto.data_raccolta = datetime.now().isoformat()

        # Nome
        contatto.nome_salone = place.get('name', '')

        # Indirizzo
        contatto.indirizzo = place.get('formatted_address', '')

        # Telefono
        telefono = place.get('formatted_phone_number', '')
        if telefono:
            contatto.cellulare = ValidatoreContatti.normalizza_cellulare(telefono) or ""

        # Sito web
        contatto.sito_web = place.get('website', '')

        # Categoria
        types = place.get('types', [])
        contatto.categoria = ', '.join(types[:2]) if types else 'centro estetico'

        if contatto.nome_salone and contatto.cellulare:
            return contatto
        return None


def salva_contatti(contatti: List[Contatto], filename: str = "contatti_catania.json"):
    """Salva contatti in file JSON"""
    data = {
        "data_generazione": datetime.now().isoformat(),
        "totale_contatti": len(contatti),
        "area": "Catania e dintorni (40km)",
        "servizio_target": "noleggio stampante unghie",
        "contatti": [c.to_dict() for c in contatti]
    }

    filepath = f"/home/ioilmio/quadro/nailstech/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Salvati {len(contatti)} contatti in {filepath}")


def main():
    """Funzione principale"""
    print("=" * 60)
    print("RACCOLTA CONTATTI - CENTRI UNGHIE CATANIA")
    print("=" * 60)
    print()

    tutti_contatti: List[Contatto] = []

    # 1. Pagine Gialle
    print("FASE 1: Pagine Gialle")
    print("-" * 40)
    pg = ScraperPagineGialle()

    queries_pg = [
        "centri unghie",
        "manicure",
        "ricostruzione unghie",
        "centri estetici",
        "nail bar"
    ]

    for query in queries_pg:
        contatti = pg.cerca(query, pagine=3)
        tutti_contatti.extend(contatti)
        time.sleep(3)

    print(f"Totale da Pagine Gialle: {len(tutti_contatti)}\n")

    # 2. Treatwell
    print("FASE 2: Treatwell")
    print("-" * 40)
    tw = ScraperTreatwell()
    contatti_tw = tw.cerca_saloni_catania()
    tutti_contatti.extend(contatti_tw)
    print(f"Totale da Treatwell: {len(contatti_tw)}\n")

    # 3. Fresha
    print("FASE 3: Fresha")
    print("-" * 40)
    fr = ScraperFresha()
    contatti_fr = fr.cerca_saloni_catania()
    tutti_contatti.extend(contatti_fr)
    print(f"Totale da Fresha: {len(contatti_fr)}\n")

    # 4. Google Maps (se API key disponibile)
    print("FASE 4: Google Maps")
    print("-" * 40)
    api_key = None  # Inserisci qui la tua API key se disponibile
    gm = GoogleMapsScraper(api_key=api_key)

    if api_key:
        queries_gm = [
            "centri unghie",
            "nail bar",
            "manicure",
            "centro estetico",
            "salone bellezza"
        ]
        for query in queries_gm:
            contatti = gm.cerca_luoghi(query)
            tutti_contatti.extend(contatti)
            time.sleep(2)
    else:
        print("  (Saltato - richiede Google Places API key)\n")

    # 5. Validazione e deduplicazione
    print("FASE 5: Validazione e Deduplicazione")
    print("-" * 40)
    print(f"Contatti prima della deduplicazione: {len(tutti_contatti)}")

    # Filtra solo contatti con cellulare valido
    contatti_validi = [c for c in tutti_contatti if c.cellulare]
    print(f"Contatti con cellulare valido: {len(contatti_validi)}")

    # Deduplica
    contatti_unici = ValidatoreContatti.deduplica_contatti(contatti_validi)
    print(f"Contatti unici dopo deduplicazione: {len(contatti_unici)}")

    # 6. Salvataggio
    print()
    salva_contatti(contatti_unici)

    print()
    print("=" * 60)
    print("RACCOLTA COMPLETATA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
