"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MapPin, Award, Calendar, ArrowUpRight } from "lucide-react";
import { Destination } from "@/lib/types";
import { getDestinationImageUrl } from "@/lib/images";

interface DestinationCardProps {
  destination: Destination;
  priority?: boolean;
}

export function DestinationCard({ destination, priority = false }: DestinationCardProps) {
  const [imgError, setImgError] = useState(false);
  const imageUrl = getDestinationImageUrl(
    destination.id || destination.slug || "",
    destination.category || [],
    destination.image_url
  );

  return (
    <Link
      href={`/destinations/${destination.slug || destination.id}`}
      className="group block relative rounded-2xl overflow-hidden bg-white dark:bg-obsidian-800 border border-ivory-300/80 dark:border-obsidian-700/80 shadow-editorial hover:shadow-editorial-lg transition-all duration-300 hover:-translate-y-1"
    >
      {/* Visual Container */}
      <div className="relative aspect-[16/11] overflow-hidden bg-ivory-200 dark:bg-obsidian-900">
        {!imgError ? (
          <img
            src={imageUrl}
            alt={destination.place}
            loading={priority ? "eager" : "lazy"}
            onError={() => setImgError(true)}
            className="w-full h-full object-cover object-center transition-transform duration-700 ease-out group-hover:scale-105"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-terracotta/20 via-saffron/10 to-obsidian-900 flex items-center justify-center p-6 text-center">
            <span className="font-serif text-lg font-bold text-terracotta dark:text-saffron">
              {destination.place}
            </span>
          </div>
        )}

        {/* Subtle Vignette Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950/70 via-obsidian-950/20 to-transparent opacity-60 group-hover:opacity-40 transition-opacity" />

        {/* UNESCO Badge */}
        {destination.is_unesco && (
          <div className="absolute top-3 left-3 z-10 flex items-center space-x-1.5 px-3 py-1 rounded-full bg-gold/90 text-obsidian-950 text-[11px] font-bold tracking-wider uppercase shadow-md backdrop-blur-sm">
            <Award className="w-3.5 h-3.5 text-obsidian-950" />
            <span>UNESCO Heritage</span>
          </div>
        )}

        {/* Region & Location Badge */}
        <div className="absolute bottom-3 left-3 z-10 flex items-center space-x-1 text-white text-xs font-medium drop-shadow-md">
          <MapPin className="w-3.5 h-3.5 text-saffron" />
          <span>
            {destination.city ? `${destination.city}, ` : ""}
            {destination.state}
          </span>
        </div>

        {/* Corner Quick Actions on Hover: Google Maps + Dossier Link */}
        <div className="absolute top-3 right-3 z-10 flex items-center space-x-1.5 opacity-0 group-hover:opacity-100 transform translate-y-1 group-hover:translate-y-0 transition-all duration-200">
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              const gmapsUrl =
                destination.google_maps_url ||
                (destination.lat && destination.lon
                  ? `https://www.google.com/maps/search/?api=1&query=${destination.lat},${destination.lon}`
                  : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(destination.place + ", " + destination.state + ", India")}`);
              window.open(gmapsUrl, "_blank", "noopener,noreferrer");
            }}
            title="Open in Google Maps"
            className="w-8 h-8 rounded-full bg-ivory-50/95 dark:bg-obsidian-900/95 text-terracotta hover:bg-terracotta hover:text-white flex items-center justify-center shadow-md transition-colors"
          >
            <MapPin className="w-4 h-4" />
          </button>
          <div className="w-8 h-8 rounded-full bg-ivory-50/90 dark:bg-obsidian-900/90 text-obsidian-900 dark:text-ivory-100 flex items-center justify-center shadow-md">
            <ArrowUpRight className="w-4 h-4 text-terracotta" />
          </div>
        </div>
      </div>

      {/* Editorial Content */}
      <div className="p-5">
        {/* Category Pills */}
        <div className="flex flex-wrap gap-1.5 mb-2.5">
          {destination.category.slice(0, 2).map((cat, i) => (
            <span
              key={i}
              className="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full bg-ivory-200 dark:bg-obsidian-700 text-obsidian-700 dark:text-ivory-300"
            >
              {cat}
            </span>
          ))}
        </div>

        {/* Title */}
        <h3 className="font-serif text-lg font-bold text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta dark:group-hover:text-saffron transition-colors line-clamp-1 mb-2">
          {destination.place}
        </h3>

        {/* Excerpt */}
        {destination.excerpt && (
          <p className="text-xs text-obsidian-600 dark:text-ivory-300 line-clamp-2 leading-relaxed mb-4">
            {destination.excerpt}
          </p>
        )}

        {/* Best time to visit chip if verified */}
        {destination.best_time && (
          <div className="flex items-center space-x-1.5 pt-3 border-t border-ivory-200 dark:border-obsidian-700/60 text-[11px] text-terracotta dark:text-saffron font-medium">
            <Calendar className="w-3 h-3 flex-shrink-0" />
            <span className="truncate">{destination.best_time}</span>
          </div>
        )}
      </div>
    </Link>
  );
}
