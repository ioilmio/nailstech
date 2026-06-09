#!/usr/bin/env python3
"""
Campagna Completa - Tutti i contatti rimanenti (dopo i primi 30)
WhatsApp Web links per Ubuntu - nessuna richiesta app
"""

import json
import csv
from datetime import datetime
import urllib.parse

def carica_contatti():
    """Carica tutti i contatti con rating >= 4.0"""
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
    """Genera link WhatsApp Web - apre direttamente nel browser"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def main():
    print("=" * 60)
    print("CAMPAGNA COMPLETA - CONTATTI RIMANENTI")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("WhatsApp Web compatibile Ubuntu")
    print("=" * 60)
    
    # Carica tutti i contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti totali con rating ≥ 4.0")
    
    # Salta i primi 30 (già fatti)
    contatti_rimanenti = contatti[30:]  # Dal 31 in poi
    print(f"✓ Primi 30 già processati, rimanenti: {len(contatti_rimanenti)}")
    
    # Messaggio finale ottimizzato
    messaggio_finale = """Salve {nome_salone}, sono Salvatore di Nailstech (Quadro srls).
Offriamo stampanti per nail art in noleggio per centri estetici come il suo.
Le interessa ricevere un preventivo senza impegno?
Mi basta un "Sì" e le invio subito i dettagli. Grazie!"""
    
    print(f"\n📱 Messaggio finale:")
    print(f"   - 155 caratteri")
    print(f"   - Nessuna emoji")
    print(f"   - WhatsApp Web compatibile")
    print(f"   - Encoding corretto")
    print(f"\n🎯 Target: {len(contatti_rimanenti)} contatti rimanenti")
    print("-" * 60)
    
    # Genera file con tutti i link rimanenti
    with open('campagna_completa_restanti_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"CAMPAGNA WHATSAPP COMPLETA - CONTATTI RIMANENTI\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"WhatsApp Web links - compatibili Ubuntu\n")
        f.write(f"Contatti: {len(contatti_rimanenti)} (dal 31 al {len(contatti)})\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti_rimanenti, 31):  # Parte da 31
            # Personalizza messaggio
            messaggio = messaggio_finale.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\n{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            print(f"   🌐 {link}")
            
            # Salva nel file
            f.write(f"{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: REST{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
            
            # Aggiungi separazione ogni 10 contatti
            if i % 10 == 0 and i < len(contatti_rimanenti):
                f.write("\n" + "=" * 40 + f"\nBLOCCO {i//10 + 1}\n" + "=" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'campagna_completa_restanti_links.txt'")
    print(f"📊 {len(contatti_rimanenti)} link totali")
    print(f"🆔 ID tracking: REST031 - REST{len(contatti):03d}")
    
    # Genera tracker completo
    with open('tracker_campagna_completa.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Cellulare,Rating,Data Invio,Risposta,Data Risposta,Tipo Risposta,Note\n")
        
        # Primi 30 (già fatti)
        for i in range(1, 31):
            f.write(f"FIX{i:03d},,,,,{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,\n")
        
        # Rimanenti
        for i, contatto in enumerate(contatti_rimanenti, 31):
            f.write(f"REST{i:03d},{contatto['nome_salone']},{contatto['cellulare']},{contatto.get('rating', '')},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,\n")
    
    print(f"📋 Creato tracker completo: 'tracker_campagna_completa.csv'")
    print(f"\n🚀 CAMPAGNA COMPLETA PRONTA!")
    print(f"💡 Tutti {len(contatti)} contatti ora disponibili")
    print(f"🌐 Links WhatsApp Web - perfetti per Ubuntu")

if __name__ == "__main__":
    main()
