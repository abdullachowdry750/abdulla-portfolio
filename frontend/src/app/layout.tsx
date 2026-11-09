import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://abdullachowdry.com"),

  title: {
    default: "Abdulla Chowdry | AI + Data Engineer",
    template: "%s | Abdulla Chowdry",
  },

  description:
    "AI + Data Engineer with 5+ years of experience building intelligent systems, enterprise data platforms, production AI applications and scalable cloud infrastructure.",

  applicationName: "Abdulla Chowdry Portfolio",

  authors: [
    {
      name: "Abdulla Chowdry",
      url: "https://abdullachowdry.com",
    },
  ],

  openGraph: {
    type: "website",
    locale: "en_IN",
    url: "https://abdullachowdry.com",
    siteName: "Abdulla Chowdry",
    title: "Abdulla Chowdry | AI + Data Engineer",
    description:
      "Building intelligent systems, enterprise data platforms and production-ready AI solutions.",
  },

  twitter: {
    card: "summary_large_image",
    title: "Abdulla Chowdry | AI + Data Engineer",
    description:
      "AI + Data Engineer building intelligent systems and scalable data platforms.",
  },

  icons: {
    icon: "/icon.svg",
    shortcut: "/icon.svg",
    apple: "/icon.svg",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
