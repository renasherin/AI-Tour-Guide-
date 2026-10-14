"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  Sparkles,
  X,
  Send,
  Minimize2,
  Maximize2,
  Globe,
  RotateCcw,
  ExternalLink,
} from "lucide-react";
import { ChatMessageItem } from "./ChatMessageItem";
import { LanguageSelector } from "./LanguageSelector";
import { ChatMessage, SourceCitation, FollowUpSuggestion, SupportedLanguage } from "@/lib/types";
import { getLanguageOption } from "@/lib/languages";
import { streamRAGChat } from "@/lib/api";

export function GlobalChatDrawer() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [language, setLanguage] = useState<SupportedLanguage>("en");
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId, setSessionId] = useState("session-" + Date.now());

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Initialize or restore session
  useEffect(() => {
    const saved = sessionStorage.getItem("incredible_journeys_chat_history");
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {}
    } else {
      setMessages([
        {
          id: "welcome-1",
          role: "assistant",
          content:
            "Namaste! I am your AI Tour Guide for Incredible Journeys. Ask me about any destination, ancient temple, Mughal fort, Himalayan pass, or regional delicacy across India's 28 states and 8 union territories.",
          timestamp: "Just now",
          suggestions: [
            { prompt: "Tell me about the boulder monuments of Hampi" },
            { prompt: "What are the best places to visit in Kerala in winter?" },
            { prompt: "Which UNESCO sites are located in Madhya Pradesh?" },
          ],
        },
      ]);
    }

    // Listen for custom trigger to open chat with preloaded prompt
    const handleOpenChat = (event: CustomEvent<{ prompt?: string }>) => {
      setIsOpen(true);
      setIsMinimized(false);
      if (event.detail?.prompt) {
        setInputMessage(event.detail.prompt);
        setTimeout(() => {
          inputRef.current?.focus();
        }, 300);
      }
    };

    window.addEventListener("open-ai-chat" as any, handleOpenChat);
    return () => window.removeEventListener("open-ai-chat" as any, handleOpenChat);
  }, []);

  // Persist session
  useEffect(() => {
    if (messages.length > 0) {
      sessionStorage.setItem("incredible_journeys_chat_history", JSON.stringify(messages));
    }
  }, [messages]);

  // Scroll to bottom
  useEffect(() => {
    if (isOpen && !isMinimized) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen, isMinimized]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputMessage).trim();
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
        timestamp: "Generating...",
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
      onToken: (token) => {
        accumulatedContent += token;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? { ...msg, content: accumulatedContent, isStreaming: true }
              : msg
          )
        );
      },
      onSources: (sources) => {
        capturedSources = sources;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId ? { ...msg, sources } : msg
          )
        );
      },
      onSuggestions: (suggestions) => {
        capturedSuggestions = suggestions;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId ? { ...msg, suggestions } : msg
          )
        );
      },
      onDone: () => {
        setIsStreaming(false);
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? {
                  ...msg,
                  content: accumulatedContent || "Here are insights based on verified open travel sources.",
                  isStreaming: false,
                  sources: capturedSources,
                  suggestions: capturedSuggestions,
                }
              : msg
          )
        );
      },
      onError: (err) => {
        setIsStreaming(false);
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? {
                  ...msg,
                  content:
                    "I encountered a temporary connection issue reaching the knowledge engine. Please verify the backend service is active.",
                  isStreaming: false,
                }
              : msg
          )
        );
      },
    });
  };

  const handleReset = () => {
    sessionStorage.removeItem("incredible_journeys_chat_history");
    setSessionId("session-" + Date.now());
    setMessages([
      {
        id: "welcome-fresh",
        role: "assistant",
        content:
          "Namaste! Session reset. How can I assist your Indian voyage today?",
        timestamp: "Just now",
        suggestions: [
          { prompt: "Tell me about the Living Root Bridges in Meghalaya" },
          { prompt: "What are the key sights in Old Goa?" },
        ],
      },
    ]);
  };

  return (
    <>
      {/* Floating Launcher Pill */}
      {!isOpen && (
        <button
          onClick={() => {
            setIsOpen(true);
            setIsMinimized(false);
          }}
          className="fixed bottom-6 right-6 z-50 flex items-center space-x-2 px-5 py-3.5 rounded-full bg-terracotta hover:bg-terracotta-600 text-white font-medium text-sm shadow-editorial-lg hover:shadow-gold transition-all duration-300 hover:scale-105 active:scale-95 group"
          aria-label="Open AI Tour Guide"
        >
          <Sparkles className="w-4 h-4 text-saffron group-hover:rotate-12 transition-transform" />
          <span className="font-semibold tracking-wide">Ask Tour Guide</span>
        </button>
      )}

      {/* Popover / Mobile Bottom Sheet */}
      {isOpen && (
        <div
          className={`fixed z-50 transition-all duration-300 ${
            isMinimized
              ? "bottom-6 right-6 w-72 h-14 rounded-2xl shadow-editorial-lg"
              : "bottom-0 right-0 sm:bottom-6 sm:right-6 w-full sm:w-[440px] h-[85vh] sm:h-[620px] rounded-t-3xl sm:rounded-2xl shadow-2xl"
          } bg-ivory-100 dark:bg-obsidian-900 border border-ivory-300 dark:border-obsidian-700 flex flex-col overflow-hidden backdrop-blur-xl`}
        >
          {/* Header Bar */}
          <div className="px-5 py-3.5 bg-ivory-200/80 dark:bg-obsidian-800/80 border-b border-ivory-300 dark:border-obsidian-700 flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <div className="w-7 h-7 rounded-full bg-terracotta flex items-center justify-center text-white">
                <Sparkles className="w-3.5 h-3.5" />
              </div>
              <div>
                <h3 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100 flex items-center space-x-2">
                  <span>AI Tour Guide</span>
                  <span className="text-[10px] font-sans px-1.5 py-0.2 rounded bg-terracotta/10 text-terracotta dark:text-saffron font-semibold uppercase">
                    RAG Verified
                  </span>
                </h3>
              </div>
            </div>

            <div className="flex items-center space-x-1.5 text-obsidian-600 dark:text-ivory-400">
              {/* Native Language Selector */}
              <LanguageSelector
                currentLanguage={language}
                onSelectLanguage={setLanguage}
                compact={true}
              />

              {/* Reset Session */}
              <button
                onClick={handleReset}
                className="p-1.5 rounded hover:bg-ivory-300 dark:hover:bg-obsidian-700 transition-colors"
                title="Reset session"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              {/* Open Full Guide */}
              <Link
                href="/guide"
                className="p-1.5 rounded hover:bg-ivory-300 dark:hover:bg-obsidian-700 transition-colors"
                title="Open Dedicated Fullscreen Tour Guide"
              >
                <ExternalLink className="w-3.5 h-3.5" />
              </Link>

              {/* Minimize */}
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="hidden sm:block p-1.5 rounded hover:bg-ivory-300 dark:hover:bg-obsidian-700 transition-colors"
                title={isMinimized ? "Expand" : "Minimize"}
              >
                {isMinimized ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}
              </button>

              {/* Close */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded hover:bg-ivory-300 dark:hover:bg-obsidian-700 transition-colors"
                title="Close drawer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {!isMinimized && (
            <>
              {/* Message Scroll View */}
              <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-3 bg-ivory-50/50 dark:bg-obsidian-950/40">
                {messages.map((msg) => (
                  <ChatMessageItem
                    key={msg.id}
                    message={msg}
                    onSuggestionClick={(prompt) => handleSendMessage(prompt)}
                  />
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Form Bar */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendMessage();
                }}
                className="p-3 bg-white dark:bg-obsidian-900 border-t border-ivory-300 dark:border-obsidian-800 flex items-center space-x-2"
              >
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder={getLanguageOption(language).placeholder}
                  disabled={isStreaming}
                  className="flex-1 px-4 py-2.5 rounded-full bg-ivory-100 dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-xs sm:text-sm text-obsidian-900 dark:text-ivory-100 focus:outline-none focus:ring-2 focus:ring-terracotta disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={!inputMessage.trim() || isStreaming}
                  className="p-2.5 rounded-full bg-terracotta hover:bg-terracotta-600 text-white disabled:opacity-40 disabled:hover:bg-terracotta transition-colors shadow-sm"
                  aria-label="Send message"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </>
          )}
        </div>
      )}
    </>
  );
}
