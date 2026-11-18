"""Prompts científicos para las fotos de euromar.com.ar (versión B, noviembre 2026).

Cada prompt sale de una ficha de FishBase / SeaLifeBase (morfología y color tal como
los publica la fuente) más la anatomía general de la familia. Ninguna foto ajena se usa
como entrada: todo es texto a imagen.

Fuentes: fishbase.se/summary/<Genero-especie>.html, consultadas el 10-nov-2026.
"""

ESTILO = (
    "Displayed on crushed ice on a dark charcoal slate surface, three-quarter overhead angle, "
    "soft natural side light, true-to-life muted colours, wet skin with fine water droplets, "
    "sharp focus, documentary seafood-market photography, anatomically accurate proportions, "
    "no props, no garnish, no hands, no text, no logos, no watermark."
)

ESTILO_PRODUCTO = (
    "On a dark charcoal slate surface, three-quarter overhead angle, soft natural side light, "
    "true-to-life colours, sharp focus, clean commercial frozen-seafood product photography, "
    "no props, no garnish, no sauces, no hands, no text, no logos, no packaging, no watermark."
)

MERLUZA = (
    "Argentine hake (Merluccius hubbsi): elongated body with oval cross-section; large head about a "
    "quarter of body length; large terminal mouth with the lower jaw slightly projecting; two separate "
    "dorsal fins, a short triangular first dorsal and a long low second dorsal running towards the tail, "
    "mirrored underneath by a long anal fin; short pectoral fins not reaching the anal fin; truncate tail "
    "fin, not forked. Colour: silvery with a subtle golden lustre along the back, silvery-white belly; "
    "fine scales."
)

FOTOS = [
    # --- Página de inicio: reemplazan fotos de terceros ---------------------------------
    {"archivo": "fish-merluza.jpg", "motivo": "foto de otra marca (inicio y productos)",
     "fuente": "FishBase Merluccius hubbsi",
     "prompt": "One whole Argentine hake about 50 cm long lying beside four skinless, boneless white "
               f"hake fillets with a thin frost glaze (individually quick frozen). {MERLUZA} {ESTILO}"},
    {"archivo": "langostinos-inicio.jpg", "motivo": "reemplaza langostinos.avif (bajado, y mostraba rebozados)",
     "fuente": "SeaLifeBase Pleoticus muelleri",
     "prompt": "A generous pile of whole raw Argentine red shrimp (Pleoticus muelleri), 15 to 18 cm long, "
               "head-on and shell-on, every shrimp different in size, curl and position, some overlapping, a few antennae broken, no two alike, with the characteristic deep pinkish-red colour that this species has "
               "even when raw, long slender antennae, segmented abdomen, light frost glaze. "
               f"{ESTILO}"},
    {"archivo": "harina-pescado.jpg", "motivo": "foto bajada de la web",
     "fuente": "—",
     "prompt": "A neat conical heap of fish meal, a fine granular powder in light brown to golden-brown "
               "tones, with a small clear laboratory glass beaker of amber fish oil beside it. Raw-material "
               f"product photography for an industrial feed and aquaculture buyer. {ESTILO_PRODUCTO}"},
    {"archivo": "apanados-bastones.jpg", "motivo": "foto bajada de otra marca",
     "fuente": "—",
     "prompt": "Breaded hake fish sticks, evenly shaped rectangular bars with a fine golden-brown crumb "
               "coating, arranged in a neat row, one stick cut open to show the flaky white hake flesh "
               f"inside. {ESTILO_PRODUCTO}"},
    {"archivo": "atun.jpg", "motivo": "foto de stock sin origen claro",
     "fuente": "FishBase Thunnus albacares",
     "prompt": "One whole yellowfin tuna (Thunnus albacares) about 120 cm long and, beside it, one thick "
               "cross-section steak with deep ruby-red flesh. Fusiform, torpedo-shaped body; long sickle-"
               "shaped second dorsal and anal fins in bright yellow; a row of small bright yellow finlets "
               "with narrow black edges between those fins and the tail; crescent-shaped tail. Colour: "
               "metallic dark blue back changing through a yellow band to a silver belly crossed by about "
               f"twenty broken near-vertical lines. {ESTILO}"},
    # --- Especies mal representadas ------------------------------------------------------
    {"archivo": "merluza.jpg", "motivo": "producto principal: precisión",
     "fuente": "FishBase Merluccius hubbsi",
     "prompt": f"One whole Argentine hake about 50 cm long. {MERLUZA} {ESTILO}"},
    {"archivo": "abadejo.jpg", "motivo": "parecía una trucha",
     "fuente": "FishBase Genypterus blacodes",
     "prompt": "One whole pink cusk-eel, abadejo (Genypterus blacodes), about 90 cm long. Eel-like, very "
               "elongated, laterally compressed body tapering to a point; a single long low dorsal fin and a "
               "long anal fin run along the back and belly and merge with the small pointed tail, with no "
               "separate tail fin; pelvic fins reduced to a pair of thin filaments under the throat; small "
               "eye, rounded snout. Colour: pinkish-yellow body marbled with irregular reddish-brown "
               f"blotches on the back and upper sides, paler belly, smooth skin. {ESTILO}"},
    {"archivo": "mahi-mahi.jpg", "motivo": "parecía un jurel",
     "fuente": "FishBase Coryphaena hippurus",
     "prompt": "One whole mahi-mahi, dolphinfish (Coryphaena hippurus), a mature male about 100 cm long. "
               "Elongated, laterally compressed body tapering towards the tail; a prominent bony crest at "
               "the front of the head giving a steep, almost vertical blunt forehead; one single long dorsal "
               "fin starting right above the eye and running almost to the deeply forked tail. Colour: "
               "metallic blue-green back, silver sides with a golden sheen and scattered dark spots, dark "
               f"dorsal and anal fins, tail silvery with a golden sheen. {ESTILO}"},
    {"archivo": "salmon-blanco.jpg", "motivo": "salía plateado liso",
     "fuente": "FishBase Pseudopercis semifasciata",
     "prompt": "One whole Argentine sandperch, salmón blanco (Pseudopercis semifasciata), about 60 cm long. "
               "Robust, elongated fusiform body; large head and mouth. The colour pattern is essential: "
               "pale brown body crossed by several dark brown vertical and horizontal stripes made of dark "
               "brown blotches; a row of dark brown blotches along the middle of the dorsal fin; an obvious "
               f"black blotch at the base of the upper lobe of the tail fin; lighter belly. {ESTILO}"},
    {"archivo": "salmon-atlantico.jpg", "motivo": "el corte salía gris",
     "fuente": "conocimiento general (Salmo salar)",
     "prompt": "One whole Atlantic salmon (Salmo salar) about 70 cm long and, beside it, one thick cross-"
               "section steak showing bright orange-pink flesh with fine white fat lines. Streamlined body, "
               "small adipose fin, slightly forked tail; steel-blue to silver back with scattered small black "
               f"X-shaped spots above the lateral line, silver sides, white belly. {ESTILO}"},
    {"archivo": "hoki.jpg", "motivo": "pez plateado genérico",
     "fuente": "FishBase Macruronus magellanicus",
     "prompt": "One whole Patagonian grenadier, hoki or merluza de cola (Macruronus magellanicus), about 80 cm "
               "long. Long, laterally compressed body that tapers gradually into a long, pointed, whip-like "
               "tail; the very long second dorsal fin and the long anal fin run all the way back and merge "
               "into the tapering tail, with no separate tail fin; short first dorsal fin; large eye; large "
               "mouth with a blackish lining. Colour: purplish-blue back, silvery belly with a slight bluish "
               f"tinge. {ESTILO}"},
    {"archivo": "besugo.jpg", "motivo": "prompt con especie inexistente (Pagrus sedicem)",
     "fuente": "FishBase Pagrus pagrus",
     "prompt": "One whole red porgy, besugo (Pagrus pagrus), about 35 cm long. Oval, moderately deep, "
               "compressed body; convex head profile, slightly steeper in front of the eye; spiny dorsal fin. "
               "Colour: pink with silvery reflections, lighter on the belly; head darker from the nape to the "
               "angle of the mouth; fine blue dots on the upper sides; tail fin dark pink with both tips "
               f"white. {ESTILO}"},
]

# --- Segunda tanda (10-nov-2026): resto de especies y apanados -----------------------------
FOTOS += [
    {"archivo": "corvina.jpg", "motivo": "salía plateada lisa", "fuente": "FishBase Micropogonias furnieri",
     "prompt": "One whole whitemouth croaker, corvina rubia (Micropogonias furnieri), about 50 cm long. Moderately "
               "deep, elongated body with arched back; inferior mouth with a row of small chin barbels; long "
               "continuous dorsal fin with a deep notch between the spiny and soft parts; rounded-truncate tail. "
               "Colour: silvery body with a golden cast, greyish back, with distinct oblique dark streaks following "
               f"the scale rows from the back to well below the lateral line; yellowish pelvic and anal fins. {ESTILO}"},
    {"archivo": "pescadilla.jpg", "motivo": "pez plateado genérico", "fuente": "FishBase Cynoscion guatucupa",
     "prompt": "One whole striped weakfish, pescadilla de red (Cynoscion guatucupa), about 45 cm long. Slender "
               "fusiform body; pointed snout; large oblique mouth with the lower jaw projecting and one or two "
               "prominent canine teeth at the tip of the upper jaw; dorsal fin deeply notched; tail slightly "
               "pointed (rhomboid). Colour: bluish-grey back with faint oblique dark lines along the scale rows, "
               f"bright silvery sides and belly, yellowish pelvic and anal fins. {ESTILO}"},
    {"archivo": "pez-palo.jpg", "motivo": "forma poco fiel", "fuente": "FishBase Percophis brasiliensis",
     "prompt": "One whole Brazilian flathead, pez palo (Percophis brasiliensis), about 55 cm long. Very elongated, "
               "almost cylindrical body; long, strongly depressed, flat head with a long snout like a crocodile's; "
               "large mouth with the lower jaw projecting and visible fang-like teeth; eyes on top of the head; a "
               "short spiny first dorsal fin followed by a very long soft second dorsal fin, mirrored by a very long "
               "anal fin; truncate tail. Colour: light brownish-olive back with small dark brown spots and "
               f"blotches, pale cream belly. {ESTILO}"},
    {"archivo": "raya.jpg", "motivo": "parecía una mantarraya", "fuente": "FishBase Zearaja chilensis",
     "prompt": "One whole yellownose skate, raya (Zearaja chilensis), about 80 cm long, seen from above. Broad "
               "rhomboid disc with angular outer corners; long, pointed, slightly translucent snout; small eyes on "
               "top with spiracles behind them; a long slender tail with a row of small thorns and two small dorsal "
               "fins near its tip, no stinging spine. Colour: plain brownish-grey upper side with a few small "
               f"lighter spots and one irregular dark reddish-purple eye-spot in the middle of each wing. {ESTILO}"},
    {"archivo": "white-drum.jpg", "motivo": "pez plateado genérico", "fuente": "FishBase Plagioscion squamosissimus",
     "prompt": "One whole South American silver croaker, white drum (Plagioscion squamosissimus), about 45 cm "
               "long. Fusiform body with oval cross-section; terminal oblique mouth; long dorsal fin with a deep "
               "notch between spiny and soft parts; pointed-rhomboid tail with the scaled body extending into it; "
               "rear edge of the gill cover slightly toothed. Colour: uniform silvery with a greyish back and a "
               f"distinct black spot at the base of each pectoral fin. {ESTILO}"},
    {"archivo": "rape.jpg", "motivo": "no se entendía qué era", "fuente": "FishBase Lophius gastrophysus",
     "prompt": "One whole blackfin goosefish, rape (Lophius gastrophysus), about 60 cm long, next to "
               "ONE skinned monkfish tail (cola de rape) lying beside it. The tail is a thick, rounded, cone-shaped "
               "piece of firm white flesh about 25 cm long, wide at the cut end and tapering to the back, with a thin "
               "translucent grey-purple membrane in patches, and the round cut face showing the single thick central "
               "cartilage backbone; NO fins, NO skin, NOT a flat fillet. Enormous, broad, flattened head making up most of the body; huge "
               "wide mouth with rows of long needle-like inward-pointing teeth and a fringe of small skin flaps "
               "along the jaws; a thin fishing-rod spine (illicium) on top of the snout; wide fan-like pectoral "
               "fins; body tapering quickly to a short tail. Colour: mottled brown upper side, pale underside, "
               f"dark-tipped dorsal fin. {ESTILO}"},
    {"archivo": "langostino.jpg", "motivo": "filas clonadas (IA)", "fuente": "SeaLifeBase Pleoticus muelleri",
     "prompt": "Frozen raw Argentine red shrimp (Pleoticus muelleri), head-on and shell-on, packed in an open plain "
               "unprinted waxed cardboard export box seen from above at an angle: shrimp layered by hand in loose "
               "overlapping rows, each one slightly different in size (13 to 18 cm), curl and colour, deep "
               "pinkish-red even raw, darker heads, long antennae partly broken, covered by a thin uneven ice "
               "glaze with white frost; two loose shrimp lying on the surface beside the box. Wholesale frozen "
               f"seafood. {ESTILO_PRODUCTO}"},
    {"archivo": "calamar.jpg", "motivo": "tubos poco naturales", "fuente": "FishBase/SeaLifeBase Illex argentinus",
     "prompt": "One whole Argentine shortfin squid (Illex argentinus), mantle about 25 cm long, next to two "
               "cleaned white squid tubes of different sizes. Long, slender, cylindrical mantle tapering to a point, with a short "
               "rhomboid (diamond-shaped) pair of fins at the tail end; large eyes; eight arms and two longer "
               "tentacles with suckers. Colour: reddish-brown to purplish skin densely covered with tiny dark "
               f"chromatophore dots, paler on the underside; white glossy flesh on the cleaned tubes. {ESTILO}"},
    {"archivo": "merluza-negra.jpg", "motivo": "muy oscura, sin detalle", "fuente": "FishBase Dissostichus eleginoides",
     "prompt": "One whole Patagonian toothfish, merluza negra (Dissostichus eleginoides), about 90 cm long, and "
               "beside it one thick cross-section steak with snow-white, oily flesh. Robust, elongated fusiform "
               "body; large head with a big mouth and the lower jaw projecting beyond the upper; two separate "
               "dorsal fins, a short spiny first and a long soft second, mirrored by a long anal fin; truncate "
               "tail; two lateral lines. Colour: dark greyish-brown back and sides with faint darker mottling, "
               f"slightly paler belly, scales visible. {ESTILO}"},
    {"archivo": "trucha.jpg", "motivo": "sin pintas ni banda rosada", "fuente": "FishBase Oncorhynchus mykiss",
     "prompt": "One whole rainbow trout (Oncorhynchus mykiss), farmed, about 40 cm long. Elongated, somewhat "
               "compressed body; small adipose fin; slightly forked tail. Colour: olive-green to steel-blue back, "
               "a wide pink to red stripe running along the side from the gill cover to the base of the tail, "
               "silvery-white belly, and many small black spots on the back, sides, dorsal fin and tail. "
               f"{ESTILO}"},
    {"archivo": "apanado-bastones.jpg", "motivo": "reemplaza productos-empanados-mar-02 (nombre de otra marca)",
     "fuente": "—",
     "prompt": "A small stack of frozen breaded hake fish sticks, rectangular bars with an even fine golden crumb "
               "coating, two of them broken in half to show flaky white hake flesh. Uncooked frozen product "
               f"look, light frost. {ESTILO_PRODUCTO}"},
    {"archivo": "apanado-rabas.jpg", "motivo": "parecían aros de cebolla clonados",
     "fuente": "—",
     "prompt": "A loose heap of frozen breaded squid rings (rabas) made from Argentine shortfin squid: irregular "
               "oval rings of different sizes (4 to 7 cm), thin squid walls, uneven light golden crumb with a few "
               "bare patches and loose crumbs, some rings slightly broken, bent or overlapping, light white frost; "
               "one ring snapped open to show the white squid flesh. Every ring different, not onion rings, "
               f"not perfect circles. {ESTILO_PRODUCTO}"},
    {"archivo": "apanado-romana.jpg", "motivo": "reemplaza productos-empanados-mar-06",
     "fuente": "—",
     "prompt": "Four battered hake fillet portions in Roman style (a la romana), smooth light golden batter "
               "coating, rectangular portions about 12 cm long, one cut open to show the white flaky hake inside. "
               f"{ESTILO_PRODUCTO}"},
    {"archivo": "apanado-formitas.jpg", "motivo": "reemplaza productos-empanados-mar-05",
     "fuente": "—",
     "prompt": "Breaded hake shapes for children: fish-shaped, star-shaped and small dinosaur-shaped nuggets about "
               "6 cm wide, with an even golden crumb coating, neatly arranged in rows, no faces drawn on them. "
               f"{ESTILO_PRODUCTO}"},
]

# Estilo claro (prueba, inspirado en pescaderías online: luz alta, hielo blanco, encuadre cerrado)
ESTILO_CLARO = (
    "Bright high-key fishmonger photography: the fish rests on a deep bed of fresh white crushed ice filling the "
    "frame, close three-quarter view focused on the head and front half with the rest of the body visible, soft "
    "diffused daylight, crisp natural colours, glistening wet skin, shallow depth of field, white background, "
    "no garnish, no props, no hands, no text, no logos, no watermark."
)

# Realismo (10-nov-2026): las tandas anteriores se veían "de IA". Pedir foto sin retocar con imperfecciones.
ESTILO_REAL = (
    "Real, unretouched studio photograph of a freshly landed fish, taken with a full-frame DSLR and a 100 mm "
    "macro lens at f/8, seen from a high angle almost from above. The fish lies diagonally across the frame on a "
    "scattering of irregular broken and crushed ice chunks of different sizes (not perfect cubes), partly melted, on a clean matte black stone surface with subtle "
    "texture; soft directional light from the upper left, deep black falloff at the edges. Natural imperfections "
    "on the fish only: a few missing or lifted scales, matte natural skin without glossy highlights, fins slightly frayed, a little blood "
    "at the gills, true-to-life colours. If there is more than one piece, every piece looks different (never repeated or "
    "cloned shapes). Fine sensor grain, no HDR, no CGI look, no illustration, no props, "
    "no garnish, no hands, no text, no logos, no watermark."
)
