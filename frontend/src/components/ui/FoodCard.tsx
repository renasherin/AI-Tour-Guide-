"use client";

import React, { useState } from "react";
import { Utensils, MapPin, Sparkles, MessageSquare, Coffee } from "lucide-react";
import { FoodItem } from "@/lib/types";

interface FoodCardProps {
  food: FoodItem;
}

export function FoodCard({ food }: FoodCardProps) {
  const [imgError, setImgError] = useState(false);

  const handleAskAI = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    const prompt = `Tell me the rich cultural story, authentic recipe secrets, and best historic spots to taste ${food.name} (${food.native_name}) in ${food.state}!`;
    const event = new CustomEvent("open-ai-chat", { detail: { prompt } });
    window.dispatchEvent(event);
  };

  return (
    <div className="group relative rounded-2xl overflow-hidden bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-editorial hover:shadow-editorial-lg transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
      {/* Visual Header */}
      <div className="relative aspect-[16/11] overflow-hidden bg-ivory-200 dark:bg-obsidian-900">
        {!imgError ? (
          <img
            src={food.image_url}
            alt={food.name}
            onError={() => setImgError(true)}
            className="w-full h-full object-cover object-center transition-transform duration-700 ease-out group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-terracotta/20 via-saffron/10 to-obsidian-900 flex items-center justify-center p-6 text-center">
            <span className="font-serif text-lg font-bold text-terracotta dark:text-saffron">
              {food.name}
            </span>
          </div>
        )}

        <div className="absolute inset-0 bg-gradient-to-t from-obsidian-950/80 via-obsidian-950/20 to-transparent opacity-60 group-hover:opacity-40 transition-opacity" />

        {/* Veg / Non-Veg Standard Mark */}
        <div className="absolute top-3 left-3 z-10 flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-white/95 dark:bg-obsidian-900/95 backdrop-blur-md shadow-sm">
          <div
            className={`w-3 h-3 rounded-sm border flex items-center justify-center ${
              food.is_veg
                ? "border-green-600 bg-green-50"
                : "border-red-600 bg-red-50"
            }`}
          >
            <div
              className={`w-1.5 h-1.5 rounded-full ${
                food.is_veg ? "bg-green-600" : "bg-red-600"
              }`}
            />
          </div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-obsidian-800 dark:text-ivory-200">
            {food.is_veg ? "Veg" : "Non-Veg"}
          </span>
        </div>

        {/* State / Region Pill */}
        <div className="absolute bottom-3 left-3 z-10 flex items-center space-x-1 text-white text-xs font-semibold drop-shadow-md">
          <MapPin className="w-3.5 h-3.5 text-saffron" />
          <span>{food.state} ({food.region})</span>
        </div>

        {/* Category Pill */}
        <div className="absolute top-3 right-3 z-10 px-2.5 py-0.5 rounded-full bg-black/60 text-white text-[10px] font-bold uppercase tracking-wider backdrop-blur-sm">
          {food.category}
        </div>
      </div>

      {/* Content */}
      <div className="p-5 flex-1 flex flex-col justify-between space-y-3">
        <div>
          <div className="flex items-baseline justify-between gap-1 mb-1">
            <h3 className="font-serif text-lg font-bold text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta transition-colors line-clamp-1">
              {food.name}
            </h3>
          </div>
          <p className="text-xs font-medium text-terracotta dark:text-saffron mb-2">
            {food.native_name}
          </p>

          <p className="text-xs text-obsidian-600 dark:text-ivory-300 line-clamp-2 leading-relaxed mb-3">
            {food.story}
          </p>

          {/* Flavor Profile */}
          <div className="p-2.5 rounded-xl bg-ivory-100 dark:bg-obsidian-900 border border-ivory-200 dark:border-obsidian-750 text-[11px] text-obsidian-700 dark:text-ivory-300 leading-normal">
            <span className="font-semibold text-terracotta dark:text-saffron block mb-0.5">
              Flavor Profile:
            </span>
            <span className="line-clamp-2">{food.flavor_profile}</span>
          </div>
        </div>

        {/* Best Places & Ask AI CTA */}
        <div className="pt-2 border-t border-ivory-200 dark:border-obsidian-750 space-y-2">
          {food.pairing && (
            <div className="flex items-center space-x-1.5 text-[11px] text-obsidian-500 dark:text-ivory-400">
              <Coffee className="w-3.5 h-3.5 text-saffron flex-shrink-0" />
              <span className="truncate">Pairing: {food.pairing}</span>
            </div>
          )}

          <button
            type="button"
            onClick={handleAskAI}
            className="w-full inline-flex items-center justify-center space-x-2 py-2 px-3 rounded-xl bg-ivory-200 dark:bg-obsidian-700 hover:bg-terracotta hover:text-white dark:hover:bg-terracotta text-obsidian-800 dark:text-ivory-200 text-xs font-semibold transition-all group/btn"
          >
            <Sparkles className="w-3.5 h-3.5 text-saffron group-hover/btn:text-white" />
            <span>Ask AI Storyteller</span>
          </button>
        </div>
      </div>
    </div>
  );
}
