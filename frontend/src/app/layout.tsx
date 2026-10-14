import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/ui/Navbar";
import { Footer } from "@/components/ui/Footer";
import { GlobalChatDrawer } from "@/components/chat/GlobalChatDrawer";

export const metadata: Metadata = {
  title: "Incredible Journeys — Discover India with AI",
  description:
    "An award-caliber editorial travel atlas and conversational RAG tour guide celebrating India's 28 states and 8 union territories.",
  keywords: [
    "India Travel",
    "UNESCO World Heritage India",
    "AI Tour Guide",
    "Incredible India",
    "Hampi",
    "Taj Mahal",
    "Varanasi",
    "Kerala Backwaters",
    "Ladakh",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="min-h-screen flex flex-col bg-ivory-100 dark:bg-obsidian-900 text-obsidian-900 dark:text-ivory-100 antialiased selection:bg-terracotta selection:text-white">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
        <GlobalChatDrawer />
      </body>
    </html>
  );
}
