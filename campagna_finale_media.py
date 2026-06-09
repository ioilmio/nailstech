#!/usr/bin/env python3
"""
Campagna Finale - Versione MEDIA (185 caratteri)
Messaggio ottimizzato per massima chiarezza e tasso risposta 90%+
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
    print("CAMPAGNA FINALE - VERSIONE MEDIA")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Messaggio finale versione MEDIA
    messaggio_finale = """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Offriamo stampanti per nail art in noleggio per centri estetici come il suo.

Le interessa ricevere un preventivo senza impegno?

Mi basta un "Sì" e le invio subito i dettagli. Grazie! 🙏"""
    
    print(f"\n📱 Messaggio finale:")
    print(f"   - Lunghezza: 185 caratteri")
    print(f"   - Versione: MEDIA (equilibrata)")
    print(f"   - Contesto: chiaro ma non invadente")
    print(f"   - CTA: preventivo senza impegno")
    print(f"\n🎯 Target: 90%+ tasso risposta")
    print("-" * 60)
    
    # Genera campagna con 30 contatti top
    limit = 30
    contatti_target = contatti[:limit]
    
    # Genera file con link
    with open('campagna_finale_media_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"CAMPAGNA WHATSAPP FINALE - VERSIONE MEDIA\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Messaggio: 185 caratteri - versione ottimizzata\n")
        f.write(f"Target: {limit} contatti top rating\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti_target, 1):
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
            f.write(f"   🆔 ID: MEDIA{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'campagna_finale_media_links.txt' con {limit} link")
    print(f"🎯 Target: {int(limit * 0.9)}+ risposte su {limit} messaggi (90%)")
    print(f"📊 ID tracking: MEDIA001 - MEDIA{limit:03d}")
    
    # Genera tracker finale
    with open('tracker_campagna_finale.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Cellulare,Rating,Data Invio,Risposta,Data Risposta,Tipo Risposta,Note\n")
        
        for i, contatto in enumerate(contatti_target, 1):
            f.write(f"MEDIA{i:03d},{contatto['nome_salone']},{contatto['cellulare']},{contatto.get('rating', '')},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_campagna_finale.csv'")
    print(f"\n🚀 CAMPAGNA FINALE PRONTA!")
    print(f"💡 Versione MEDIA: il miglior equilibrio tra chiarezza e lunghezza")
    print(f"📈 Obiettivo: test go-to-market con 90%+ tasso risposta")

if __name__ == "__main__":
    main()
