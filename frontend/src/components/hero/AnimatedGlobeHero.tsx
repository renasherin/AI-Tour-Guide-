"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Sparkles,
  Plane,
  Award,
  ChevronLeft,
  ChevronRight,
  MapPin,
  ExternalLink,
  Flame,
  ArrowRight,
} from "lucide-react";

export interface WonderItem {
  id: string;
  name: string;
  location: string;
  state: string;
  badge: string;
  wowFactor: string;
  secretLore: string;
  image: string;
  slug: string;
}

export const SEVEN_WONDERS_OF_INDIA: WonderItem[] = [
  {
    id: "taj_mahal",
    name: "Taj Mahal",
    location: "Agra",
    state: "Uttar Pradesh",
    badge: "World Wonder",
    wowFactor:
      "Engineered on deep teak-and-sal wood wells along the Yamuna, the minarets slant subtly outwards by 2 degrees so that during an earthquake they collapse away from the central tomb. The ivory translucent Makrana marble changes color from pinkish at dawn to milky white at noon and burnished gold under moonlight.",
    secretLore:
      "Commissioned in 1631 by Emperor Shah Jahan. Over 20,000 artisans inlaid 28 varieties of rare semi-precious stones (jade from China, lapis lazuli from Afghanistan, carnelian from Arabia) using microscopic Pietra Dura technique.",
    image: "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    slug: "taj_mahal",
  },
  {
    id: "kailasa_temple",
    name: "Kailasa Temple (Cave 16)",
    location: "Ellora Caves",
    state: "Maharashtra",
    badge: "Monolithic Marvel",
    wowFactor:
      "The largest monolithic rock-cut structure on Earth. Carved strictly from the top downwards out of a single vertical volcanic basalt cliff, removing 200,000 to 400,000 tonnes of solid stone with hand chisels—without a single crane, mortar, or scaffolding.",
    secretLore:
      "Constructed in the 8th century under Rashtrakuta King Krishna I to replicate Lord Shiva's Himalayan abode Mount Kailash. The complex is twice the area of the Parthenon in Athens and 1.5 times its height.",
    image: "https://images.unsplash.com/photo-1609137144820-2216597980ee?auto=format&fit=crop&w=800&q=80",
    slug: "kailasa_temple_ellora_cave_16",
  },
  {
    id: "konark_sun_temple",
    name: "Sun Temple, Konark",
    location: "Konark",
    state: "Odisha",
    badge: "Cosmic Sundial",
    wowFactor:
      "Conceived as a colossal 24-wheeled stone chariot of the Sun God Surya, pulled by seven galloping stone stallions. The 24 carved stone wheels are precise astronomical sundials; the spokes cast shadows that can calculate time down to the exact minute.",
    secretLore:
      "Built in 1250 AD by King Narasimhadeva I of the Eastern Ganga Dynasty using Khondalite stone and iron clamps. Legend holds that a massive lodestone magnet originally hung at the sanctum crown, keeping the main idol floating in mid-air.",
    image: "https://images.unsplash.com/photo-1626014303757-656c1d18f566?auto=format&fit=crop&w=800&q=80",
    slug: "sun_temple_konark",
  },
  {
    id: "golden_temple",
    name: "Harmandir Sahib (Golden Temple)",
    location: "Amritsar",
    state: "Punjab",
    badge: "Gilded Sanctuary",
    wowFactor:
      "Its upper storeys are clad in over 500 kilograms of pure 24-karat gold foil. Its 24/7 community langar kitchen feeds over 100,000 pilgrims and visitors daily free of cost, making it the largest continuous open humanitarian kitchen on Earth.",
    secretLore:
      "Founded by Guru Ram Das in 1577 around the sacred Amrit Sarovar (Pool of Nectar). Uniquely designed with entrances on all four cardinal directions to symbolize that every human being, regardless of caste, faith, or origin, is warmly welcome.",
    image: "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=800&q=80",
    slug: "golden_temple",
  },
  {
    id: "hampi_stone_chariot",
    name: "Hampi Stone Chariot & Ruins",
    location: "Vijayanagara",
    state: "Karnataka",
    badge: "Imperial Boulder City",
    wowFactor:
      "The iconic Garuda Stone Chariot in the Vittala Temple complex appears carved from a single boulder, but is actually assembled from interlocking carved granite slabs with hidden joints. In the surrounding musical pillars hall, tapping the slender granite pillars produces distinct musical swaras.",
    secretLore:
      "Capital of the 14th-century Vijayanagara Empire, once the second largest city in the medieval world after Beijing. Portuguese and Persian chronicles described markets where rubies, diamonds, and pearls were sold by the kilogram on open streets.",
    image: "https://images.unsplash.com/photo-1600100397608-f010f4439066?auto=format&fit=crop&w=800&q=80",
    slug: "group_of_monuments_at_hampi",
  },
  {
    id: "meenakshi_amman",
    name: "Meenakshi Amman Temple",
    location: "Madurai",
    state: "Tamil Nadu",
    badge: "Sculpted Rainbow Towers",
    wowFactor:
      "Dominating the skyline of 2,500-year-old Madurai, its 14 soaring gopurams (gateway towers) are clad in more than 33,000 hand-sculpted, vibrant mythological figures. The Hall of 1,000 Pillars features intricately carved monolithic granite columns aligned in flawless optical perspective.",
    secretLore:
      "Celebrated as the heart of the ancient Pandyan kingdom. The entire historic city of Madurai was planned in concentric square rings replicating a sacred cosmic lotus, radiating outwards from the temple sanctum.",
    image: "https://images.unsplash.com/photo-1621252179027-94459d278660?auto=format&fit=crop&w=800&q=80",
    slug: "meenakshi_amman_temple",
  },
  {
    id: "rani_ki_vav",
    name: "Rani ki Vav Stepwell",
    location: "Patan",
    state: "Gujarat",
    badge: "Subterranean Palace",
    wowFactor:
      "Designed not as a building rising into the sky, but as an inverted subterranean temple plunging 30 meters underground into the earth across seven tiers. Over 500 principal sculptures and 1,000 minor figurines depict Lord Vishnu's avatars with unbelievable sculptural delicacy.",
    secretLore:
      "Commissioned in 1063 AD by Queen Udayamati in memory of King Bhima I of the Chaulukya dynasty. For centuries it remained buried beneath the silt of the Saraswati River, preserving its 900-year-old sandstone carvings in immaculate pristine condition.",
    image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
    slug: "rani_ki_vav",
  },
];

export function AnimatedGlobeHero() {
  const [activeWonderIdx, setActiveWonderIdx] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  // Auto-advance wonders every 6 seconds
  useEffect(() => {
    if (!isAutoPlaying) return;
    const interval = setInterval(() => {
      setActiveWonderIdx((prev) => (prev + 1) % SEVEN_WONDERS_OF_INDIA.length);
    }, 6000);
    return () => clearInterval(interval);
  }, [isAutoPlaying]);

  const activeWonder = SEVEN_WONDERS_OF_INDIA[activeWonderIdx];

  const handleLaunchChat = (wonderName: string, stateName: string) => {
    const prompt = `Tell me all the jaw-dropping wow factors, architectural secrets, and royal legends of ${wonderName} in ${stateName}. What makes it truly extraordinary?`;
    const event = new CustomEvent("open-ai-chat", { detail: { prompt } });
    window.dispatchEvent(event);
  };

  return (
    <div className="relative w-full max-w-6xl mx-auto my-6 px-4 sm:px-6">
      {/* 1. AEROPLANE FLIGHT TRAJECTORY OVERHEAD */}
      <div className="relative w-full h-16 sm:h-20 overflow-hidden pointer-events-none mb-2">
        {/* Curved Dashed Flight Path SVG */}
        <svg
          className="absolute inset-0 w-full h-full text-saffron/40"
          viewBox="0 0 1000 100"
          fill="none"
          preserveAspectRatio="none"
        >
          <path
            d="M 20,80 Q 250,10 500,30 T 980,20"
            stroke="currentColor"
            strokeWidth="2"
            strokeDasharray="6 8"
            className="opacity-60"
          />
        </svg>

        {/* Animated Flying Airplane */}
        <div className="absolute top-0 left-0 w-full h-full animate-flight-glide">
          <div className="relative inline-flex items-center space-x-2">
            {/* Plane Icon with Banking Angle */}
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-terracotta via-saffron to-gold text-white flex items-center justify-center shadow-lg transform -rotate-12 hover:scale-110 transition-transform">
              <Plane className="w-5 h-5 fill-white stroke-white" />
            </div>
            {/* Glowing Contrail Vapor Effect */}
            <div className="hidden sm:flex items-center space-x-1.5 px-3 py-1 rounded-full bg-obsidian-900/80 border border-saffron/40 text-[11px] font-mono text-saffron backdrop-blur-md shadow-md">
              <span className="w-1.5 h-1.5 rounded-full bg-saffron animate-ping" />
              <span>FLIGHT IN-07 // OVERFLYING 7 WONDERS OF INDIA</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. THE 7 WONDERS ON TOP OF THE GLOBE */}
      <div className="relative rounded-3xl bg-gradient-to-b from-obsidian-900/95 via-obsidian-900/90 to-obsidian-950/95 border border-gold/30 p-6 sm:p-8 md:p-10 shadow-2xl backdrop-blur-xl overflow-hidden">
        {/* Atmospheric Radial Gradients */}
        <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-gradient-to-b from-saffron/20 via-terracotta/10 to-transparent blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-80 h-80 bg-viridian/20 blur-3xl pointer-events-none" />

        {/* Header Ribbon on Top of Globe */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 mb-8 border-b border-obsidian-800 gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-gold/15 text-gold text-xs font-bold uppercase tracking-widest mb-2 border border-gold/30">
              <Award className="w-3.5 h-3.5" />
              <span>Epic Indian Heritage Showcase</span>
            </div>
            <h2 className="font-serif text-2xl sm:text-4xl font-bold text-ivory-50 tracking-tight">
              The 7 Wonders Elevated on the Globe
            </h2>
            <p className="text-xs sm:text-sm text-ivory-300 font-light mt-1">
              Select any monumental wonder orbiting the subcontinental sphere to unlock its awe-inspiring engineering marvels.
            </p>
          </div>

          {/* Navigation Controls */}
          <div className="flex items-center space-x-2 self-start sm:self-center">
            <button
              onClick={() => {
                setIsAutoPlaying(false);
                setActiveWonderIdx(
                  (prev) => (prev - 1 + SEVEN_WONDERS_OF_INDIA.length) % SEVEN_WONDERS_OF_INDIA.length
                );
              }}
              className="p-2.5 rounded-full bg-obsidian-800 hover:bg-terracotta text-ivory-200 hover:text-white border border-obsidian-700 transition-colors shadow-md"
              aria-label="Previous wonder"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-mono text-saffron px-2">
              {activeWonderIdx + 1} / {SEVEN_WONDERS_OF_INDIA.length}
            </span>
            <button
              onClick={() => {
                setIsAutoPlaying(false);
                setActiveWonderIdx((prev) => (prev + 1) % SEVEN_WONDERS_OF_INDIA.length);
              }}
              className="p-2.5 rounded-full bg-obsidian-800 hover:bg-terracotta text-ivory-200 hover:text-white border border-obsidian-700 transition-colors shadow-md"
              aria-label="Next wonder"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 7 Wonders Quick Selector Tabs Carousel */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-4 mb-8 scrollbar-none">
          {SEVEN_WONDERS_OF_INDIA.map((wonder, idx) => {
            const isActive = idx === activeWonderIdx;
            return (
              <button
                key={wonder.id}
                onClick={() => {
                  setIsAutoPlaying(false);
                  setActiveWonderIdx(idx);
                }}
                className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-medium transition-all flex items-center space-x-2 border ${
                  isActive
                    ? "bg-gradient-to-r from-terracotta to-saffron text-white border-transparent shadow-lg scale-105"
                    : "bg-obsidian-850 hover:bg-obsidian-800 text-ivory-300 border-obsidian-750 hover:border-saffron/40"
                }`}
              >
                <span className="font-mono text-[10px] opacity-75">{idx + 1}</span>
                <span className="font-serif font-bold">{wonder.name.split(" (")[0]}</span>
              </button>
            );
          })}
        </div>

        {/* 3. MAIN STAGE: THE ANIMATED GLOBE SPHERE + SPOTLIGHT WONDER DETAILS */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* LEFT: THE ANIMATED 3D ROTATING GLOBE */}
          <div className="lg:col-span-5 flex flex-col items-center justify-center relative">
            {/* The Globe Sphere */}
            <div className="relative w-64 h-64 sm:w-80 sm:h-80 rounded-full bg-gradient-to-br from-obsidian-800 via-obsidian-900 to-obsidian-950 p-2 shadow-[0_0_80px_rgba(217,130,43,0.25)] border border-saffron/40 flex items-center justify-center overflow-hidden group">
              {/* Spinning Vector Globe Surface */}
              <div className="absolute inset-0 rounded-full animate-globe-spin opacity-40 bg-[radial-gradient(#D9822B_1px,transparent_1px)] [background-size:16px_16px]" />

              {/* Latitude and Longitude Graticule Rings */}
              <div className="absolute inset-4 rounded-full border border-gold/25" />
              <div className="absolute inset-10 rounded-full border border-dashed border-saffron/20" />
              <div className="absolute inset-x-0 top-1/2 h-px bg-saffron/30" />
              <div className="absolute inset-y-0 left-1/2 w-px bg-saffron/30" />

              {/* Subcontinental Core Center (India Glowing Radiance) */}
              <div className="relative z-10 text-center space-y-1">
                <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-terracotta/40 via-saffron/30 to-gold/20 border-2 border-saffron flex items-center justify-center mx-auto shadow-[0_0_30px_rgba(200,90,50,0.6)] animate-pulse">
                  <Flame className="w-8 h-8 text-saffron animate-bounce" />
                </div>
                <div className="pt-2">
                  <span className="font-serif text-sm sm:text-base font-bold text-ivory-100 tracking-wider uppercase block">
                    INDIA
                  </span>
                  <span className="text-[10px] font-mono text-saffron tracking-widest uppercase">
                    28° N, 77° E
                  </span>
                </div>
              </div>

              {/* Orbiting Satellite Marker */}
              <div className="absolute inset-0 rounded-full animate-orbit pointer-events-none">
                <div className="absolute top-2 left-1/2 -translate-x-1/2 w-3.5 h-3.5 rounded-full bg-gold border-2 border-white shadow-[0_0_15px_#C5A869]" />
              </div>

              {/* Atmospheric Rim Glow */}
              <div className="absolute inset-0 rounded-full pointer-events-none bg-gradient-to-tr from-transparent via-transparent to-saffron/20" />
            </div>

            {/* Subtitle Under Globe */}
            <div className="mt-4 text-center">
              <span className="text-[11px] font-mono text-ivory-400 uppercase tracking-widest flex items-center justify-center space-x-1.5">
                <span className="w-2 h-2 rounded-full bg-viridian" />
                <span>Geodetic Datum: WGS84 // Grounded Vector</span>
              </span>
            </div>
          </div>

          {/* RIGHT: SPOTLIGHT ON THE SELECTED WONDER WITH ALL WOW FACTORS */}
          <div className="lg:col-span-7 space-y-5 text-left">
            <div className="relative rounded-2xl overflow-hidden border border-obsidian-750 bg-obsidian-850 p-6 sm:p-7 space-y-4 shadow-xl">
              {/* Badge & Location */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="px-3 py-1 rounded-full bg-gold/20 text-gold text-xs font-bold uppercase tracking-wider border border-gold/40">
                    {activeWonder.badge}
                  </span>
                  <span className="flex items-center space-x-1 text-xs text-ivory-300 font-medium">
                    <MapPin className="w-3.5 h-3.5 text-saffron" />
                    <span>
                      {activeWonder.location}, {activeWonder.state}
                    </span>
                  </span>
                </div>
                <span className="font-serif text-2xl font-bold text-gold/40">
                  0{activeWonderIdx + 1}
                </span>
              </div>

              {/* Title & Preview Image */}
              <div className="flex flex-col sm:flex-row gap-5 items-start">
                <div className="relative w-full sm:w-36 h-28 rounded-xl overflow-hidden flex-shrink-0 border border-obsidian-700 shadow-md">
                  <img
                    src={activeWonder.image}
                    alt={activeWonder.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950/70 to-transparent" />
                </div>
                <div>
                  <h3 className="font-serif text-2xl sm:text-3xl font-bold text-white tracking-tight">
                    {activeWonder.name}
                  </h3>
                  <p className="text-xs text-saffron font-semibold mt-0.5">
                    Architectural & Cultural Marvel of {activeWonder.state}
                  </p>
                </div>
              </div>

              {/* Dedicated Wow Factor Highlight Box */}
              <div className="p-4 rounded-xl bg-gradient-to-br from-terracotta/15 to-saffron/10 border border-terracotta/30 space-y-2">
                <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-saffron">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>The Jaw-Dropping Wow Factor:</span>
                </div>
                <p className="text-xs sm:text-sm text-ivory-100 font-serif leading-relaxed">
                  {activeWonder.wowFactor}
                </p>
              </div>

              {/* Secret Lore / Historical Wonder */}
              <div className="space-y-1 text-xs text-ivory-300 leading-relaxed font-light">
                <strong className="font-semibold text-gold block text-[11px] uppercase tracking-wider">
                  Royal Lore & Craftsmanship:
                </strong>
                <p>{activeWonder.secretLore}</p>
              </div>

              {/* Interactive CTAs */}
              <div className="pt-2 flex flex-wrap gap-3 items-center">
                <button
                  onClick={() => handleLaunchChat(activeWonder.name, activeWonder.state)}
                  className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-full bg-terracotta hover:bg-terracotta-600 text-white text-xs font-semibold uppercase tracking-wider shadow-md hover:shadow-lg transition-all active:scale-95"
                >
                  <Sparkles className="w-3.5 h-3.5 text-saffron" />
                  <span>Ask AI Guide About All Wow Factors</span>
                </button>

                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${activeWonder.name}, ${activeWonder.location}, ${activeWonder.state}, India`)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-full bg-obsidian-800 hover:bg-obsidian-750 text-white text-xs font-semibold border border-terracotta/50 shadow-sm transition-colors hover:border-terracotta"
                >
                  <MapPin className="w-3.5 h-3.5 text-saffron" />
                  <span>Google Maps</span>
                  <ExternalLink className="w-3 h-3 text-ivory-400" />
                </a>

                <Link
                  href={`/destinations/${activeWonder.slug}`}
                  className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-full bg-obsidian-800 hover:bg-obsidian-750 text-ivory-200 text-xs font-medium border border-obsidian-700 transition-colors"
                >
                  <span>View Full Dossier</span>
                  <ArrowRight className="w-3 h-3 text-saffron" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
