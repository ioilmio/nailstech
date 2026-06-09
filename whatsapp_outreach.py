#!/usr/bin/env python3
"""
WhatsApp Outreach Automation - Noleggio Stampante Unghie
Script per automatizzare contatti WhatsApp con i centri unghie raccolti

Opzioni disponibili:
1. WhatsApp Web (manual - sicuro)
2. Twilio WhatsApp API (automatico - richiede account)
3. WhatsApp Business API (automatico - richiede account)
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import csv

# Carica variabili d'ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# WhatsApp Web solo - nessuna API esterna necessaria


@dataclass
class MessaggioTemplate:
    """Template per messaggi WhatsApp"""
    nome_template: str
    testo: str
    variabili: List[str]  # es: ["{nome_salone}", "{responsabile}"]

    def personalizza(self, contatto: Dict) -> str:
        """Personalizza template con dati contatto"""
        testo = self.testo
        for var in self.variabili:
            valore = contatto.get(var.replace("{", "").replace("}", ""), "")
            testo = testo.replace(var, valore)
        return testo


class WhatsAppOutreach:
    """Sistema di automazione WhatsApp outreach - WhatsApp Web solo"""

    def __init__(self):
        self.contatti: List[Dict] = []
        self.templates: List[MessaggioTemplate] = []
        self.inviati: List[Dict] = []
        self.falliti: List[Dict] = []

    def carica_contatti(self, filepath: str = "contatti_catania.json"):
        """Carica contatti dal file JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.contatti = data.get('contatti', [])
                print(f"✓ Caricati {len(self.contatti)} contatti da {filepath}")
                return True
        except Exception as e:
            print(f"✗ Errore caricamento contatti: {e}")
            return False

    def carica_contatti_csv(self, filepath: str = "contatti_catania.csv"):
        """Carica contatti da CSV"""
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.contatti = list(reader)
                print(f"✓ Caricati {len(self.contatti)} contatti da {filepath}")
                return True
        except Exception as e:
            print(f"✗ Errore caricamento CSV: {e}")
            return False

    def imposta_templates(self):
        """Imposta i template di messaggio"""
        self.templates = [
            MessaggioTemplate(
                nome_template="primo_contatto_corto",
                testo="""👋 Buongiorno {nome_salone}!

Sono Marco di NailTech Solutions. Offriamo stampanti per unghie in noleggio a partire da 99€/mese.

Le interessa un preventivo senza impegno?""",
                variabili=["{nome_salone}"]
            ),

            MessaggioTemplate(
                nome_template="primo_contatto_dettagliato",
                testo="""👋 Buongiorno {nome_salone}!

Mi chiamo Marco e lavoro con NailTech Solutions. Abbiamo notato il vostro centro e pensavo che potreste essere interessati al nostro servizio di noleggio stampanti per unghie.

✅ Stampanti professionali di ultima generazione
✅ Assistenza tecnica inclusa
✅ Formazione per il personale
✅ Costi a partire da 99€/mese

Volete ricevere un catalogo e un preventivo personalizzato?

Grazie mille,
Marco
NailTech Solutions
📞 3331234567""",
                variabili=["{nome_salone}"]
            ),

            MessaggioTemplate(
                nome_template="follow_up",
                testo="""👋 Buongiorno {nome_salone},

Le scrivo in riferimento al mio messaggio di ieri riguardo il noleggio stampanti per unghie.

Voleva solo sapere se ha avuto modo di valutare la nostra proposta? Posso inviarle il catalogo con i modelli disponibili?

Grazie ancora,
Marco
NailTech Solutions""",
                variabili=["{nome_salone}"]
            ),

            MessaggioTemplate(
                nome_template="offerta_speciale",
                testo="""🎉 OFFERTA SPECIALE per {nome_salone}!

Solo per questa settimana: primo mese di noleggio stampante unghie a soli 49€!

✅ Modello professional HD
✅ Installazione gratuita
✅ Training 2 ore incluso

L'offerta scade venerdì. Vuole prenotare una demo gratuita?

Marco
NailTech Solutions""",
                variabili=["{nome_salone}"]
            )
        ]

        print(f"✓ Caricati {len(self.templates)} template messaggi")

    def genera_link_whatsapp(self, telefono: str, messaggio: str) -> str:
        """Genera link WhatsApp Web per invio messaggio"""
        # Rimuovi +39 se presente
        telefono_pulito = telefono.replace("+39", "")
        
        # URL encode messaggio
        messaggio_encoded = messaggio.replace('\n', '%0A').replace(' ', '%20')
        
        return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

    def invia_whatsapp_web(self, contatto: Dict, template: MessaggioTemplate):
        """Genera link WhatsApp Web per invio manuale"""
        messaggio = template.personalizza(contatto)
        link = self.genera_link_whatsapp(contatto['cellulare'], messaggio)
        
        print(f"\n📱 {contatto['nome_salone']}")
        print(f"📞 {contatto['cellulare']}")
        print(f"🌐 Apri questo link: {link}")
        print("-" * 50)
        
        return link

    def filtra_contatti(self, min_rating: float = 0.0, limit: Optional[int] = None) -> List[Dict]:
        """Filtra contatti per rating e limita numero"""
        filtrati = []
        
        for c in self.contatti:
            # Salta contatti senza cellulare
            if not c.get('cellulare'):
                continue
                
            # Filtra per rating
            rating = float(c.get('rating') or 0)
            if rating < min_rating:
                continue
                
            filtrati.append(c)
        
        # Ordina per rating (decrescente)
        filtrati.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
        
        if limit:
            filtrati = filtrati[:limit]
            
        return filtrati

    def simula_outreach(self, 
                       template_nome: str = "primo_contatto_corto",
                       limit: int = 5,
                       min_rating: float = 4.0,
                       delay_min: int = 30,
                       delay_max: int = 90):
        """
        Simula invio messaggi (genera link per invio manuale)
        
        Args:
            template_nome: Nome template da usare
            limit: Numero massimo contatti
            min_rating: Rating minimo
            delay_min/max: Secondi di attesa tra invii
        """
        
        print(f"\n{'='*60}")
        print(f"SIMULAZIONE WHATSAPP OUTREACH")
        print(f"Template: {template_nome}")
        print(f"Limit: {limit} contatti")
        print(f"Rating minimo: {min_rating}")
        print(f"{'='*60}")

        # Carica template
        template = None
        for t in self.templates:
            if t.nome_template == template_nome:
                template = t
                break
        
        if not template:
            print(f"✗ Template '{template_nome}' non trovato")
            return

        # Filtra contatti
        contatti_target = self.filtra_contatti(min_rating=min_rating, limit=limit)
        
        if not contatti_target:
            print("✗ Nessun contatto soddisfa i filtri")
            return

        print(f"📋 Contatti target: {len(contatti_target)}")
        print(f"⏰ Tempo stimato: {len(contatti_target) * ((delay_min + delay_max) / 2) / 60:.1f} minuti")
        print()

        # Genera link per ogni contatto
        for i, contatto in enumerate(contatti_target, 1):
            print(f"📩 {i}/{len(contatti_target)}")
            
            link = self.invia_web_manual(contatto, template)
            
            # Salva nei log
            self.inviati.append({
                'contatto': contatto,
                'template': template_nome,
                'link': link,
                'timestamp': datetime.now().isoformat(),
                'stato': 'link_generato'
            })

            # Attesa tra invii (simulazione)
            if i < len(contatti_target):
                delay = random.randint(delay_min, delay_max)
                print(f"⏳ Attendo {delay} secondi prima del prossimo invio...")
                time.sleep(delay)

        print(f"\n✓ Completato! {len(self.inviati)} link generati")

    def genera_batch_links(self, 
                          template_nome: str = "primo_contatto_corto",
                          limit: int = 20,
                          min_rating: float = 4.0,
                          output_file: str = "whatsapp_batch_links.txt"):
        """
        Genera batch di link WhatsApp Web per invio manuale
        
        Args:
            template_nome: Template da usare
            limit: Max contatti
            min_rating: Rating minimo
            output_file: File di output
        """
        
        print(f"\n{'='*60}")
        print(f"GENERAZIONE BATCH LINK WHATSAPP")
        print(f"Template: {template_nome}")
        print(f"Limit: {limit} contatti")
        print(f"Rating minimo: {min_rating}")
        print(f"Output: {output_file}")
        print(f"{'='*60}")

        # Carica template
        template = None
        for t in self.templates:
            if t.nome_template == template_nome:
                template = t
                break
        
        if not template:
            print(f"✗ Template '{template_nome}' non trovato")
            return

        # Filtra contatti
        contatti_target = self.filtra_contatti(min_rating=min_rating, limit=limit)
        
        if not contatti_target:
            print("✗ Nessun contatto soddisfa i filtri")
            return

        # Genera file con link
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"WhatsApp Outreach Links - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, contatto in enumerate(contatti_target, 1):
                messaggio = template.personalizza(contatto)
                link = self.genera_link_whatsapp(contatto['cellulare'], messaggio)
                
                f.write(f"{i}. {contatto['nome_salone']}\n")
                f.write(f"   📞 {contatto['cellulare']}\n")
                f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
                f.write(f"   🌐 {link}\n")
                f.write("-" * 40 + "\n\n")

        print(f"✓ Creato file {output_file} con {len(contatti_target)} link")
        print(f"📂 Apri il file e clicca sui link per inviare i messaggi")

    def salva_log(self, filename: str = "whatsapp_outreach_log.json"):
        """Salva log delle attività"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'metodo': self.metodo,
            'contatti_totali': len(self.contatti),
            'inviati': len(self.inviati),
            'falliti': len(self.falliti),
            'inviati_detail': self.inviati,
            'falliti_detail': self.falliti
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Log salvato in {filename}")

    def statistiche(self):
        """Mostra statistiche campagne"""
        print(f"\n{'='*60}")
        print(f"STATISTICHE OUTREACH")
        print(f"{'='*60}")
        print(f"📊 Contatti caricati: {len(self.contatti)}")
        print(f"✅ Inviati: {len(self.inviati)}")
        print(f"❌ Falliti: {len(self.falliti)}")
        
        if self.contatti:
            rating_medio = sum(float(c.get('rating', 0)) for c in self.contatti if c.get('rating')) / len([c for c in self.contatti if c.get('rating')])
            print(f"⭐ Rating medio: {rating_medio:.1f}")
        
        if (len(self.inviati)+len(self.falliti)) > 0:
            print(f"📈 Tasso successo: {len(self.inviati)/(len(self.inviati)+len(self.falliti))*100:.1f}%")


def main():
    """Funzione principale"""
    print("=" * 60)
    print("WHATSAPP OUTREACH AUTOMATION")
    print("Noleggio Stampante Unghie - Catania")
    print("WhatsApp Web Only - No API Required")
    print("=" * 60)

    # Inizializza sistema
    outreach = WhatsAppOutreach()

    # Carica contatti
    if not outreach.carica_contatti():
        return

    # Imposta template
    outreach.imposta_templates()

    # Menu opzioni
    print("\nCosa vuoi fare?")
    print("1. Simula invio manuale (genera link)")
    print("2. Genera batch link per invio manuale")
    print("3. Simula follow-up")
    print("4. Offerta speciale")
    print("5. Statistiche contatti")
    print("6. Esci")

    scelta = input("\nScelta (1-6): ").strip()

    if scelta == "1":
        # Simula invio manuale
        limit = int(input("Numero contatti (default 5): ") or "5")
        min_rating = float(input("Rating minimo (default 4.0): ") or "4.0")
        
        outreach.simula_outreach(
            template_nome="primo_contatto_corto",
            limit=limit,
            min_rating=min_rating
        )

    elif scelta == "2":
        # Genera batch link
        limit = int(input("Numero contatti (default 20): ") or "20")
        min_rating = float(input("Rating minimo (default 4.0): ") or "4.0")
        
        outreach.genera_batch_links(
            template_nome="primo_contatto_dettagliato",
            limit=limit,
            min_rating=min_rating
        )

    elif scelta == "3":
        # Follow-up
        limit = int(input("Numero contatti (default 5): ") or "5")
        
        outreach.simula_outreach(
            template_nome="follow_up",
            limit=limit,
            min_rating=4.0
        )

    elif scelta == "4":
        # Offerta speciale
        limit = int(input("Numero contatti (default 10): ") or "10")
        
        outreach.simula_outreach(
            template_nome="offerta_speciale",
            limit=limit,
            min_rating=4.5
        )

    elif scelta == "5":
        # Statistiche
        outreach.statistiche()

    else:
        print("Arrivederci!")
        return

    # Salva log
    outreach.salva_log()


if __name__ == "__main__":
    main()
