"use client";

import React, { useState, useRef, useEffect } from "react";
import { Globe, ChevronDown, Check, Sparkles } from "lucide-react";
import { INDIAN_LANGUAGES, getLanguageOption, DetailedLanguageOption } from "@/lib/languages";
import { SupportedLanguage } from "@/lib/types";

interface LanguageSelectorProps {
  currentLanguage: SupportedLanguage;
  onSelectLanguage: (lang: SupportedLanguage) => void;
  className?: string;
  compact?: boolean;
}

export function LanguageSelector({
  currentLanguage,
  onSelectLanguage,
  className = "",
  compact = false,
}: LanguageSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const activeOption = getLanguageOption(currentLanguage);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className={`relative inline-block text-left ${className}`} ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-ivory-200/90 dark:bg-obsidian-800/90 border border-ivory-300 dark:border-obsidian-700 text-obsidian-800 dark:text-ivory-100 text-xs font-semibold hover:border-terracotta dark:hover:border-saffron shadow-sm transition-all"
        title="Select Native Indian Language"
      >
        <span className="text-sm">{activeOption.flag}</span>
        <span className="font-medium truncate max-w-[100px]">{activeOption.native}</span>
        {!compact && (
          <span className="text-[10px] text-obsidian-500 dark:text-ivory-400 uppercase hidden sm:inline">
            ({activeOption.code})
          </span>
        )}
        <ChevronDown className={`w-3.5 h-3.5 text-obsidian-500 dark:text-ivory-400 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-72 sm:w-80 max-h-96 overflow-y-auto rounded-2xl bg-white dark:bg-obsidian-900 border border-ivory-300 dark:border-obsidian-700 shadow-2xl z-50 p-2 scrollbar-thin">
          <div className="px-3 py-2 border-b border-ivory-200 dark:border-obsidian-800 mb-1 flex items-center justify-between">
            <div className="flex items-center space-x-1.5 text-xs font-bold uppercase tracking-wider text-terracotta dark:text-saffron">
              <Globe className="w-3.5 h-3.5" />
              <span>Native Languages ({INDIAN_LANGUAGES.length})</span>
            </div>
            <span className="text-[10px] text-obsidian-500 dark:text-ivory-400">Jokes & Storytelling</span>
          </div>

          <div className="grid grid-cols-1 gap-1">
            {INDIAN_LANGUAGES.map((lang) => {
              const isSelected = lang.code === currentLanguage;
              return (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => {
                    onSelectLanguage(lang.code);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-xl text-xs transition-colors flex items-center justify-between ${
                    isSelected
                      ? "bg-terracotta/10 dark:bg-saffron/10 text-terracotta dark:text-saffron font-bold border border-terracotta/30 dark:border-saffron/30"
                      : "hover:bg-ivory-100 dark:hover:bg-obsidian-800 text-obsidian-800 dark:text-ivory-200"
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <span className="text-base">{lang.flag}</span>
                    <div>
                      <div className="font-semibold text-xs leading-tight flex items-center space-x-1.5">
                        <span>{lang.native}</span>
                        <span className="text-[11px] font-normal text-obsidian-500 dark:text-ivory-400">
                          ({lang.name})
                        </span>
                      </div>
                      <div className="text-[10px] text-obsidian-500 dark:text-ivory-400 line-clamp-1 mt-0.5 font-light">
                        {lang.sampleJoke.slice(0, 38)}...
                      </div>
                    </div>
                  </div>
                  {isSelected && <Check className="w-4 h-4 text-terracotta dark:text-saffron flex-shrink-0" />}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
