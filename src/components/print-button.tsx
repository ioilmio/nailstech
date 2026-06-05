"use client";

import { Printer } from "lucide-react";
import { Button } from "@/components/ui/button";

/**
 * Pulsante che apre la finestra di stampa del browser.
 * Da lì l'utente può stampare o scegliere "Salva come PDF".
 * Viene nascosto in fase di stampa grazie alla classe `no-print`.
 */
export function PrintButton({
  className,
  label = "Scarica PDF",
}: {
  className?: string;
  label?: string;
}) {
  return (
    <Button
      type="button"
      variant="outline"
      onClick={() => window.print()}
      className={className}
    >
      <Printer />
      {label}
    </Button>
  );
}
