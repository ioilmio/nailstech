#!/usr/bin/env python3
"""
A/B Testing - Strategie Completamente Diverse
Test su 20 contatti per trovare l'approccio migliore
"""

import json
import csv
from datetime import datetime
import urllib.parse

def carica_contatti():
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
        print(f"Errore: {e}")
        return []

def genera_link_whatsapp(telefono, messaggio):
    """Genera link WhatsApp Web"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def main():
    print("=" * 60)
    print("A/B TESTING - STRATEGIE COMPLETAMENTE DIVERSE")
    print("Nailstech - Divisione Quadro srls")
    print("Salvatore +393515035361")
    print("Test su 20 contatti (10 per strategia)")
    print("=" * 60)
    
    # Carica contatti
    contatti = carica_contatti()
    print(f"✓ Caricati {len(contatti)} contatti con rating ≥ 4.0")
    
    # Salta i primi 30 (già testati)
    contatti_test = contatti[30:50]  # 20 contatti per A/B test
    print(f"✓ Selezionati {len(contatti_test)} contatti per A/B test")
    
    # STRATEGIA A: Valore e Contesto
    strategia_a = """Salve {nome_salone}, sono Salvatore di Nailstech. Ho notato il suo centro e penso che una stampante per nail art potrebbe aumentare i suoi clienti. A 100€/giorno le permette di offrire design unici che i concorrenti non hanno. Le interessa scoprire come funziona?"""
    
    # STRATEGIA B: Curiosità e Benefici
    strategia_b = """Salve {nome_salone}, sono Salvatore di Nailstech. Offro stampanti per nail art in noleggio che creano design complessi in 2 minuti. Le interessa scoprire come aumentare i profitti del suo centro con questa tecnologia?"""
    
    # STRATEGIA C: Efficienza e Profitto
    strategia_c = """Salve {nome_salone}, sono Salvatore di Nailstech. Quanto tempo impiega il suo staff per creare nail art complesse? Con le nostre stampanti riduce i tempi del 70% e aumenta i profitti del centro. Vuoi scoprire come trasformare il suo business?"""
    
    print(f"\n📱 STRATEGIE DI TEST:")
    print(f"   A: Valore e contesto (100€/giorno + vantaggi)")
    print(f"   B: Curiosità e benefici (2 minuti design)")
    print(f"   C: Efficienza e profitto (70% tempo + profitti)")
    
    # Dividi contatti per strategie
    gruppo_a = contatti_test[:7]   # 7 contatti
    gruppo_b = contatti_test[7:14] # 7 contatti  
    gruppo_c = contatti_test[14:20]# 6 contatti
    
    print(f"\n📊 DISTRIBUZIONE:")
    print(f"   Strategia A: {len(gruppo_a)} contatti")
    print(f"   Strategia B: {len(gruppo_b)} contatti")
    print(f"   Strategia C: {len(gruppo_c)} contatti")
    print("-" * 60)
    
    # Genera file A/B test
    with open('ab_test_strategie_links.txt', 'w', encoding='utf-8') as f:
        f.write(f"A/B TESTING - STRATEGIE COMPLETAMENTE DIVERSE\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Nailstech - Divisione Quadro srls\n")
        f.write(f"Salvatore +393515035361\n")
        f.write(f"Test: 20 contatti, 3 strategie diverse\n")
        f.write("=" * 60 + "\n\n")
        
        # Strategia A
        f.write("🔥 STRATEGIA A - DIRETTA CON PREZZO\n")
        f.write("-" * 40 + "\n")
        for i, contatto in enumerate(gruppo_a, 1):
            messaggio = strategia_a.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\nA{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            
            f.write(f"A{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: TESTA{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
        
        # Strategia B
        f.write("🎯 STRATEGIA B - DOMANDA APERTA\n")
        f.write("-" * 40 + "\n")
        for i, contatto in enumerate(gruppo_b, 1):
            messaggio = strategia_b.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\nB{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            
            f.write(f"B{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: TESTB{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
        
        # Strategia C
        f.write("💡 STRATEGIA C - PROBLEMA-SOLUZIONE\n")
        f.write("-" * 40 + "\n")
        for i, contatto in enumerate(gruppo_c, 1):
            messaggio = strategia_c.format(nome_salone=contatto['nome_salone'])
            link = genera_link_whatsapp(contatto['cellulare'], messaggio)
            
            print(f"\nC{i}. {contatto['nome_salone']}")
            print(f"   📞 {contatto['cellulare']}")
            print(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}")
            
            f.write(f"C{i}. {contatto['nome_salone']}\n")
            f.write(f"   📞 {contatto['cellulare']}\n")
            f.write(f"   ⭐ Rating: {contatto.get('rating', 'N/A')}\n")
            f.write(f"   🆔 ID: TESTC{i:03d}\n")
            f.write(f"   🌐 {link}\n")
            f.write("-" * 40 + "\n\n")
    
    # Genera tracker A/B test
    with open('tracker_ab_test.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID Messaggio', 'Nome Salone', 'Cellulare', 'Rating', 'Strategia', 'Data Invio', 'Risposta', 'Data Risposta', 'Tipo Risposta', 'Note'])
        
        # Strategia A
        for i, contatto in enumerate(gruppo_a, 1):
            writer.writerow([f'TESTA{i:03d}', contatto['nome_salone'], contatto['cellulare'], contatto.get('rating', ''), 'A - Diretta Prezzo', datetime.now().strftime('%Y-%m-%d %H:%M'), '', '', '', ''])
        
        # Strategia B
        for i, contatto in enumerate(gruppo_b, 1):
            writer.writerow([f'TESTB{i:03d}', contatto['nome_salone'], contatto['cellulare'], contatto.get('rating', ''), 'B - Domanda Aperta', datetime.now().strftime('%Y-%m-%d %H:%M'), '', '', '', ''])
        
        # Strategia C
        for i, contatto in enumerate(gruppo_c, 1):
            writer.writerow([f'TESTC{i:03d}', contatto['nome_salone'], contatto['cellulare'], contatto.get('rating', ''), 'C - Problema Soluzione', datetime.now().strftime('%Y-%m-%d %H:%M'), '', '', '', ''])
    
    print(f"\n✓ Creato file 'ab_test_strategie_links.txt' con 20 link")
    print(f"📊 ID tracking: TESTA001-TESTA007, TESTB001-TESTB007, TESTC001-TESTC006")
    print(f"📋 Creato tracker: 'tracker_ab_test.csv'")
    print(f"\n🚀 A/B TEST PRONTO!")
    print(f"💡 Testa le 3 strategie e confronta i risultati")

if __name__ == "__main__":
    main()
