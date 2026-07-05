import Link from "next/link";
import { Fish, Phone, Mail } from "lucide-react";
import type { Dictionary } from "@/lib/i18n";

export default function Footer({
  lang,
  t,
}: {
  lang: string;
  t: Dictionary;
}) {
  return (
    <footer className="bg-navy-950 text-white">
      <div className="max-w-6xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-3 gap-10">
        <div>
          <div className="flex items-center gap-2 font-bold text-lg tracking-widest uppercase mb-3">
            <Fish className="w-5 h-5 text-gold-light" />
            Euromar SA
          </div>
          <p className="text-slate-400 text-sm leading-relaxed mb-4">
            {t.footer.location}
          </p>
          <p className="text-slate-500 text-xs">
            © {new Date().getFullYear()} Euromar SA. {t.footer.rights}
          </p>
        </div>

        <div>
          <h3 className="font-semibold text-gold-light mb-4 text-sm uppercase tracking-wider">
            Euromar
          </h3>
          <div className="space-y-2 text-sm text-slate-400">
            <Link href={`/${lang}/productos`} className="block hover:text-white transition-colors">
              {t.nav.products}
            </Link>
            <Link href={`/${lang}/servicios`} className="block hover:text-white transition-colors">
              {t.nav.services}
            </Link>
            <Link href={`/${lang}/nosotros`} className="block hover:text-white transition-colors">
              {t.nav.about}
            </Link>
            <Link href={`/${lang}/contacto`} className="block hover:text-white transition-colors">
              {t.nav.contact}
            </Link>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-gold-light mb-4 text-sm uppercase tracking-wider">
            {t.contact.direct_title}
          </h3>
          <div className="space-y-3 text-sm text-slate-400">
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4 shrink-0" />
              +54 223 421-7777
            </div>
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4 shrink-0" />
              +54 223 594-2314
            </div>
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4 shrink-0" />
              hpedeconi@euromar.com.ar
            </div>
            <a
              href="https://www.linkedin.com/company/euromar-sa"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 hover:text-white transition-colors"
            >
              <svg className="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              LinkedIn
            </a>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10 py-4 text-center text-xs text-slate-600">
        euromar.com.ar
      </div>
    </footer>
  );
}
