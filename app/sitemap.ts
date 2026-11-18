import type { MetadataRoute } from "next";
import { LANGS } from "@/lib/i18n";
import { SITE_URL } from "@/lib/seo";

const PATHS = ["", "/productos", "/servicios", "/nosotros", "/contacto"];

export default function sitemap(): MetadataRoute.Sitemap {
  return PATHS.flatMap((path) =>
    LANGS.map((lang) => ({
      url: `${SITE_URL}/${lang}${path}`,
      lastModified: new Date(),
      alternates: {
        languages: Object.fromEntries(LANGS.map((l) => [l, `${SITE_URL}/${l}${path}`])),
      },
    }))
  );
}
