#!/usr/bin/env python3
"""
Follow-up Prioritario - Convertire NO in NÌ
Piano d'azione per chiudere primo contratto e convertire rifiuti
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

def identifica_target_prioritari():
    """Identifica contatti per follow-up prioritario"""
    contatti = carica_tracker_unificato()
    
    # Target prioritari
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

def crea_messaggio_conversione(contatto):
    """Crea messaggio personalizzato per conversione"""
    
    nome = contatto.get('Nome Salone', '')
    risposta = contatto.get('Risposta', '').lower()
    
    # Messaggio per TESTA006 - INTERESSE REALE
    if contatto['ID Messaggio'] == 'TESTA006':
        return f"""Buonasera {nome}! Sono Salvatore di Nailstech. La nostra stampante per nail art crea design complessi in 2 minuti e aumenta i clienti del centro. A 100€/giorno le permette di offrire servizi premium che i concorrenti non hanno. Vuole vedere qualche esempio di lavori realizzati? Posso inviarle 2 foto subito."""
    
    # Messaggio per rifiuti diretti - CONVERSIONE NO→NÌ
    if "no grazie" in risposta or "non interessat" in risposta:
        return f"""Capisco {nome}. Prima di decidere definitivamente, le chiedo: sa che molti centri come il suo aumentano i profitti del 30% con nail art personalizzate? Non le costa nulla vedere qualche esempio. Posso inviarle 2 foto di lavori realizzati da centri estetici come il suo? Magari cambia idea..."""
    
    # Messaggio per risposte automatiche - FOLLOW-UP
    return f"""Salve {nome}, sono Salvatore di Nailstech. Ho visto la sua risposta automatica. Le offro stampanti per nail art in noleggio a 100€/giorno che creano design unici in 2 minuti. Posso aumentare i suoi clienti con servizi premium. Le interessa scoprire come funziona?"""

def genera_link_prioritario():
    """Genera follow-up prioritario"""
    
    print("🎯 FOLLOW-UP PRIORITARIO - CONVERTIRE NO IN NÌ")
    print("=" * 60)
    
    interessi_reali, rifiuti_convertibili, risposte_automatiche = identifica_target_prioritari()
    
    print(f"\n📊 TARGET IDENTIFICATI:")
    print(f"   🔥 Interessi reali: {len(interessi_reali)} (PRIORITÀ MASSIMA)")
    print(f"   🔄 Rifiuti convertibili: {len(rifiuti_convertibili)}")
    print(f"   ⏳ Risposte automatiche: {len(risposte_automatiche)}")
    
    # Crea file follow-up prioritario
    with open('follow_up_prioritario.txt', 'w', encoding='utf-8') as f:
        f.write(f"FOLLOW-UP PRIORITARIO - CONVERSIONE NO→NÌ\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write("=" * 60 + "\n\n")
        
        # 1. INTERESSI REALI - PRIORITÀ ASSOLUTA
        f.write("🔥 PRIORITÀ ASSOLUTA - INTERESSI REALI\n")
        f.write("-" * 40 + "\n\n")
        
        for contatto in interessi_reali:
            messaggio = crea_messaggio_conversione(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"🎯 {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Messaggio: {contatto['Risposta']}\n")
            f.write(f"   🌐 Follow-up: {link}\n\n")
        
        # 2. RIFIUTI CONVERTIBILI
        f.write("🔄 POTENZIALE CONVERSIONE - RIFIUTI\n")
        f.write("-" * 40 + "\n\n")
        
        for contatto in rifiuti_convertibili:
            messaggio = crea_messaggio_conversione(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"🔄 {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Messaggio: {contatto['Risposta']}\n")
            f.write(f"   🌐 Follow-up: {link}\n\n")
        
        # 3. RISPOSTE AUTOMATICHE - ATTESA
        f.write("⏳ RISPOSTE AUTOMATICHE - ATTESA\n")
        f.write("-" * 40 + "\n\n")
        
        for contatto in risposte_automatiche:
            messaggio = crea_messaggio_conversione(contatto)
            link = genera_link_whatsapp(contatto['Cellulare'], messaggio)
            
            f.write(f"⏳ {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"   📞 {contatto['Cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto['Rating']}\n")
            f.write(f"   💬 Risposta automatica\n")
            f.write(f"   🌐 Follow-up: {link}\n\n")
    
    print(f"\n✅ Creato file: 'follow_up_prioritario.txt'")
    
    # Mostra piano d'azione immediato
    print(f"\n🚀 PIANO D'AZIONE IMMEDIATO:")
    
    if interessi_reali:
        contatto = interessi_reali[0]
        print(f"\n1️⃣ CHIUDERE PRIMO CONTRATTO:")
        print(f"   🎯 {contatto['ID Messaggio']} - {contatto['Nome Salone']}")
        print(f"   📞 {contatto['Cellulare']}")
        print(f"   💬 Ha chiesto: '{contatto['Risposta']}'")
        print(f"   🔥 INVIA SUBITO FOLLOW-UP CON ESEMPI")
    
    if rifiuti_convertibili:
        print(f"\n2️⃣ CONVERSIONE NO→NÌ:")
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

def mostra_piano_contratto():
    """Mostra piano per chiudere primo contratto"""
    
    print("\n" + "=" * 60)
    print("🔥 PIANO CHIUSURA PRIMO CONTRATTO - TESTA006")
    print("=" * 60)
    
    print("\n📋 DATI CONTATTO:")
    print("   🏢 Extension ciglia Catania")
    print("   📞 +393248882599")
    print("   ⭐ Rating: 5.0")
    print("   💬 Ha chiesto: 'Buona sera, in cosa consiste?'")
    
    print("\n🎯 STRATEGIA CHIUSURA:")
    print("   1. Rispondere subito con dettagli chiari")
    print("   2. Inviare 2-3 esempi di nail art")
    print("   3. Proporre prova gratuita di 1 giorno")
    print("   4. Chiudere contratto settimana prova")
    
    print("\n💬 MESSAGGIO CONVERSIONE:")
    print("   'Buonasera! La nostra stampante crea design complessi in 2 minuti.'")
    print("   'Aumenta i clienti del centro con servizi premium.'")
    print("   '100€/giorno - Le interessa vedere esempi realizzati?'")
    
    print("\n📈 PROBABILITÀ SUCCESSO: 80%")
    print("   ✅ Ha mostrato interesse attivo")
    print("   ✅ Rating 5.0 - centro qualità")
    print("   ✅ Orario sereno per conversazione")

if __name__ == "__main__":
    print("FOLLOW-UP PRIORITARIO - CONVERTIRE NO IN NÌ")
    print("1. Genera follow-up prioritario")
    print("2. Mostra piano contratto TESTA006")
    print("3. Tutti")
    
    scelta = input("\nScelta (1-3): ").strip()
    
    if scelta == "1":
        genera_link_prioritario()
    elif scelta == "2":
        mostra_piano_contratto()
    elif scelta == "3":
        genera_link_prioritario()
        mostra_piano_contratto()
    else:
        print("Scelta non valida.")
