import {
  Phone,
  Mail,
  MessageCircle,
  Sparkles,
  Check,
  CalendarDays,
  PackageCheck,
  Wand2,
} from "lucide-react";

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
import { PrintButton } from "@/components/print-button";
import {
  business,
  heroHighlights,
  product,
  plans,
  steps,
  faqs,
} from "@/lib/content";

const whatsappHref = `https://wa.me/${business.phoneRaw.replace(
  "+",
  ""
)}?text=${encodeURIComponent(business.whatsappMessage)}`;
const telHref = `tel:${business.phoneRaw}`;
const mailHref = `mailto:${business.email}?subject=${encodeURIComponent(
  "Richiesta noleggio stampante NailsTech"
)}`;

export default function Home() {
  return (
    <>
      {/* ───── Header ───── */}
      <header className="no-print sticky top-0 z-40 border-b bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3">
          <a href="#top" className="flex items-center gap-2 font-semibold">
            <span className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Sparkles className="size-4" />
            </span>
            <span className="text-lg">{business.name}</span>
          </a>
          <nav className="hidden items-center gap-6 text-sm text-muted-foreground sm:flex">
            <a href="#stampante" className="hover:text-foreground">
              Stampante
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
              render={<a href={whatsappHref} target="_blank" rel="noopener noreferrer" />}
            >
              <MessageCircle />
              WhatsApp
            </Button>
          </div>
        </div>
      </header>

      <main id="top" className="flex-1">
        {/* ───── Hero ───── */}
        <section className="relative overflow-hidden">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-b from-accent/60 via-background to-background"
          />
          <div className="mx-auto max-w-5xl px-4 py-16 text-center sm:py-24">
            <Badge variant="secondary" className="mb-5">
              <Sparkles className="size-3" />
              {product.model}
            </Badge>
            <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight text-balance sm:text-5xl">
              {business.name}
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-lg font-medium text-primary">
              {business.tagline}
            </p>
            <p className="mx-auto mt-5 max-w-2xl text-pretty text-muted-foreground">
              {business.intro}
            </p>

            <div className="no-print mt-8 flex flex-wrap items-center justify-center gap-3">
              <Button
                size="lg"
                nativeButton={false}
                render={<a href={whatsappHref} target="_blank" rel="noopener noreferrer" />}
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

            <ul className="mx-auto mt-10 grid max-w-3xl gap-3 sm:grid-cols-3">
              {heroHighlights.map((item) => (
                <li
                  key={item}
                  className="flex items-center gap-2 rounded-lg border bg-card px-4 py-3 text-left text-sm"
                >
                  <Check className="size-4 shrink-0 text-primary" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* ───── Stampante / Specifiche ───── */}
        <section id="stampante" className="border-t bg-muted/30">
          <div className="mx-auto grid max-w-5xl items-center gap-10 px-4 py-16 md:grid-cols-2">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">
                {product.heading}
              </h2>
              <p className="mt-4 text-muted-foreground">{product.description}</p>
            </div>
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
          </div>
        </section>

        {/* ───── Prezzi ───── */}
        <section id="prezzi" className="border-t">
          <div className="mx-auto max-w-5xl px-4 py-16">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight">
                Tariffe di noleggio
              </h2>
              <p className="mt-3 text-muted-foreground">
                Scegli la formula più adatta a te. Prezzi chiari, senza sorprese.
              </p>
            </div>

            <div className="mt-10 grid gap-6 md:grid-cols-3">
              {plans.map((plan) => (
                <Card
                  key={plan.name}
                  className={`avoid-break relative flex flex-col ${
                    plan.featured ? "border-primary shadow-lg ring-1 ring-primary/30" : ""
                  }`}
                >
                  {plan.badge && (
                    <Badge className="absolute -top-2.5 left-1/2 -translate-x-1/2">
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
                        <a href={whatsappHref} target="_blank" rel="noopener noreferrer" />
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
        <section className="border-t bg-muted/30">
          <div className="mx-auto max-w-5xl px-4 py-16">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight">Come funziona</h2>
              <p className="mt-3 text-muted-foreground">
                Dal primo contatto alla nail art in tre semplici passi.
              </p>
            </div>
            <div className="mt-10 grid gap-6 sm:grid-cols-3">
              {steps.map((step, i) => {
                const Icon = [MessageCircle, CalendarDays, Wand2][i] ?? PackageCheck;
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
        <section id="faq" className="border-t">
          <div className="mx-auto max-w-3xl px-4 py-16">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight">
                Domande frequenti
              </h2>
              <p className="mt-3 text-muted-foreground">
                Non trovi la risposta? Scrivici, ti rispondiamo volentieri.
              </p>
            </div>
            <Accordion className="mt-8">
              {faqs.map((faq) => (
                <AccordionItem key={faq.q} value={faq.q}>
                  <AccordionTrigger className="text-base">{faq.q}</AccordionTrigger>
                  <AccordionContent className="text-muted-foreground">
                    {faq.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>

        {/* ───── Contatti ───── */}
        <section id="contatti" className="border-t bg-primary text-primary-foreground">
          <div className="mx-auto max-w-5xl px-4 py-16 text-center">
            <h2 className="text-3xl font-bold tracking-tight">
              Prenota la tua stampante
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-primary-foreground/80">
              Contattaci per verificare la disponibilità e ricevere un preventivo
              su misura. Risposta rapida via WhatsApp, telefono o email.
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

      {/* ───── Footer ───── */}
      <footer className="border-t py-8 text-center text-sm text-muted-foreground">
        <div className="mx-auto max-w-5xl px-4">
          <p className="font-medium text-foreground">{business.name}</p>
          <p className="mt-1">
            {business.tagline}
            {business.location ? ` · ${business.location}` : ""}
          </p>
          <p className="mt-3">
            © {new Date().getFullYear()} {business.name}. Tutti i diritti
            riservati.
          </p>
        </div>
      </footer>
    </>
  );
}
