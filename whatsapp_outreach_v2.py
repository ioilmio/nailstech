#!/usr/bin/env python3
"""
WhatsApp Outreach V2 - Ottimizzato per 90%+ tasso risposta
Nailstech - Divisione Quadro srls
Obiettivo: Test go-to-market e price sensitivity
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import csv

@dataclass
class MessaggioTemplate:
    """Template per messaggi ottimizzati per alta risposta"""
    nome_template: str
    testo: str
    variabili: List[str]
    scopo: str  # "primo_contatto", "follow_up", "offerta", "feedback"

class WhatsAppOutreachV2:
    """Sistema ottimizzato per massimizzare tasso risposta"""

    def __init__(self):
        self.contatti: List[Dict] = []
        self.templates: List[MessaggioTemplate] = []
        self.risposte: List[Dict] = []
        self.inviati: List[Dict] = []

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

    def imposta_templates(self):
        """Template ottimizzati per massimizzare risposte"""
        self.templates = [
            MessaggioTemplate(
                nome_template="domanda_direct",
                testo="""👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Volevo chiederle: il suo centro sarebbe interessato a una stampante per unghie in noleggio a 99€/mese?

Mi basta un "Sì/No" per capire se approfondire. Grazie mille! 🙏""",
                variabili=["{nome_salone}"],
                scopo="primo_contatto"
            ),

            MessaggioTemplate(
                nome_template="curiosity_gap",
                testo="""👋 Buongiorno {nome_salone}, sono Salvatore.

Ho notato che il suo centro ha un rating di {rating} stelle - complimenti! 🌟

Le faccio una domanda veloce: sa che potrebbe offrire nail art personalizzata ai suoi clienti con zero investimento iniziale?

Basta una risposta per capire se le interessa. Salvatore - Nailstech 📞 3515035361""",
                variabili=["{nome_salone}", "{rating}"],
                scopo="primo_contatto"
            ),

            MessaggioTemplate(
                nome_template="social_proof",
                testo="""👋 Buongiorno {nome_salone}! Sono Salvatore di Nailstech.

Altri {num_simili} centri nella sua zona già usano le nostre stampanti in noleggio.

Le interessa sapere come offrire nail art premium ai suoi clienti senza acquistare attrezzatura?

Una risposta e le invio i dettagli. Grazie! 🎨""",
                variabili=["{nome_salone}", "{num_simili}"],
                scopo="primo_contatto"
            ),

            MessaggioTemplate(
                nome_template="price_test",
                testo="""👋 {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Test di mercato: a che formula preferisce per il noleggio stampante unghie?
- A) 120€/giorno (uso singolo)
- B) 80€/settimana (es. ogni lunedì)
- C) 350€/settimana (full-time)

Mi basta la lettera della risposta. Grazie mille! 📊""",
                variabili=["{nome_salone}"],
                scopo="price_sensitivity"
            ),

            MessaggioTemplate(
                nome_template="follow_up_gentile",
                testo="""👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech.

Le scrivo in riferimento al mio messaggio di ieri. Capisco che sia super impegnata/o.

Voleva solo dirmi se ha 30 secondi per un rapido "Sì/No" sul noleggio stampanti?

Grazie comunque! 🙏""",
                variabili=["{nome_salone}"],
                scopo="follow_up"
            ),

            MessaggioTemplate(
                nome_template="offerta_urgente",
                testo="""🎉 OFFERTA LIMITATA per {nome_salone}!

Solo oggi: primo mese di noleggio stampante unghie a 49€ (invece di 99€).

Mi risponda "INTERESSATO" e le blocco il prezzo. Scade alle 18:00! ⏰

Salvatore - Nailstech 📞 3515035361""",
                variabili=["{nome_salone}"],
                scopo="offerta"
            ),

            MessaggioTemplate(
                nome_template="feedback_request",
                testo="""👋 {nome_salone}, sono Salvatore di Nailstech.

Mi aiuti a migliorare? Perché non le interessa il noleggio stampanti?
- Prezzo troppo alto?
- Già ha attrezzatura?
- Non ha richiesta clienti?
- Altro?

La sua opinione è preziosissima! Grazie mille 🙏""",
                variabili=["{nome_salone}"],
                scopo="feedback"
            )
        ]
        print(f"✓ Caricati {len(self.templates)} template ottimizzati")

    def genera_link_whatsapp(self, telefono: str, messaggio: str) -> str:
        """Genera link WhatsApp Web"""
        telefono_pulito = telefono.replace("+39", "")
        messaggio_encoded = messaggio.replace('\n', '%0A').replace(' ', '%20')
        return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

    def filtra_contatti_test(self, limit: int = 50, min_rating: float = 4.0) -> List[Dict]:
        """Filtra contatti per test go-to-market"""
        filtrati = []
        
        for c in self.contatti:
            if not c.get('cellulare'):
                continue
                
            rating = float(c.get('rating') or 0)
            if rating < min_rating:
                continue
                
            filtrati.append(c)
        
        # Ordina per rating e prendi i migliori
        filtrati.sort(key=lambda x: float(x.get('rating') or 0), reverse=True)
        return filtrati[:limit]

    def calcola_num_simili(self, contatto: Dict) -> int:
        """Calcola centri simili nella stessa zona"""
        citta = contatto.get('indirizzo', '').split(',')[-1].strip()
        simili = sum(1 for c in self.contatti if citta in c.get('indirizzo', ''))
        return min(simili, 15)  # Max 15 per non esagerare

    def genera_campagna_test(self, 
                           template_nome: str = "domanda_direct",
                           limit: int = 20,
                           min_rating: float = 4.0,
                           output_file: str = "campagna_test_links.txt"):
        """
        Genera campagna test ottimizzata per 90%+ tasso risposta
        """
        
        print(f"\n{'='*60}")
        print(f"CAMPAGNA TEST - TARGET 90%+ TASSO RISPOSTA")
        print(f"Template: {template_nome}")
        print(f"Contatti: {limit} (rating ≥ {min_rating})")
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
        contatti_target = self.filtra_contatti_test(limit=limit, min_rating=min_rating)
        
        if not contatti_target:
            print("✗ Nessun contatto soddisfa i filtri")
            return

        # Genera file con link e tracking
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"CAMPAGNA WHATSAPP TEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Template: {template_nome}\n")
            f.write(f"Obiettivo: 90%+ tasso risposta\n")
            f.write("=" * 60 + "\n\n")
            
            for i, contatto in enumerate(contatti_target, 1):
                # Prepara variabili template
                vars_contatto = {
                    'nome_salone': contatto.get('nome_salone', ''),
                    'rating': contatto.get('rating', ''),
                    'num_simili': self.calcola_num_simili(contatto)
                }
                
                # Personalizza messaggio
                messaggio = template.testo
                for var in template.variabili:
                    chiave = var.replace("{", "").replace("}", "")
                    valore = vars_contatto.get(chiave, '')
                    messaggio = messaggio.replace(var, str(valore))
                
                link = self.genera_link_whatsapp(contatto['cellulare'], messaggio)
                
                # Salva nel file
                f.write(f"{i}. {contatto['nome_salone']}\n")
                f.write(f"   📞 {contatto['cellulare']}\n")
                f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
                f.write(f"   🌐 {link}\n")
                f.write(f"   📊 ID: MSG{i:03d}\n")
                f.write("-" * 40 + "\n\n")
                
                # Salva nei log
                self.inviati.append({
                    'id': f"MSG{i:03d}",
                    'contatto': contatto,
                    'template': template_nome,
                    'link': link,
                    'timestamp': datetime.now().isoformat(),
                    'stato': 'inviato',
                    'scopo': template.scopo
                })

        print(f"✓ Creato {output_file} con {len(contatti_target)} link")
        print(f"📊 ID messaggi: MSG001 - MSG{len(contatti_target):03d}")
        print(f"🎯 Obiettivo: 90%+ risposte ({len(contatti_target) * 0.9:.0f}+ risposte)")
        
        return output_file

    def genera_tracker_risposte(self, output_file: str = "tracker_risposte.csv"):
        """Genera file CSV per tracciare risposte"""
        
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.write("ID Messaggio,Nome Salone,Cellulare,Template,Data Invio,Risposta,Data Risposta,Tipo Risposta,Note\n")
            
            for invio in self.inviati:
                f.write(f"{invio['id']},{invio['contatto']['nome_salone']},")
                f.write(f"{invio['contatto']['cellulare']},{invio['template']},")
                f.write(f"{invio['timestamp']},,,,,\n")
        
        print(f"✓ Creato tracker risposte: {output_file}")
        return output_file

    def analizza_risposte(self, tracker_file: str = "tracker_risposte.csv"):
        """Analizza le risposte ricevute"""
        try:
            import pandas as pd
            
            df = pd.read_csv(tracker_file)
            
            # Statistiche base
            tot_invii = len(df)
            tot_risposte = df['Risposta'].notna().sum()
            tasso_risposta = (tot_risposte / tot_invii) * 100 if tot_invii > 0 else 0
            
            print(f"\n{'='*60}")
            print(f"ANALISI CAMPAGNA")
            print(f"{'='*60}")
            print(f"📊 Messaggi inviati: {tot_invii}")
            print(f"📨 Risposte ricevute: {tot_risposte}")
            print(f"📈 Tasso risposta: {tasso_risposta:.1f}%")
            
            if tasso_risposta >= 90:
                print("🎉 OBIETTIVO RAGGIUNTO! Tasso ≥ 90%")
            elif tasso_risposta >= 70:
                print("✅ Buon risultato! Tasso ≥ 70%")
            else:
                print("⚠️ Tasso risposta basso - ottimizzare template")
            
            # Analisi per template
            if 'Risposta' in df.columns and df['Risposta'].notna().any():
                print(f"\n📋 Breakdown per template:")
                for template in df['Template'].unique():
                    subset = df[df['Template'] == template]
                    risposte_template = subset['Risposta'].notna().sum()
                    tasso_template = (risposte_template / len(subset)) * 100
                    print(f"  - {template}: {risposte_template}/{len(subset)} ({tasso_template:.1f}%)")
            
            return tasso_risposta
            
        except Exception as e:
            print(f"✗ Errore analisi: {e}")
            return 0

    def statistiche_mercato(self):
        """Statistiche sul mercato target"""
        print(f"\n{'='*60}")
        print(f"STATISTICHE MERCATO TARGET")
        print(f"{'='*60}")
        
        if not self.contatti:
            print("Nessun contatto caricato")
            return
        
        # Rating distribution
        ratings = [float(c.get('rating') or 0) for c in self.contatti if c.get('rating')]
        if ratings:
            print(f"⭐ Rating medio: {sum(ratings)/len(ratings):.1f}")
            print(f"📊 Rating ≥ 4.5: {len([r for r in ratings if r >= 4.5])}/{len(ratings)}")
            print(f"📊 Rating ≥ 4.0: {len([r for r in ratings if r >= 4.0])}/{len(ratings)}")
        
        # Città principali
        citta = {}
        for c in self.contatti:
            if c.get('indirizzo'):
                citta_nome = c.get('indirizzo', '').split(',')[-1].strip()
                citta[citta_nome] = citta.get(citta_nome, 0) + 1
        
        print(f"\n🏙️ Top 5 città:")
        for citta_nome, count in sorted(citta.items(), key=lambda x: -x[1])[:5]:
            print(f"  - {citta_nome}: {count} contatti")


def main():
    """Menu principale per campagna test"""
    print("=" * 60)
    print("WHATSAPP OUTREACH V2 - TEST GO-TO-MARKET")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("Obiettivo: 90%+ tasso risposta")
    print("=" * 60)

    outreach = WhatsAppOutreachV2()

    # Carica contatti
    if not outreach.carica_contatti():
        return

    # Imposta template
    outreach.imposta_templates()

    # Statistiche mercato
    outreach.statistiche_mercato()

    print(f"\n📋 Template disponibili:")
    for i, t in enumerate(outreach.templates, 1):
        print(f"{i}. {t.nome_template} ({t.scopo})")

    print(f"\nCosa vuoi testare?")
    print("1. Domanda diretta (Sì/No)")
    print("2. Curiosity gap (con rating)")
    print("3. Social proof (num simili)")
    print("4. Test prezzo sensitivity")
    print("5. Follow-up gentile")
    print("6. Offerta urgente")
    print("7. Analizza risposte")
    print("8. Statistiche complete")

    scelta = input("\nScelta (1-8): ").strip()

    template_map = {
        "1": "domanda_direct",
        "2": "curiosity_gap", 
        "3": "social_proof",
        "4": "price_test",
        "5": "follow_up_gentile",
        "6": "offerta_urgente"
    }

    if scelta in template_map:
        limit = int(input("Numero contatti (default 20): ") or "20")
        min_rating = float(input("Rating minimo (default 4.0): ") or "4.0")
        
        outreach.genera_campagna_test(
            template_nome=template_map[scelta],
            limit=limit,
            min_rating=min_rating
        )
        
        # Genera tracker
        outreach.genera_tracker_risposte()
        
    elif scelta == "7":
        outreach.analizza_risposte()
    elif scelta == "8":
        outreach.statistiche_mercato()
    else:
        print("Scelta non valida")


if __name__ == "__main__":
    main()
