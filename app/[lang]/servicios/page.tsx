import { notFound } from "next/navigation";
import {
  Anchor,
  FileCheck,
  CheckCircle,
  TrendingUp,
  Truck,
  Settings,
  Package,
  Search,
  Thermometer,
} from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const serviceIcons = [
  Anchor,
  FileCheck,
  CheckCircle,
  TrendingUp,
  Truck,
  Settings,
  Package,
  Search,
  Thermometer,
];

export default async function ServiciosPage({
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
          <h1 className="text-4xl font-bold mb-3">{t.services.title}</h1>
          <p className="text-slate-300 max-w-xl">{t.services.subtitle}</p>
        </div>
      </section>

      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {t.services.items.map((service, i) => {
              const Icon = serviceIcons[i];
              return (
                <div
                  key={service.name}
                  className="bg-white rounded-xl p-6 border border-slate-100 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all"
                >
                  <div className="w-12 h-12 rounded-lg bg-navy-900 flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-gold-light" />
                  </div>
                  <h3 className="font-bold text-navy-900 mb-2">{service.name}</h3>
                  <p className="text-sm text-slate-500 leading-relaxed">{service.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-navy-900 mb-4">
            {lang === "es" ? "Servicio integral de exportación" : lang === "zh" ? "全程出口服务" : lang === "ar" ? "خدمة تصدير متكاملة" : lang === "fr" ? "Service d'exportation complet" : lang === "nl" ? "Volledig exportpakket" : "Full export service"}
          </h2>
          <p className="text-slate-500 leading-relaxed">
            {lang === "es" ? "Cada servicio puede contratarse de forma independiente o como parte de un paquete completo. Adaptamos nuestra operación a las necesidades de cada cliente y mercado." : lang === "zh" ? "每项服务可单独订购，也可作为完整套餐的一部分。我们根据每位客户和市场的需求调整我们的运营方式。" : lang === "ar" ? "يمكن الاستعانة بكل خدمة بشكل مستقل أو ضمن حزمة متكاملة. نكيّف عملياتنا وفقاً لاحتياجات كل عميل وسوق." : lang === "fr" ? "Chaque service peut être contracté indépendamment ou dans le cadre d'un forfait complet. Nous adaptons notre opération aux besoins de chaque client et marché." : lang === "nl" ? "Elke dienst kan onafhankelijk of als onderdeel van een volledig pakket worden afgenomen. Wij passen onze werkwijze aan op de behoeften van elke klant en markt." : "Each service can be contracted independently or as part of a complete package. We adapt our operation to the needs of each client and market."}
          </p>
        </div>
      </section>
    </div>
  );
}
