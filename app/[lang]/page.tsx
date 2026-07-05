import { notFound } from "next/navigation";
import Link from "next/link";
import {
  ArrowRight,
  Fish,
  Anchor,
  Globe,
  Shield,
  Waves,
  Droplets,
  UtensilsCrossed,
} from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const productIcons = [Fish, Waves, Droplets, UtensilsCrossed];

export default async function HomePage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isValidLang(lang)) notFound();
  const t = await getDictionary(lang as Lang);

  return (
    <div>
      {/* Hero */}
      <section className="relative bg-navy-900 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 50%, #1a3a6b 0%, transparent 50%), radial-gradient(circle at 80% 20%, #1e4d8c 0%, transparent 40%)",
          }}
        />
        <div className="relative max-w-6xl mx-auto px-4 py-28 md:py-36">
          <div className="max-w-2xl">
            <p className="flex items-center gap-2 text-gold-light text-sm font-semibold uppercase tracking-widest mb-5">
              <Fish className="w-4 h-4" />
              {t.hero.badge}
            </p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight tracking-tight">
              {t.hero.headline}
            </h1>
            <p className="text-lg md:text-xl text-slate-300 mb-10 leading-relaxed max-w-xl">
              {t.hero.sub}
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                href={`/${lang}/productos`}
                className="inline-flex items-center gap-2 bg-gold hover:bg-gold-light text-navy-900 font-bold px-7 py-3.5 rounded-lg transition-colors"
              >
                {t.hero.cta_products}
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                href={`/${lang}/contacto`}
                className="inline-flex items-center gap-2 border-2 border-white/40 hover:border-white text-white font-bold px-7 py-3.5 rounded-lg transition-colors"
              >
                {t.hero.cta_contact}
              </Link>
            </div>
          </div>
        </div>

        {/* Wave divider */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 60L60 50C120 40 240 20 360 15C480 10 600 20 720 28C840 36 960 40 1080 38C1200 36 1320 28 1380 24L1440 20V60H0Z" fill="#f8fafc" />
          </svg>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-slate-50 pt-6 pb-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 -mt-2">
            {[
              { value: "+45", label: t.stats.years, icon: Shield },
              { value: "4", label: t.stats.continents, icon: Globe },
              { value: "9", label: t.stats.services, icon: Anchor },
              { value: "3", label: t.stats.partners, icon: Fish },
            ].map((stat) => (
              <div
                key={stat.label}
                className="bg-white rounded-xl p-6 text-center shadow-sm border border-slate-100"
              >
                <stat.icon className="w-6 h-6 text-navy-700 mx-auto mb-2" />
                <div className="text-3xl font-bold text-navy-900">{stat.value}</div>
                <div className="text-sm text-slate-500 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Products preview */}
      <section className="py-20 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-navy-900 mb-3">
              {t.products.title}
            </h2>
            <p className="text-slate-500 max-w-xl mx-auto">{t.products.subtitle}</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {t.products.items.map((product, i) => {
              const Icon = productIcons[i];
              return (
                <div
                  key={product.name}
                  className="bg-white rounded-xl p-6 border border-slate-100 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all"
                >
                  <div className="w-12 h-12 rounded-lg bg-navy-900 flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-gold-light" />
                  </div>
                  <h3 className="font-bold text-navy-900 mb-2">{product.name}</h3>
                  <p className="text-sm text-slate-500 leading-relaxed">{product.desc}</p>
                </div>
              );
            })}
          </div>
          <div className="text-center mt-10">
            <Link
              href={`/${lang}/productos`}
              className="inline-flex items-center gap-2 text-navy-700 font-semibold hover:text-navy-900 transition-colors"
            >
              {t.products.cta} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Services strip */}
      <section className="py-20 bg-navy-900 text-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-3">{t.services.title}</h2>
            <p className="text-slate-400 max-w-xl mx-auto">{t.services.subtitle}</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {t.services.items.map((s) => (
              <div
                key={s.name}
                className="border border-white/10 rounded-lg px-5 py-4 hover:border-gold/40 hover:bg-white/5 transition-all"
              >
                <div className="w-2 h-2 rounded-full bg-gold-light mb-3" />
                <div className="font-semibold text-sm mb-1">{s.name}</div>
                <div className="text-slate-400 text-xs leading-relaxed">{s.desc}</div>
              </div>
            ))}
          </div>
          <div className="text-center mt-10">
            <Link
              href={`/${lang}/servicios`}
              className="inline-flex items-center gap-2 border border-gold/40 text-gold-light hover:bg-gold hover:text-navy-900 font-semibold px-6 py-3 rounded-lg transition-all"
            >
              {t.nav.services} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-white">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-navy-900 mb-4">
            {lang === "es" && "¿Listo para trabajar juntos?"}
            {lang === "en" && "Ready to work together?"}
            {lang === "zh" && "准备好合作了吗？"}
          </h2>
          <p className="text-slate-500 mb-8">
            {lang === "es" && "Contáctanos y te asesoramos sin compromiso sobre nuestros productos y servicios."}
            {lang === "en" && "Contact us and we'll advise you with no commitment about our products and services."}
            {lang === "zh" && "联系我们，我们将无偿为您提供产品和服务咨询。"}
          </p>
          <Link
            href={`/${lang}/contacto`}
            className="inline-flex items-center gap-2 bg-navy-900 hover:bg-navy-800 text-white font-bold px-8 py-4 rounded-lg transition-colors"
          >
            {t.nav.contact} <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}
