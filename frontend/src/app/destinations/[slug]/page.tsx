"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import {
  MapPin,
  Calendar,
  Award,
  Sparkles,
  ExternalLink,
  ShieldCheck,
  ChevronLeft,
  Share2,
  Compass,
} from "lucide-react";
import { fetchDestinationBySlug } from "@/lib/api";
import { Destination } from "@/lib/types";
import { DestinationMap } from "@/components/map/DestinationMap";
import { DestinationCard } from "@/components/ui/DestinationCard";
import { getDestinationImageUrl } from "@/lib/images";

export default function DestinationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params?.slug as string;

  const [destination, setDestination] = useState<Destination | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    fetchDestinationBySlug(slug)
      .then((data) => {
        setDestination(data);
      })
      .finally(() => setLoading(false));
  }, [slug]);

  const handleLaunchChat = () => {
    if (!destination) return;
    const prompt = `Tell me in rich storytelling detail about ${destination.place} in ${destination.state}: its history, architecture, best experiences, and local food.`;
    const event = new CustomEvent("open-ai-chat", { detail: { prompt } });
    window.dispatchEvent(event);
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-32 pb-20 max-w-5xl mx-auto px-4 text-center">
        <div className="w-12 h-12 rounded-full border-4 border-terracotta border-t-transparent animate-spin mx-auto mb-4" />
        <p className="text-sm text-obsidian-600 dark:text-ivory-300">
          Loading editorial dossier...
        </p>
      </div>
    );
  }

  if (!destination) {
    return (
      <div className="min-h-screen pt-32 pb-20 max-w-md mx-auto px-4 text-center">
        <Compass className="w-16 h-16 text-terracotta mx-auto mb-4 opacity-50" />
        <h2 className="font-serif text-2xl font-bold text-obsidian-900 dark:text-ivory-100">
          Destination Not Found
        </h2>
        <p className="text-xs text-obsidian-500 dark:text-ivory-400 mt-2 mb-6">
          The requested destination dossier could not be retrieved from our verified archives.
        </p>
        <Link
          href="/explore"
          className="px-6 py-2.5 rounded-full bg-terracotta text-white text-xs font-semibold uppercase tracking-wider"
        >
          Return to Atlas
        </Link>
      </div>
    );
  }

  const imageUrl = getDestinationImageUrl(
    destination.id || destination.slug || "",
    destination.category,
    destination.image_url
  );

  return (
    <div className="min-h-screen bg-ivory-100 dark:bg-obsidian-900 pb-24 transition-colors">
      {/* 1. IMMERSIVE HERO WITH ATTRIBUTION */}
      <div className="relative h-[65vh] min-h-[460px] w-full overflow-hidden bg-obsidian-950">
        <img
          src={imageUrl}
          alt={destination.place}
          className="w-full h-full object-cover object-center filter brightness-95"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950 via-obsidian-950/40 to-obsidian-950/20" />

        {/* Back Button & Top Meta */}
        <div className="absolute top-24 left-4 sm:left-8 z-20">
          <button
            onClick={() => router.back()}
            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-white/20 hover:bg-white/30 backdrop-blur-md text-white text-xs font-semibold transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
        </div>

        {/* Licensing, Attribution & Google Maps Quick Link */}
        <div className="absolute top-24 right-4 sm:right-8 z-20 flex items-center space-x-2">
          <a
            href={
              destination.google_maps_url ||
              (destination.lat && destination.lon
                ? `https://www.google.com/maps/search/?api=1&query=${destination.lat},${destination.lon}`
                : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(destination.place + ", " + destination.state + ", India")}`)
            }
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-terracotta hover:bg-terracotta/90 backdrop-blur-md text-white text-[11px] font-semibold border border-white/20 shadow-md transition-all hover:scale-105"
          >
            <MapPin className="w-3.5 h-3.5 text-saffron" />
            <span>Open in Google Maps</span>
            <ExternalLink className="w-3 h-3 opacity-80" />
          </a>
          <a
            href={destination.source_url || destination.wikipedia_url || "https://en.wikipedia.org"}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-black/40 hover:bg-black/60 backdrop-blur-md text-ivory-200 text-[11px] font-medium border border-white/10 transition-colors"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-gold" />
            <span>Verified Source</span>
            <ExternalLink className="w-3 h-3 opacity-60" />
          </a>
        </div>

        {/* Bottom Hero Title & Metadata */}
        <div className="absolute bottom-10 left-0 right-0 z-20 max-w-5xl mx-auto px-4 sm:px-6">
          <div className="space-y-3">
            {/* UNESCO & Category Badges */}
            <div className="flex flex-wrap items-center gap-2">
              {destination.is_unesco && (
                <span className="inline-flex items-center space-x-1 px-3 py-0.5 rounded-full bg-gold text-obsidian-950 text-xs font-bold uppercase tracking-wider shadow-md">
                  <Award className="w-3.5 h-3.5" />
                  <span>UNESCO World Heritage Site</span>
                </span>
              )}
              {destination.category.map((cat, i) => (
                <span
                  key={i}
                  className="px-3 py-0.5 rounded-full bg-white/20 backdrop-blur-md text-ivory-100 text-xs uppercase tracking-wider font-semibold"
                >
                  {cat}
                </span>
              ))}
            </div>

            <h1 className="font-serif text-3xl sm:text-5xl md:text-6xl font-bold text-white tracking-tight drop-shadow-md">
              {destination.place}
            </h1>

            <div className="flex flex-wrap items-center gap-4 text-xs sm:text-sm text-ivory-200">
              <span className="flex items-center space-x-1 font-medium">
                <MapPin className="w-4 h-4 text-saffron" />
                <span>
                  {destination.city ? `${destination.city}, ` : ""}
                  {destination.state}, India
                </span>
              </span>

              {destination.best_time && (
                <span className="flex items-center space-x-1 font-medium text-saffron">
                  <Calendar className="w-4 h-4" />
                  <span>{destination.best_time}</span>
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 2. DOSSIER CONTENT BODY */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 mt-12 grid grid-cols-1 lg:grid-cols-12 gap-10">
        {/* Left Column: Narrative & Significance */}
        <div className="lg:col-span-7 space-y-8">
          {/* Curated Overview */}
          <div className="bg-white dark:bg-obsidian-800 rounded-3xl p-6 sm:p-8 border border-ivory-300 dark:border-obsidian-700 shadow-editorial space-y-4">
            <h2 className="font-serif text-2xl font-bold text-obsidian-900 dark:text-ivory-100 border-b border-ivory-200 dark:border-obsidian-700 pb-3">
              Editorial Dossier & Cultural Significance
            </h2>
            <div className="font-serif text-base sm:text-lg leading-relaxed text-obsidian-800 dark:text-ivory-200 space-y-4 font-light">
              {destination.text ? (
                destination.text.split("\n").map((para, idx) => (
                  <p key={idx}>{para}</p>
                ))
              ) : (
                <p>{destination.excerpt}</p>
              )}
            </div>

            {/* Attribution Disclosure */}
            <div className="pt-4 border-t border-ivory-200 dark:border-obsidian-700 text-xs text-obsidian-500 dark:text-ivory-400 flex items-center justify-between">
              <span>{destination.attribution || "Licensed under CC BY-SA 4.0"}</span>
              <a
                href={destination.source_url || destination.wikipedia_url || "https://en.wikipedia.org"}
                target="_blank"
                rel="noopener noreferrer"
                className="text-terracotta hover:underline inline-flex items-center space-x-1"
              >
                <span>Canonical Wiki Entry</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* Interactive "Ask AI about Place" CTA */}
          <div className="rounded-3xl p-6 sm:p-8 bg-gradient-to-br from-terracotta to-saffron text-white shadow-xl space-y-4">
            <div className="flex items-center space-x-2 text-ivory-100 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Interactive Tour Guide Consultation</span>
            </div>
            <h3 className="font-serif text-2xl font-bold">
              Ask AI About {destination.place}
            </h3>
            <p className="text-xs sm:text-sm text-ivory-100 font-light leading-relaxed">
              Explore hidden architectural motifs, dynasties, surrounding sacred routes, or regional feast recipes with our grounded conversational guide.
            </p>
            <button
              onClick={handleLaunchChat}
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-full bg-obsidian-950 text-white hover:bg-black text-xs font-semibold uppercase tracking-wider shadow-lg active:scale-95 transition-all"
            >
              <Sparkles className="w-3.5 h-3.5 text-saffron" />
              <span>Consult Local AI Guide Now</span>
            </button>
          </div>
        </div>

        {/* Right Column: Geographical Context & Interactive Map */}
        <div className="lg:col-span-5 space-y-8">
          <div>
            <h3 className="font-serif text-lg font-bold text-obsidian-900 dark:text-ivory-100 mb-3 flex items-center space-x-2">
              <MapPin className="w-4 h-4 text-terracotta" />
              <span>Geographical Context & Cartography</span>
            </h3>
            <DestinationMap
              lat={destination.lat || destination.latitude || null}
              lon={destination.lon || destination.longitude || null}
              placeName={destination.place}
              stateName={destination.state}
              googleMapsUrl={destination.google_maps_url}
              directionsUrl={destination.directions_url}
            />
          </div>

          {/* Practical Planning Metadata */}
          <div className="bg-white dark:bg-obsidian-800 rounded-2xl p-6 border border-ivory-300 dark:border-obsidian-700 shadow-editorial space-y-3.5 text-xs">
            <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100 uppercase tracking-wider">
              Verified Dossier Facts
            </h4>
            <div className="flex justify-between py-1.5 border-b border-ivory-200 dark:border-obsidian-700">
              <span className="text-obsidian-500 dark:text-ivory-400">Google Maps GPS Pin:</span>
              <a
                href={
                  destination.google_maps_url ||
                  (destination.lat && destination.lon
                    ? `https://www.google.com/maps/search/?api=1&query=${destination.lat},${destination.lon}`
                    : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(destination.place + ", " + destination.state)}`)
                }
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold text-terracotta hover:underline inline-flex items-center space-x-1"
              >
                <span>
                  {destination.lat && destination.lon
                    ? `${destination.lat.toFixed(4)}° N, ${destination.lon.toFixed(4)}° E`
                    : "Open in Google Maps"}
                </span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
            <div className="flex justify-between py-1.5 border-b border-ivory-200 dark:border-obsidian-700">
              <span className="text-obsidian-500 dark:text-ivory-400">Administrative Region:</span>
              <span className="font-semibold text-obsidian-800 dark:text-ivory-200">{destination.state}</span>
            </div>
            {destination.city && (
              <div className="flex justify-between py-1.5 border-b border-ivory-200 dark:border-obsidian-700">
                <span className="text-obsidian-500 dark:text-ivory-400">Nearest Hub / City:</span>
                <span className="font-semibold text-obsidian-800 dark:text-ivory-200">{destination.city}</span>
              </div>
            )}
            <div className="flex justify-between py-1.5 border-b border-ivory-200 dark:border-obsidian-700">
              <span className="text-obsidian-500 dark:text-ivory-400">UNESCO World Heritage:</span>
              <span className="font-semibold text-obsidian-800 dark:text-ivory-200">
                {destination.is_unesco ? "Yes (Authoritative)" : "National Importance / Cultural Site"}
              </span>
            </div>
            {destination.best_time && (
              <div className="flex justify-between py-1.5">
                <span className="text-obsidian-500 dark:text-ivory-400">Best Season:</span>
                <span className="font-semibold text-terracotta dark:text-saffron">{destination.best_time}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 3. NEARBY PLACES GRID */}
      {destination.nearby && destination.nearby.length > 0 && (
        <div className="max-w-5xl mx-auto px-4 sm:px-6 mt-20 pt-12 border-t border-ivory-300 dark:border-obsidian-800">
          <div className="mb-8">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Subcontinental Proximity
            </span>
            <h3 className="font-serif text-2xl sm:text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
              Neighboring Wonders & Circuit Routes
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {destination.nearby.map((near, idx) => {
              const nearImg =
                near.image_url ||
                getDestinationImageUrl(near.id || near.slug || "", near.category || [], near.image_url);
              return (
                <Link
                  key={near.id || idx}
                  href={`/destinations/${near.slug || near.id}`}
                  className="group block rounded-2xl overflow-hidden bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-editorial hover:shadow-editorial-lg transition-all hover:-translate-y-1"
                >
                  <div className="relative h-32 w-full overflow-hidden bg-ivory-200 dark:bg-obsidian-900">
                    <img
                      src={nearImg}
                      alt={near.place}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950/70 via-obsidian-950/20 to-transparent" />
                    <div className="absolute top-2 right-2 text-[10px] px-2 py-0.5 rounded-full bg-black/60 text-white font-medium backdrop-blur-sm">
                      {near.distance_km ? `~${near.distance_km} km` : near.state}
                    </div>
                    <div className="absolute bottom-2 left-3 text-[11px] font-semibold text-saffron uppercase">
                      {near.state}
                    </div>
                  </div>
                  <div className="p-4">
                    <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta transition-colors line-clamp-1">
                      {near.place}
                    </h4>
                    <p className="text-xs text-obsidian-500 dark:text-ivory-400 mt-1 line-clamp-1">
                      Continue exploring this regional heritage circuit.
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
