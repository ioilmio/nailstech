# NailsTech — Sito vetrina noleggio stampante per unghie

Sito web a pagina singola (in italiano) per il noleggio della stampante per
unghie **Sunwin SW-NA03**. È pensato per essere **semplice da modificare** e
**stampabile in PDF** (pulsante "Scarica PDF" / Stampa del browser).

Realizzato con **Next.js 16**, **TypeScript**, **Tailwind CSS v4** e
**shadcn/ui**. Pronto per il deploy su **Vercel**.

## Avvio in locale

```bash
npm install
npm run dev
```

Apri [http://localhost:3000](http://localhost:3000) nel browser.

## Come modificare i contenuti

Tutti i testi, i prezzi, le FAQ e i recapiti sono raccolti in un unico file:

```
src/lib/content.ts
```

Modifica quel file per aggiornare nome attività, tagline, descrizione del
prodotto, tariffe, passaggi "come funziona", domande frequenti e contatti
(telefono/WhatsApp ed email). Non serve toccare il codice dei componenti.

La struttura e lo stile della pagina sono in `src/app/page.tsx`, mentre i colori
del brand e gli stili di stampa/PDF sono in `src/app/globals.css`.

## Esportare in PDF

Apri il sito e usa il pulsante **"Scarica PDF"** (oppure `Ctrl/Cmd + P` →
"Salva come PDF"). Gli stili di stampa nascondono automaticamente i pulsanti e
ottimizzano il layout su formato A4.

## Comandi utili

```bash
npm run dev     # server di sviluppo
npm run build   # build di produzione
npm run start   # avvia la build di produzione
npm run lint    # ESLint
```

## Deploy su Vercel

1. Vai su [vercel.com/new](https://vercel.com/new) e importa questo repository.
2. Vercel rileva automaticamente Next.js: lascia le impostazioni di default.
3. Premi **Deploy**. Nessuna variabile d'ambiente è necessaria.

Ad ogni push su `main` Vercel pubblicherà automaticamente la nuova versione.
