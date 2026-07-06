"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Menu, X, ChevronDown } from "lucide-react";

const LANGS = [
  { code: "es", label: "Español",    flag: "🇦🇷" },
  { code: "en", label: "English",    flag: "🇬🇧" },
  { code: "fr", label: "Français",   flag: "🇫🇷" },
  { code: "nl", label: "Nederlands", flag: "🇳🇱" },
  { code: "ar", label: "العربية",    flag: "🇦🇪" },
  { code: "zh", label: "中文",        flag: "🇨🇳" },
];

type Nav = {
  home: string;
  products: string;
  services: string;
  about: string;
  contact: string;
};

export default function Header({ lang, nav }: { lang: string; nav: Nav }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const langRef = useRef<HTMLDivElement>(null);

  const current = LANGS.find((l) => l.code === lang) ?? LANGS[0];

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

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (langRef.current && !langRef.current.contains(e.target as Node)) {
        setLangOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <header className="bg-navy-900 text-white sticky top-0 z-50 shadow-lg border-b border-white/5">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-16">
        {/* Logo */}
        <Link href={`/${lang}`} className="flex items-center shrink-0">
          <div className="bg-white rounded-lg px-3 py-1">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/euromar-logo.jpg"
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
          {/* Language dropdown */}
          <div className="hidden sm:block relative" ref={langRef}>
            <button
              onClick={() => setLangOpen(!langOpen)}
              className="flex items-center gap-2 bg-white/10 hover:bg-white/15 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
            >
              <span className="text-white/90">{current.label}</span>
              <ChevronDown className={`w-3.5 h-3.5 text-white/50 transition-transform ${langOpen ? "rotate-180" : ""}`} />
            </button>

            {langOpen && (
              <div className="absolute right-0 top-full mt-1.5 bg-navy-800 border border-white/10 rounded-xl shadow-xl overflow-hidden w-36 z-50">
                {LANGS.map((l) => (
                  <Link
                    key={l.code}
                    href={switchLang(l.code)}
                    onClick={() => setLangOpen(false)}
                    className={`flex items-center gap-3 px-4 py-2.5 text-sm transition-colors ${
                      lang === l.code
                        ? "bg-gold/20 text-gold-light font-semibold"
                        : "text-white/80 hover:bg-white/10 hover:text-white"
                    }`}
                  >
                    <span className="text-base leading-none">{l.flag}</span>
                    {l.label}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-1.5 rounded-md hover:bg-white/10 transition-colors"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Menú"
          >
            {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-navy-800 border-t border-white/10">
          <div className="px-4 py-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block px-3 py-2.5 text-sm font-medium rounded-lg hover:bg-white/10 hover:text-gold-light transition-all"
                onClick={() => setMenuOpen(false)}
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
                  className={`flex-1 text-center py-2.5 rounded-lg text-sm font-medium transition-all ${
                    lang === l.code
                      ? "bg-gold text-navy-900 font-bold"
                      : "bg-white/10 text-white hover:bg-white/20"
                  }`}
                  onClick={() => setMenuOpen(false)}
                >
                  <span className="block text-lg leading-none mb-0.5">{l.flag}</span>
                  <span className="text-xs opacity-80">{l.label}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
