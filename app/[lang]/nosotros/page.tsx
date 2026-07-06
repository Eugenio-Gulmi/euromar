import { notFound } from "next/navigation";
import { Shield, Globe, CheckCircle, Handshake } from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const CDN = "";

const valueIcons = [Shield, Globe, CheckCircle, Handshake];

type LangKey = "es" | "en" | "zh";

const team = [
  {
    name: "Hugo Pedeconi",
    photo: `${CDN}/images/hugo-pedeconi.jpg`,
    role: {
      es: "Presidente",
      en: "President",
      zh: "总裁",
    },
    bio: {
      es: "Más de 43 años al frente de Euromar S.A. Licenciado en Comercio Exterior, Hugo es uno de los referentes históricos del sector pesquero argentino. Especialista en intermediación y bróker de pesca, con foco principal en las pesquerías del Atlántico Sur. Su trayectoria abarca desde la gestión operativa en planta hasta la negociación directa con armadores, frigoríficos y compradores internacionales.",
      en: "Over 43 years leading Euromar S.A. With a degree in Foreign Trade, Hugo is one of Argentina's most experienced figures in the fishing industry. A specialist in fishing brokerage and intermediation, with a primary focus on South Atlantic fisheries. His career spans from plant operations management to direct negotiation with shipowners, cold-storage plants, and international buyers.",
      zh: "在欧罗马公司任职超过43年。毕业于对外贸易专业，Hugo是阿根廷渔业领域最具经验的人士之一。专注于南大西洋渔业的渔业经纪与中介业务，拥有从工厂运营管理到直接与船东、冷藏工厂及国际买家谈判的丰富经历。",
    },
    langs: null,
    detail: {
      es: "Especialista en Atlántico Sur · Desde 1983",
      en: "South Atlantic Expert · Since 1983",
      zh: "南大西洋专家 · 自1983年",
    },
  },
  {
    name: "Luciano Gulminelli",
    photo: `${CDN}/images/luciano-gulminelli.jpg`,
    role: {
      es: "Export Manager",
      en: "Export Manager",
      zh: "出口经理",
    },
    bio: {
      es: "Licenciado en Comercio Internacional, Luciano acumuló años de experiencia viviendo y trabajando en Brasil y en Shanghai, China — dos de los mercados estratégicos clave para la exportación pesquera argentina. En Brasil consolidó relaciones comerciales con importadores y distribuidores de la región; en Shanghai profundizó su conocimiento de las cadenas de distribución asiáticas y la cultura de negocios china. Habla con fluidez español, inglés, mandarín, portugués e italiano, convirtiéndose en el nexo directo de Euromar con compradores de cuatro continentes.",
      en: "With a degree in International Trade, Luciano built years of experience living and working in both Brazil and Shanghai, China — two of the most strategic markets for Argentine seafood exports. In Brazil he established strong commercial relationships with regional importers and distributors; in Shanghai he developed an in-depth understanding of Asian distribution chains and Chinese business culture. He speaks Spanish, English, Mandarin, Portuguese and Italian fluently, making him Euromar's direct link to buyers across four continents.",
      zh: "Luciano拥有国际贸易学位，曾在巴西和中国上海两地生活和工作多年——这两个地区都是阿根廷水产出口的战略核心市场。在巴西，他与当地进口商和分销商建立了深厚的商业关系；在上海，他深入掌握了亚洲分销链和中国商业文化。他流利掌握西班牙语、英语、普通话、葡萄牙语和意大利语，是欧罗马公司连接四大洲买家的直接纽带。",
    },
    langs: [
      { flag: "🇦🇷", label: "Español" },
      { flag: "🇬🇧", label: "English" },
      { flag: "🇨🇳", label: "中文" },
      { flag: "🇧🇷", label: "Português" },
      { flag: "🇮🇹", label: "Italiano" },
    ],
    detail: {
      es: "Shanghai · Brasil · 5 idiomas",
      en: "Shanghai · Brazil · 5 languages",
      zh: "上海 · 巴西 · 5种语言",
    },
  },
];

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
  const l = lang as LangKey;

  return (
    <div>
      <section className="relative bg-navy-900 text-white py-24 overflow-hidden">
        <img
          src="/images/edi-libedinsky-kSG7nXDxZ_E-unsplash.jpg"
          alt="Puerto de Mar del Plata"
          className="absolute inset-0 w-full h-full object-cover opacity-30"
        />
        <div className="relative max-w-6xl mx-auto px-4">
          <p className="text-gold-light text-sm font-semibold uppercase tracking-widest mb-3">
            1975 →{" "}
            {lang === "es" ? "hoy" : lang === "en" ? "today" : "至今"}
          </p>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">{t.about.title}</h1>
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

      {/* Team */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-navy-900 mb-10 text-center">
            {l === "es" ? "Nuestro Equipo" : l === "en" ? "Our Team" : "我们的团队"}
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {team.map((member) => (
              <div key={member.name} className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100">
                {/* Header with photo */}
                <div className="flex items-center gap-5 p-6 border-b border-slate-100">
                  <img
                    src={member.photo}
                    alt={member.name}
                    className="w-20 h-20 rounded-full object-cover object-top border-2 border-slate-200 shrink-0"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-navy-900 text-lg">{member.name}</div>
                    <div className="text-sm text-gold-light font-semibold mb-2">{member.role[l]}</div>
                    {member.langs && (
                      <div className="flex items-center gap-1.5 flex-wrap">
                        {member.langs.map((fl) => (
                          <span key={fl.label} title={fl.label} className="text-xl leading-none" aria-label={fl.label}>
                            {fl.flag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                {/* Bio */}
                <div className="p-6">
                  <p className="text-slate-600 text-sm leading-relaxed mb-4">{member.bio[l]}</p>
                  <div className="inline-flex items-center gap-2 bg-navy-900/5 border border-navy-900/10 rounded-lg px-3 py-1.5 text-xs text-navy-700 font-medium">
                    <span className="w-1.5 h-1.5 rounded-full bg-gold-light shrink-0" />
                    {member.detail[l]}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-16 bg-white">
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
