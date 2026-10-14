"use client";

import React, { useEffect, useState } from "react";
import { MapPin, Navigation, ExternalLink, Compass } from "lucide-react";

interface DestinationMapProps {
  lat: number | null;
  lon: number | null;
  placeName: string;
  stateName: string;
  googleMapsUrl?: string;
  directionsUrl?: string;
}

export function DestinationMap({
  lat,
  lon,
  placeName,
  stateName,
  googleMapsUrl,
  directionsUrl,
}: DestinationMapProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const gmapsSearchUrl =
    googleMapsUrl ||
    (lat && lon
      ? `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`
      : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${placeName}, ${stateName}, India`)}`);

  const gmapsDirectionsUrl =
    directionsUrl ||
    (lat && lon
      ? `https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}`
      : `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(`${placeName}, ${stateName}`)}`);

  if (!lat || !lon) {
    return (
      <div className="rounded-2xl border border-dashed border-ivory-300 dark:border-obsidian-700 bg-ivory-200/50 dark:bg-obsidian-800/50 p-8 text-center space-y-3">
        <MapPin className="w-8 h-8 mx-auto text-terracotta dark:text-saffron mb-2 opacity-80" />
        <h4 className="font-serif text-base font-semibold text-obsidian-800 dark:text-ivory-200">
          Open in Google Maps
        </h4>
        <p className="text-xs text-obsidian-500 dark:text-ivory-400 max-w-sm mx-auto">
          Explore {placeName} with live satellite imagery and GPS navigation on Google Maps.
        </p>
        <a
          href={gmapsSearchUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-terracotta text-white text-xs font-semibold hover:bg-terracotta/90 transition-all shadow-sm"
        >
          <MapPin className="w-3.5 h-3.5" />
          <span>Search on Google Maps</span>
          <ExternalLink className="w-3 h-3 ml-1" />
        </a>
      </div>
    );
  }

  // OpenStreetMap embed for live visual preview
  const osmUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${lon - 0.05}%2C${lat - 0.05}%2C${lon + 0.05}%2C${lat + 0.05}&layer=mapnik&marker=${lat}%2C${lon}`;

  return (
    <div className="rounded-2xl overflow-hidden border border-ivory-300 dark:border-obsidian-700 bg-white dark:bg-obsidian-800 shadow-editorial">
      {/* Map Header */}
      <div className="px-5 py-3.5 border-b border-ivory-200 dark:border-obsidian-700 flex flex-wrap items-center justify-between gap-2 bg-ivory-100/60 dark:bg-obsidian-900/60">
        <div className="flex items-center space-x-2">
          <Navigation className="w-4 h-4 text-terracotta" />
          <span className="text-xs font-semibold text-obsidian-800 dark:text-ivory-100 uppercase tracking-wider">
            GPS: {lat.toFixed(4)}° N, {lon.toFixed(4)}° E
          </span>
        </div>
        <div className="flex items-center space-x-2">
          {/* Direct Google Maps Action Pill */}
          <a
            href={gmapsSearchUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-terracotta text-white text-xs font-semibold hover:bg-terracotta/90 transition-all shadow-sm"
          >
            <MapPin className="w-3 h-3" />
            <span>Open in Google Maps</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      {/* Map View */}
      <div className="relative w-full h-[360px] bg-ivory-200 dark:bg-obsidian-900">
        {mounted && (
          <iframe
            title={`Interactive map of ${placeName}`}
            src={osmUrl}
            className="w-full h-full border-0 filter contrast-[1.02]"
            loading="lazy"
          />
        )}

        {/* Floating Quick Navigation Overlay */}
        <div className="absolute bottom-4 right-4 z-10 flex flex-col sm:flex-row gap-2">
          <a
            href={gmapsDirectionsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-obsidian-950/90 text-white hover:bg-black text-xs font-semibold backdrop-blur-md border border-white/20 shadow-lg transition-transform hover:scale-105"
          >
            <Compass className="w-3.5 h-3.5 text-saffron" />
            <span>Get Directions</span>
          </a>
          <a
            href={gmapsSearchUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-white/95 text-obsidian-950 hover:bg-white text-xs font-semibold backdrop-blur-md border border-black/10 shadow-lg transition-transform hover:scale-105"
          >
            <MapPin className="w-3.5 h-3.5 text-terracotta" />
            <span>Google Maps Pin</span>
          </a>
        </div>
      </div>

      {/* Map Footer Attribution & Info */}
      <div className="px-5 py-2.5 bg-ivory-100/40 dark:bg-obsidian-900/40 border-t border-ivory-200 dark:border-obsidian-700/60 text-[11px] text-obsidian-500 dark:text-ivory-400 flex items-center justify-between">
        <span>Cartography verified & linked to Google Maps GPS coordinates</span>
        <span className="font-serif italic text-terracotta dark:text-saffron">
          {placeName}, {stateName}
        </span>
      </div>
    </div>
  );
}
