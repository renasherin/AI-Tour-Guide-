"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import { Sparkles, User, ExternalLink, BookmarkCheck, ArrowRight, MapPin } from "lucide-react";
import { ChatMessage, SourceCitation, FollowUpSuggestion } from "@/lib/types";

interface ChatMessageItemProps {
  message: ChatMessage;
  onSuggestionClick?: (prompt: string) => void;
}

export function ChatMessageItem({ message, onSuggestionClick }: ChatMessageItemProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex flex-col space-y-2.5 my-3 ${
        isUser ? "items-end" : "items-start"
      } animate-fade-in-slide`}
    >
      {/* Message Header & Role Avatar */}
      <div className={`flex items-center space-x-2 text-xs text-obsidian-500 dark:text-ivory-400 ${isUser ? "flex-row-reverse space-x-reverse" : ""}`}>
        <div
          className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${
            isUser
              ? "bg-obsidian-700 text-ivory-100 dark:bg-ivory-300 dark:text-obsidian-900"
              : "bg-terracotta text-white"
          }`}
        >
          {isUser ? <User className="w-3.5 h-3.5" /> : <Sparkles className="w-3.5 h-3.5" />}
        </div>
        <span className="font-medium tracking-wide">
          {isUser ? "You" : "Incredible Journeys Guide"}
        </span>
        <span className="text-[10px] opacity-60">{message.timestamp}</span>
      </div>

      {/* Bubble Container */}
      <div
        className={`max-w-[88%] sm:max-w-[80%] rounded-2xl px-5 py-4 text-sm leading-relaxed shadow-sm ${
          isUser
            ? "bg-terracotta text-white rounded-tr-none font-normal"
            : "bg-white dark:bg-obsidian-800 text-obsidian-900 dark:text-ivory-100 border border-ivory-300 dark:border-obsidian-700 rounded-tl-none font-serif"
        }`}
      >
        <div className={`prose dark:prose-invert max-w-none text-sm ${isUser ? "text-white" : ""}`}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {/* Streaming Cursor Indicator */}
        {message.isStreaming && (
          <span className="inline-block w-2 h-4 ml-1 bg-terracotta dark:bg-saffron animate-pulse" />
        )}
      </div>

      {/* Source Citations Badges with Direct Google Maps Link */}
      {!isUser && message.sources && message.sources.length > 0 && (
        <div className="max-w-[88%] sm:max-w-[80%] space-y-1.5 pt-1">
          <div className="flex items-center space-x-1 text-[11px] font-semibold uppercase tracking-wider text-obsidian-600 dark:text-ivory-400">
            <BookmarkCheck className="w-3.5 h-3.5 text-terracotta dark:text-saffron" />
            <span>Authoritative Sources & Google Maps:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {message.sources.map((src, idx) => {
              const gmapsUrl =
                src.google_maps_url ||
                (src.lat && src.lon
                  ? `https://www.google.com/maps/search/?api=1&query=${src.lat},${src.lon}`
                  : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${src.place || src.title}, ${src.state || "India"}`)}`);
              return (
                <div key={idx} className="inline-flex items-center shadow-sm">
                  <a
                    href={src.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-l-lg text-xs bg-ivory-200/90 dark:bg-obsidian-700/80 border border-r-0 border-ivory-300 dark:border-obsidian-600 text-obsidian-800 dark:text-ivory-200 hover:border-terracotta hover:bg-white dark:hover:bg-obsidian-600 transition-all"
                  >
                    <span className="font-semibold text-terracotta dark:text-saffron">
                      {src.title || src.place || "Verified Source"}
                    </span>
                    <span className="text-[10px] text-obsidian-500 dark:text-ivory-400">
                      ({src.state || "India"})
                    </span>
                    <ExternalLink className="w-3 h-3 text-obsidian-400 group-hover:text-terracotta transition-colors" />
                  </a>
                  <a
                    href={gmapsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    title={`Open ${src.place || src.title} in Google Maps`}
                    className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-r-lg text-xs bg-terracotta hover:bg-terracotta/90 text-white font-medium border border-terracotta transition-colors"
                  >
                    <MapPin className="w-3 h-3 text-saffron" />
                    <span className="text-[11px] font-semibold">Maps</span>
                  </a>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Interactive Follow-Up Suggestion Chips */}
      {!isUser && message.suggestions && message.suggestions.length > 0 && (
        <div className="max-w-[88%] sm:max-w-[80%] pt-2 space-y-1.5">
          <p className="text-[11px] font-semibold text-obsidian-500 dark:text-ivory-400 uppercase tracking-wider">
            Suggested Next Inquiries:
          </p>
          <div className="flex flex-wrap gap-2">
            {message.suggestions.map((sugg, idx) => (
              <button
                key={idx}
                onClick={() => onSuggestionClick?.(sugg.prompt)}
                className="group inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-medium bg-ivory-100 dark:bg-obsidian-800 border border-saffron/40 hover:border-terracotta text-obsidian-800 dark:text-ivory-200 hover:text-terracotta transition-all shadow-sm"
              >
                <span>{sugg.prompt}</span>
                <ArrowRight className="w-3 h-3 text-saffron group-hover:translate-x-0.5 transition-transform" />
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
