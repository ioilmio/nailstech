# WhatsApp Outreach Automation

Script per automatizzare contatti WhatsApp con i centri unghie raccolti per il servizio di noleggio stampante unghie.

**WhatsApp Web Only - No API Required**

## Setup

```bash
cd /home/ioilmio/quadro/nailstech
source venv/bin/activate
pip install python-dotenv
```

## Come Funziona

### WhatsApp Web (Sicuro - Consigliato)
- Genera link WhatsApp Web personalizzati
- Clicca sui link per inviare messaggi manualmente
- Nessun rischio di blocco account
- Nessun costo aggiuntivo
- Rate limiting automatico

## Uso Rapido

```bash
python whatsapp_outreach.py
```

### Menu Opzioni:

1. **Simula invio manuale** - Genera link per invio immediato
2. **Genera batch link** - Crea file con 20+ link pronti
3. **Simula follow-up** - Messaggi di follow-up automatici
4. **Offerta speciale** - Campagne promozionali
5. **Statistiche** - Analisi performance contatti

## Template Messaggi

### 1. Primo Contatto (Corto)
```
👋 Buongiorno {nome_salone}!

Sono Marco di NailTech Solutions. Offriamo stampanti per unghie in noleggio a partire da 99€/mese.

Le interessa un preventivo senza impegno?
```

### 2. Primo Contatto (Dettagliato)
```
👋 Buongiorno {nome_salone}!

Mi chiamo Marco e lavoro con NailTech Solutions. Abbiamo notato il vostro centro e pensavo che potreste essere interessati al nostro servizio di noleggio stampanti per unghie.

✅ Stampanti professionali di ultima generazione
✅ Assistenza tecnica inclusa
✅ Formazione per il personale
✅ Costi a partire da 99€/mese

Volete ricevere un catalogo e un preventivo personalizzato?
```

### 3. Follow-up
```
👋 Buongiorno {nome_salone},

Le scrivo in riferimento al mio messaggio di ieri riguardo il noleggio stampanti per unghie.

Voleva solo sapere se ha avuto modo di valutare la nostra proposta?
```

### 4. Offerta Speciale
```
🎉 OFFERTA SPECIALE per {nome_salone}!

Solo per questa settimana: primo mese di noleggio stampante unghie a soli 49€!

✅ Modello professional HD
✅ Installazione gratuita
✅ Training 2 ore incluso
```

## Esempi Pratici

### Genera 10 link per centri con rating > 4.5
```python
python whatsapp_outreach.py
# Scelta: 2
# Limit: 10
# Rating minimo: 4.5
```

Output: `whatsapp_batch_links.txt` con link cliccabili

### Simula campagna con rate limiting
```python
python whatsapp_outreach.py
# Scelta: 1
# Limit: 5
# Rating minimo: 4.0
```

Genera link con attesa 30-90 secondi tra invii

## File Generati

- `whatsapp_batch_links.txt` - Link batch per invio manuale
- `whatsapp_outreach_log.json` - Log attività campagne

## Best Practices

### ✅ Cosa Fare
- Iniziare con rating alto (4.5+)
- Personalizzare nome salone
- Rispettare rate limiting (30-90s)
- Testare template su piccoli gruppi
- Monitorare risposte

### ❌ Cosa Evitare
- Spamming massivo
- Messaggi troppo lunghi
- Ignorare risposte
- Contattare orari inappropriati
- Usare solo template generici

## Rate Limiting

- **WhatsApp Web**: 30-90 secondi tra invii
- **Consigliato**: 10-20 contatti/giorno per evitare blocchi
- **Batch mode**: Genera file con link da inviare manualmente

## Monitoraggio

Il sistema salva automaticamente:
- Timestamp di ogni invio
- Template utilizzato
- Risposte ricevute
- Tasso di conversione

## Supporto

Per problemi tecnici:
- Controlla file log
- Verifica connessione internet
- Assicurati che contatti siano validi
- Rispetta limiti WhatsApp
