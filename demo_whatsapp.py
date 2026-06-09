#!/usr/bin/env python3
"""
Demo WhatsApp Outreach - Genera link per invio manuale
"""

import json
import csv

def carica_contatti():
    """Carica contatti dal CSV"""
    contatti = []
    try:
        with open('contatti_catania.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('cellulare') and row.get('rating'):
                    rating = float(row['rating'] or 0)
                    if rating >= 4.0:
                        contatti.append(row)
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
    print("DEMO WHATSAPP OUTREACH")
    print("Noleggio Stampante Unghie - Catania")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating >= 4.0")
    
    # Template messaggio
    template = """👋 Buongiorno {nome_salone}!

Sono Marco di NailTech Solutions. Offriamo stampanti per unghie in noleggio a partire da 99€/mese.

Le interessa un preventivo senza impegno?"""
    
    # Genera link per primi 5 contatti
    print(f"\n📱 Link WhatsApp per primi 5 contatti:")
    print("-" * 60)
    
    for i, contatto in enumerate(contatti[:5], 1):
        messaggio = template.format(nome_salone=contatto['nome_salone'])
        link = genera_link_whatsapp(contatto['cellulare'], messaggio)
        
        print(f"\n{i}. {contatto['nome_salone']}")
        print(f"   📞 {contatto['cellulare']}")
        print(f"   ⭐ Rating: {contatto['rating']}")
        print(f"   🌐 {link}")
    
    print(f"\n✓ Generati {min(5, len(contatti))} link WhatsApp")
    print(f"📂 Copia e incolla i link nel browser per inviare i messaggi")

if __name__ == "__main__":
    main()
