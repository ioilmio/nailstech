#!/usr/bin/env python3
"""
Messaggi Ottimizzati - Versioni con diverso livello di dettaglio
Test per trovare il miglior equilibrio tra chiarezza e lunghezza
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
    print("MESSAGGI OTTIMIZZATI - TEST CHIAREZZA VS LUNGHEZZA")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Diverse versioni del messaggio
    messaggi = {
        "breve": {
            "testo": """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech.

Le interessa una stampante per nail art unghie in noleggio?

Mi basta un "Sì" e le invio i dettagli. Grazie! 🙏""",
            "caratteri": 158,
            "note": "Molto breve, rischio ambiguità"
        },
        
        "medio": {
            "testo": """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech (Quadro srls).

Offriamo stampanti per nail art in noleggio per centri estetici come il suo.

Le interessa ricevere un preventivo senza impegno?

Mi basta un "Sì" e le invio subito i dettagli. Grazie! 🙏""",
            "caratteri": 185,
            "note": "Equilibrato, più contesto"
        },
        
        "dettagliato": {
            "testo": """👋 Buongiorno {nome_salone}, sono Salvatore di Nailstech.

Abbiamo notato il suo centro e pensavamo che potrebbe essere interessato al nostro servizio di noleggio stampanti per nail art.

✅ Stampanti professionali HD
✅ Assistenza tecnica inclusa  
✅ Formazione per il personale
✅ Costi flessibili (da 80€/settimana)

Le interessa ricevere un catalogo e preventivo personalizzato?

Un "Sì" è sufficiente. Grazie mille! 🙏""",
            "caratteri": 248,
            "note": "Più dettagli, rischio troppo lungo"
        }
    }
    
    print(f"\n📱 Versioni messaggi disponibili:")
    for nome, info in messaggi.items():
        print(f"   {nome}: {info['caratteri']} caratteri - {info['note']}")
    
    print(f"\n🎯 Testiamo tutte e 3 le versioni su 5 contatti ciascuna")
    print("-" * 60)
    
    # Genera file di test
    with open('messaggi_test_comparazione.txt', 'w', encoding='utf-8') as f:
        f.write(f"TEST MESSAGGI - CONFRONTO VERSIONI\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write("=" * 60 + "\n\n")
        
        contatti_test = contatti[:5]  # 5 contatti per ogni versione
        
        for versione, info in messaggi.items():
            f.write(f"VERSIONE: {versione.upper()} ({info['caratteri']} caratteri)\n")
            f.write(f"Note: {info['note']}\n")
            f.write("-" * 40 + "\n\n")
            
            print(f"\n📧 VERSIONE {versione.upper()}:")
            
            for i, contatto in enumerate(contatti_test, 1):
                # Personalizza messaggio
                messaggio = info['testo'].format(nome_salone=contatto['nome_salone'])
                link = genera_link_whatsapp(contatto['cellulare'], messaggio)
                
                print(f"  {i}. {contatto['nome_salone']} (⭐ {contatto.get('rating', 'N/A')})")
                
                # Salva nel file
                f.write(f"{i}. {contatto['nome_salone']}\n")
                f.write(f"   📞 {contatto['cellulare']}\n")
                f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
                f.write(f"   🆔 ID: {versione.upper()}{i:03d}\n")
                f.write(f"   🌐 {link}\n\n")
            
            f.write("\n" + "=" * 60 + "\n\n")
    
    print(f"\n✓ Creato file 'messaggi_test_comparazione.txt'")
    print(f"📊 15 link totali: 5 per ogni versione")
    print(f"🎯 Obiettivo: testare quale versione genera più risposte")
    
    # Genera tracker comparazione
    with open('tracker_messaggi_comparazione.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Versione,Nome Salone,Cellulare,Rating,Caratteri,Data Invio,Risposta,Data Risposta,Note\n")
        
        for versione, info in messaggi.items():
            for i, contatto in enumerate(contatti_test, 1):
                f.write(f"{versione.upper()}{i:03d},{versione},{contatto['nome_salone']},{contatto['cellulare']},{contatto.get('rating', '')},{info['caratteri']},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_messaggi_comparazione.csv'")
    print(f"\n🚀 PRONTO PER IL TEST COMPARATIVO!")
    print(f"💡 Invia i 15 messaggi e vedi quale versione funziona meglio")

if __name__ == "__main__":
    main()
