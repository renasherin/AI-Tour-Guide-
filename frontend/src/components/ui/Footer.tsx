import React from "react";
import Link from "next/link";
import { Landmark, ShieldCheck, Database, ExternalLink } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-obsidian-900 text-ivory-200 border-t border-obsidian-800 pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-obsidian-800">
          {/* Column 1: Brand & Editorial Mission */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-full bg-terracotta flex items-center justify-center text-white">
                <Landmark className="w-4 h-4 text-ivory-100" />
              </div>
              <span className="font-serif text-2xl font-bold tracking-tight text-ivory-100">
                Incredible Journeys
              </span>
            </div>
            <p className="text-sm leading-relaxed text-ivory-300 max-w-lg font-light">
              An award-grade, AI-assisted editorial atlas celebrating the living heritage, sacred geography,
              biodiversity, and cultural soul of India across all 28 states and 8 union territories.
            </p>
            <div className="flex flex-wrap gap-4 pt-2 text-xs text-ivory-400">
              <div className="flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-gold" />
                <span>Zero-Hallucination Policy</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <Database className="w-4 h-4 text-saffron" />
                <span>Verified ChromaDB Knowledge Base</span>
              </div>
            </div>
          </div>

          {/* Column 2: Editorial Navigation */}
          <div>
            <h4 className="font-serif text-sm tracking-wider uppercase text-gold font-semibold mb-4">
              Editorial Atlas
            </h4>
            <ul className="space-y-2.5 text-xs text-ivory-300 font-medium">
              <li>
                <Link href="/explore" className="hover:text-saffron transition-colors">
                  Explore Destinations
                </Link>
              </li>
              <li>
                <Link href="/explore?unesco=true" className="hover:text-saffron transition-colors">
                  UNESCO World Heritage Sites
                </Link>
              </li>
              <li>
                <Link href="/guide" className="hover:text-saffron transition-colors">
                  Conversational Tour Guide
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-saffron transition-colors">
                  RAG Architecture & Provenance
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Provenance & Attribution */}
          <div>
            <h4 className="font-serif text-sm tracking-wider uppercase text-gold font-semibold mb-4">
              Open Data Provenance
            </h4>
            <p className="text-xs text-ivory-400 leading-relaxed mb-3">
              Content and geographical records are rigorously verified against Wikimedia Open APIs
              (Wikipedia, Wikivoyage, Wikidata) under the Creative Commons Attribution-ShareAlike 4.0
              International License (CC BY-SA 4.0).
            </p>
            <a
              href="https://creativecommons.org/licenses/by-sa/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1 text-xs text-saffron hover:underline"
            >
              <span>CC BY-SA 4.0 Details</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-ivory-400 gap-4">
          <p>
            &copy; {new Date().getFullYear()} Incredible Journeys — Discover India with AI. Designed with luxury editorial care.
          </p>
          <div className="flex items-center space-x-6 text-xs">
            <Link href="/about#transparency" className="hover:text-ivory-200 transition-colors">
              Data Transparency
            </Link>
            <Link href="/about#rag-architecture" className="hover:text-ivory-200 transition-colors">
              RAG Pipeline
            </Link>
            <Link href="/about#licensing" className="hover:text-ivory-200 transition-colors">
              Open Licensing
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
