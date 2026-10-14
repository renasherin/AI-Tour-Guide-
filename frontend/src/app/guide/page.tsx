"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  Send,
  RotateCcw,
  Compass,
  ArrowRight,
  ShieldCheck,
  Smile,
  UtensilsCrossed,
} from "lucide-react";
import { ChatMessageItem } from "@/components/chat/ChatMessageItem";
import { ChatMessage, SourceCitation, FollowUpSuggestion, SupportedLanguage } from "@/lib/types";
import { LanguageSelector } from "@/components/chat/LanguageSelector";
import { getLanguageOption } from "@/lib/languages";
import { streamRAGChat } from "@/lib/api";

export default function GuidePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [language, setLanguage] = useState<SupportedLanguage>("en");
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId, setSessionId] = useState("guide-session-" + Date.now());

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const activeLangConfig = getLanguageOption(language);

  // Initialize or restore session
  useEffect(() => {
    const saved = localStorage.getItem("incredible_journeys_guide_history");
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {}
    } else {
      setMessages([
        {
          id: "intro-1",
          role: "assistant",
          content: `${activeLangConfig.greeting}\n\n${activeLangConfig.sampleJoke}`,
          timestamp: "Just now",
          suggestions: activeLangConfig.starterPrompts.map((s) => ({ prompt: s.prompt })),
        },
      ]);
    }
  }, []);

  // Save to local storage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("incredible_journeys_guide_history", JSON.stringify(messages));
    }
  }, [messages]);

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (customPrompt?: string) => {
    const query = (customPrompt || inputMessage).trim();
    if (!query || isStreaming) return;

    setInputMessage("");

    const userMsgId = "user-" + Date.now();
    const assistantMsgId = "assistant-" + (Date.now() + 1);

    const newMessages: ChatMessage[] = [
      ...messages,
      {
        id: userMsgId,
        role: "user",
        content: query,
        timestamp: "Just now",
      },
      {
        id: assistantMsgId,
        role: "assistant",
        content: "",
        timestamp: "Consulting Archives...",
        isStreaming: true,
        sources: [],
        suggestions: [],
      },
    ];

    setMessages(newMessages);
    setIsStreaming(true);

    let accumulatedContent = "";
    let capturedSources: SourceCitation[] = [];
    let capturedSuggestions: FollowUpSuggestion[] = [];

    await streamRAGChat(query, sessionId, language, {
      onToken: (token: string) => {
        accumulatedContent += token;
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, content: accumulatedContent } : m
          )
        );
      },
      onSources: (sources: SourceCitation[]) => {
        capturedSources = sources;
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, sources } : m
          )
        );
      },
      onSuggestions: (suggestions: FollowUpSuggestion[]) => {
        capturedSuggestions = suggestions;
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, suggestions } : m
          )
        );
      },
      onDone: () => {
        setIsStreaming(false);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  isStreaming: false,
                  timestamp: "Just now",
                  sources: capturedSources,
                  suggestions: capturedSuggestions,
                }
              : m
          )
        );
      },
      onError: (err: Error) => {
        setIsStreaming(false);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  isStreaming: false,
                  content:
                    accumulatedContent ||
                    "I encountered a temporary communication glitch while consulting the knowledge base. Please try asking again!",
                }
              : m
          )
        );
      },
    });
  };

  const handleResetSession = () => {
    localStorage.removeItem("incredible_journeys_guide_history");
    setSessionId("guide-session-" + Date.now());
    setMessages([
      {
        id: "fresh-session",
        role: "assistant",
        content: `${activeLangConfig.greeting}\n\n${activeLangConfig.sampleJoke}`,
        timestamp: "Just now",
        suggestions: activeLangConfig.starterPrompts.map((s) => ({ prompt: s.prompt })),
      },
    ]);
  };

  const handleSelectLanguage = (newLang: SupportedLanguage) => {
    setLanguage(newLang);
    const cfg = getLanguageOption(newLang);
    // Add brief friendly greeting announcing language switch
    setMessages((prev) => [
      ...prev,
      {
        id: "lang-switch-" + Date.now(),
        role: "assistant",
        content: `🌐 **Language Switched to ${cfg.native} (${cfg.name})**\n\n${cfg.greeting}\n\n${cfg.sampleJoke}`,
        timestamp: "Just now",
        suggestions: cfg.starterPrompts.map((s) => ({ prompt: s.prompt })),
      },
    ]);
  };

  return (
    <div className="pt-20 min-h-screen flex flex-col bg-ivory-100 dark:bg-obsidian-900 transition-colors">
      {/* Top Banner & Control Bar */}
      <div className="bg-white dark:bg-obsidian-850 border-b border-ivory-300 dark:border-obsidian-750 px-4 sm:px-8 py-3.5 shadow-sm sticky top-16 z-30">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-terracotta flex items-center justify-center text-white shadow-sm">
              <Sparkles className="w-4 h-4 text-saffron" />
            </div>
            <div>
              <h1 className="font-serif text-base sm:text-lg font-bold text-obsidian-900 dark:text-ivory-100 flex items-center space-x-2">
                <span>AI Tour Guide for India</span>
                <span className="hidden sm:inline-block text-[10px] font-sans px-2 py-0.5 rounded-full bg-viridian/10 text-viridian font-bold">
                  {activeLangConfig.native} Mode
                </span>
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Native Indian Language Selector */}
            <LanguageSelector
              currentLanguage={language}
              onSelectLanguage={handleSelectLanguage}
            />

            {/* Reset Button */}
            <button
              onClick={handleResetSession}
              className="p-2 rounded-full bg-ivory-200 dark:bg-obsidian-750 text-obsidian-700 dark:text-ivory-300 hover:bg-terracotta hover:text-white transition-colors"
              title="Reset conversation session"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Conversation Stream */}
      <div className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-6 overflow-y-auto space-y-4">
        {/* Starter Prompt Inspiration Chips (if only welcome message) */}
        {messages.length <= 2 && (
          <div className="my-4 p-6 rounded-3xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-editorial space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-ivory-200 dark:border-obsidian-750 pb-3">
              <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-terracotta dark:text-saffron">
                <Compass className="w-4 h-4" />
                <span>{activeLangConfig.native} Explorations & Legends:</span>
              </div>
              <button
                onClick={() =>
                  handleSendMessage(
                    language === "ml"
                      ? "യാത്രകളെക്കുറിച്ച് രസകരമായ ഒരു തമാശ പറയൂ!"
                      : language === "hi"
                      ? "यात्रा और खान-पान पर एक मजेदार चुटकुला सुनाओ!"
                      : "Tell me a hilarious and witty travel joke about India!"
                  )
                }
                className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-saffron/10 text-saffron dark:text-saffron-400 text-xs font-semibold hover:bg-saffron/20 transition-colors self-start sm:self-auto"
              >
                <Smile className="w-3.5 h-3.5" />
                <span>Hear a Travel Joke 😄</span>
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              {activeLangConfig.starterPrompts.map((starter, i) => (
                <button
                  key={i}
                  onClick={() => handleSendMessage(starter.prompt)}
                  className="text-left p-3.5 rounded-xl bg-ivory-100 dark:bg-obsidian-900 border border-ivory-200 dark:border-obsidian-750 hover:border-terracotta hover:shadow-sm transition-all group"
                >
                  <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta flex items-center justify-between">
                    <span>{starter.title}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-terracotta opacity-0 group-hover:opacity-100 transition-opacity" />
                  </h4>
                  <p className="text-xs text-obsidian-500 dark:text-ivory-400 line-clamp-1 mt-1 font-light">
                    {starter.prompt}
                  </p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message Items */}
        {messages.map((msg) => (
          <ChatMessageItem
            key={msg.id}
            message={msg}
            onSuggestionClick={(prompt) => handleSendMessage(prompt)}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Sticky Bottom Input Bar */}
      <div className="sticky bottom-0 z-20 bg-ivory-100/90 dark:bg-obsidian-900/90 backdrop-blur-md border-t border-ivory-300 dark:border-obsidian-800 py-4 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto space-y-2">
          {/* Quick Action Chips */}
          <div className="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-none text-xs">
            <button
              type="button"
              onClick={() =>
                handleSendMessage(
                  language === "ml"
                    ? "കോഴിക്കോടൻ ദം ബിരിയാണിയും ഹൽവയും എവിടെയാണ് ഏറ്റവും മികച്ചത്?"
                    : "Tell me about Kozhikode Dum Biryani and S.M. Street Halwa with authentic photos and places to try!"
                )
              }
              className="whitespace-nowrap px-3 py-1 rounded-full bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-700 dark:text-ivory-300 hover:border-terracotta flex items-center space-x-1"
            >
              <UtensilsCrossed className="w-3 h-3 text-terracotta" />
              <span>Famous Foods 🍲</span>
            </button>
            <button
              type="button"
              onClick={() =>
                handleSendMessage(
                  language === "ml"
                    ? "ഒരു അടിപൊളി ട്രാവൽ തമാശ പറയൂ!"
                    : language === "hi"
                    ? "एक मजेदार यात्रा का जोक सुनाओ!"
                    : "Tell me a funny and witty travel joke!"
                )
              }
              className="whitespace-nowrap px-3 py-1 rounded-full bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-700 dark:text-ivory-300 hover:border-terracotta flex items-center space-x-1"
            >
              <Smile className="w-3 h-3 text-saffron" />
              <span>Tell Joke 😄</span>
            </button>
            <button
              type="button"
              onClick={() =>
                handleSendMessage(
                  language === "ml"
                    ? "പാലക്കാട്ടെ കാഞ്ഞിരപ്പുഴ ഡാമും വെറ്റിലച്ചോലയും സന്ദർശിക്കാൻ പറ്റിയ സമയം എപ്പോഴാണ്?"
                    : "Tell me about Kanjirapuzha Dam in Palakkad and how to plan a visit!"
                )
              }
              className="whitespace-nowrap px-3 py-1 rounded-full bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-700 dark:text-ivory-300 hover:border-terracotta flex items-center space-x-1"
            >
              <Compass className="w-3 h-3 text-viridian" />
              <span>Kanjirapuzha Dam 💧</span>
            </button>
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center space-x-3 bg-white dark:bg-obsidian-800 rounded-full p-2 border border-ivory-300 dark:border-obsidian-700 shadow-xl"
          >
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={activeLangConfig.placeholder}
              disabled={isStreaming}
              className="flex-1 bg-transparent px-5 py-2.5 text-sm text-obsidian-900 dark:text-ivory-100 placeholder-obsidian-400 dark:placeholder-ivory-400 focus:outline-none disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isStreaming}
              className="p-3 rounded-full bg-terracotta hover:bg-terracotta-600 text-white disabled:opacity-40 transition-all shadow-md active:scale-95 flex items-center justify-center"
              aria-label="Send query"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          <div className="flex items-center justify-between text-[11px] text-obsidian-500 dark:text-ivory-400 px-4 pt-1">
            <span className="flex items-center space-x-1">
              <ShieldCheck className="w-3.5 h-3.5 text-viridian" />
              <span>Grounded with verified Wikipedia open data & Google Maps</span>
            </span>
            <span className="font-medium text-terracotta dark:text-saffron">
              {activeLangConfig.native} ({activeLangConfig.name})
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
