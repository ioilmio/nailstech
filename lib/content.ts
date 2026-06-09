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
  tagline: "Il nail bar pop-up che noleggi in un giorno",
  intro:
    "Trasforma eventi, aperture e giornate in salone in un'esperienza che fa parlare di sé. Noleggi la stampante per unghie NailsTech NT-NA03 e crei nail art in HD in ~10 secondi — senza comprare nulla e senza esperienza. La consegniamo pronta all'uso: tu accendi il nail bar, i tuoi ospiti se ne vanno con le unghie perfette.",
  // Recapiti — usati anche per i link cliccabili (tel:, mailto:, WhatsApp)
  phone: "+39 351 503 5361",
  phoneRaw: "+393515035361", // senza spazi, per i link tel: e WhatsApp
  email: "illuminato.salvatore@gmail.com",
  whatsappMessage:
    "Ciao! Vorrei informazioni sul noleggio del nail bar pop-up NailsTech per il mio evento o salone.",
  // Località mostrata nei contatti (opzionale: lascia "" per nasconderla)
  location: "Italia",
} as const;

export const heroHighlights = [
  "Nail art in HD in ~10 secondi: ospiti felici, file che scorrono",
  "Zero acquisto e zero competenze: noleggi e sei subito operativo",
  "Consegna sanificata, calibrazione e assistenza all'avvio incluse",
] as const;

/** Numeri chiave mostrati nella barra statistiche sotto l'hero */
export const stats: { value: string; label: string }[] = [
  { value: "~10s", label: "per unghia stampata" },
  { value: "500–800", label: "unghie per cartuccia" },
  { value: "0", label: "esperienza richiesta" },
  { value: "100%", label: "pronta all'uso alla consegna" },
];

/** Casi d'uso del nail bar pop-up — ognuno con immagine dedicata */
export const useCases: { title: string; text: string; image: string }[] = [
  {
    title: "Eventi & brand activation",
    text: "Un'attrazione che ferma le persone: nail art brandizzata in tempo reale per fiere, lanci di prodotto e attivazioni. Crea code, contenuti social e ricordi che restano.",
    image: "2.jpg",
  },
  {
    title: "Feste & celebrazioni",
    text: "Compleanni, addii al nubilato, baby shower e matrimoni: regala alle tue ospiti un angolo beauty divertente dove ognuna sceglie il proprio design in pochi secondi.",
    image: "3.jpg",
  },
  {
    title: "Saloni & nail artist",
    text: "Aggiungi un servizio premium senza investimenti: offri centinaia di design e nail art personalizzata nelle tue giornate di punta, pagando solo il noleggio.",
    image: "5.jpg",
  },
  {
    title: "Negozi, aperture & pop-up",
    text: "Inaugurazioni, mercatini e temporary store: porta traffico al tuo spazio con un servizio gratuito o a pagamento che trasforma i curiosi in clienti.",
    image: "6.jpg",
  },
];

export const product = {
  model: "NailsTech NT-NA03",
  heading: "La macchina: NailsTech NT-NA03",
  description:
    "Il cuore del tuo nail bar pop-up. La NT-NA03 è una stampante all-in-one di ultima generazione: schermo touch da 5\", fotocamera integrata per il riconoscimento automatico dell'unghia, inkjet ad alta definizione e lampada UV/LED incorporata. Compatta e portatile, si allestisce ovunque in pochi minuti — perfetta da spostare tra eventi, location e postazioni.",
  features: [
    "Stampa HD direttamente sull'unghia (risoluzione elevata, colori vividi)",
    "Riconoscimento automatico dell'unghia via fotocamera integrata",
    "Lampada UV/LED integrata: asciugatura immediata dopo la stampa",
    "Schermo touch da 5\" con guida visiva all'altezza del dito",
    "Connessione Wi-Fi e Bluetooth — nessuna app obbligatoria",
    "Migliaia di design + caricamento libero di immagini personalizzate",
    "Consegna sanificata, calibrata e pronta all'uso",
  ],
} as const;

/** Specifiche tecniche dettagliate della NT-NA03 */
export const specs: { label: string; value: string }[] = [
  { label: "Tecnologia di stampa",  value: "Inkjet a getto d'inchiostro" },
  { label: "Schermo",               value: "Touch screen 5\"" },
  { label: "Velocità di stampa",    value: "~10 secondi per unghia" },
  { label: "Resa cartuccia",        value: "500–800 unghie per cartuccia" },
  { label: "Connettività",          value: "Wi-Fi 2.4 GHz + Bluetooth" },
  { label: "Lampada essiccante",    value: "UV/LED integrata con ventola" },
  { label: "Superfici compatibili", value: "Unghia naturale, gel, acrilico, tips" },
  { label: "Alimentazione",         value: "Adattatore AC (incluso)" },
  { label: "Forma fisica",          value: "Compatta e portatile" },
  { label: "Certificazioni",        value: "CE · RoHS · FCC" },
];

/** Consumabili necessari per l'utilizzo */
export const consumables: {
  name: string;
  description: string;
  note?: string;
}[] = [
  {
    name: "Cartuccia inchiostro",
    description:
      "Inchiostro a base acquosa in 3 colori primari + bianco. Resa: 500–800 unghie. Fornita con MSDS (scheda di sicurezza materiale).",
    note: "Inclusa nel noleggio (quantità in base alla formula scelta)",
  },
  {
    name: "Primer / Base coat",
    description:
      "Strato preparatorio che migliora l'adesione dell'inchiostro sull'unghia naturale o sul gel. Applicare prima della stampa e lasciar asciugare.",
  },
  {
    name: "Top coat gel UV/LED (HEMA-free & TPO-free)",
    description:
      "Sigilla e protegge il design stampato. Utilizza esclusivamente top coat certificati senza HEMA (idrossietil metacrilato) e senza TPO, in conformità con la normativa cosmetica UE (Reg. 1223/2009 e aggiornamenti 2025/877).",
    note: "Consigliati per una durata di 1–2 settimane",
  },
  {
    name: "Solvente detergente / Nail cleaner",
    description:
      "Pulisce la piastra del dito e la testina di stampa. Usare anche per la rimozione del top coat prima di un nuovo design.",
  },
];

/** Certificazioni e conformità normativa */
export const certifications: {
  label: string;
  description: string;
}[] = [
  {
    label: "CE",
    description:
      "Marchio obbligatorio per il mercato europeo. Attesta la conformità della macchina alle direttive UE in materia di sicurezza elettrica e compatibilità elettromagnetica (EMC).",
  },
  {
    label: "RoHS",
    description:
      "Direttiva 2011/65/UE sulla restrizione delle sostanze pericolose nei componenti elettronici. La NT-NA03 è priva di piombo, mercurio, cadmio e altri metalli pesanti.",
  },
  {
    label: "FCC",
    description:
      "Certificazione radio-frequenza USA (rilevante per l'emissione Wi-Fi/Bluetooth). Ulteriore garanzia di qualità costruttiva internazionale.",
  },
  {
    label: "MSDS consumabili",
    description:
      "Tutti i consumabili originali (inchiostro, primer, top coat) sono accompagnati da scheda di sicurezza (Material Safety Data Sheet) conforme GHS/CLP.",
  },
  {
    label: "HEMA-free & TPO-free",
    description:
      "I top coat consigliati non contengono HEMA (idrossietil metacrilato) né TPO (Trimethylbenzoyl Diphenylphosphine Oxide), in linea con le più recenti restrizioni cosmetiche UE (Reg. UE 2025/877) per la protezione di operatori e clienti.",
  },
];

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
    name: "Giornata / Evento",
    price: "120€",
    period: "al giorno",
    description: "Una singola giornata. Perfetta per un evento, una festa o un pop-up in salone.",
    features: ["Noleggio 1 giorno", "Consegna pronta all'uso", "Assistenza all'avvio"],
  },
  {
    name: "Giornata fissa settimanale",
    price: "80€",
    period: "a giornata / settimana",
    description:
      "Una giornata fissa ogni settimana (es. ogni lunedì). La formula più conveniente per saloni e attività ricorrenti.",
    features: [
      "Stesso giorno ogni settimana",
      "Tariffa scontata a giornata",
      "Priorità di prenotazione",
    ],
    featured: true,
    badge: "Più conveniente",
  },
  {
    name: "Settimana / Tour eventi",
    price: "350€",
    period: "per 7 giorni",
    description:
      "Sette giorni a disposizione. Ideale per aperture, festività e tour tra più location ed eventi.",
    features: ["Noleggio 7 giorni consecutivi", "Massima flessibilità di spostamento", "Ideale per eventi e festività"],
  },
];

export const steps = [
  {
    title: "1. Raccontaci l'occasione",
    text: "Scrivici su WhatsApp con date, location e tipo di evento: ti consigliamo la formula più adatta.",
  },
  {
    title: "2. Ricevi il nail bar",
    text: "Ti consegniamo la stampante sanificata, calibrata e pronta, con una guida rapida all'avvio.",
  },
  {
    title: "3. Accendi e stampa",
    text: "I tuoi ospiti scelgono il design, appoggiano il dito e in ~10 secondi la nail art è pronta.",
  },
] as const;

export const faqs = [
  {
    q: "Per che tipo di eventi e occasioni è adatta?",
    a: "Per tutto ciò che richiede un'attrazione beauty: brand activation e fiere, aperture e temporary store, feste private, addii al nubilato, compleanni e matrimoni, oltre alle giornate di punta in salone. Il nail bar pop-up si allestisce ovunque ci sia una presa di corrente.",
  },
  {
    q: "Quante persone posso servire in una giornata?",
    a: "Con ~10 secondi di stampa per unghia, una manicure completa richiede pochi minuti tra scelta del design, stampa e asciugatura UV/LED. In una giornata di evento puoi servire comodamente decine di ospiti, e una cartuccia copre 500–800 unghie.",
  },
  {
    q: "Serve esperienza per usare la stampante?",
    a: "No. La NailsTech NT-NA03 riconosce automaticamente la forma e le dimensioni di ogni unghia grazie alla fotocamera integrata. Lo schermo touch da 5\" guida l'operatore passo dopo passo: in pochi minuti sei operativo, anche senza esperienza tecnica.",
  },
  {
    q: "Quanto tempo ci vuole per stampare un'unghia?",
    a: "Circa 10 secondi per unghia. La lampada UV/LED integrata asciuga il design immediatamente dopo la stampa, per un servizio rapido e professionale.",
  },
  {
    q: "Quante unghie posso stampare con una cartuccia?",
    a: "Una cartuccia originale copre 500–800 unghie. Per il noleggio giornaliero o settimanale questo è più che sufficiente per una giornata intensa di lavoro.",
  },
  {
    q: "Cosa è incluso nel noleggio?",
    a: "La stampante sanificata e calibrata, la cartuccia inchiostro (quantità in base alla formula scelta), il primer e le istruzioni. Per i top coat consigliati HEMA-free/TPO-free contattaci al momento della prenotazione.",
  },
  {
    q: "La stampante e i consumabili sono sicuri? Quali certificazioni hanno?",
    a: "Sì. La NT-NA03 è certificata CE e RoHS per il mercato europeo. L'inchiostro originale è a base acquosa ed è corredato da MSDS (scheda di sicurezza). I top coat consigliati sono HEMA-free e TPO-free, in linea con le ultime normative cosmetiche UE.",
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
