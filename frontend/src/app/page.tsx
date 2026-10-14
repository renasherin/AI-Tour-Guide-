"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Compass,
  Sparkles,
  MapPin,
  Award,
  ArrowRight,
  Search,
  BookOpen,
  ChevronRight,
  ShieldCheck,
  CheckCircle2,
  Calendar,
} from "lucide-react";
import { DestinationCard } from "@/components/ui/DestinationCard";
import { FoodCard } from "@/components/ui/FoodCard";
import { AnimatedGlobeHero } from "@/components/hero/AnimatedGlobeHero";
import { Destination, RegionDivision, FoodItem } from "@/lib/types";
import { fetchDestinations, fetchRegions } from "@/lib/api";
import { CURATED_HERO_IMAGES } from "@/lib/images";
import foodsJson from "@/lib/foods.json";

const FEATURED_FOODS: FoodItem[] = (foodsJson as FoodItem[]).slice(0, 8);

// Curated Journeys themed stories
const CURATED_THEMES = [
  {
    id: "spiritual-paths",
    title: "Sacred Waters & Sacred Stone",
    subtitle: "Spiritual Journeys of the Subcontinent",
    tagline: "Varanasi, Rishikesh, Puri & Bodh Gaya",
    description:
      "From dawn Ganga aartis on ancient ghats to Bodhi trees where meditative epiphanies reshaped civilization.",
    image: "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80",
    category: "Pilgrimage & Sacred Heritage",
  },
  {
    id: "mughal-splendor",
    title: "Marble, Minarets & Sandstone",
    subtitle: "Imperial Architecture of Northern India",
    tagline: "Agra, Delhi, Fatehpur Sikri & Lahore Corridors",
    description:
      "Symmetrical garden mausoleums, intricate Pietra Dura stone inlays, and fortified palaces overlooking riverbanks.",
    image: "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
    category: "Mughal & Islamic Architecture",
  },
  {
    id: "coastal-flavors",
    title: "Spice Valleys & Palm Lagoons",
    subtitle: "Slow Travel on the Malabar & Konkan Coasts",
    tagline: "Alleppey, Munnar, Fort Kochi & Old Goa",
    description:
      "Houseboats drifting through coconut canal labyrinths, cardamom hills shrouded in morning mist, and Portuguese colonial facades.",
    image: "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
    category: "Nature & Coastal Heritage",
  },
  {
    id: "himalayan-altitudes",
    title: "High Passes & Sacred Monasteries",
    subtitle: "Trans-Himalayan Horizons",
    tagline: "Ladakh, Spiti Valley, Zanskar & Sikkim",
    description:
      "Prayer flags fluttering over 18,000-foot passes, cliffside gompas echoing with horn chants, and glacial lakes reflecting indigo skies.",
    image: "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1200&q=80",
    category: "Mountains & Monasteries",
  },
];

export default function HomePage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [regions, setRegions] = useState<RegionDivision[]>([]);
  const [regionFilter, setRegionFilter] = useState<"All" | "States" | "UTs">("All");
  const [regionSearch, setRegionSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [destRes, regRes] = await Promise.all([
          fetchDestinations({ limit: 8 }),
          fetchRegions(),
        ]);
        setDestinations(destRes.destinations);
        setRegions(regRes.divisions);
      } catch (e) {
        console.error("Error loading home data:", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/explore?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleLaunchChatPrompt = (prompt: string) => {
    const event = new CustomEvent("open-ai-chat", { detail: { prompt } });
    window.dispatchEvent(event);
  };

  // Filtered regions
  const filteredRegions = regions.filter((r) => {
    const matchesType =
      regionFilter === "All" ||
      (regionFilter === "States" && r.type === "State") ||
      (regionFilter === "UTs" && r.type !== "State");
    const matchesSearch =
      !regionSearch ||
      r.name.toLowerCase().includes(regionSearch.toLowerCase()) ||
      r.capital?.toLowerCase().includes(regionSearch.toLowerCase()) ||
      r.zone?.toLowerCase().includes(regionSearch.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-ivory-100 dark:bg-obsidian-900 transition-colors">
      {/* 1. CINEMATIC HERO SECTION */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden pt-24 pb-16">
        {/* Background Atmospheric Photography */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=2000&q=85"
            alt="Atmospheric sunset over Indian heritage waters"
            className="w-full h-full object-cover object-center scale-105 transition-transform duration-1000 ease-out"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950 via-obsidian-950/75 to-obsidian-950/45" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,rgba(15,20,28,0.75)_100%)]" />
        </div>

        {/* Hero Content Box */}
        <div className="relative z-10 w-full max-w-6xl mx-auto px-4 sm:px-6 text-center text-white space-y-6">
          {/* Highlighted Heritage Floating Badge */}
          <div className="inline-flex items-center space-x-2.5 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-ivory-200 text-xs tracking-wider uppercase font-medium shadow-lg animate-fade-in-slide">
            <span className="w-2 h-2 rounded-full bg-saffron animate-ping" />
            <Award className="w-3.5 h-3.5 text-gold" />
            <span>Discover All 28 States & 8 Union Territories</span>
          </div>

          {/* Staggered Serif Entrance Title */}
          <div className="space-y-3">
            <h1 className="font-serif text-4xl sm:text-6xl md:text-7xl font-bold tracking-tight text-ivory-50 drop-shadow-md">
              India Is a Thousand <span className="italic text-saffron">Journeys</span>.
            </h1>
            <p className="max-w-2xl mx-auto text-sm sm:text-base text-ivory-300 font-light leading-relaxed">
              An authoritative, AI-grounded editorial voyage across sacred rivers, ancient stone monoliths,
              Himalayan passes, and culinary sanctuaries.
            </p>
          </div>

          {/* ANIMATED GLOBE + 7 WONDERS ELEVATED ON TOP + FLYING AEROPLANE */}
          <AnimatedGlobeHero />

          {/* Quick-Search Bar */}
          <form
            onSubmit={handleSearchSubmit}
            className="max-w-2xl mx-auto relative flex items-center bg-ivory-50/95 dark:bg-obsidian-900/95 rounded-full p-2 shadow-2xl border border-ivory-200/80 dark:border-obsidian-700/80 backdrop-blur-md"
          >
            <div className="pl-4 text-terracotta">
              <Search className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search forts, monasteries, backwaters, festivals, or dishes..."
              className="w-full bg-transparent px-3 py-2 text-sm text-obsidian-900 dark:text-ivory-100 placeholder-obsidian-400 dark:placeholder-ivory-400 focus:outline-none"
            />
            <button
              type="submit"
              className="px-6 py-2.5 rounded-full bg-terracotta hover:bg-terracotta-600 text-white text-xs font-semibold uppercase tracking-wider transition-all shadow-md active:scale-95"
            >
              Explore
            </button>
          </form>

          {/* Quick Category Chips */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
            <span className="text-ivory-400 font-medium">Trending Inquiries:</span>
            {[
              { label: "Hampi Ruins", query: "Hampi" },
              { label: "Varanasi Ghats", query: "Varanasi" },
              { label: "Kerala Backwaters", query: "Alleppey" },
              { label: "Pangong Lake", query: "Ladakh" },
              { label: "UNESCO Sites", query: "UNESCO" },
            ].map((chip) => (
              <button
                key={chip.label}
                onClick={() => router.push(`/explore?search=${chip.query}`)}
                className="px-3 py-1 rounded-full bg-white/10 hover:bg-white/20 border border-white/15 text-ivory-200 hover:text-white transition-all backdrop-blur-sm"
              >
                {chip.label}
              </button>
            ))}
          </div>
        </div>

        {/* Live Heritage Highlight Card Floating at Corner */}
        <div className="hidden lg:block absolute bottom-8 left-8 z-10 max-w-xs p-4 rounded-2xl bg-obsidian-900/80 border border-obsidian-700 text-left text-white backdrop-blur-md shadow-2xl">
          <div className="flex items-center space-x-2 text-gold text-[11px] font-semibold uppercase tracking-wider mb-1">
            <Award className="w-3.5 h-3.5" />
            <span>Featured World Heritage</span>
          </div>
          <h4 className="font-serif text-base font-bold text-ivory-100 mb-1">Taj Mahal, Agra</h4>
          <p className="text-xs text-ivory-300 line-clamp-2">
            Ivory-white marble mausoleum on the Yamuna riverbank, commissioned by Shah Jahan in 1631.
          </p>
          <Link
            href="/destinations/taj_mahal"
            className="inline-flex items-center space-x-1 mt-2 text-xs text-saffron hover:underline font-medium"
          >
            <span>Read Editorial Dossier</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </section>

      {/* 2. CURATED EDITORIAL GRID (ASYMMETRIC SIGNATURES) */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 border-b border-ivory-300 dark:border-obsidian-800 pb-6">
          <div className="space-y-2 max-w-2xl">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Curated Masterpieces
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-obsidian-900 dark:text-ivory-100">
              Living Stones, Sacred Waters & High Valleys
            </h2>
            <p className="text-sm text-obsidian-600 dark:text-ivory-300 leading-relaxed font-light">
              Signature destinations documented with authoritative coordinate verification, UNESCO provenance,
              and historical context.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <Link
              href="/explore"
              className="inline-flex items-center space-x-2 text-sm font-semibold text-terracotta dark:text-saffron hover:underline"
            >
              <span>View All 600+ Destinations</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {destinations.map((dest, idx) => (
            <DestinationCard key={dest.id || idx} destination={dest} priority={idx < 4} />
          ))}
        </div>
      </section>

      {/* 3. TRAVEL STORIES / CURATED THEMATIC JOURNEYS */}
      <section className="py-20 bg-ivory-200/60 dark:bg-obsidian-800/40 border-y border-ivory-300 dark:border-obsidian-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-3">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Curated Thematic Routes
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-obsidian-900 dark:text-ivory-100">
              Journeys Across Epochs & Landscapes
            </h2>
            <p className="text-sm text-obsidian-600 dark:text-ivory-300 leading-relaxed font-light">
              Explore interconnected narratives that weave ancient temples, desert fortresses, tea slopes, and culinary traditions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {CURATED_THEMES.map((theme) => (
              <div
                key={theme.id}
                className="group relative rounded-2xl overflow-hidden bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-editorial flex flex-col justify-between"
              >
                <div className="relative aspect-[4/3] overflow-hidden bg-obsidian-900">
                  <img
                    src={theme.image}
                    alt={theme.title}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950/80 via-transparent to-transparent" />
                  <span className="absolute top-3 left-3 px-2.5 py-0.5 rounded-full bg-white/90 dark:bg-obsidian-900/90 text-obsidian-900 dark:text-ivory-100 text-[10px] font-bold uppercase tracking-wider backdrop-blur-sm">
                    {theme.category}
                  </span>
                </div>
                <div className="p-5 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="font-serif text-lg font-bold text-obsidian-900 dark:text-ivory-100 mb-1 group-hover:text-terracotta transition-colors">
                      {theme.title}
                    </h3>
                    <p className="text-xs font-semibold text-terracotta dark:text-saffron mb-2">
                      {theme.tagline}
                    </p>
                    <p className="text-xs text-obsidian-600 dark:text-ivory-300 line-clamp-3 leading-relaxed">
                      {theme.description}
                    </p>
                  </div>
                  <div className="pt-4 mt-3 border-t border-ivory-200 dark:border-obsidian-700">
                    <button
                      onClick={() => handleLaunchChatPrompt(`Tell me more about the journey: ${theme.title} (${theme.tagline})`)}
                      className="w-full py-2 px-3 rounded-xl bg-ivory-200 dark:bg-obsidian-700 hover:bg-terracotta hover:text-white dark:hover:bg-terracotta text-xs font-semibold text-obsidian-800 dark:text-ivory-200 transition-colors flex items-center justify-center space-x-1.5"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Ask AI About This Route</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. CULINARY SOUL: REGIONAL GASTRONOMY OF INDIA */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 border-b border-ivory-300 dark:border-obsidian-800 pb-6">
          <div className="space-y-2 max-w-2xl">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Subcontinental Gastronomy
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-obsidian-900 dark:text-ivory-100">
              Flavors Forged in Clay, Ghee & Spices
            </h2>
            <p className="text-sm text-obsidian-600 dark:text-ivory-300 leading-relaxed font-light">
              From Kozhikode dum biryani and S.M. Street halwa to Amritsari tandoori kulcha, Bihari litti chokha, and Tuluva kori rotti—taste the culinary soul of every region.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <button
              onClick={() => handleLaunchChatPrompt("Recommend the top traditional feasts and street food specialties across South, North, East, and West India with authentic recipes and places to try!")}
              className="inline-flex items-center space-x-2 text-sm font-semibold text-terracotta dark:text-saffron hover:underline"
            >
              <span>Explore All Delicacies with AI Guide</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Food Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {FEATURED_FOODS.map((food) => (
            <FoodCard key={food.id} food={food} />
          ))}
        </div>
      </section>

      {/* 5. REGION & STATE EXPLORER (ALL 28 STATES & 8 UTs) */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-ivory-300 dark:border-obsidian-800">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Subcontinental Geography
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-obsidian-900 dark:text-ivory-100">
              Atlas of 28 States & 8 Union Territories
            </h2>
            <p className="text-sm text-obsidian-600 dark:text-ivory-300 font-light">
              Every administrative division of the Republic of India covered with verified destination inventories.
            </p>
          </div>

          {/* Filter Toggles & Search */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="inline-flex rounded-lg bg-ivory-200 dark:bg-obsidian-800 p-1 border border-ivory-300 dark:border-obsidian-700 text-xs">
              {(["All", "States", "UTs"] as const).map((filter) => (
                <button
                  key={filter}
                  onClick={() => setRegionFilter(filter)}
                  className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                    regionFilter === filter
                      ? "bg-terracotta text-white shadow-sm"
                      : "text-obsidian-700 dark:text-ivory-300 hover:text-terracotta"
                  }`}
                >
                  {filter}
                </button>
              ))}
            </div>

            <div className="relative">
              <input
                type="text"
                value={regionSearch}
                onChange={(e) => setRegionSearch(e.target.value)}
                placeholder="Search state/UT..."
                className="px-3 py-1.5 pl-8 rounded-lg bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-xs text-obsidian-900 dark:text-ivory-100 focus:outline-none focus:ring-1 focus:ring-terracotta"
              />
              <Search className="w-3.5 h-3.5 text-obsidian-400 absolute left-2.5 top-2.5" />
            </div>
          </div>
        </div>

        {/* Regions Visual Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3.5">
          {filteredRegions.map((reg) => (
            <Link
              key={reg.name}
              href={`/explore?state=${encodeURIComponent(reg.name)}`}
              className="group p-3.5 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-300/80 dark:border-obsidian-700/80 hover:border-terracotta hover:shadow-md transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                <span className="text-[9px] uppercase tracking-wider font-semibold text-terracotta dark:text-saffron block mb-0.5">
                  {reg.type}
                </span>
                <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta transition-colors line-clamp-1">
                  {reg.name}
                </h4>
                <p className="text-[11px] text-obsidian-500 dark:text-ivory-400 line-clamp-1 mt-0.5">
                  {reg.capital}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-ivory-200 dark:border-obsidian-700/60 flex items-center justify-between text-[11px] text-obsidian-600 dark:text-ivory-300">
                <span>{reg.count} sights</span>
                <ChevronRight className="w-3.5 h-3.5 text-obsidian-400 group-hover:translate-x-0.5 group-hover:text-terracotta transition-all" />
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 5. INTERACTIVE AI PREVIEW & ZERO-HALLUCINATION POLICY */}
      <section className="py-20 bg-gradient-to-br from-ivory-200/80 via-ivory-100 to-ivory-200/80 dark:from-obsidian-900 dark:via-obsidian-850 dark:to-obsidian-900 border-t border-ivory-300 dark:border-obsidian-800">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="rounded-3xl p-8 sm:p-12 bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-2xl relative overflow-hidden">
            {/* Background Accent */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-terracotta/5 rounded-full blur-3xl pointer-events-none" />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div className="space-y-4">
                <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-terracotta/10 text-terracotta text-xs font-bold uppercase tracking-wider">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Interactive RAG Engine</span>
                </div>
                <h2 className="font-serif text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
                  Grounded in Verified Fact, Weaved with Editorial Warmth
                </h2>
                <p className="text-xs sm:text-sm text-obsidian-600 dark:text-ivory-300 leading-relaxed font-light">
                  Unlike generic models prone to fabricating ticket prices or ghost routes, Incredible Journeys
                  synthesizes answers exclusively from authoritative open travel repositories with transparent citations.
                </p>

                <div className="space-y-2 pt-2">
                  <div className="flex items-center space-x-2 text-xs text-obsidian-700 dark:text-ivory-300">
                    <CheckCircle2 className="w-4 h-4 text-viridian" />
                    <span>Real-time semantic retrieval via persistent ChromaDB</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-obsidian-700 dark:text-ivory-300">
                    <CheckCircle2 className="w-4 h-4 text-viridian" />
                    <span>Explicit Wikipedia & Wikivoyage open license citations</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-obsidian-700 dark:text-ivory-300">
                    <CheckCircle2 className="w-4 h-4 text-viridian" />
                    <span>Multilingual guidance in English and Hindi (हिन्दी)</span>
                  </div>
                </div>

                <div className="pt-4">
                  <Link
                    href="/guide"
                    className="inline-flex items-center space-x-2 px-6 py-3 rounded-full bg-terracotta hover:bg-terracotta-600 text-white text-xs font-semibold uppercase tracking-wider shadow-md hover:shadow-lg transition-all"
                  >
                    <span>Launch AI Tour Guide</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>

              {/* Simulated Interactive Prompt Card */}
              <div className="rounded-2xl bg-ivory-100 dark:bg-obsidian-900 p-6 border border-ivory-300 dark:border-obsidian-700 space-y-4">
                <div className="flex items-center justify-between text-xs text-obsidian-500 dark:text-ivory-400 border-b border-ivory-200 dark:border-obsidian-800 pb-3">
                  <span className="font-mono text-[11px]">SAMPLE GROUNDED INTERACTION</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-viridian/10 text-viridian font-bold">100% Grounded</span>
                </div>

                <div className="p-3 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-200 dark:border-obsidian-700 text-xs">
                  <span className="font-semibold text-terracotta block mb-1">Traveler:</span>
                  "What makes the stepwell of Rani ki Vav in Gujarat historically unique?"
                </div>

                <div className="p-4 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-200 dark:border-obsidian-700 text-xs leading-relaxed font-serif text-obsidian-900 dark:text-ivory-100 space-y-2">
                  <span className="font-sans font-semibold text-saffron block text-[11px]">AI Tour Guide:</span>
                  <p>
                    Rani ki Vav (The Queen's Stepwell) in Patan, Gujarat, was constructed in the 11th century during the Chaulukya dynasty. Designed as an inverted subterranean temple honouring the sanctity of water, it features seven levels of stairs lined with more than 500 principal sculptures depicting Lord Vishnu's avatars.
                  </p>
                  <div className="pt-2 border-t border-ivory-200 dark:border-obsidian-700 flex items-center justify-between text-[10px] text-obsidian-500">
                    <span className="font-sans font-semibold text-terracotta">[Source: Rani ki Vav, Gujarat]</span>
                    <span className="font-sans">License: CC BY-SA 4.0</span>
                  </div>
                </div>

                <button
                  onClick={() => handleLaunchChatPrompt("Tell me about Rani ki Vav in Gujarat and other historic stepwells of India")}
                  className="w-full py-2.5 rounded-xl border border-terracotta text-terracotta hover:bg-terracotta hover:text-white transition-colors text-xs font-semibold uppercase tracking-wider"
                >
                  Test This Query Live
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
