import {
  Phone,
  Mail,
  MessageCircle,
  Sparkles,
  Check,
  CalendarDays,
  PackageCheck,
  Wand2,
  ShieldCheck,
  Droplets,
  Zap,
  PartyPopper,
  Store,
  Building2,
  Briefcase,
  ArrowRight,
  Menu,
} from "lucide-react";
import Image from "next/image";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Separator } from "@/components/ui/separator";
import { PrintButton } from "@/components/print-button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import {
  business,
  heroHighlights,
  stats,
  useCases,
  product,
  specs,
  consumables,
  certifications,
  plans,
  steps,
  faqs,
} from "@/lib/content";
import Link from "next/link";

const whatsappHref = `https://wa.me/${business.phoneRaw.replace(
  "+",
  "",
)}?text=${encodeURIComponent(business.whatsappMessage)}`;
const telHref = `tel:${business.phoneRaw}`;
const mailHref = `mailto:${business.email}?subject=${encodeURIComponent(
  "Richiesta noleggio stampante NailsTech",
)}`;

export default function Home() {
  return (
    <>
      {/* ───── Header ───── */}
      <header className="no-print sticky top-0 z-40 border-b bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Link href="#top" className="flex items-center font-semibold">
            {/* <Image
              src="/logo-image.png"
              alt="NailsTech"
              width={80}
              height={80}
              className="h-12 w-auto rounded-lg object-contain sm:h-10"
            /> */}
            <Image
              src="/logo-text.png"
              alt="NailsTech"
              width={260}
              height={40}
              className="h-8 w-auto object-contain sm:h-10"
            />
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden items-center gap-6 text-sm text-muted-foreground sm:flex">
            <a href="#usi" className="hover:text-foreground">
              Per chi
            </a>
            <a href="#stampante" className="hover:text-foreground">
              Stampante
            </a>
            <a href="#consumabili" className="hover:text-foreground">
              Consumabili
            </a>
            <a href="#prezzi" className="hover:text-foreground">
              Prezzi
            </a>
            <a href="#faq" className="hover:text-foreground">
              FAQ
            </a>
            <a href="#contatti" className="hover:text-foreground">
              Contatti
            </a>
          </nav>
          
          <div className="flex items-center gap-2">
            <PrintButton className="hidden sm:inline-flex" />
            <Button
              nativeButton={false}
              render={
                <a
                  href={whatsappHref}
                  target="_blank"
                  rel="noopener noreferrer"
                />
              }
              className="hidden sm:flex"
            >
              <MessageCircle />
              WhatsApp
            </Button>
            
            {/* Mobile Menu */}
            <Sheet>
              <SheetTrigger className="sm:hidden inline-flex items-center justify-center rounded-lg hover:bg-accent hover:text-accent-foreground h-9 w-9">
                <Menu className="h-5 w-5" />
                <span className="sr-only hidden">Menu</span>
              </SheetTrigger>
              <SheetContent side="right" className="w-80 px-4">
                <SheetHeader>
                  <SheetTitle className="sr-only hidden">Menu</SheetTitle>
                </SheetHeader>
                <nav className="flex flex-col gap-4 mt-6">
                  <a href="#usi" className="text-lg font-medium hover:text-primary">
                    Per chi
                  </a>
                  <a href="#stampante" className="text-lg font-medium hover:text-primary">
                    Stampante
                  </a>
                  <a href="#consumabili" className="text-lg font-medium hover:text-primary">
                    Consumabili
                  </a>
                  <a href="#prezzi" className="text-lg font-medium hover:text-primary">
                    Prezzi
                  </a>
                  <a href="#faq" className="text-lg font-medium hover:text-primary">
                    FAQ
                  </a>
                  <a href="#contatti" className="text-lg font-medium hover:text-primary">
                    Contatti
                  </a>
                  <Separator className="my-2" />
                  <Button
                    nativeButton={false}
                    render={
                      <a
                        href={whatsappHref}
                        target="_blank"
                        rel="noopener noreferrer"
                      />
                    }
                    className="w-full"
                  >
                    <MessageCircle />
                    WhatsApp
                  </Button>
                </nav>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </header>

      <main id="top" className="flex-1">
        {/* ───── Hero ───── */}
        <section className="relative overflow-hidden">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 -z-10 bg-linear-to-b from-accent/70 via-background to-background"
          />
          <div
            aria-hidden
            className="pointer-events-none absolute -top-24 -right-20 -z-10 size-72 rounded-full bg-primary/20 blur-3xl"
          />
          <div
            aria-hidden
            className="pointer-events-none absolute top-44 -left-24 -z-10 size-72 rounded-full bg-accent/50 blur-3xl"
          />
          <div className="mx-auto grid max-w-5xl items-center gap-12 px-4 py-12 sm:px-6 sm:py-16 lg:grid-cols-2">
            {/* testo */}
            <div className="text-center lg:text-left">
              <Badge variant="secondary" className="mb-5">
                <Sparkles className="size-3" />
                {product.model} · Nail bar pop-up
              </Badge>
              <h1 className="text-4xl font-bold tracking-tight text-balance sm:text-5xl lg:text-6xl">
                {business.tagline}
              </h1>
              <p className="mx-auto mt-5 max-w-xl text-pretty text-muted-foreground sm:text-lg lg:mx-0">
                {business.intro}
              </p>
              <div className="no-print mt-8 flex flex-wrap items-center justify-center gap-3 lg:justify-start">
                <Button
                  size="lg"
                  nativeButton={false}
                  render={
                    <a
                      href={whatsappHref}
                      target="_blank"
                      rel="noopener noreferrer"
                    />
                  }
                >
                  <MessageCircle />
                  Prenota su WhatsApp
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  nativeButton={false}
                  render={<a href={telHref} />}
                >
                  <Phone />
                  {business.phone}
                </Button>
              </div>
              <ul className="mt-8 grid gap-3">
                {heroHighlights.map((item) => (
                  <li
                    key={item}
                    className="flex items-center gap-2.5 rounded-lg border bg-card/70 px-4 py-3 text-left text-sm backdrop-blur"
                  >
                    <Check className="size-4 shrink-0 text-primary" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* visual — immagine lifestyle + video sovrapposto */}
            <div className="relative mx-auto w-full max-w-md">
              <div className="overflow-hidden rounded-3xl border shadow-2xl ring-1 ring-border">
                <Image
                  src="/4.jpg"
                  alt="Nail bar pop-up con stampante NailsTech NT-NA03 a un evento"
                  width={750}
                  height={750}
                  className="aspect-square w-full object-cover"
                  priority
                />
              </div>

              {/* video — phone frame sovrapposto */}
              {/* <div className="no-print absolute -bottom-6 -left-5 w-28 overflow-hidden rounded-2xl border bg-background shadow-xl ring-1 ring-border sm:w-36">
                <video
                  src="/v.mp4"
                  poster="/v_poster.jpg"
                  autoPlay
                  muted
                  loop
                  playsInline
                  className="block aspect-9/16 w-full object-cover"
                  aria-label="Stampante NT-NA03 in azione"
                />
              </div> */}

              {/* badge fluttuante */}
              <div className="absolute -top-4 -right-3 rounded-2xl border bg-background px-4 py-2.5 text-center shadow-lg">
                <p className="text-2xl font-bold leading-none text-primary">
                  ~10s
                </p>
                <p className="mt-1 text-[11px] text-muted-foreground">
                  per unghia
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* ───── Statistiche ───── */}
        <section className="border-y bg-card">
          <div className="mx-auto grid max-w-5xl grid-cols-2 divide-x divide-y md:grid-cols-4 md:divide-y-0">
            {stats.map((s) => (
              <div key={s.label} className="px-3 py-6 text-center sm:px-4 sm:py-8">
                <p className="text-2xl font-bold tracking-tight text-primary sm:text-3xl md:text-4xl">
                  {s.value}
                </p>
                <p className="mt-1.5 text-xs text-muted-foreground sm:text-sm">
                  {s.label}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* ───── Casi d'uso / Per chi ───── */}
        <section id="usi" className="border-t">
          <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
            <div className="mx-auto max-w-2xl text-center">
              <Badge variant="secondary" className="mb-4">
                <PartyPopper className="size-3" />
                Per ogni occasione
              </Badge>
              <h2 className="text-3xl font-bold tracking-tight">
                Un nail bar pop-up, mille occasioni
              </h2>
              <p className="mt-3 text-muted-foreground">
                Dal salone all&apos;evento aziendale: ovunque tu lo porti, la
                NT-NA03 diventa l&apos;attrazione del momento.
              </p>
            </div>
            <div className="mt-10 grid gap-6 sm:grid-cols-2">
              {useCases.map((u, i) => {
                const Icon =
                  [Building2, PartyPopper, Sparkles, Store][i] ?? Briefcase;
                return (
                  <Card
                    key={u.title}
                    className="avoid-break group gap-0 overflow-hidden p-0"
                  >
                    <div className="relative aspect-16/10 overflow-hidden">
                      <Image
                        src={u.image}
                        alt={u.title}
                        fill
                        sizes="(min-width: 640px) 50vw, 100vw"
                        className="object-cover transition-transform duration-500 group-hover:scale-105"
                      />
                      <div
                        aria-hidden
                        className="absolute inset-0 bg-linear-to-t from-black/70 via-black/15 to-transparent"
                      />
                      <h3 className="absolute inset-x-4 bottom-3 flex items-center gap-2 text-lg font-semibold text-white">
                        <Icon className="size-5 shrink-0" />
                        {u.title}
                      </h3>
                    </div>
                    <CardContent className="px-5 py-5 text-sm text-muted-foreground">
                      {u.text}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
            <div className="no-print mt-10 flex justify-center">
              <Button
                size="lg"
                nativeButton={false}
                render={<a href="#prezzi" />}
              >
                Scopri le tariffe
                <ArrowRight />
              </Button>
            </div>
          </div>
        </section>

        {/* ───── Stampante / Specifiche ───── */}
        <section id="stampante" className="border-t bg-muted/30">
          <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
            {/* foto macchina full-width */}
            {/* <div className="overflow-hidden rounded-2xl border shadow-md">
              <Image
                src="/Na03.jpg"
                alt="NailsTech NT-NA03 — nail printer professionale"
                width={1139}
                height={650}
                className="w-full object-cover"
                priority
              />
            </div> */}

            {/* thumbnail gallery */}
            <div className="mt-4 sm:flex gap-3 sm:justify-center grid grid-cols-2">
              {(["na03-4.jpg","na03-5.jpg", "nao3-2.avif", "na03-3.avif"] as const).map(
                (src) => (
                  <div
                    key={src}
                    className="overflow-hidden rounded-xl border shadow-sm"
                  >
                    <Image
                      src={`/${src}`}
                      alt="NT-NA03 dettaglio"
                      width={220}
                      height={220}
                      className="h-40 object-cover "
                    />
                  </div>
                ),
              )}
            </div>

            <div className="mt-10 grid items-start gap-10 md:grid-cols-2">
              <div>
                <h2 className="text-3xl font-bold tracking-tight">
                  {product.heading}
                </h2>
                <p className="mt-4 text-muted-foreground">
                  {product.description}
                </p>

                {/* video demo */}
                <div className="mt-8 overflow-hidden rounded-2xl border shadow-md">
                  <video
                    src="/d.mp4"
                    poster="/d_poster.jpg"
                    autoPlay
                    muted
                    loop
                    playsInline
                    className="block aspect-9/16 w-full object-cover"
                    aria-label="Demo stampa con NT-NA03"
                  />
                </div>

                {/* specifiche tecniche */}
                <div className="avoid-break mt-8">
                  <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
                    Specifiche tecniche
                  </h3>
                  <dl className="divide-y rounded-xl border bg-card text-sm">
                    {specs.map((s) => (
                      <div
                        key={s.label}
                        className="flex items-baseline gap-3 px-4 py-2.5"
                      >
                        <dt className="w-44 shrink-0 text-muted-foreground">
                          {s.label}
                        </dt>
                        <dd className="font-medium">{s.value}</dd>
                      </div>
                    ))}
                  </dl>
                </div>
              </div>

              <div className="grid gap-6">
                <Card className="avoid-break">
                  <CardHeader>
                    <CardTitle>Caratteristiche principali</CardTitle>
                    <CardDescription>
                      Tutto ciò che ottieni con il noleggio.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="grid gap-3">
                      {product.features.map((f) => (
                        <li key={f} className="flex items-start gap-3 text-sm">
                          <Check className="mt-0.5 size-4 shrink-0 text-primary" />
                          <span>{f}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card className="avoid-break">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <ShieldCheck className="size-5 text-primary" />
                      Certificazioni &amp; conformità UE
                    </CardTitle>
                    <CardDescription>
                      La NT-NA03 è omologata per il mercato europeo.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="grid gap-4">
                      {certifications.map((c) => (
                        <li
                          key={c.label}
                          className="flex items-start gap-3 text-sm"
                        >
                          <Badge
                            variant="secondary"
                            className="mt-0.5 shrink-0 font-mono text-xs"
                          >
                            {c.label}
                          </Badge>
                          <span className="text-muted-foreground">
                            {c.description}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* ───── Consumabili ───── */}
        <section id="consumabili" className="border-t">
          <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
            <div className="grid items-start gap-12 lg:grid-cols-[1fr_300px]">
              {/* contenuto */}
              <div>
                <h2 className="text-3xl font-bold tracking-tight">
                  Consumabili e materiali
                </h2>
                <p className="mt-3 text-muted-foreground">
                  Tutto ciò che serve per stampare in sicurezza — con inchiostri
                  certificati e gel privi di HEMA e TPO.
                </p>

                <div className="mt-8 grid gap-6 sm:grid-cols-2">
                  {consumables.map((c, i) => {
                    const Icon =
                      [Zap, Droplets, ShieldCheck, Sparkles][i] ?? PackageCheck;
                    return (
                      <Card key={c.name} className="avoid-break">
                        <CardHeader className="pb-2">
                          <CardTitle className="flex items-center gap-2 text-base">
                            <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                              <Icon className="size-4" />
                            </span>
                            {c.name}
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="text-sm text-muted-foreground">
                          <p>{c.description}</p>
                          {c.note && (
                            <>
                              <Separator className="my-3" />
                              <p className="flex items-center gap-1.5 font-medium text-foreground">
                                <Check className="size-3.5 shrink-0 text-primary" />
                                {c.note}
                              </p>
                            </>
                          )}
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>

                {/* cosa è incluso nel kit */}
                <div className="avoid-break mt-8 grid gap-5 rounded-xl border bg-card p-5 sm:grid-cols-[210px_1fr] sm:items-center">
                  <div className="overflow-hidden rounded-lg border bg-muted">
                    <Image
                      src="/images.jpeg"
                      alt="Kit di noleggio NT-NA03 con cartuccia, primer e accessori"
                      width={420}
                      height={300}
                      className="w-full object-contain"
                    />
                  </div>
                  <div>
                    <p className="flex items-center gap-2 font-semibold text-foreground">
                      <PackageCheck className="size-4 text-primary" />
                      Tutto pronto nella valigia
                    </p>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Ogni noleggio arriva completo: stampante calibrata,
                      cartuccia d&apos;inchiostro, primer, base/holder per il
                      dito, telecomando e tutto il necessario per allestire il
                      nail bar e iniziare a stampare in pochi minuti.
                    </p>
                  </div>
                </div>

                <div className="avoid-break mt-6 rounded-xl border border-primary/30 bg-primary/5 px-6 py-5 text-sm">
                  <p className="font-semibold text-foreground">
                    Perché HEMA-free e TPO-free?
                  </p>
                  <p className="mt-1 text-muted-foreground">
                    L&apos;HEMA (idrossietil metacrilato) è un allergizzante
                    potenzialmente sensibilizzante vietato o limitato dalla
                    normativa cosmetica UE. Il TPO (Trimethylbenzoyl
                    Diphenylphosphine Oxide), foto-iniziatore comune nei gel UV,
                    è incluso nella lista delle sostanze vietate dalla{" "}
                    <strong>Reg. UE 2025/877</strong>. Utilizzando top coat
                    senza questi ingredienti proteggi te, i tuoi clienti e i
                    tuoi operatori.
                  </p>
                </div>
              </div>

              {/* immagine vantaggi — sticky lato destro */}
              <div className="hidden lg:block">
                <div className="sticky top-24 overflow-hidden rounded-2xl border shadow-md">
                  <Image
                    src="/digital-nail-art-printing-na03-advantage.webp"
                    alt="Vantaggi della stampante NT-NA03"
                    width={750}
                    height={750}
                    className="w-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ───── Prezzi ───── */}
        <section id="prezzi" className="border-t bg-muted/30">
          <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight">
                Tariffe di noleggio
              </h2>
              <p className="mt-3 text-muted-foreground">
                Una giornata, un evento o un&apos;intera settimana: scegli la
                formula più adatta. Prezzi chiari, senza sorprese.
              </p>
            </div>
            <div className="mt-10 grid gap-6 md:grid-cols-3">
              {plans.map((plan) => (
                <Card
                  key={plan.name}
                  className={`avoid-break relative flex flex-col p-4 ${
                    plan.featured
                      ? "border-primary shadow-lg ring-1 ring-primary/30"
                      : ""
                  }`}
                >
                  {plan.badge && (
                    <Badge className="relative -top-2.5 left-1/2 -translate-x-1/2">
                      {plan.badge}
                    </Badge>
                  )}
                  <CardHeader>
                    <CardTitle className="text-xl">{plan.name}</CardTitle>
                    <CardDescription>{plan.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="flex flex-1 flex-col">
                    <div className="mb-5 flex items-baseline gap-1.5">
                      <span className="text-4xl font-bold tracking-tight">
                        {plan.price}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        {plan.period}
                      </span>
                    </div>
                    <ul className="grid gap-2.5">
                      {plan.features.map((f) => (
                        <li key={f} className="flex items-start gap-2 text-sm">
                          <Check className="mt-0.5 size-4 shrink-0 text-primary" />
                          <span>{f}</span>
                        </li>
                      ))}
                    </ul>
                    <Button
                      className="no-print mt-6 w-full"
                      variant={plan.featured ? "default" : "outline"}
                      nativeButton={false}
                      render={
                        <a
                          href={whatsappHref}
                          target="_blank"
                          rel="noopener noreferrer"
                        />
                      }
                    >
                      Richiedi disponibilità
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* ───── Come funziona ───── */}
        <section className="border-t">
          <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight">
                Come funziona
              </h2>
              <p className="mt-3 text-muted-foreground">
                Dal primo contatto alla nail art in tre semplici passi.
              </p>
            </div>
            <div className="mt-10 grid gap-6 sm:grid-cols-3">
              {steps.map((step, i) => {
                const Icon =
                  [MessageCircle, CalendarDays, Wand2][i] ?? PackageCheck;
                return (
                  <div
                    key={step.title}
                    className="avoid-break rounded-xl border bg-card p-6 text-center"
                  >
                    <div className="mx-auto mb-4 flex size-11 items-center justify-center rounded-full bg-primary/10 text-primary">
                      <Icon className="size-5" />
                    </div>
                    <h3 className="font-semibold">{step.title}</h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {step.text}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* ───── FAQ ───── */}
        <section id="faq" className="border-t bg-muted/30">
          <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight">
                Domande frequenti
              </h2>
              <p className="mt-3 text-muted-foreground">
                Non trovi la risposta? Scrivici, ti rispondiamo volentieri.
              </p>
            </div>
            <Accordion className="mt-8" defaultValue={faqs.map(f => f.q)}>
              {faqs.map((faq) => (
                <AccordionItem key={faq.q} value={faq.q}>
                  <AccordionTrigger className="text-base">
                    {faq.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground">
                    {faq.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>

        {/* ───── Contatti ───── */}
        <section
          id="contatti"
          className="border-t bg-primary text-primary-foreground"
        >
          <div className="mx-auto max-w-5xl px-4 py-12 text-center sm:px-6 sm:py-16">
            <div className="flex justify-center">
            <Image
              src="/logo-image.png"
              alt="NailsTech"
              width={320}
              height={320}
              className="rounded-xl w-80 h-80"
            />
              </div>
            <h2 className="mt-4 text-3xl font-bold tracking-tight">
              Prenota il tuo nail bar pop-up
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-primary-foreground/80">
              Raccontaci date, location e tipo di evento: verifichiamo la
              disponibilità e ti inviamo un preventivo su misura. Risposta
              rapida via WhatsApp, telefono o email.
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-3">
              <a
                href={whatsappHref}
                target="_blank"
                rel="noopener noreferrer"
                className="avoid-break flex flex-col items-center gap-2 rounded-xl bg-primary-foreground/10 px-4 py-6 transition-colors hover:bg-primary-foreground/20"
              >
                <MessageCircle className="size-6" />
                <span className="text-sm font-medium">WhatsApp</span>
                <span className="text-sm text-primary-foreground/80">
                  {business.phone}
                </span>
              </a>
              <a
                href={telHref}
                className="avoid-break flex flex-col items-center gap-2 rounded-xl bg-primary-foreground/10 px-4 py-6 transition-colors hover:bg-primary-foreground/20"
              >
                <Phone className="size-6" />
                <span className="text-sm font-medium">Telefono</span>
                <span className="text-sm text-primary-foreground/80">
                  {business.phone}
                </span>
              </a>
              <a
                href={mailHref}
                className="avoid-break flex flex-col items-center gap-2 rounded-xl bg-primary-foreground/10 px-4 py-6 transition-colors hover:bg-primary-foreground/20"
              >
                <Mail className="size-6" />
                <span className="text-sm font-medium">Email</span>
                <span className="break-all text-sm text-primary-foreground/80">
                  {business.email}
                </span>
              </a>
            </div>
            <div className="no-print mt-8 flex justify-center">
              <PrintButton
                label="Salva questa pagina in PDF"
                className="border-primary-foreground/30 bg-transparent text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
              />
            </div>
          </div>
        </section>
      </main>

      {/* ───── Footer ──no-print ─── */}
      <footer className="border-t py-8 text-center text-sm text-muted-foreground no-print">
        <div className="mx-auto max-w-5xl px-4">
          <Image
            src="/logo-full.png"
            alt="NailsTech"
            width={600}
            height={600}
            className="mx-auto h-80 w-80 object-contain"
          />
          <p className="mt-3">
            {business.tagline}
            {business.location ? ` · ${business.location}` : ""}
          </p>
          <p className="mt-3">
            © {new Date().getFullYear()} {business.name}. Tutti i diritti riservati.
          </p>
        </div>
      </footer>
    </>
  );
}
