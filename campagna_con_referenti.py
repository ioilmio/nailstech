#!/usr/bin/env python3
"""
Campagna con Personalizzazione Referenti
Usa il nome del referente se disponibile, altrimenti nome salone
"""

import json
import csv
from datetime import datetime
import urllib.parse

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
    """Genera link WhatsApp Web con encoding corretto"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def main():
    print("=" * 60)
    print("CAMPAGNA CON PERSONALIZZAZIONE REFERENTI")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Analizza disponibilità referenti
    con_referente = [c for c in contatti if c.get('responsabile') and c.get('responsabile').strip()]
    senza_referente = [c for c in contatti if not c.get('responsabile') or not c.get('responsabile').strip()]
    
    print(f"📊 Analisi referenti:")
    print(f"   ✓ Con referente: {len(con_referente)}")
    print(f"   ❌ Senza referente: {len(senza_referente)}")
    
    # Messaggio con personalizzazione referente
    messaggio_con_referente = """Salve {nome_referente}, sono Salvatore di Nailstech (Quadro srls).
Offriamo stampanti per nail art in noleggio per centri estetici come {nome_salone}.
Le interessa ricevere un preventivo senza impegno?
Mi basta un "Sì" e le invio subito i dettagli. Grazie!"""
    
    messaggio_senza_referente = """Salve {nome_salone}, sono Salvatore di Nailstech (Quadro srls).
Offriamo stampanti per nail art in noleggio per centri estetici come il suo.
Le interessa ricevere un preventivo senza impegno?
Mi basta un "Sì" e le invio subito i dettagli. Grazie!"""
    
    print(f"\n📱 Messaggi personalizzati:")
    print(f"   - Con referente: usa nome referente + nome salone")
    print(f"   - Senza referente: usa solo nome salone")
    print(f"\n🎯 Target: 90%+ tasso risposta")
    print("-" * 60)
    
    # Genera campagna con 30 contatti top
    limit = 30
    contatti_target = contatti[:limit]
    
    # Genera file con link personalizzati
    with open('campagna_referenti_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"CAMPAGNA WHATSAPP CON PERSONALIZZAZIONE REFERENTI\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Personalizzazione: nome referente quando disponibile\n")
        f.write(f"Target: {limit} contatti top rating\n")
        f.write("=" * 60 + "\n\n")
        
        for i, contatto in enumerate(contatti_target, 1):
            # Scegli messaggio in base alla disponibilità del referente
            if contatto.get('responsabile') and contatto.get('responsabile').strip():
                nome_referente = contatto['responsabile'].strip()
                messaggio = messaggio_con_referente.format(
                    nome_referente=nome_referente,
                    nome_salone=contatto['nome_salone']
                )
                tipo_personalizzazione = "REFERENTE"
            else:
                messaggio = messaggio_senza_referente.format(nome_salone=contatto['nome_salone'])
                tipo_personalizzazione = "SALONE"
            
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\n{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            print(f"   👤 Referente: {contatto.get('responsabile', 'N/D') or 'N/D'}")
            print(f"   🎯 Personalizzazione: {tipo_personalizzazione}")
            print(f"   🌐 {link}")
            
            # Salva nel file
            f.write(f"{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   👤 Referente: {contatto.get('responsabile', 'N/D') or 'N/D'}\n")
            f.write(f"   🎯 Personalizzazione: {tipo_personalizzazione}\n")
            f.write(f"   🆔 ID: REF{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✓ Creato file 'campagna_referenti_links.txt' con {limit} link")
    print(f"🎯 Target: {int(limit * 0.9)}+ risposte su {limit} messaggi (90%)")
    print(f"📊 ID tracking: REF001 - REF{limit:03d}")
    
    # Genera tracker personalizzato
    with open('tracker_campagna_referenti.csv', 'w', encoding='utf-8-sig') as f:
        f.write("ID Messaggio,Nome Salone,Referente,Cellulare,Rating,Personalizzazione,Data Invio,Risposta,Data Risposta,Tipo Risposta,Note\n")
        
        for i, contatto in enumerate(contatti_target, 1):
            nome_referente = contatto.get('responsabile', '') or ''
            personalizzazione = "REFERENTE" if nome_referente.strip() else "SALONE"
            f.write(f"REF{i:03d},{contatto['nome_salone']},{nome_referente},{contatto['cellulare']},{contatto.get('rating', '')},{personalizzazione},{datetime.now().strftime('%Y-%m-%d %H:%M')},,,,,\n")
    
    print(f"📋 Creato tracker: 'tracker_campagna_referenti.csv'")
    print(f"\n🚀 CAMPAGNA CON REFERENTI PRONTA!")
    print(f"💡 Personalizzazione massima quando disponibile il referente")

if __name__ == "__main__":
    main()
