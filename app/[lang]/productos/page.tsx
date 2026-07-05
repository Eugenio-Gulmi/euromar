import { notFound } from "next/navigation";
import { Fish, Waves, Droplets, UtensilsCrossed } from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const icons = [Fish, Waves, Droplets, UtensilsCrossed];
const bgColors = [
  "bg-navy-900",
  "bg-navy-800",
  "bg-navy-700",
  "bg-navy-600",
];

export default async function ProductosPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isValidLang(lang)) notFound();
  const t = await getDictionary(lang as Lang);

  return (
    <div>
      {/* Page header con foto de langostinos */}
      <section className="relative bg-navy-900 text-white py-20 overflow-hidden">
        <img
          src="/images/head-productos.jpg"
          alt="Productos del mar"
          className="absolute inset-0 w-full h-full object-cover opacity-35"
        />
        <div className="relative max-w-6xl mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-3">{t.products.title}</h1>
          <p className="text-slate-300 max-w-xl">{t.products.subtitle}</p>
        </div>
      </section>

      {/* Products grid */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {t.products.items.map((product, i) => {
              const Icon = icons[i];
              return (
                <div
                  key={product.name}
                  className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100 hover:shadow-md transition-shadow"
                >
                  <div className={`${bgColors[i]} p-8 flex items-center gap-4`}>
                    <div className="w-14 h-14 rounded-xl bg-white/10 flex items-center justify-center">
                      <Icon className="w-8 h-8 text-gold-light" />
                    </div>
                    <h2 className="text-xl font-bold text-white">{product.name}</h2>
                  </div>
                  <div className="p-8">
                    <p className="text-slate-600 leading-relaxed mb-4">{product.desc}</p>
                    <div className="inline-flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-sm text-slate-600">
                      <span className="w-2 h-2 rounded-full bg-gold-light" />
                      {product.detail}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Note about custom orders */}
      <section className="py-12 bg-navy-900 text-white">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <Fish className="w-10 h-10 text-gold-light mx-auto mb-4" />
          <p className="text-slate-300 text-lg leading-relaxed">
            {lang === "es" && "Todos nuestros productos pueden adaptarse a las especificaciones y requerimientos de tu mercado. Contáctanos para más información."}
            {lang === "en" && "All our products can be adapted to your market's specifications and requirements. Contact us for more information."}
            {lang === "zh" && "我们所有产品均可根据您市场的规格和要求进行定制。请联系我们了解更多信息。"}
          </p>
        </div>
      </section>
    </div>
  );
}
