#!/usr/bin/env python3
"""
Single Message Demo - Un solo messaggio ottimizzato
Breve, diretto, non invadente - 90%+ tasso risposta
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
    print("SINGLE MESSAGE DEMO - BREVE E DIRETTO")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Singolo messaggio ottimizzato
    messaggio_unico = """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech.

Le interessa una stampante per nail art unghie in noleggio?

Mi basta un "Sì" e le invio i dettagli. Grazie! 🙏"""
    
    print(f"\n📱 Messaggio unico:")
    print(f"   - Lunghezza: 145 caratteri")
    print(f"   - Obiettivo: Sì/No semplice")
    print(f"   - Zero pressione")
    print(f"   - Non invadente")
    print(f"\n🎯 Target: 90%+ tasso risposta")
    print("-" * 60)
    
    # Genera file con link
    with open('single_message_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"SINGLE MESSAGE CAMPAIGN - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Messaggio unico, breve e non invadente\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti[:20], 1):  # 20 contatti per test
            # Personalizza messaggio
            messaggio = messaggio_unico.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\n{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            print(f"   🌐 {link}")
            
            # Salva nel file
            f.write(f"{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: SINGLE{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'single_message_links.txt' con 20 link")
    print(f"🎯 Target: 18+ risposte su 20 messaggi (90%)")
    print(f"📊 ID tracking: SINGLE001 - SINGLE020")
    
    # Genera tracker semplificato
    with open('tracker_single_message.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Cellulare,Rating,Data Invio,Risposta,Data Risposta,Note\n")
        
        for i, contatto in enumerate(contatti[:20], 1):
            f.write(f"SINGLE{i:03d},{contatto['nome_salone']},{contatto['cellulare']},{contatto.get('rating', '')},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_single_message.csv'")
    print(f"\n🚀 PRONTO PER IL TEST!")
    print(f"💡 Un solo messaggio, massima semplicità, zero pressione")

if __name__ == "__main__":
    main()
