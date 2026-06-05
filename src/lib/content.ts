/**
 * Contenuti del sito NailsTech.
 *
 * ───────────────────────────────────────────────────────────────────────────
 *  MODIFICA QUI per aggiornare il sito.
 *  Tutto il testo, i prezzi e i contatti sono in questo unico file così da
 *  poterli cambiare facilmente senza toccare il codice dei componenti.
 * ───────────────────────────────────────────────────────────────────────────
 */

export const business = {
  name: "NailsTech",
  tagline: "Noleggio stampante per unghie professionale",
  intro:
    "Porta la nail art di ultima generazione nel tuo salone, al tuo evento o a casa tua. Noleggia la stampante per unghie Sunwin SW-NA03 e crea decorazioni perfette in pochi secondi, senza acquistare il macchinario.",
  // Recapiti — usati anche per i link cliccabili (tel:, mailto:, WhatsApp)
  phone: "+39 351 503 5361",
  phoneRaw: "+393515035361", // senza spazi, per i link tel: e WhatsApp
  email: "illuminato.salvatore@gmail.com",
  whatsappMessage:
    "Ciao! Vorrei avere informazioni sul noleggio della stampante per unghie NailsTech.",
  // Località mostrata nei contatti (opzionale: lascia "" per nasconderla)
  location: "Italia",
} as const;

export const heroHighlights = [
  "Risultati professionali in pochi secondi",
  "Nessun acquisto: paghi solo il noleggio",
  "Ideale per saloni, eventi e occasioni speciali",
] as const;

export const product = {
  model: "Sunwin SW-NA03",
  heading: "La stampante: Sunwin SW-NA03",
  description:
    "Una stampante per unghie compatta e intuitiva che applica design ad alta definizione direttamente sull'unghia. Perfetta per chi vuole offrire nail art curata e veloce senza esperienza tecnica.",
  features: [
    "Stampa ad alta risoluzione direttamente sull'unghia",
    "Migliaia di design e possibilità di caricare le tue immagini",
    "Semplice da usare tramite app dedicata",
    "Compatta e trasportabile, pronta all'uso in pochi minuti",
    "Consegna pulita, sanificata e pronta all'uso",
  ],
} as const;

export type Plan = {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  featured?: boolean;
  badge?: string;
};

export const plans: Plan[] = [
  {
    name: "Giornaliero",
    price: "120€",
    period: "al giorno",
    description: "Una singola giornata di noleggio. Ideale per provare o per un evento singolo.",
    features: ["Noleggio 1 giorno", "Consegna pronta all'uso", "Assistenza all'avvio"],
  },
  {
    name: "Settimanale ricorrente",
    price: "80€",
    period: "a giornata fissa / settimana",
    description:
      "Una giornata fissa ogni settimana (es. ogni lunedì). La soluzione più conveniente per i saloni.",
    features: [
      "Stesso giorno ogni settimana",
      "Tariffa scontata a giornata",
      "Priorità di prenotazione",
    ],
    featured: true,
    badge: "Più conveniente",
  },
  {
    name: "Settimana intera",
    price: "350€",
    period: "per 7 giorni",
    description:
      "L'intera settimana a disposizione. Perfetta per aperture, celebrazioni e festività.",
    features: ["Noleggio 7 giorni consecutivi", "Massima flessibilità", "Ideale per eventi e festività"],
  },
];

export const steps = [
  {
    title: "1. Contattaci",
    text: "Scrivici su WhatsApp o via email indicando le date che ti interessano.",
  },
  {
    title: "2. Prenota",
    text: "Confermiamo disponibilità e formula di noleggio più adatta a te.",
  },
  {
    title: "3. Crea",
    text: "Ricevi la stampante pronta all'uso e inizia subito a creare nail art.",
  },
] as const;

export const faqs = [
  {
    q: "Serve esperienza per usare la stampante?",
    a: "No. La Sunwin SW-NA03 è pensata per essere semplice: ti guidiamo all'avvio e in pochi minuti sei operativo.",
  },
  {
    q: "Cosa è incluso nel noleggio?",
    a: "La stampante sanificata e pronta all'uso, insieme alle istruzioni e all'assistenza per l'avvio. Per i materiali di consumo (es. smalti/coating compatibili) chiedici i dettagli al momento della prenotazione.",
  },
  {
    q: "Come avviene la consegna o il ritiro?",
    a: "Concordiamo insieme consegna o ritiro al momento della prenotazione, in base alla tua zona e alle date scelte.",
  },
  {
    q: "Posso noleggiare lo stesso giorno ogni settimana?",
    a: "Sì. La formula settimanale ricorrente ti riserva una giornata fissa ogni settimana (ad esempio ogni lunedì) a una tariffa agevolata.",
  },
  {
    q: "È previsto un deposito cauzionale?",
    a: "I dettagli su cauzione e condizioni vengono comunicati in fase di prenotazione. Contattaci per un preventivo chiaro e senza impegno.",
  },
] as const;
