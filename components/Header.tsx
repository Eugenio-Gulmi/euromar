"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";

const LANGS = [
  { code: "es", label: "Español", short: "ES" },
  { code: "en", label: "English", short: "EN" },
  { code: "zh", label: "中文", short: "中" },
];

type Nav = {
  home: string;
  products: string;
  services: string;
  about: string;
  contact: string;
};

export default function Header({ lang, nav }: { lang: string; nav: Nav }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  const navItems = [
    { href: `/${lang}`, label: nav.home },
    { href: `/${lang}/productos`, label: nav.products },
    { href: `/${lang}/servicios`, label: nav.services },
    { href: `/${lang}/nosotros`, label: nav.about },
    { href: `/${lang}/contacto`, label: nav.contact },
  ];

  function switchLang(newLang: string) {
    const segments = pathname.split("/");
    segments[1] = newLang;
    return segments.join("/") || `/${newLang}`;
  }

  return (
    <header className="bg-navy-900 text-white sticky top-0 z-50 shadow-lg border-b border-white/5">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-16">
        {/* Logo */}
        <Link href={`/${lang}`} className="flex items-center shrink-0">
          <div className="bg-white rounded-lg px-3 py-1">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="https://cdn.jsdelivr.net/gh/Eugenio-Gulmi/euromar@master/public/euromar-logo.jpg"
              alt="Euromar SA — Frozen Seafoods"
              className="h-8 w-auto"
            />
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`transition-colors ${
                  active ? "text-gold-light" : "text-white/80 hover:text-white"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          {/* Language switcher — larger + labeled */}
          <div className="hidden sm:flex items-center gap-px bg-white/10 rounded-lg p-0.5">
            {LANGS.map((l) => (
              <Link
                key={l.code}
                href={switchLang(l.code)}
                title={l.label}
                className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
                  lang === l.code
                    ? "bg-gold text-navy-900 shadow-sm"
                    : "text-white/70 hover:text-white hover:bg-white/10"
                }`}
              >
                {l.short}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-1.5 rounded-md hover:bg-white/10 transition-colors"
            onClick={() => setOpen(!open)}
            aria-label="Menú"
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-navy-800 border-t border-white/10">
          <div className="px-4 py-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block px-3 py-2.5 text-sm font-medium rounded-lg hover:bg-white/10 hover:text-gold-light transition-all"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
          {/* Language picker in mobile menu */}
          <div className="px-4 pb-4">
            <p className="text-xs text-white/40 uppercase tracking-widest mb-2 px-3">Idioma / Language</p>
            <div className="flex gap-2">
              {LANGS.map((l) => (
                <Link
                  key={l.code}
                  href={switchLang(l.code)}
                  className={`flex-1 text-center py-2 rounded-lg text-sm font-bold transition-all ${
                    lang === l.code
                      ? "bg-gold text-navy-900"
                      : "bg-white/10 text-white hover:bg-white/20"
                  }`}
                  onClick={() => setOpen(false)}
                >
                  {l.short}
                  <span className="block text-xs font-normal opacity-70">{l.label}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
