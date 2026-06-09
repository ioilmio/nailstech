#!/usr/bin/env python3
"""
Gestione Risposte A/B Test e Follow-up
Permette di registrare risposte e creare messaggi di follow-up personalizzati
"""

import csv
import json
import urllib.parse
from datetime import datetime

def carica_tracker():
    """Carica il tracker A/B test"""
    contatti = []
    try:
        with open('tracker_ab_test.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        return contatti
    except Exception as e:
        print(f"Errore caricamento tracker: {e}")
        return []

def aggiorna_risposta(id_messaggio, risposta, note=""):
    """Aggiorna la risposta nel tracker"""
    contatti = carica_tracker()
    
    for contatto in contatti:
        if contatto['ID Messaggio'] == id_messaggio:
            contatto['Risposta'] = risposta
            contatto['Data Risposta'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            contatto['Note'] = note
            break
    
    # Salva tracker aggiornato
    with open('tracker_ab_test.csv', 'w', encoding='utf-8-sig', newline='') as f:
        if contatti:
            writer = csv.DictWriter(f, fieldnames=contatti[0].keys())
            writer.writeheader()
            writer.writerows(contatti)
    
    print(f"✅ Aggiornato {id_messaggio}: {risposta}")

def crea_follow_up_rifiutato(nome_salone, cellulare, motivazione=""):
    """Crea messaggio di follow-up per chi ha rifiutato"""
    
    if "chiuso" in motivazione.lower():
        # Se è chiuso oggi
        messaggio = f"""Salve {nome_salone}, capisco che oggi siete chiusi. Posso ricontattarla domani o martedì? Le stampanti per nail art possono aumentare i suoi clienti e profitti in modo significativo. Quando preferisce che la richiami?"""
    
    elif "non interessato" in motivazione.lower() or "no grazie" in motivazione.lower():
        # Follow-up per chi ha rifiutato
        messaggio = f"""Capisco {nome_salone}. Prima di decidere definitivamente, le chiedo: sa che molte centri estetici come il suo aumentano i profitti del 30% con nail art personalizzate? Non le costa nulla vedere qualche esempio. Posso inviarle 2 foto di lavori realizzati da centri come il suo?"""
    
    elif "automatico" in motivazione.lower() or "bot" in motivazione.lower():
        # Risposta automatica
        messaggio = f"""Salve {nome_salone}, ho visto la sua risposta automatica. Sono Salvatore di Nailstech, le offro stampanti per nail art in noleggio a 100€/giorno. Posso aumentare i suoi clienti con design unici che i concorrenti non hanno. Le interessa scoprire come funziona?"""
    
    else:
        # Follow-up generico
        messaggio = f"""Salve {nome_salone}, sono Salvatore di Nailstech. Capisco la sua posizione. Le chiedo solo 2 minuti per mostrarle come le nostre stampanti possono trasformare il suo business. Molti centri come il suo sono partiti scettici e ora non possono più farne a meno. Vuoi vedere qualche esempio?"""
    
    return messaggio

def genera_link_follow_up(nome_salone, cellulare, messaggio):
    """Genera link WhatsApp per follow-up"""
    cellulare_pulito = cellulare.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{cellulare_pulito}?text={messaggio_encoded}"

def menu_principale():
    """Menu interattivo per gestione risposte"""
    
    while True:
        print("\n" + "=" * 60)
        print("GESTIONE RISPOSTE A/B TEST")
        print("Nailstech - Divisione Quadro srls")
        print("=" * 60)
        print("1. Aggiorna risposta")
        print("2. Crea follow-up per rifiutati")
        print("3. Mostra statistiche attuali")
        print("4. Esci")
        
        scelta = input("\nScelta (1-4): ").strip()
        
        if scelta == "1":
            aggiungi_risposta_interattiva()
        elif scelta == "2":
            crea_follow_up_interattivo()
        elif scelta == "3":
            mostra_statistiche()
        elif scelta == "4":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")

def aggiungi_risposta_interattiva():
    """Interfaccia per aggiungere risposte"""
    contatti = carica_tracker()
    
    print("\n--- AGGIUNGI RISPOSTA ---")
    id_messaggio = input("ID Messaggio (es. TESTA001): ").strip().upper()
    
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
    print(f"Strategia: {contatto_trovato['Strategia']}")
    
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
    
    aggiorna_risposta(id_messaggio, risposta, note)

def crea_follow_up_interattivo():
    """Interfaccia per creare follow-up"""
    contatti = carica_tracker()
    
    print("\n--- CREA FOLLOW-UP ---")
    
    # Mostra solo contatti con risposte negative/chiusi/automatici
    contatti_target = []
    for contatto in contatti:
        if contatto['Risposta'] in ['Negativo', 'Chiuso oggi', 'Automatico']:
            contatti_target.append(contatto)
    
    if not contatti_target:
        print("Nessun contatto target per follow-up.")
        return
    
    print(f"\nTrovati {len(contatti_target)} contatti per follow-up:")
    for i, contatto in enumerate(contatti_target, 1):
        print(f"{i}. {contatto['ID Messaggio']} - {contatto['Nome Salone']} ({contatto['Risposta']})")
    
    scelta = input("\nNumero contatto (0 per tutti): ").strip()
    
    if scelta == "0":
        # Crea follow-up per tutti
        crea_follow_up_multipli(contatti_target)
    else:
        try:
            idx = int(scelta) - 1
            if 0 <= idx < len(contatti_target):
                crea_follow_up_singolo(contatti_target[idx])
            else:
                print("Scelta non valida.")
        except ValueError:
            print("Input non valido.")

def crea_follow_up_singolo(contatto):
    """Crea follow-up per un singolo contatto"""
    print(f"\n--- FOLLOW-UP PER {contatto['Nome Salone']} ---")
    
    motivazione = contatto.get('Note', contatto['Risposta'])
    messaggio = crea_follow_up_rifiutato(contatto['Nome Salone'], contatto['Cellulare'], motivazione)
    link = genera_link_follow_up(contatto['Nome Salone'], contatto['Cellulare'], messaggio)
    
    print(f"\n💬 Messaggio follow-up:")
    print(f"{messaggio}")
    print(f"\n🌐 Link WhatsApp:")
    print(f"{link}")
    
    # Salva su file
    with open('follow_up_links.txt', 'a', encoding='utf-8') as f:
        f.write(f"\nFOLLOW-UP - {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
        f.write(f"📞 {contatto['Cellulare']}\n")
        f.write(f"💬 {messaggio}\n")
        f.write(f"🌐 {link}\n")
        f.write("-" * 60 + "\n")
    
    print(f"\n✅ Salvato in 'follow_up_links.txt'")

def crea_follow_up_multipli(contatti):
    """Crea follow-up per più contatti"""
    print(f"\n--- FOLLOW-UP MULTIPLI ({len(contatti)} contatti) ---")
    
    with open('follow_up_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"FOLLOW-UP MULTIPLI - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("Nailstech - Divisione Quadro srls\n")
        f.write("=" * 60 + "\n\n")
        
        for contatto in contatti:
            motivazione = contatto.get('Note', contatto['Risposta'])
            messaggio = crea_follow_up_rifiutato(contatto['Nome Salone'], contatto['Cellulare'], motivazione)
            link = genera_link_follow_up(contatto['Nome Salone'], contatto['Cellulare'], messaggio)
            
            f.write(f"FOLLOW-UP - {contatto['ID Messaggio']} - {contatto['Nome Salone']}\n")
            f.write(f"📞 {contatto['Cellulare']}\n")
            f.write(f"💬 {messaggio}\n")
            f.write(f"🌐 {link}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"✅ Creato file 'follow_up_links.txt' con {len(contatti)} follow-up")

def mostra_statistiche():
    """Mostra statistiche attuali"""
    contatti = carica_tracker()
    
    totali = len(contatti)
    risposte = len([c for c in contatti if c['Risposta']])
    positivi = len([c for c in contatti if 'Positivo' in c['Risposta']])
    negativi = len([c for c in contatti if 'Negativo' in c['Risposta']])
    chiusi = len([c for c in contatti if 'Chiuso' in c['Risposta']])
    automatici = len([c for c in contatti if 'Automatico' in c['Risposta']])
    
    print(f"\n📊 STATISTICHE A/B TEST:")
    print(f"   📤 Messaggi inviati: {totali}")
    print(f"   ✅ Risposte ricevute: {risposte} ({risposte/totali*100:.1f}%)")
    print(f"   👍 Risposte positive: {positivi}")
    print(f"   👎 Risposte negative: {negativi}")
    print(f"   🏢 Chiusi oggi: {chiusi}")
    print(f"   🤖 Risposte automatiche: {automatici}")
    print(f"   ⏳ In attesa: {totali - risposte}")
    
    # Statistiche per strategia
    print(f"\n📈 PER STRATEGIA:")
    for strategia in ['A - Valore e contesto', 'B - Curiosità e benefici', 'C - Efficienza e profitto']:
        contatti_strategia = [c for c in contatti if c['Strategia'] == strategia]
        risposte_strategia = len([c for c in contatti_strategia if c['Risposta']])
        if contatti_strategia:
            tasso = risposte_strategia / len(contatti_strategia) * 100
            print(f"   {strategia}: {risposte_strategia}/{len(contatti_strategia)} ({tasso:.1f}%)")

if __name__ == "__main__":
    menu_principale()
