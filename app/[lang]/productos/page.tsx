import { notFound } from "next/navigation";
import { Fish, Waves, Droplets, UtensilsCrossed, MapPin, Calendar, Anchor, Shell } from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";

const CDN = "";
const icons = [Fish, Waves, Droplets, UtensilsCrossed];
const categoryPhotos = [
  `${CDN}/images/fish-merluza.jpg`,
  `${CDN}/images/productos-congelados-01-calamar-1-960x640.jpg`,
  `${CDN}/images/harina-pescado.jpg`,
  `${CDN}/images/productos-empanados-mar-02-bastones-merluza-1-960x640.jpg`,
];

type LangKey = "es" | "en" | "zh";

const speciesGroups: {
  category: Record<LangKey, string>;
  icon: typeof Fish;
  color: string;
  species: {
    name: string;
    nameEn: string;
    nameZh: string;
    scientific: string;
    desc: Record<LangKey, string>;
    zone: Record<LangKey, string>;
    season: string;
    method: Record<LangKey, string>;
    photo?: string;
  }[];
}[] = [
  {
    category: { es: "Pescados Blancos", en: "White Fish", zh: "白鱼类" },
    icon: Fish,
    color: "bg-navy-900",
    species: [
      {
        name: "Merluza",
        nameEn: "Hake",
        nameZh: "无须鳕",
        scientific: "Merluccius hubbsi",
        desc: { es: "Carne blanca, textura firme, sabor suave.", en: "White flesh, firm texture, mild flavor.", zh: "白肉，质地紧实，味道清淡。" },
        zone: { es: "Costas de Argentina", en: "Argentine coast", zh: "阿根廷沿海" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
        photo: `${CDN}/images/productos-congelados-04-merluza-1-960x640.jpg`,
      },
      {
        name: "Abadejo",
        nameEn: "Pink Cusk-eel",
        nameZh: "粉红穴鳗",
        scientific: "Genipterus blacodes",
        desc: { es: "Carne blanca, textura firme, buen gusto.", en: "White flesh, firm texture, good taste.", zh: "白肉，质地紧实，口感好。" },
        zone: { es: "Sur de Argentina", en: "Southern Argentina", zh: "阿根廷南部" },
        season: "Ago–Dic / Aug–Dec",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
        photo: `${CDN}/images/productos-congelados-05-abadejo-1-960x640.jpg`,
      },
      {
        name: "Corvina",
        nameEn: "Whitemouth Croaker",
        nameZh: "白口石首鱼",
        scientific: "Micropogonias furnieri",
        desc: { es: "Carne blanca, textura firme, sabor muy agradable.", en: "White flesh, firm texture, very pleasant flavor.", zh: "白肉，质地紧实，风味宜人。" },
        zone: { es: "Costa de Buenos Aires", en: "Buenos Aires coast", zh: "布宜诺斯艾利斯海岸" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
      {
        name: "Pescadilla",
        nameEn: "Striped Weakfish",
        nameZh: "条纹弱棘鱼",
        scientific: "Cynoscion striatus",
        desc: { es: "Carne blanca, textura firme, buen sabor.", en: "White flesh, firm texture, good flavor.", zh: "白肉，质地紧实，口味好。" },
        zone: { es: "Costas de Buenos Aires", en: "Buenos Aires coast", zh: "布宜诺斯艾利斯沿海" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre de fondo", en: "Bottom trawl", zh: "底拖网" },
      },
      {
        name: "Hoki",
        nameEn: "Hoki",
        nameZh: "长尾鳕",
        scientific: "Macruronus dactylopterus lahilllei",
        desc: { es: "Carne suave, agradable sabor.", en: "Soft flesh, pleasant flavor.", zh: "肉质柔软，风味怡人。" },
        zone: { es: "Costa Sur de Argentina", en: "Southern Argentine coast", zh: "阿根廷南部沿海" },
        season: "Jun–Sep (peak) / Todo el año",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
      {
        name: "Besugo",
        nameEn: "Red Porgy",
        nameZh: "红鲷",
        scientific: "Pagrus sedicem",
        desc: { es: "Carne blanca, textura firme, buen gusto.", en: "White flesh, firm texture, good taste.", zh: "白肉，质地紧实，口感好。" },
        zone: { es: "Costa de Buenos Aires", en: "Buenos Aires coast", zh: "布宜诺斯艾利斯海岸" },
        season: "Oct–Dic / Oct–Dec",
        method: { es: "Red de arrastre / trampa", en: "Trawl / trap", zh: "拖网/陷阱" },
      },
      {
        name: "Pez Palo",
        nameEn: "Brazilian Flathead",
        nameZh: "巴西鲬鱼",
        scientific: "Percophis brasiliensis",
        desc: { es: "Alargado, textura firme y sabor agradable.", en: "Elongated, firm texture, pleasant flavor.", zh: "细长，质地紧实，风味怡人。" },
        zone: { es: "Norte de Argentina y Sur de Brasil", en: "Northern Argentina & Southern Brazil", zh: "阿根廷北部与巴西南部" },
        season: "Oct–Feb",
        method: { es: "Red de arrastre de fondo", en: "Bottom trawl", zh: "底拖网" },
      },
      {
        name: "Raya",
        nameEn: "Skate / Ray",
        nameZh: "鳐鱼",
        scientific: "Raja spp.",
        desc: { es: "Carne blanca, textura firme, buen sabor.", en: "White flesh, firm texture, good flavor.", zh: "白肉，质地紧实，口味好。" },
        zone: { es: "Costas de Buenos Aires", en: "Buenos Aires coast", zh: "布宜诺斯艾利斯沿海" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
      {
        name: "Salmón Blanco",
        nameEn: "Peruvian Sandperch",
        nameZh: "秘鲁沙鲈",
        scientific: "Pseudopercis semifasciata",
        desc: { es: "Carne blanca, textura firme, abundante.", en: "White flesh, firm and abundant.", zh: "白肉，质地紧实，产量丰富。" },
        zone: { es: "Sur de Argentina", en: "Southern Argentina", zh: "阿根廷南部" },
        season: "Oct–Ene / Oct–Jan",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
      {
        name: "White Drum",
        nameEn: "Cuca / White Drum",
        nameZh: "白鼓鱼",
        scientific: "Plagioscion squamosissimus",
        desc: { es: "Carne blanca, textura firme, buen sabor.", en: "White flesh, firm texture, good flavor.", zh: "白肉，质地紧实，口味好。" },
        zone: { es: "Norte de Brasil", en: "Northern Brazil", zh: "巴西北部" },
        season: "Jul–Dic (peak) / Jul–Dec",
        method: { es: "Red de arrastre de fondo", en: "Bottom trawl", zh: "底拖网" },
      },
      {
        name: "Rape",
        nameEn: "Monkfish",
        nameZh: "安康鱼",
        scientific: "Lophius gastrophysus",
        desc: { es: "Carne suave, agradable sabor.", en: "Soft flesh, pleasant flavor.", zh: "肉质柔软，风味怡人。" },
        zone: { es: "Costa de Brasil", en: "Brazilian coast", zh: "巴西沿海" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
    ],
  },
  {
    category: { es: "Mariscos, Crustáceos y Moluscos", en: "Shellfish, Crustaceans & Mollusks", zh: "贝类、甲壳类与软体类" },
    icon: Shell,
    color: "bg-teal-700",
    species: [
      {
        name: "Langostinos Patagónicos",
        nameEn: "Argentine Red Shrimp",
        nameZh: "巴塔哥尼亚大虾",
        scientific: "Pleoticus muelleri",
        desc: { es: "El langostino silvestre más cotizado del Atlántico Sur. Sabor intenso, carne firme y color coral característico.", en: "The most prized wild shrimp of the South Atlantic. Intense flavor, firm flesh and characteristic coral color.", zh: "南大西洋最受追捧的野生对虾。风味浓郁，肉质紧实，呈标志性珊瑚色。" },
        zone: { es: "Patagonia Argentina", en: "Argentine Patagonia", zh: "阿根廷巴塔哥尼亚" },
        season: "Feb–Jun (peak) / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
        photo: `${CDN}/images/productos-empanados-mar-04-langostinos-empanados-960x640.jpg`,
      },
      {
        name: "Calamar Patagónico",
        nameEn: "Patagonian Squid",
        nameZh: "巴塔哥尼亚鱿鱼",
        scientific: "Illex argentinus",
        desc: { es: "Carne blanca y firme, ideal para anillas, tentáculos y productos elaborados. Uno de los moluscos de mayor volumen de exportación argentina.", en: "White and firm flesh, ideal for rings, tentacles and processed products. One of Argentina's highest-volume mollusk exports.", zh: "肉质白嫩紧实，适合制作鱿鱼圈、触须及精加工产品，是阿根廷出口量最大的软体动物之一。" },
        zone: { es: "Atlántico Sur argentino", en: "South Atlantic (Argentina)", zh: "阿根廷南大西洋" },
        season: "Feb–May (peak) / Year-round",
        method: { es: "Jigger / Red de arrastre", en: "Jigger / Trawl net", zh: "鱿鱼钩/拖网捕捞" },
        photo: `${CDN}/images/productos-congelados-01-calamar-1-960x640.jpg`,
      },
    ],
  },
  {
    category: { es: "Especies Premium", en: "Premium Species", zh: "优质鱼类" },
    icon: Anchor,
    color: "bg-navy-700",
    species: [
      {
        name: "Merluza Negra",
        nameEn: "Patagonian Toothfish",
        nameZh: "巴塔哥尼亚犬牙鱼",
        scientific: "Dissostichus eleginoides",
        desc: { es: "Carne suave, agradable sabor. Alta cotización internacional.", en: "Soft flesh, pleasant flavor. Highly valued internationally.", zh: "肉质柔软，风味怡人，国际市场价值极高。" },
        zone: { es: "Costa Sur de Sudamérica", en: "Southern South America", zh: "南美洲南部海域" },
        season: "Todo el año / Year-round",
        method: { es: "Pesca con palangre", en: "Longline fishing", zh: "延绳钓捕捞" },
      },
      {
        name: "Salmón Atlántico",
        nameEn: "Atlantic Salmon",
        nameZh: "大西洋鲑鱼",
        scientific: "Salmo salar sebago",
        desc: { es: "Carne roja, textura firme, sabor abundante.", en: "Red flesh, firm texture, rich flavor.", zh: "红肉，质地紧实，风味浓郁。" },
        zone: { es: "Sur de Chile", en: "Southern Chile", zh: "智利南部" },
        season: "Todo el año / Year-round",
        method: { es: "Criadero", en: "Fish farm", zh: "水产养殖" },
        photo: undefined,
      },
      {
        name: "Atún",
        nameEn: "Yellowfin Tuna",
        nameZh: "黄鳍金枪鱼",
        scientific: "Thunnus albacares",
        desc: { es: "Carne roja, textura firme, buen gusto.", en: "Red flesh, firm texture, good taste.", zh: "红肉，质地紧实，口感好。" },
        zone: { es: "Costa de Ecuador", en: "Ecuadorian coast", zh: "厄瓜多尔沿海" },
        season: "Todo el año / Year-round",
        method: { es: "Red de arrastre", en: "Trawl net", zh: "拖网捕捞" },
      },
      {
        name: "Trucha",
        nameEn: "Rainbow Trout",
        nameZh: "虹鳟鱼",
        scientific: "Oncorhynchus mykiss",
        desc: { es: "Carne roja/anaranjada, excelente sabor.", en: "Red/orange flesh, excellent flavor.", zh: "红/橙色肉，风味极佳。" },
        zone: { es: "Argentina y Chile", en: "Argentina & Chile", zh: "阿根廷与智利" },
        season: "Todo el año / Year-round",
        method: { es: "Criadero", en: "Fish farm", zh: "水产养殖" },
      },
      {
        name: "Mahi-Mahi",
        nameEn: "Dolphinfish / Mahi-Mahi",
        nameZh: "鲯鳅",
        scientific: "Coryphaena hippurus",
        desc: { es: "Textura firme, sabor suave y versátil.", en: "Firm texture, mild and versatile flavor.", zh: "质地紧实，味道清淡多变。" },
        zone: { es: "Centroamérica", en: "Central America", zh: "中美洲" },
        season: "Nov–Mar",
        method: { es: "Red de arrastre de fondo", en: "Bottom trawl", zh: "底拖网" },
      },
    ],
  },
  {
    category: { es: "Productos Apanados", en: "Breaded Products", zh: "裹粉制品" },
    icon: UtensilsCrossed,
    color: "bg-amber-700",
    species: [
      {
        name: "Bastones de Merluza",
        nameEn: "Hake Fish Sticks",
        nameZh: "无须鳕鱼棒",
        scientific: "Merluccius hubbsi — procesado",
        desc: { es: "Bastones de merluza rebozados, listos para freír. Crujientes por fuera, jugosos por dentro.", en: "Breaded hake sticks, ready to fry. Crispy on the outside, juicy inside.", zh: "裹粉无须鳕鱼棒，即炸即食，外脆里嫩。" },
        zone: { es: "Procesado en Mar del Plata", en: "Processed in Mar del Plata", zh: "马德普拉塔加工" },
        season: "Todo el año / Year-round",
        method: { es: "Captura + procesado en planta", en: "Wild caught + plant processed", zh: "野生捕捞 + 工厂加工" },
        photo: `${CDN}/images/productos-empanados-mar-02-bastones-merluza-1-960x640.jpg`,
      },
      {
        name: "Calamar Apanado",
        nameEn: "Breaded Squid",
        nameZh: "裹粉鱿鱼",
        scientific: "Illex argentinus — procesado",
        desc: { es: "Anillas y tiras de calamar patagónico apanadas. Textura única, sabor intenso.", en: "Breaded Patagonian squid rings and strips. Unique texture, intense flavor.", zh: "裹粉巴塔哥尼亚鱿鱼圈和条，口感独特，风味浓郁。" },
        zone: { es: "Procesado en Mar del Plata", en: "Processed in Mar del Plata", zh: "马德普拉塔加工" },
        season: "Todo el año / Year-round",
        method: { es: "Captura + procesado en planta", en: "Wild caught + plant processed", zh: "野生捕捞 + 工厂加工" },
        photo: `${CDN}/images/productos-empanados-mar-03-rabas-960x640.jpg`,
      },
      {
        name: "Filet Apanado",
        nameEn: "Breaded Fillet",
        nameZh: "裹粉鱼排",
        scientific: "Merluccius hubbsi — procesado",
        desc: { es: "Filet de merluza apanado en formato porción. Ideal para foodservice y retail.", en: "Portion-sized breaded hake fillet. Ideal for foodservice and retail.", zh: "份装裹粉无须鳕鱼排，适合餐饮服务和零售。" },
        zone: { es: "Procesado en Mar del Plata", en: "Processed in Mar del Plata", zh: "马德普拉塔加工" },
        season: "Todo el año / Year-round",
        method: { es: "Captura + procesado en planta", en: "Wild caught + plant processed", zh: "野生捕捞 + 工厂加工" },
        photo: `${CDN}/images/productos-empanados-mar-06-filet-merluza-a-la-romana-960x640.jpg`,
      },
      {
        name: "Formitas de Merluza",
        nameEn: "Hake Portions",
        nameZh: "无须鳕鱼排块",
        scientific: "Merluccius hubbsi — procesado",
        desc: { es: "Porciones de merluza apanadas en distintos formatos. Ideales para foodservice, catering y segmento infantil.", en: "Breaded hake portions in various formats. Ideal for foodservice, catering and the children's segment.", zh: "各式裹粉无须鳕鱼块，适合餐饮服务、外卖配餐及儿童市场。" },
        zone: { es: "Procesado en Mar del Plata", en: "Processed in Mar del Plata", zh: "马德普拉塔加工" },
        season: "Todo el año / Year-round",
        method: { es: "Captura + procesado en planta", en: "Wild caught + plant processed", zh: "野生捕捞 + 工厂加工" },
        photo: `${CDN}/images/productos-empanados-mar-05-formitas-de-merluza-960x640.jpg`,
      },
    ],
  },
];

const captureLabel: Record<LangKey, string> = {
  es: "Zona de captura",
  en: "Capture zone",
  zh: "捕获区域",
};
const seasonLabel: Record<LangKey, string> = {
  es: "Temporada",
  en: "Season",
  zh: "季节",
};
const methodLabel: Record<LangKey, string> = {
  es: "Método",
  en: "Method",
  zh: "方法",
};
const catalogTitle: Record<LangKey, string> = {
  es: "Catálogo Completo de Especies",
  en: "Full Species Catalog",
  zh: "完整鱼类目录",
};
const catalogSub: Record<LangKey, string> = {
  es: "Trabajamos con más de 15 especies del Atlántico Sur y el Pacífico. Todos los productos se adaptan a las especificaciones del cliente.",
  en: "We work with over 15 species from the South Atlantic and Pacific. All products are adapted to customer specifications.",
  zh: "我们经营来自南大西洋和太平洋的15余种鱼类，所有产品均可根据客户要求定制。",
};
const noteText: Record<LangKey, string> = {
  es: "* Las formas de packaging no son excluyentes. Todo producto puede adaptarse a las necesidades del cliente en cuanto a presentación, calibre y certificaciones.",
  en: "* Packaging formats are not exclusive. Every product can be adapted to the customer's needs in terms of presentation, size, and certifications.",
  zh: "* 包装形式不受限制。所有产品均可根据客户在产品规格、尺寸和认证方面的要求进行调整。",
};

export default async function ProductosPage({
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
      {/* Page header */}
      <section className="bg-navy-900 text-white py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-3">{t.products.title}</h1>
          <p className="text-slate-300 max-w-xl">{t.products.subtitle}</p>
        </div>
      </section>

      {/* Main product categories with photos */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {t.products.items.map((product, i) => {
              const Icon = icons[i];
              return (
                <div
                  key={product.name}
                  className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-0.5 transition-all group"
                >
                  {/* Photo header */}
                  <div className="relative h-52 overflow-hidden">
                    <img
                      src={categoryPhotos[i]}
                      alt={product.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-navy-900/85 via-navy-900/40 to-transparent" />
                    <div className="absolute bottom-0 left-0 right-0 p-5 flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-white/15 backdrop-blur-sm border border-white/20 flex items-center justify-center shrink-0">
                        <Icon className="w-5 h-5 text-gold-light" />
                      </div>
                      <h2 className="text-lg font-bold text-white leading-tight">{product.name}</h2>
                    </div>
                  </div>
                  <div className="p-6">
                    <p className="text-slate-600 leading-relaxed mb-4 text-sm">{product.desc}</p>
                    <div className="inline-flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-sm text-slate-600">
                      <span className="w-2 h-2 rounded-full bg-gold-light shrink-0" />
                      {product.detail}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Full species catalog */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-bold text-navy-900 mb-3">
              {catalogTitle[l]}
            </h2>
            <p className="text-slate-500 max-w-2xl mx-auto">{catalogSub[l]}</p>
          </div>

          <div className="space-y-14">
            {speciesGroups.map((group) => {
              const GroupIcon = group.icon;
              return (
                <div key={group.category.es}>
                  {/* Group header */}
                  <div className="flex items-center gap-3 mb-6">
                    <div className={`${group.color} w-10 h-10 rounded-lg flex items-center justify-center`}>
                      <GroupIcon className="w-5 h-5 text-gold-light" />
                    </div>
                    <h3 className="text-2xl font-bold text-navy-900">{group.category[l]}</h3>
                    <div className="flex-1 h-px bg-slate-200 ml-2" />
                    <span className="text-sm text-slate-400 font-medium">
                      {group.species.length} {l === "es" ? "especies" : l === "en" ? "species" : "种"}
                    </span>
                  </div>

                  {/* Species grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {group.species.map((sp) => (
                      <div
                        key={sp.scientific}
                        className="bg-slate-50 border border-slate-100 rounded-xl overflow-hidden hover:border-navy-300 hover:shadow-sm transition-all"
                      >
                        {/* Photo (if available) */}
                        {sp.photo && (
                          <div className="relative h-40 overflow-hidden">
                            <img
                              src={sp.photo}
                              alt={sp.name}
                              className="w-full h-full object-cover"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-navy-900/70 via-transparent to-transparent" />
                            <div className="absolute bottom-0 left-0 right-0 px-4 py-3">
                              <div className="font-bold text-white text-sm leading-tight">
                                {l === "es" ? sp.name : l === "en" ? sp.nameEn : sp.nameZh}
                              </div>
                              <div className="text-xs italic text-white/60 mt-0.5">{sp.scientific}</div>
                            </div>
                          </div>
                        )}

                        <div className="p-5">
                          {/* Name (only when no photo) */}
                          {!sp.photo && (
                            <div className="mb-3">
                              <div className="font-bold text-navy-900 text-base">
                                {l === "es" ? sp.name : l === "en" ? sp.nameEn : sp.nameZh}
                              </div>
                              <div className="text-xs italic text-slate-400 mt-0.5">{sp.scientific}</div>
                              {l !== "es" && (
                                <div className="text-xs text-slate-500 mt-0.5">{sp.name}</div>
                              )}
                            </div>
                          )}
                          {/* Alt name when photo shows main name */}
                          {sp.photo && l !== "es" && (
                            <div className="text-xs text-slate-400 mb-2">{sp.name}</div>
                          )}

                          {/* Description */}
                          <p className="text-sm text-slate-600 leading-relaxed mb-4">
                            {sp.desc[l]}
                          </p>

                          {/* Meta info */}
                          <div className="space-y-1.5">
                            <div className="flex items-start gap-2 text-xs text-slate-500">
                              <MapPin className="w-3.5 h-3.5 mt-0.5 shrink-0 text-navy-400" />
                              <span>{sp.zone[l]}</span>
                            </div>
                            <div className="flex items-start gap-2 text-xs text-slate-500">
                              <Calendar className="w-3.5 h-3.5 mt-0.5 shrink-0 text-navy-400" />
                              <span>{sp.season}</span>
                            </div>
                            <div className="flex items-start gap-2 text-xs text-slate-500">
                              <Waves className="w-3.5 h-3.5 mt-0.5 shrink-0 text-navy-400" />
                              <span>{sp.method[l]}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Note */}
          <div className="mt-12 p-5 bg-slate-50 border border-slate-200 rounded-xl">
            <p className="text-sm text-slate-500 leading-relaxed">{noteText[l]}</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-12 bg-navy-900 text-white">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <Fish className="w-10 h-10 text-gold-light mx-auto mb-4" />
          <p className="text-slate-300 text-lg leading-relaxed">
            {l === "es" && "Todos nuestros productos pueden adaptarse a las especificaciones y requerimientos de tu mercado. Contáctanos para más información."}
            {l === "en" && "All our products can be adapted to your market's specifications and requirements. Contact us for more information."}
            {l === "zh" && "我们所有产品均可根据您市场的规格和要求进行定制。请联系我们了解更多信息。"}
          </p>
        </div>
      </section>
    </div>
  );
}
