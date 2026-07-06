import { notFound } from "next/navigation";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import WhatsAppButton from "@/components/WhatsAppButton";

export default async function LangLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isValidLang(lang)) notFound();

  const t = await getDictionary(lang as Lang);

  const dir = lang === "ar" ? "rtl" : "ltr";

  return (
    <div dir={dir}>
      <Header lang={lang} nav={t.nav} />
      <main className="flex-1">{children}</main>
      <Footer lang={lang} t={t} />
      <WhatsAppButton label={t.whatsapp_label} />
    </div>
  );
}
