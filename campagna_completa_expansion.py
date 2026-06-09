#!/usr/bin/env python3
"""
Campagna Completa Expansion - Tutti i Contatti Pertinenti
Espande a tutti i contatti filtrati non ancora contattati
"""

import json
import csv
import urllib.parse
from datetime import datetime

def carica_contatti_filtrati():
    """Carica contatti filtrati con rating >= 4.0"""
    contatti = []
    try:
        with open('contatti_catania_filtrati.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for contatto in data.get('contatti', []):
                if contatto.get('cellulare'):
                    rating = float(contatto.get('rating') or 0)
                    if rating >= 4.0:
                        contatti.append(contatto)
        return contatti
    except Exception as e:
        print(f"Errore caricamento contatti filtrati: {e}")
        return []

def carica_contatti_gia_contattati():
    """Carica tutti i contatti già contattati (primi 30 + A/B test)"""
    contatti_gia_contattati = []
    
    # Carica tracker unificato se esiste
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti_gia_contattati = list(reader)
    except:
        # Se non esiste, prova con i singoli tracker
        try:
            # Primi 30
            with open('tracker_campagna_corretta.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                contatti_gia_contattati.extend(list(reader))
        except:
            pass
        
        try:
            # A/B test
            with open('tracker_ab_test.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                contatti_gia_contattati.extend(list(reader))
        except:
            pass
    
    return contatti_gia_contattati

def identifica_contatti_da_contattare():
    """Identifica contatti non ancora contattati"""
    tutti_contatti = carica_contatti_filtrati()
    gia_contattati = carica_contatti_gia_contattati()
    
    # Crea set di telefoni già contattati
    telefoni_contattati = set()
    for contatto in gia_contattati:
        telefono = contatto.get('Cellulare', contatto.get('cellulare', ''))
        if telefono:
            telefoni_contattati.add(telefono)
    
    # Filtra contatti non ancora contattati
    contatti_da_contattare = []
    for contatto in tutti_contatti:
        telefono = contatto.get('cellulare', '')
        if telefono and telefono not in telefoni_contattati:
            contatti_da_contattare.append(contatto)
    
    return contatti_da_contattare

def crea_campagna_completa():
    """Crea campagna completa per tutti i contatti rimanenti"""
    
    print("=" * 60)
    print("CAMPAGNA COMPLETA EXPANSION")
    print("Nailstech - Divisione Quadro srls")
    print("Tutti i contatti pertinenti non ancora contattati")
    print("=" * 60)
    
    tutti_contatti = carica_contatti_filtrati()
    gia_contattati = carica_contatti_gia_contattati()
    contatti_da_contattare = identifica_contatti_da_contattare()
    
    print(f"📊 SITUAZIONE ATTUALE:")
    print(f"   📋 Contatti filtrati totali: {len(tutti_contatti)}")
    print(f"   ✅ Già contattati: {len(gia_contattati)}")
    print(f"   🆕 Da contattare: {len(contatti_da_contattare)}")
    
    if not contatti_da_contattare:
        print("\n✅ Tutti i contatti pertinenti sono già stati contattati!")
        return
    
    # Usa la strategia migliore dall'A/B test (per ora Strategia A - Valore e Contesto)
    strategia_vincente = """Salve {nome_salone}, sono Salvatore di Nailstech. Ho notato il suo centro e penso che una stampante per nail art potrebbe aumentare i suoi clienti. A 100€/giorno le permette di offrire design unici che i concorrenti non hanno. Le interessa scoprire come funziona?"""
    
    print(f"\n📱 STRATEGIA SELEZIONATA:")
    print(f"   Valore e Contesto (basata su A/B test)")
    print(f"   Prezzo: 100€/giorno")
    
    # Genera ID progressivi
    ultimo_id = 0
    if gia_contattati:
        for contatto in gia_contattati:
            id_messaggio = contatto.get('ID Messaggio', '')
            if id_messaggio.startswith('EXP'):
                try:
                    num = int(id_messaggio[3:])
                    if num > ultimo_id:
                        ultimo_id = num
                except:
                    pass
    
    # Crea tracker e link
    tracker_data = []
    links_data = []
    
    print(f"\n🔄 GENERAZIONE LINK E TRACKER...")
    
    for i, contatto in enumerate(contatti_da_contattare):
        ultimo_id += 1
        id_messaggio = f"EXP{ultimo_id:03d}"
        
        nome_salone = contatto['nome_salone']
        cellulare = contatto['cellulare']
        rating = contatto['rating']
        
        # Personalizza messaggio
        messaggio = strategia_vincente.format(nome_salone=nome_salone)
        
        # Genera link WhatsApp
        cellulare_pulito = cellulare.replace("+39", "")
        messaggio_encoded = urllib.parse.quote(messaggio, safe='')
        link_whatsapp = f"https://wa.me/39{cellulare_pulito}?text={messaggio_encoded}"
        
        # Aggiungi al tracker
        tracker_data.append({
            'ID Messaggio': id_messaggio,
            'Nome Salone': nome_salone,
            'Cellulare': cellulare,
            'Rating': rating,
            'Campagna': 'Expansion Completa',
            'Strategia': 'Valore e Contesto',
            'Data Invio': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Risposta': '',
            'Data Risposta': '',
            'Tipo Risposta': '',
            'Note': ''
        })
        
        # Aggiungi ai links
        links_data.append({
            'id': id_messaggio,
            'nome': nome_salone,
            'cellulare': cellulare,
            'rating': rating,
            'link': link_whatsapp
        })
        
        if (i + 1) % 10 == 0:
            print(f"   Processati {i + 1}/{len(contatti_da_contattare)} contatti...")
    
    # Salva tracker
    with open('tracker_expansion.csv', 'w', encoding='utf-8-sig', newline='') as f:
        if tracker_data:
            writer = csv.DictWriter(f, fieldnames=tracker_data[0].keys())
            writer.writeheader()
            writer.writerows(tracker_data)
    
    # Salva links
    with open('expansion_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"CAMPAGNA EXPANSION COMPLETA\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"={len(links_data)} contatti - Strategia Valore e Contesto\n")
        f.write(f"=" * 60 + "\n\n")
        
        for i, link_data in enumerate(links_data, 1):
            f.write(f"{i}. {link_data['nome']}\n")
            f.write(f"   📞 {link_data['cellulare']}\n")
            f.write(f"   ⭐ Rating: {link_data['rating']}\n")
            f.write(f"   🆔 ID: {link_data['id']}\n")
            f.write(f"   🌐 {link_data['link']}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"\n✅ CAMPAGNA COMPLETA CREATA!")
    print(f"   📋 Tracker: 'tracker_expansion.csv'")
    print(f"   🔗 Links: 'expansion_links.txt'")
    print(f"   📊 Contatti: {len(links_data)}")
    print(f"   🎯 Pronti per l'invio!")
    
    return links_data

def aggiorna_tracker_unificato_con_expansion():
    """Aggiorna tracker unificato includendo expansion"""
    
    # Carica tracker unificato esistente
    contatti_unificati = []
    try:
        with open('tracker_unificato.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            contatti_unificati = list(reader)
    except:
        # Se non esiste, crealo
        from tracking_unificato_risposte import crea_tracker_unificato
        contatti_unificati = crea_tracker_unificato()
    
    # Carica expansion
    expansion_contatti = []
    try:
        with open('tracker_expansion.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            expansion_contatti = list(reader)
    except:
        print("Nessuna campagna expansion trovata.")
        return
    
    # Aggiungi expansion al tracker unificato
    contatti_unificati.extend(expansion_contatti)
    
    # Salva tracker unificato aggiornato
    with open('tracker_unificato.csv', 'w', encoding='utf-8-sig', newline='') as f:
        if contatti_unificati:
            writer = csv.DictWriter(f, fieldnames=contatti_unificati[0].keys())
            writer.writeheader()
            writer.writerows(contatti_unificati)
    
    print(f"✅ Tracker unificato aggiornato con {len(expansion_contatti)} contatti expansion")

def mostra_situazione_completa():
    """Mostra situazione completa di tutte le campagne"""
    
    print("\n" + "=" * 60)
    print("SITUAZIONE COMPLETA CAMPAGNE")
    print("Nailstech - Divisione Quadro srls")
    print("=" * 60)
    
    # Carica tutti i dati
    tutti_filtrati = carica_contatti_filtrati()
    gia_contattati = carica_contatti_gia_contattati()
    da_contattare = identifica_contatti_da_contattare()
    
    # Statistiche campagne esistenti
    iniziale = len([c for c in gia_contattati if c.get('Campagna') == 'Iniziale'])
    ab_test = len([c for c in gia_contattati if c.get('Campagna') == 'A/B Test'])
    expansion = len([c for c in gia_contattati if c.get('Campagna') == 'Expansion Completa'])
    
    print(f"\n📊 DATABASE COMPLETO:")
    print(f"   📋 Contatti filtrati totali: {len(tutti_filtrati)}")
    print(f"   ✅ Già contattati: {len(gia_contattati)}")
    print(f"   🆕 Da contattare: {len(da_contattare)}")
    print(f"   📈 Copertura: {len(gia_contattati)/len(tutti_filtrati)*100:.1f}%")
    
    print(f"\n🎯 PER CAMPAGNA:")
    print(f"   🚀 Campagna Iniziale: {iniziale} contatti")
    print(f"   🧪 A/B Test: {ab_test} contatti")
    print(f"   📈 Expansion: {expansion} contatti")
    print(f"   ⏳ Rimanenti: {len(da_contattare)} contatti")
    
    if da_contattare:
        print(f"\n📋 CONTATTI RIMANENTI (Top 10):")
        for i, contatto in enumerate(da_contattare[:10], 1):
            print(f"   {i}. {contatto['nome_salone']} (⭐ {contatto['rating']})")
        
        if len(da_contattare) > 10:
            print(f"   ... e altri {len(da_contattare) - 10} contatti")

if __name__ == "__main__":
    print("CAMPAGNA COMPLETA EXPANSION")
    print("1. Mostra situazione attuale")
    print("2. Crea campagna expansion")
    print("3. Aggiorna tracker unificato")
    print("4. Tutti")
    
    scelta = input("\nScelta (1-4): ").strip()
    
    if scelta == "1":
        mostra_situazione_completa()
    elif scelta == "2":
        crea_campagna_completa()
    elif scelta == "3":
        aggiorna_tracker_unificato_con_expansion()
    elif scelta == "4":
        mostra_situazione_completa()
        crea_campagna_completa()
        aggiorna_tracker_unificato_con_expansion()
    else:
        print("Scelta non valida.")
