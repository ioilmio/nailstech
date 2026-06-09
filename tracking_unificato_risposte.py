#!/usr/bin/env python3
"""
Tracking Unificato Risposte - Sistema Completo
Gestisce tutte le risposte: primi 30 contatti + A/B test 20 contatti
"""

import csv
import json
import urllib.parse
from datetime import datetime

def carica_tracker_primi_30():
    """Carica tracker dei primi 30 contatti"""
    contatti = []
    try:
        with open('tracker_campagna_corretta.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        return contatti
    except Exception as e:
        print(f"Errore tracker primi 30: {e}")
        return []

def carica_tracker_ab_test():
    """Carica tracker A/B test"""
    contatti = []
    try:
        with open('tracker_ab_test.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        return contatti
    except Exception as e:
        print(f"Errore tracker A/B test: {e}")
        return []

def crea_tracker_unificato():
    """Crea tracker unificato con tutti i contatti"""
    primi_30 = carica_tracker_primi_30()
    ab_test = carica_tracker_ab_test()
    
    # Unifica tutti i contatti
    tutti_contatti = []
    
    # Aggiungi primi 30 con campagna "Iniziale"
    for contatto in primi_30:
        contatto['Campagna'] = 'Iniziale'
        contatto['Strategia'] = 'Media (185 caratteri)'
        tutti_contatti.append(contatto)
    
    # Aggiungi A/B test con campagna "A/B Test"
    for contatto in ab_test:
        contatto['Campagna'] = 'A/B Test'
        tutti_contatti.append(contatto)
    
    # Salva tracker unificato
    if tutti_contatti:
        with open('tracker_unificato.csv', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=tutti_contatti[0].keys())
            writer.writeheader()
            writer.writerows(tutti_contatti)
        
        print(f"✅ Creato tracker unificato con {len(tutti_contatti)} contatti")
        print(f"   📊 Primi 30: {len(primi_30)}")
        print(f"   🧪 A/B Test: {len(ab_test)}")
    
    return tutti_contatti

def aggiorna_risposta_unificata(id_messaggio, risposta, note=""):
    """Aggiorna risposta nel tracker unificato"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        # Se non esiste, crealo
        contatti = crea_tracker_unificato()
        return
    
    aggiornato = False
    for contatto in contatti:
        if contatto['ID Messaggio'] == id_messaggio:
            contatto['Risposta'] = risposta
            contatto['Data Risposta'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            contatto['Note'] = note
            aggiornato = True
            break
    
    if aggiornato:
        # Salva tracker aggiornato
        with open('tracker_unificato.csv', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=contatti[0].keys())
            writer.writeheader()
            writer.writerows(contatti)
        
        print(f"✅ Aggiornato {id_messaggio}: {risposta}")
    else:
        print(f"❌ ID {id_messaggio} non trovato")

def mostra_statistiche_complete():
    """Mostra statistiche complete di tutte le campagne"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        contatti = crea_tracker_unificato()
    
    print("\n" + "=" * 60)
    print("STATISTICHE COMPLETE - TUTTE LE CAMPAGNE")
    print("Nailstech - Divisione Quadro srls")
    print("=" * 60)
    
    # Statistiche totali
    totali = len(contatti)
    risposte = len([c for c in contatti if c.get('Risposta')])
    positivi = len([c for c in contatti if 'Positivo' in c.get('Risposta', '')])
    negativi = len([c for c in contatti if 'Negativo' in c.get('Risposta', '')])
    chiusi = len([c for c in contatti if 'Chiuso' in c.get('Risposta', '')])
    automatici = len([c for c in contatti if 'Automatico' in c.get('Risposta', '')])
    
    print(f"\n📊 STATISTICHE TOTALI:")
    print(f"   📤 Messaggi inviati: {totali}")
    print(f"   ✅ Risposte ricevute: {risposte} ({risposte/totali*100:.1f}%)")
    print(f"   👍 Risposte positive: {positivi}")
    print(f"   👎 Risposte negative: {negativi}")
    print(f"   🏢 Chiusi oggi: {chiusi}")
    print(f"   🤖 Risposte automatiche: {automatici}")
    print(f"   ⏳ In attesa: {totali - risposte}")
    
    # Statistiche per campagna
    print(f"\n📈 PER CAMPAGNA:")
    
    # Campagna Iniziale (primi 30)
    iniziale = [c for c in contatti if c.get('Campagna') == 'Iniziale']
    if iniziale:
        risposte_iniziale = len([c for c in iniziale if c.get('Risposta')])
        tasso_iniziale = risposte_iniziale / len(iniziale) * 100
        print(f"   🎯 Campagna Iniziale: {risposte_iniziale}/{len(iniziale)} ({tasso_iniziale:.1f}%)")
    
    # Campagna A/B Test
    ab_test_contatti = [c for c in contatti if c.get('Campagna') == 'A/B Test']
    if ab_test_contatti:
        risposte_ab = len([c for c in ab_test_contatti if c.get('Risposta')])
        tasso_ab = risposte_ab / len(ab_test_contatti) * 100
        print(f"   🧪 A/B Test: {risposte_ab}/{len(ab_test_contatti)} ({tasso_ab:.1f}%)")
    
    # Statistiche per strategia A/B test
    if ab_test_contatti:
        print(f"\n📊 A/B TEST - PER STRATEGIA:")
        for strategia in ['A - Valore e contesto', 'B - Curiosità e benefici', 'C - Efficienza e profitto']:
            contatti_strategia = [c for c in ab_test_contatti if c.get('Strategia') == strategia]
            if contatti_strategia:
                risposte_strategia = len([c for c in contatti_strategia if c.get('Risposta')])
                tasso = risposte_strategia / len(contatti_strategia) * 100
                print(f"   {strategia}: {risposte_strategia}/{len(contatti_strategia)} ({tasso:.1f}%)")

def menu_interattivo():
    """Menu principale per gestione risposte"""
    
    while True:
        print("\n" + "=" * 60)
        print("TRACKING UNIFICATO RISPOSTE")
        print("Nailstech - Divisione Quadro srls")
        print("=" * 60)
        print("1. Aggiorna risposta")
        print("2. Mostra statistiche complete")
        print("3. Lista contatti senza risposta")
        print("4. Lista contatti con risposta")
        print("5. Crea follow-up per rifiutati")
        print("6. Esci")
        
        scelta = input("\nScelta (1-6): ").strip()
        
        if scelta == "1":
            aggiungi_risposta_interattiva()
        elif scelta == "2":
            mostra_statistiche_complete()
        elif scelta == "3":
            mostra_contatti_senza_risposta()
        elif scelta == "4":
            mostra_contatti_con_risposta()
        elif scelta == "5":
            crea_follow_up_rifiutati()
        elif scelta == "6":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")

def aggiungi_risposta_interattiva():
    """Interfaccia per aggiungere risposte"""
    # Assicura che il tracker esista
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        contatti = crea_tracker_unificato()
    
    print("\n--- AGGIUNGI RISPOSTA ---")
    id_messaggio = input("ID Messaggio (es. FIX001, TESTA001): ").strip().upper()
    
    # Trova contatto
    contatto_trovato = None
    for contatto in contatti:
        if contatto['ID Messaggio'] == id_messaggio:
            contatto_trovato = contatto
            break
    
    if not contatto_trovato:
        print(f"❌ ID {id_messaggio} non trovato!")
        return
    
    print(f"\nContatto: {contatto_trovato['Nome Salone']}")
    print(f"Campagna: {contatto_trovato.get('Campagna', 'N/A')}")
    print(f"Strategia: {contatto_trovato.get('Strategia', 'N/A')}")
    
    print("\nTipi risposta:")
    print("1. Positivo")
    print("2. Negativo") 
    print("3. Chiuso oggi")
    print("4. Risposta automatica")
    print("5. Altro")
    
    tipo_risposta = input("Tipo risposta (1-5): ").strip()
    
    risposte_map = {
        "1": "Positivo",
        "2": "Negativo", 
        "3": "Chiuso oggi",
        "4": "Automatico",
        "5": "Altro"
    }
    
    risposta = risposte_map.get(tipo_risposta, "Altro")
    note = input("Note (opzionale): ").strip()
    
    aggiorna_risposta_unificata(id_messaggio, risposta, note)

def mostra_contatti_senza_risposta():
    """Mostra contatti che non hanno ancora risposto"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        contatti = crea_tracker_unificato()
    
    senza_risposta = [c for c in contatti if not c.get('Risposta')]
    
    print(f"\n--- CONTATTI SENZA RISPOSTA ({len(senza_risposta)}) ---")
    
    for contatto in senza_risposta:
        campagna = contatto.get('Campagna', 'N/A')
        strategia = contatto.get('Strategia', 'N/A')
        print(f"{contatto['ID Messaggio']} - {contatto['Nome Salone']} ({campagna})")

def mostra_contatti_con_risposta():
    """Mostra contatti che hanno risposto"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        contatti = crea_tracker_unificato()
    
    con_risposta = [c for c in contatti if c.get('Risposta')]
    
    print(f"\n--- CONTATTI CON RISPOSTA ({len(con_risposta)}) ---")
    
    for contatto in con_risposta:
        campagna = contatto.get('Campagna', 'N/A')
        print(f"{contatto['ID Messaggio']} - {contatto['Nome Salone']} - {contatto['Risposta']} ({campagna})")

def crea_follow_up_rifiutati():
    """Crea follow-up per contatti che hanno rifiutato"""
    contatti = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
    except:
        contatti = crea_tracker_unificato()
    
    # Filtra contatti target per follow-up
    contatti_target = []
    for contatto in contatti:
        risposta = contatto.get('Risposta', '')
        if risposta in ['Negativo', 'Chiuso oggi', 'Automatico']:
            contatti_target.append(contatto)
    
    if not contatti_target:
        print("Nessun contatto target per follow-up.")
        return
    
    print(f"\n--- FOLLOW-UP PER RIFIUTATI ({len(contatti_target)} contatti) ---")
    
    with open('follow_up_unificati.txt', 'w', encoding='utf-8') as f:
        f.write(f"FOLLOW-UP UNIFICATI - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("Nailstech - Divisione Quadro srls\n")
        f.write("=" * 60 + "\n\n")
        
        for contatto in contatti_target:
            nome = contatto['Nome Salone']
            cellulare = contatto['Cellulare']
            motivazione = contatto.get('Note', contatto['Risposta'])
            
            # Crea messaggio follow-up personalizzato
            if "chiuso" in motivazione.lower():
                messaggio = f"""Salve {nome}, capisco che oggi siete chiusi. Posso ricontattarla domani o martedì? Le stampanti per nail art possono aumentare i suoi clienti e profitti in modo significativo. Quando preferisce che la richiami?"""
            elif "automatico" in motivazione.lower():
                messaggio = f"""Salve {nome}, ho visto la sua risposta automatica. Sono Salvatore di Nailstech, le offro stampanti per nail art in noleggio a 100€/giorno. Posso aumentare i suoi clienti con design unici. Le interesa scoprire come funziona?"""
            else:
                messaggio = f"""Capisco {nome}. Prima di decidere definitivamente, le chiedo: sa che molte centri estetici come il suo aumentano i profitti del 30% con nail art personalizzate? Non le costa nulla vedere qualche esempio. Posso inviarle 2 foto di lavori realizzati da centri come il suo?"""
            
            link = genera_link_whatsapp(cellulare, messaggio)
            
            f.write(f"FOLLOW-UP - {contatto['ID Messaggio']} - {nome}\n")
            f.write(f"📞 {cellulare}\n")
            f.write(f"🎯 Campagna: {contatto.get('Campagna', 'N/A')}\n")
            f.write(f"💬 {messaggio}\n")
            f.write(f"🌐 {link}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"✅ Creato file 'follow_up_unificati.txt' con {len(contatti_target)} follow-up")

def genera_link_whatsapp(telefono, messaggio):
    """Genera link WhatsApp Web"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

if __name__ == "__main__":
    # Inizializza tracker unificato se non esiste
    crea_tracker_unificato()
    menu_interattivo()
