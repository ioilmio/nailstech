#!/usr/bin/env python3
"""
Demo Campagna Test - 90%+ Tasso Risposta
Nailstech - Salvatore +393515035361
"""

import json
import csv
from datetime import datetime

def carica_contatti():
    """Carica contatti con rating >= 4.0"""
    contatti = []
    try:
        with open('contatti_catania.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for contatto in data.get('contatti', []):
                if contatto.get('cellulare'):
                    rating = float(contatto.get('rating') or 0)
                    if rating >= 4.0:
                        contatti.append(contatto)
        return contatti
    except Exception as e:
        print(f"Errore: {e}")
        return []

def genera_link_whatsapp(telefono, messaggio):
    """Genera link WhatsApp Web"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = messaggio.replace('\n', '%0A').replace(' ', '%20')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def main():
    print("=" * 60)
    print("DEMO CAMPAGNA TEST - TARGET 90%+ RISPOSTA")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Template ottimizzati per alta risposta
    templates = {
        "domanda_direct": """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Volevo chiederle: il suo centro sarebbe interessato a una stampante per unghie in noleggio a 99€/mese?

Mi basta un "Sì/No" per capire se approfondire. Grazie mille! 🙏""",
        
        "curiosity_gap": """👋 Buongiorno {nome_salone}, sono Salvatore.

Ho notato che il suo centro ha un rating di {rating} stelle - complimenti! 🌟

Le faccio una domanda veloce: sa che potrebbe offrire nail art personalizzata ai suoi clienti con zero investimento iniziale?

Basta una risposta per capire se le interessa. Salvatore - Nailstech 📞 3515035361""",
        
        "price_test": """👋 {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Test di mercato: a che formula preferisce per il noleggio stampante unghie?
- A) 120€/giorno (uso singolo)
- B) 80€/settimana (es. ogni lunedì)
- C) 350€/settimana (full-time)

Mi basta la lettera della risposta. Grazie mille! 📊"""
    }
    
    print(f"\n📋 Template disponibili:")
    for i, nome in enumerate(templates.keys(), 1):
        print(f"{i}. {nome}")
    
    # Genera demo con primo template
    template_scelto = "domanda_direct"
    messaggio_template = templates[template_scelto]
    
    print(f"\n🎯 Demo con template: {template_scelto}")
    print(f"📊 Obiettivo: 90%+ tasso risposta")
    print("-" * 60)
    
    # Genera file con link
    with open('demo_campagna_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"CAMPAGNA TEST WHATSAPP - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Template: {template_scelto}\n")
        f.write(f"Obiettivo: 90%+ tasso risposta\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti[:10], 1):  # Demo primi 10
            # Personalizza messaggio
            messaggio = messaggio_template.format(
                nome_salone=contatto['nome_salone'],
                rating=contatto.get('rating', '')
            )
            
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\n{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            print(f"   🌐 {link}")
            
            # Salva nel file
            f.write(f"{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: MSG{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'demo_campagna_links.txt' con 10 link")
    print(f"🎯 Target: 9+ risposte su 10 messaggi (90%)")
    print(f"📊 ID tracking: MSG001 - MSG010")
    
    # Genera tracker risposte
    with open('tracker_risposte_demo.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Cellulare,Template,Data Invio,Risposta,Data Risposta,Tipo Risposta,Note\n")
        
        for i, contatto in enumerate(contatti[:10], 1):
            f.write(f"MSG{i:03d},{contatto['nome_salone']},{contatto['cellulare']},{template_scelto},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_risposte_demo.csv'")
    print(f"\n🚀 PRONTO PER IL TEST! Inizia a inviare i messaggi...")

if __name__ == "__main__":
    main()
