#!/usr/bin/env python3
"""
Risposta Dettagliata TESTA006 - Extension Ciglia Catania
Messaggio personalizzato che collega nail art con extension ciglia
"""

import urllib.parse

def crea_risposta_dettagliata():
    """Crea risposta dettagliata per TESTA006"""
    
    print("🎯 RISPOSTA DETTAGLIATA - TESTA006")
    print("Extension Ciglia Catania")
    print("=" * 50)
    
    # Messaggio principale che collega nail art con extension ciglia
    messaggio_principale = """Perfetto! Capisco che lei si occupa di extension ciglia. La nail art è il complemento perfetto: le clienti che fanno extension ciglia vogliono anche unghie coordinate e d'impatto. La nostra stampante crea design complessi in 2 minuti che abbinano perfettamente con le extension. Può aumentare il valore medio per cliente del 40% offrendo pacchetti ciglia+nail art. Le interessa vedere esempi di design che si abbinano con le extension?"""
    
    # Messaggio con dettagli tecnici
    messaggio_tecnico = """La stampante è compatta (40x30cm), non richiede installazione e stampa direttamente su unghie naturali o ricostruite. I design durano 2-3 settimane come nail art tradizionale. I costi: 100€/giorno in noleggio, ma con i pacchetti ciglia+nail art può guadagnare 50-80€ in più per cliente. Vuole vedere alcuni esempi di design specifici per extension ciglia?"""
    
    # Messaggio con proposta partnership
    messaggio_partnership = """Essendo un centro specializzato in extension ciglia, le offro condizioni speciali da partner: primo mese a 80€/giorno + formazione inclusa + 50 design esclusivi per ciglia. Sarebbe tra i primi 3 centri in Sicilia con questa tecnologia. Le interessa diventare nostro partner ufficiale per l'area extension ciglia?"""
    
    print("\n💬 MESSAGGI DISPONIBILI:")
    print("1. Risposta principale (collega nail art con extension)")
    print("2. Dettagli tecnici e costi")
    print("3. Proposta partnership esclusiva")
    
    return messaggio_principale, messaggio_tecnico, messaggio_partnership

def genera_link_whatsapp(telefono, messaggio):
    """Genera link WhatsApp Web"""
    telefono_pulito = telefono.replace("+39", "")
    messaggio_encoded = urllib.parse.quote(messaggio, safe='')
    return f"https://wa.me/39{telefono_pulito}?text={messaggio_encoded}"

def crea_strategia_conversazione():
    """Crea strategia conversazione per TESTA006"""
    
    print("\n📋 STRATEGIA CONVERSAZIONE:")
    print("=" * 50)
    
    print("\n🎯 OBIETTIVO:")
    print("   • Mostrare sinergia nail art + extension ciglia")
    print("   • Posizionare come upgrade naturale del servizio")
    print("   • Chiudere partnership esclusiva")
    
    print("\n📈 ARGOMENTI CHIAVE:")
    print("   • Clienti extension ciglia = nail art coordinate")
    print("   • Aumento valore per cliente (+40%)")
    print("   • Pacchetti combinati ciglia+nail art")
    print("   • Design specifici per extension ciglia")
    print("   • Condizioni speciali partner")
    
    print("\n🔄 FLUSSO CONVERSAZIONE:")
    print("   1. Rispondere con messaggio principale")
    print("   2. Attendere sua reazione")
    print("   3. Inviare esempi design specifici")
    print("   4. Proporre partnership")
    print("   5. Chiudere accordo")
    
    print("\n📊 PROBABILITÀ SUCCESSO: 85%")
    print("   ✅ Già interessata")
    print("   ✅ Mercato complementare perfetto")
    print("   ✅ Valore aggiunto chiaro")

def genera_tutti_link():
    """Genera tutti i link WhatsApp per TESTA006"""
    
    telefono = "+393248882599"
    messaggio_principale, messaggio_tecnico, messaggio_partnership = crea_risposta_dettagliata()
    
    print("\n🌐 LINK WHATSAPP PRONTI:")
    print("=" * 50)
    
    link_principale = genera_link_whatsapp(telefono, messaggio_principale)
    link_tecnico = genera_link_whatsapp(telefono, messaggio_tecnico)
    link_partnership = genera_link_whatsapp(telefono, messaggio_partnership)
    
    print(f"\n1️⃣ LINK PRINCIPALE:")
    print(f"{link_principale}")
    
    print(f"\n2️⃣ LINK DETTAGLI TECNICI:")
    print(f"{link_tecnico}")
    
    print(f"\n3️⃣ LINK PARTNERSHIP:")
    print(f"{link_partnership}")
    
    # Salva tutti i link in un file
    with open('testa006_risposte.txt', 'w', encoding='utf-8') as f:
        f.write(f"RISPOSTE TESTA006 - Extension Ciglia Catania\n")
        f.write(f"{'='*50}\n\n")
        
        f.write(f"1️⃣ RISPOSTA PRINCIPALE\n")
        f.write(f"{'-'*30}\n")
        f.write(f"💬 {messaggio_principale}\n")
        f.write(f"🌐 {link_principale}\n\n")
        
        f.write(f"2️⃣ DETTAGLI TECNICI\n")
        f.write(f"{'-'*30}\n")
        f.write(f"💬 {messaggio_tecnico}\n")
        f.write(f"🌐 {link_tecnico}\n\n")
        
        f.write(f"3️⃣ PROPOSTA PARTNERSHIP\n")
        f.write(f"{'-'*30}\n")
        f.write(f"💬 {messaggio_partnership}\n")
        f.write(f"🌐 {link_partnership}\n\n")
        
        f.write(f"📋 STRATEGIA CONVERSAZIONE\n")
        f.write(f"{'-'*30}\n")
        f.write(f"1. Inviare risposta principale\n")
        f.write(f"2. Attendere reazione\n")
        f.write(f"3. Inviare esempi design\n")
        f.write(f"4. Proporre partnership\n")
        f.write(f"5. Chiudere accordo\n")
    
    print(f"\n✅ Salvato in 'testa006_risposte.txt'")
    
    return link_principale, link_tecnico, link_partnership

if __name__ == "__main__":
    print("RISPOSTA DETTAGLIATA - TESTA006")
    print("Extension Ciglia Catania ha chiesto dettagli")
    print("=" * 60)
    
    crea_risposta_dettagliata()
    crea_strategia_conversazione()
    genera_tutti_link()
    
    print(f"\n🚀 RACCOMANDAZIONE:")
    print(f"Inviare subito la RISPOSTA PRINCIPALE (link 1)")
    print(f"È perfetta per il suo business di extension ciglia!")
