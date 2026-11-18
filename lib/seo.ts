import type { Metadata } from "next";
import { LANGS, type Lang } from "@/lib/i18n";

export const SITE_URL = "https://euromar.com.ar";

/**
 * Canonical + hreflang de una página. Cada idioma apunta a sí mismo como canonical
 * y declara sus traducciones, para que Google no las trate como duplicados.
 * path: "" para el inicio, "/productos", "/servicios", etc.
 */
export function alternatesFor(lang: Lang, path: string): Metadata["alternates"] {
  const languages: Record<string, string> = {};
  for (const l of LANGS) languages[l] = `/${l}${path}`;
  languages["x-default"] = `/es${path}`;
  return { canonical: `/${lang}${path}`, languages };
}
