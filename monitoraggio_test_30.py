#!/usr/bin/env python3
"""
Monitoraggio Test Primi 30 Messaggi
Sistema per analizzare risposte e decidere A/B testing
"""

import csv
from datetime import datetime

def analizza_risposte():
    """Analizza le risposte dei primi 30 messaggi"""
    
    print("=" * 60)
    print("MONITORAGGIO TEST PRIMI 30 MESSAGGI")
    print("Nailstech - Divisione Quadro srls")
    print("Analisi risposte per decisione A/B testing")
    print("=" * 60)
    
    # Carica tracker
    try:
        with open('tracker_campagna_corretta.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        print(f"✓ Caricato tracker con {len(contatti)} contatti")
    except FileNotFoundError:
        print("❌ Tracker non trovato. Usa 'tracker_campagna_corretta.csv'")
        return
    
    # Filtra solo i primi 30 (FIX001-FIX030)
    primi_30 = [c for c in contatti if c['ID Messaggio'].startswith('FIX')]
    print(f"✓ Primi 30 contatti identificati")
    
    # Statistiche attuali
    totali = len(primi_30)
    risposte = len([c for c in primi_30 if c['Risposta'].strip()])
    positivi = len([c for c in primi_30 if c['Risposta'].strip() and c['Tipo Risposta'].strip() == 'POSITIVO'])
    negativi = len([c for c in primi_30 if c['Risposta'].strip() and c['Tipo Risposta'].strip() == 'NEGATIVO'])
    attesa = totali - risposte
    
    tasso_risposta = (risposte / totali) * 100 if totali > 0 else 0
    tasso_positivi = (positivi / totali) * 100 if totali > 0 else 0
    
    print(f"\n📊 STATISTICHE ATTUALI:")
    print(f"   📤 Messaggi inviati: {totali}")
    print(f"   ✅ Risposte ricevute: {risposte}")
    print(f"   👍 Risposte positive: {positivi}")
    print(f"   👎 Risposte negative: {negativi}")
    print(f"   ⏳ In attesa: {attesa}")
    print(f"\n📈 TASSI:")
    print(f"   🎯 Tasso risposta: {tasso_risposta:.1f}%")
    print(f"   💚 Tasso positivi: {tasso_positivi:.1f}%")
    
    # Analisi e raccomandazioni
    print(f"\n🎯 ANALISI E RACCOMANDAZIONI:")
    
    if risposte == 0:
        print(f"   ⚠️  NESSUNA RISPOSTA ANCORA")
        print(f"   💡 Aspetta almeno 24 ore prima di decidere")
        print(f"   📅 Prossimo check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
    elif tasso_risposta < 30:
        print(f"   ❌ TASSO RISPOSTA BASSO (<30%)")
        print(f"   💡 Raccomandazione: A/B testing OBBLIGATORIO")
        print(f"   🔧 Testare approcci completamente diversi")
        
    elif tasso_risposta < 60:
        print(f"   ⚠️  TASSO RISPOSTA MEDIO (30-60%)")
        print(f"   💡 Raccomandazione: A/B testing CONSIGLIATO")
        print(f"   🔧 Ottimizzare messaggio attuale")
        
    elif tasso_risposta < 90:
        print(f"   🟡 TASSO RISPOSTA BUONO (60-90%)")
        print(f"   💡 Raccomandazione: A/B testing OPZIONALE")
        print(f"   🔧 Piccoli miglioramenti possibili")
        
    else:
        print(f"   ✅ TASSO RISPOSTA ECCELLENTE (>90%)")
        print(f"   💡 Raccomandazione: PROSEGUIRE con stesso approccio")
        print(f"   🚀 Invia gli altri 98 messaggi")
    
    # Dettaglio risposte
    if risposte > 0:
        print(f"\n📋 DETTAGLIO RISPOSTE:")
        con_risposta = [c for c in primi_30 if c['Risposta'].strip()]
        for c in con_risposta:
            print(f"   {c['ID Messaggio']}: {c['Nome Salone']} - {c['Tipo Risposta']}")
    
    # Salva report
    with open('report_monitoraggio_30.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Data Analisi', 'Messaggi Inviati', 'Risposte Ricevute', 'Risposte Positive', 'Risposte Negative', 'Tasso Risposta %', 'Tasso Positivi %'])
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M'), totali, risposte, positivi, negativi, round(tasso_risposta, 1), round(tasso_positivi, 1)])
    print(f"\n📄 Report salvato: 'report_monitoraggio_30.csv'")
    
    return {
        'totali': totali,
        'risposte': risposte,
        'tasso_risposta': tasso_risposta,
        'raccomandazione': get_raccomandazione(tasso_risposta)
    }

def get_raccomandazione(tasso_risposta):
    """Restituisce raccomandazione basata sul tasso risposta"""
    if tasso_risposta == 0:
        return "ATTENDERE 24 ORE"
    elif tasso_risposta < 30:
        return "A/B TESTING OBBLIGATORIO"
    elif tasso_risposta < 60:
        return "A/B TESTING CONSIGLIATO"
    elif tasso_risposta < 90:
        return "A/B TESTING OPZIONALE"
    else:
        return "PROSEGUIRE STESSO APPROCCIO"

def aggiorna_risposta(id_messaggio, tipo_risposta, note=""):
    """Aggiorna una risposta nel tracker"""
    try:
        # Leggi tutti i contatti
        with open('tracker_campagna_corretta.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti = list(reader)
        
        # Trova e aggiorna la riga del messaggio
        aggiornato = False
        for contatto in contatti:
            if contatto['ID Messaggio'] == id_messaggio:
                contatto['Risposta'] = 'SÌ'
                contatto['Data Risposta'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                contatto['Tipo Risposta'] = tipo_risposta.upper()
                contatto['Note'] = note
                aggiornato = True
                break
        
        if aggiornato:
            # Riscrivi il file
            with open('tracker_campagna_corretta.csv', 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=contatti[0].keys())
                writer.writeheader()
                writer.writerows(contatti)
            print(f"✅ Aggiornato {id_messaggio}: {tipo_risposta}")
        else:
            print(f"❌ Messaggio {id_messaggio} non trovato")
            
    except Exception as e:
        print(f"❌ Errore aggiornamento: {e}")

def menu_interattivo():
    """Menu per aggiornare risposte manualmente"""
    
    while True:
        print(f"\n" + "=" * 40)
        print(f"📝 MENU AGGIORNAMENTO RISPOSTE")
        print(f"1. Aggiorna risposta")
        print(f"2. Analizza attuale")
        print(f"3. Esci")
        print("=" * 40)
        
        scelta = input("Scelta (1-3): ").strip()
        
        if scelta == "1":
            id_msg = input("ID Messaggio (es. FIX001): ").strip().upper()
            print("Tipo risposta: P=Positivo, N=Negativo, I=Interessato")
            tipo = input("Tipo (P/N/I): ").strip().upper()
            
            tipo_map = {'P': 'POSITIVO', 'N': 'NEGATIVO', 'I': 'INTERESSATO'}
            tipo_full = tipo_map.get(tipo, 'ALTRO')
            
            note = input("Note (opzionale): ").strip()
            aggiorna_risposta(id_msg, tipo_full, note)
            
        elif scelta == "2":
            analizza_risposte()
            
        elif scelta == "3":
            break
            
        else:
            print("❌ Scelta non valida")

if __name__ == "__main__":
    # Analizza situazione attuale
    risultato = analizza_risposte()
    
    # Chiedi se vuole aggiornare risposte
    if risultato['totali'] > 0:
        print(f"\n📝 Vuoi aggiornare le risposte manualmente? (s/n)")
        scelta = input().strip().lower()
        if scelta == 's':
            menu_interattivo()
