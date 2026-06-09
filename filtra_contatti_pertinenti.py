#!/usr/bin/env python3
"""
Filtra contatti pertinenti per nail art
Rimuove professioni non correlate (medici, farmacie, etc.)
"""

import json
from datetime import datetime

def filtra_contatti():
    """Filtra solo contatti pertinenti per centri estetici"""
    
    print("=" * 60)
    print("FILTRA CONTATTI PERTINENTI PER NAIL ART")
    print("Nailstech - Divisione Quadro srls")
    print("Rimozione contatti non correlati")
    print("=" * 60)
    
    # Carica contatti originali
    with open('contatti_catania.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    contatti_originali = data.get('contatti', [])
    print(f"✓ Caricati {len(contatti_originali)} contatti originali")
    
    # Parole chiave da escludere
    parole_escludere = [
        'farmacia', 'medico', 'dott\.ss', 'dott\.', 'dottoressa', 'logopedista',
        'fisioterapista', 'psicologo', 'dentista', 'oculista', 'ospedale',
        'clinica', 'laboratorio', 'radiologia', 'analisi', 'pediatra',
        'ginecologo', 'cardiologo', 'dermatologo', 'chirurgo',
        'veterinario', 'ottica', 'audiologia', 'nutrizionista'
    ]
    
    # Filtra contatti
    contatti_filtrati = []
    contatti_esclusi = []
    
    for contatto in contatti_originali:
        nome = contatto.get('nome_salone', '').lower()
        categoria = contatto.get('categoria', '').lower()
        
        # Controlla se contiene parole da escludere
        da_escludere = False
        for parola in parole_escludere:
            if parola.lower() in nome or parola.lower() in categoria:
                da_escludere = True
                break
        
        if da_escludere:
            contatti_esclusi.append(contatto)
        else:
            contatti_filtrati.append(contatto)
    
    print(f"\n📊 RISULTATI FILTRAGGIO:")
    print(f"   ❌ Contatti esclusi: {len(contatti_esclusi)}")
    print(f"   ✅ Contatti pertinenti: {len(contatti_filtrati)}")
    
    # Mostra contatti esclusi
    if contatti_esclusi:
        print(f"\n❌ CONTATTI ESCLUSI:")
        for contatto in contatti_esclusi:
            print(f"   - {contatto['nome_salone']} ({contatto.get('categoria', 'N/A')})")
    
    # Filtra per rating >= 4.0
    contatti_rating = []
    for contatto in contatti_filtrati:
        rating = float(contatto.get('rating') or 0)
        if rating >= 4.0:
            contatti_rating.append(contatto)
    
    print(f"\n⭐ FILTRAGGIO RATING ≥ 4.0:")
    print(f"   📤 Contatti pertinenti totali: {len(contatti_filtrati)}")
    print(f"   ⭐ Con rating ≥ 4.0: {len(contatti_rating)}")
    
    # Crea nuovo file filtrato
    nuovo_data = {
        "metadata": {
            "data_generazione": datetime.now().isoformat(),
            "totale_contatti": len(contatti_filtrati),
            "contatti_rating_4": len(contatti_rating),
            "area": "Catania e dintorni (40km)",
            "servizio_target": "noleggio stampante unghie",
            "fonti": data.get('metadata', {}).get('fonti', []),
            "filtraggio": "rimossi contatti medici/farmacie"
        },
        "contatti": contatti_filtrati
    }
    
    # Salva file filtrato
    with open('contatti_catania_filtrati.json', 'w', encoding='utf-8') as f:
        json.dump(nuovo_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Creato file: 'contatti_catania_filtrati.json'")
    print(f"📋 Pronto per A/B test con {len(contatti_rating)} contatti rating ≥ 4.0")
    
    return contatti_rating

if __name__ == "__main__":
    filtra_contatti()
