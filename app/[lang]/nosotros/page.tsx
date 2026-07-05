import { notFound } from "next/navigation";
import { Shield, Globe, CheckCircle, Handshake } from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const valueIcons = [Shield, Globe, CheckCircle, Handshake];

const partners = [
  {
    name: "Interocean Brokerage LLC",
    country: "🇺🇸 United States",
    desc: {
      es: "Representación exclusiva en el mercado norteamericano. Gestionamos compras desde Argentina, Chile, Uruguay, Ecuador, Brasil y Perú.",
      en: "Exclusive representation in the North American market. We manage purchases from Argentina, Chile, Uruguay, Ecuador, Brazil and Peru.",
      zh: "北美市场的独家代理。我们管理来自阿根廷、智利、乌拉圭、厄瓜多尔、巴西和秘鲁的采购。",
    },
  },
  {
    name: "Sudamgel S.A.R.L",
    country: "🇫🇷 France / Europa",
    desc: {
      es: "Socio estratégico para el mercado europeo, con presencia en Francia y distribución en toda Europa.",
      en: "Strategic partner for the European market, with presence in France and distribution across Europe.",
      zh: "欧洲市场的战略合作伙伴，在法国设有业务并覆盖整个欧洲的分销网络。",
    },
  },
  {
    name: "Ayamo Global Foods",
    country: "🇧🇷 Brazil",
    desc: {
      es: "Alianza para la comercialización de pescados y harinas en el mercado brasileño.",
      en: "Alliance for the commercialization of fish and fish meal in the Brazilian market.",
      zh: "在巴西市场销售鱼类和鱼粉的合作联盟。",
    },
  },
];

export default async function NosotrosPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isValidLang(lang)) notFound();
  const t = await getDictionary(lang as Lang);

  return (
    <div>
      <section className="bg-navy-900 text-white py-16">
        <div className="max-w-6xl mx-auto px-4">
          <p className="text-gold-light text-sm font-semibold uppercase tracking-widest mb-3">
            1975 →{" "}
            {lang === "es" ? "hoy" : lang === "en" ? "today" : "至今"}
          </p>
          <h1 className="text-4xl font-bold mb-3">{t.about.title}</h1>
          <p className="text-slate-300 max-w-xl">{t.about.subtitle}</p>
        </div>
      </section>

      {/* Main text */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 space-y-6 text-slate-600 leading-relaxed text-lg">
          <p>{t.about.body}</p>
          <p>{t.about.body2}</p>
        </div>
      </section>

      {/* Values */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-navy-900 mb-10 text-center">
            {t.about.values_title}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {t.about.values.map((v, i) => {
              const Icon = valueIcons[i];
              return (
                <div key={v.title} className="text-center">
                  <div className="w-14 h-14 rounded-full bg-navy-900 flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-7 h-7 text-gold-light" />
                  </div>
                  <h3 className="font-bold text-navy-900 mb-2">{v.title}</h3>
                  <p className="text-sm text-slate-500 leading-relaxed">{v.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Partners */}
      <section className="py-16 bg-navy-900 text-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-2xl font-bold mb-10 text-center">
            {t.about.partners_title}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {partners.map((p) => (
              <div
                key={p.name}
                className="border border-white/10 rounded-xl p-6 hover:border-gold/30 hover:bg-white/5 transition-all"
              >
                <div className="text-sm text-slate-400 mb-2">{p.country}</div>
                <h3 className="font-bold text-lg mb-3">{p.name}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  {p.desc[lang as "es" | "en" | "zh"]}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
