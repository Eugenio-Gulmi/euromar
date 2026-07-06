import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "Euromar SA | Comercialización Internacional de Mariscos",
  description:
    "Empresa argentina de exportación de pescados y mariscos con más de 45 años de experiencia. Exportamos a todo el mundo desde Mar del Plata.",
  icons: {
    icon: "/euromar-logo.svg",
    shortcut: "/euromar-logo.svg",
    apple: "/euromar-logo.svg",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html className={geist.variable}>
      <body className="min-h-screen flex flex-col antialiased">{children}</body>
    </html>
  );
}
