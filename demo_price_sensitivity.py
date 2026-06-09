#!/usr/bin/env python3
"""
Demo Price Sensitivity - Test Prezzi Reali Nailstech
Opzioni: 120€/giorno, 80€/settimana, 350€/settimana
"""

import json
import csv
from datetime import datetime

def carica_contatti():
    """Carica contatti con rating >= 4.5 per test prezzo"""
    contatti = []
    try:
        with open('contatti_catania.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for contatto in data.get('contatti', []):
                if contatto.get('cellulare'):
                    rating = float(contatto.get('rating') or 0)
                    if rating >= 4.5:  # Solo top rating per test prezzo
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
    print("DEMO PRICE SENSITIVITY - PREZZI REALI NAILSTECH")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti top rating
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.5")
    
    # Template price sensitivity con prezzi reali
    template_price = """👋 {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Test di mercato: a che formula preferisce per il noleggio stampante unghie?
- A) 120€/giorno (uso singolo)
- B) 80€/settimana (es. ogni lunedì)
- C) 350€/settimana (full-time)

Mi basta la lettera della risposta. Grazie mille! 📊"""
    
    print(f"\n💰 Prezzi in test:")
    print(f"   A) 120€/giorno - per eventi/uso occasionale")
    print(f"   B) 80€/settimana - ricorrente (es. ogni lunedì)")
    print(f"   C) 350€/settimana - full-time 7 giorni")
    print(f"\n🎯 Obiettivo: 90%+ tasso risposta")
    print("-" * 60)
    
    # Genera file con link
    with open('price_sensitivity_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"PRICE SENSITIVITY TEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Prezzi: 120€/giorno | 80€/settimana | 350€/settimana\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti[:15], 1):  # 15 top contatti
            # Personalizza messaggio
            messaggio = template_price.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\n{i}. {contatto['nome_salone']} (⭐ {contatto.get('rating', 'N/A')})")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   🌐 {link}")
            
            # Salva nel file
            f.write(f"{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: PRICE{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'price_sensitivity_links.txt' con 15 link")
    print(f"🎯 Target: 14+ risposte su 15 messaggi (93%)")
    print(f"📊 ID tracking: PRICE001 - PRICE015")
    
    # Genera tracker price sensitivity
    with open('tracker_price_sensitivity.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Cellulare,Rating,Data Invio,Risposta,Data Risposta,Prezzo Scelto,Note\n")
        
        for i, contatto in enumerate(contatti[:15], 1):
            f.write(f"PRICE{i:03d},{contatto['nome_salone']},{contatto['cellulare']},{contatto.get('rating', '')},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_price_sensitivity.csv'")
    print(f"\n🚀 PRONTO PER TEST PRICE SENSITIVITY!")
    print(f"📊 Analizzeremo: A vs B vs C per determinare prezzo ottimale")

if __name__ == "__main__":
    main()
