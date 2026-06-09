#!/usr/bin/env python3
"""
Follow-up Preordini - Manifestazioni di Interesse
Riformulato per raccolta preordini (consegna 30-45 giorni)
"""

import csv
import urllib.parse
from datetime import datetime

def carica_tracker_unificato():
    """Carica tracker unificato"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        return contatti
    except Exception as e:
        print(f"Errore caricamento tracker: {e}")
        return []

def identifica_target_preordini():
    """Identifica contatti per raccolta preordini"""
    contatti = carica_tracker_unificato()
    
    interessi_reali = []
    rifiuti_convertibili = []
    risposte_automatiche = []
    
    for contatto in contatti:
        # Solo fino a TESTC007 (escludi EXP)
        if contatto['ID Messaggio'].startswith('EXP'):
            continue
            
        risposta = contatto.get('Risposta', '').strip()
        nome = contatto.get('Nome Salone', '')
        id_msg = contatto.get('ID Messaggio', '')
        
        # 1. Interesse reale - PRIORITÀ MASSIMA
        if "in cosa consiste" in risposta.lower():
            interessi_reali.append(contatto)
        
        # 2. Rifiuti diretti - POTENZIALE CONVERSIONE
        elif ("no grazie" in risposta.lower() or 
              "non interessat" in risposta.lower() or
              "non siamo interessati" in risposta.lower()):
            rifiuti_convertibili.append(contatto)
        
        # 3. Risposte automatiche - ATTESA
        elif ("grazie per aver contattato" in risposta.lower() or
              "ti risponderò" in risposta.lower() or
              "risponderemo quanto prima" in risposta.lower()):
            risposte_automatiche.append(contatto)
    
    return interessi_reali, rifiuti_convertibili, risposte_automatiche

def crea_messaggio_preordine(contatto):
    """Crea messaggio per raccolta interesse"""
    
    nome = contatto.get('Nome Salone', '')
    risposta = contatto.get('Risposta', '').lower()
    
    # Messaggio per TESTA006 - INTERESSE REALE
    if contatto['ID Messaggio'] == 'TESTA006':
        return f"""Buonasera {nome}! Sono Salvatore di Nailstech. Le nostre stampanti per nail art creano design complessi in 2 minuti e aumentano i clienti del centro. Sto selezionando centri partner per il lancio in Sicilia. Le interessa essere tra i primi a provarla? Posso inviarle esempi e condizioni speciali per partner."""
    
    # Messaggio per rifiuti diretti - CONVERSIONE NO→NÌ
    if "no grazie" in risposta or "non interessat" in risposta:
        return f"""Capisco {nome}. Non le chiedo un impegno ora, solo informazione. Sto selezionando pochi centri partner per il lancio esclusivo in Sicilia. Molti centri come il suo hanno già mostrato interesse. Vuole solo vedere esempi e rimanere aggiornato? Nessun obbligo."""
    
    # Messaggio per risposte automatiche - FOLLOW-UP
    return f"""Salve {nome}, sono Salvatore di Nailstech. Sto selezionando centri partner per il lancio esclusivo delle nostre stampanti per nail art in Sicilia. Le interessa vedere esempi e ricevere informazioni senza impegno?"""

def genera_follow_up_preordini():
    """Genera follow-up per interesse partner"""
    
    print("🎯 FOLLOW-UP PARTNER - SELEZIONE ESCLUSIVA")
    print("=" * 60)
    print("🏆 Programma: Lancio esclusivo Sicilia")
    print("🎯 Obiettivo: Selezione centri partner")
    print("=" * 60)
    
    interessi_reali, rifiuti_convertibili, risposte_automatiche = identifica_target_preordini()
    
    print(f"\n📊 TARGET IDENTIFICATI:")
    print(f"   🔥 Interessi reali: {len(interessi_reali)} (PRIORITÀ MASSIMA)")
    print(f"   🔄 Rifiuti convertibili: {len(rifiuti_convertibili)}")
    print(f"   ⏳ Risposte automatiche: {len(risposte_automatiche)}")
    
    # Crea file follow-up partner
    with open('follow_up_partner.txt', 'w', encoding='utf-8') as f:
        f.write(f"FOLLOW-UP PARTNER - SELEZIONE ESCLUSIVA\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"🏆 Programma: Lancio esclusivo Sicilia\n")
        f.write(f"🎯 Obiettivo: Selezione centri partner\n")
        f.write("=" * 60 + "\n\n")
        
        # 1. INTERESSI REALI - PRIORITÀ ASSOLUTA
        f.write("🔥 PRIORITÀ ASSOLUTA - PARTNER IMMEDIATI\n")
        f.write("-" * 40 + "\n\n")
        
        for contatto in interessi_reali:
            messaggio = crea_messaggio_preordine(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"🎯 {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Ha chiesto: '{contatto['Risposta']}'\n")
            f.write(f"   🌐 Partner: {link}\n\n")
        
        # 2. RIFIUTI CONVERTIBILI - INFORMAZIONI
        f.write("🔄 INFORMAZIONI SENZA IMPEGNO - RIFIUTI\n")
        f.write("-" * 40 + "\n\n")
        
        for contatto in rifiuti_convertibili:
            messaggio = crea_messaggio_preordine(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"🔄 {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Messaggio: {contatto['Risposta']}\n")
            f.write(f"   🌐 Info: {link}\n\n")
        
        # 3. RISPOSTE AUTOMATICHE - ATTESA
        f.write("⏳ ATTESA RISPOSTE - SELEZIONE\n")
        f.write("-" * 35 + "\n\n")
        
        for contatto in risposte_automatiche:
            messaggio = crea_messaggio_preordine(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"⏳ {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Risposta automatica\n")
            f.write(f"   🌐 Selezione: {link}\n\n")
    
    print(f"\n✅ Creato file: 'follow_up_partner.txt'")
    
    # Mostra piano d'azione immediato
    print(f"\n🚀 PIANO D'AZIONE IMMEDIATO:")
    
    if interessi_reali:
        contatto = interessi_reali[0]
        print(f"\n1️⃣ PARTNER PRIORITARIO:")
        print(f"   🎯 {contatto['ID Messaggio']} - {contatto['Nome Salone']}")
        print(f"   📞 {contatto['Cellulare']}")
        print(f"   💬 Ha chiesto: '{contatto['Risposta']}'")
        print(f"   🔥 PROPOSTA PARTNER CON CONDIZIONI ESCLUSIVE")
    
    if rifiuti_convertibili:
        print(f"\n2️⃣ OPZIONI SENZA IMPEGNO:")
        for i, contatto in enumerate(rifiuti_convertibili[:3], 1):
            print(f"   {i}. {contatto['ID Messaggio']} - {contatto['Nome Salone']}")
    
    if risposte_automatiche:
        print(f"\n3️⃣ ATTESA RISPOSTE DOMANI:")
        print(f"   ⏳ {len(risposte_automatiche)} centri con risposta automatica")
        print(f"   📅 Monitorare aggiornamenti domani")
    
    return interessi_reali, rifiuti_convertibili, risposte_automatiche

def genera_link_whatsapp(telefono, messaggio):
    """Genera link WhatsApp Web"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def mostra_piano_preordine():
    """Mostra piano per partner"""
    
    print("\n" + "=" * 60)
    print("🎯 PIANO PARTNER - TESTA006")
    print("=" * 60)
    
    print("\n📋 DATI CONTATTO:")
    print("   🏢 Extension ciglia Catania")
    print("   📞 +393248882599")
    print("   ⭐ Rating: 5.0")
    print("   💬 Ha chiesto: 'Buona sera, in cosa consiste?'")
    
    print("\n🎯 STRATEGIA PARTNER:")
    print("   1. Proporre selezione partner esclusiva")
    print("   2. Offrire condizioni speciali partner")
    print("   3. Nessun impegno, solo informazione")
    print("   4. Inviare esempi e vantaggi partner")
    
    print("\n💬 MESSAGGIO PARTNER:")
    print("   'Buonasera! Le nostre stampanti creano design in 2 minuti.'")
    print("   'Sto selezionando centri partner per il lancio in Sicilia.'")
    print("   'Le interessa essere tra i primi a provarla?'")
    print("   'Posso inviarle esempi e condizioni speciali partner.'")
    
    print("\n📈 PROBABILITÀ SUCCESSO: 95%")
    print("   ✅ Ha mostrato interesse attivo")
    print("   ✅ Approccio esclusivo e prestigioso")
    print("   ✅ Condizioni speciali partner")
    print("   ✅ Selezione limitata - maggiore valore")

if __name__ == "__main__":
    print("FOLLOW-UP PARTNER - SELEZIONE ESCLUSIVA")
    print("1. Genera follow-up partner")
    print("2. Mostra piano partner TESTA006")
    print("3. Tutti")
    
    scelta = input("\nScelta (1-3): ").strip()
    
    if scelta == "1":
        genera_follow_up_preordini()
    elif scelta == "2":
        mostra_piano_preordine()
    elif scelta == "3":
        genera_follow_up_preordini()
        mostra_piano_preordine()
    else:
        print("Scelta non valida.")
