# Raccolta Contatti - Centri Unghie Catania

Script per raccogliere contatti di centri unghie, nail bar, centri estetici e saloni bellezza nell'area di Catania (max 40km) per il servizio di noleggio stampante unghie.

## Requisiti

- Python 3.10+
- Google Chrome (installato)
- Virtual environment (consigliato)

## Setup

```bash
# Crea virtual environment
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements_scraper.txt

# Configura API Key (opzionale ma consigliato)
cp .env.example .env
# Modifica .env e inserisci GOOGLE_PLACES_API_KEY
```

## Ottenere Google Places API Key

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto o seleziona uno esistente
3. Abilita l'API "Places API (New)"
4. Crea credenziali API Key
5. Inserisci la key in `.env`

## Uso

```bash
source venv/bin/activate
python scraper_selenium.py
```

## Output

I contatti vengono salvati in `contatti_catania.json` con struttura:

```json
{
  "nome_salone": "...",
  "cellulare": "+393...",
  "indirizzo": "...",
  "categoria": "...",
  "fonte": "google_places",
  "data_raccolta": "..."
}
```

## Fonti Dati

1. **Google Places API** (primaria) - richiede API key
2. **PagineGialle.it** (Selenium scraping)
3. **Treatwell.it** (Selenium scraping)
4. **Fresha.com** (Selenium scraping)

## Note

- Solo numeri cellulari italiani (+39 3xx xxx xxxx)
- I numeri fissi vengono automaticamente esclusi
- Duplicati rimossi automaticamente (basato su cellulare + nome)
- Scraping via Selenium puo essere lento e soggetto a rate limiting
