import type esDictionary from "@/dictionaries/es.json";

export type Lang = "es" | "en" | "zh" | "fr" | "nl" | "ar" | "pt";
export type Dictionary = typeof esDictionary;

export const LANGS: Lang[] = ["es", "en", "zh", "fr", "nl", "ar", "pt"];

export function isValidLang(lang: string): lang is Lang {
  return LANGS.includes(lang as Lang);
}

const loaders: Record<Lang, () => Promise<Dictionary>> = {
  es: () => import("@/dictionaries/es.json").then((m) => m.default as Dictionary),
  en: () => import("@/dictionaries/en.json").then((m) => m.default as Dictionary),
  zh: () => import("@/dictionaries/zh.json").then((m) => m.default as Dictionary),
  fr: () => import("@/dictionaries/fr.json").then((m) => m.default as Dictionary),
  nl: () => import("@/dictionaries/nl.json").then((m) => m.default as Dictionary),
  ar: () => import("@/dictionaries/ar.json").then((m) => m.default as Dictionary),
  pt: () => import("@/dictionaries/pt.json").then((m) => m.default as Dictionary),
};

export async function getDictionary(lang: Lang): Promise<Dictionary> {
  return loaders[lang]();
}
