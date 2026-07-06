import { notFound } from "next/navigation";
import { Phone, Mail, MapPin } from "lucide-react";
import { getDictionary, isValidLang, type Lang } from "@/lib/i18n";
import ContactForm from "@/components/ContactForm";

const contacts = [
  {
    name: "Hugo Pedeconi",
    phone: "+54 223 421-7777",
    email: "hpedeconi@euromar.com.ar",
    langs: null,
  },
  {
    name: "Luciano Gulminelli",
    phone: "+54 223 594-2314",
    email: "lgulminellibarrau@gb-grp.com",
    langs: [
      { flag: "🇦🇷", label: "Español" },
      { flag: "🇬🇧", label: "English" },
      { flag: "🇨🇳", label: "中文" },
      { flag: "🇧🇷", label: "Português" },
      { flag: "🇮🇹", label: "Italiano" },
    ],
  },
];

export default async function ContactoPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isValidLang(lang)) notFound();
  const t = await getDictionary(lang as Lang);

  const formStrings = {
    form_name: t.contact.form_name,
    form_email: t.contact.form_email,
    form_message: t.contact.form_message,
    form_submit: t.contact.form_submit,
    form_sending: t.contact.form_sending,
    form_success: t.contact.form_success,
    form_error: t.contact.form_error,
  };

  return (
    <div>
      <section className="bg-navy-900 text-white py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-4xl font-bold mb-3">{t.contact.title}</h1>
          <p className="text-slate-300 max-w-xl">{t.contact.subtitle}</p>
        </div>
      </section>

      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Form */}
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-100">
            <h2 className="text-xl font-bold text-navy-900 mb-6">
              {t.contact.form_title}
            </h2>
            <ContactForm strings={formStrings} />
          </div>

          {/* Info */}
          <div className="space-y-8">
            {/* Direct contacts */}
            <div>
              <h2 className="text-xl font-bold text-navy-900 mb-5">
                {t.contact.direct_title}
              </h2>
              <div className="space-y-4">
                {contacts.map((c) => (
                  <div
                    key={c.name}
                    className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm"
                  >
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <div className="font-semibold text-navy-900">{c.name}</div>
                      {c.langs && (
                        <div className="flex items-center gap-1">
                          {c.langs.map((l) => (
                            <span key={l.label} title={l.label} className="text-lg leading-none">
                              {l.flag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    <div className="space-y-2 text-sm text-slate-600">
                      <a
                        href={`tel:${c.phone.replace(/\s/g, "")}`}
                        className="flex items-center gap-2 hover:text-navy-900 transition-colors"
                      >
                        <Phone className="w-4 h-4 text-navy-700" />
                        {c.phone}
                      </a>
                      <a
                        href={`mailto:${c.email}`}
                        className="flex items-center gap-2 hover:text-navy-900 transition-colors"
                      >
                        <Mail className="w-4 h-4 text-navy-700" />
                        {c.email}
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Location */}
            <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm">
              <h3 className="font-semibold text-navy-900 mb-3">
                {t.contact.location_title}
              </h3>
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <MapPin className="w-4 h-4 text-navy-700" />
                Mar del Plata, Argentina
              </div>
            </div>

            {/* LinkedIn */}
            <a
              href="https://www.linkedin.com/company/euromar-sa"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 bg-[#0077B5] text-white rounded-xl px-5 py-4 hover:bg-[#006097] transition-colors"
            >
              <svg className="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              <span className="font-semibold">LinkedIn — Euromar SA</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
