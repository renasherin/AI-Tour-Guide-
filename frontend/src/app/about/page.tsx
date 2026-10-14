"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Database,
  Cpu,
  Layers,
  Sparkles,
  ShieldCheck,
  ExternalLink,
  BookOpen,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Compass,
} from "lucide-react";

const PIPELINE_STAGES = [
  {
    step: "01",
    title: "Query Normalization & Intent Routing",
    subtitle: "Input Preprocessing & Entity Disambiguation",
    description:
      "Traveler queries are cleaned, normalized, and classified into conversational intents (Destinations, Heritage, Regional Cuisine, or General Travel). Multi-turn context is seamlessly resolved with historical conversation memory.",
    icon: Compass,
    color: "from-terracotta/20 to-terracotta/5",
    accent: "text-terracotta",
    details: [
      "Regex sanitization of punctuation artifacts",
      "Coreference resolution across multi-turn chats",
      "Off-topic and hallucination trap guards",
    ],
  },
  {
    step: "02",
    title: "Multilingual Dense Embedding",
    subtitle: "High-Dimensional Vector Representation",
    description:
      "The query is converted into a 384-dimensional dense semantic vector using multilingual sentence transformers, capturing nuanced connotations in both English and Hindi.",
    icon: Cpu,
    color: "from-saffron/20 to-saffron/5",
    accent: "text-saffron",
    details: [
      "Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
      "Sub-word tokenization optimized for Indic toponyms",
      "384-dimension vector normalized for cosine similarity",
    ],
  },
  {
    step: "03",
    title: "ChromaDB Semantic Retrieval",
    subtitle: "Persistent Vector Indexing & Top-K Scoring",
    description:
      "ChromaDB queries over 700 verified chunks representing India's 28 states and 8 union territories. Metadata filters (State, Union Territory, UNESCO status) ensure high precision and geographic accuracy.",
    icon: Database,
    color: "from-gold/20 to-gold/5",
    accent: "text-gold",
    details: [
      "Persistent HNSW cosine distance collection",
      "Metadata filtering by state, category, and UNESCO status",
      "700+ indexed passages with similarity threshold enforcement",
    ],
  },
  {
    step: "04",
    title: "Context Grounding & Citation Injection",
    subtitle: "Strict Evidence Synthesis & Provenance",
    description:
      "Only retrieved chunks exceeding similarity thresholds are injected into the synthesis context. Each claim is coupled with its canonical Wikipedia / Wikivoyage URL, region tag, and CC-BY-SA 4.0 license identifier.",
    icon: Layers,
    color: "from-viridian/20 to-viridian/5",
    accent: "text-viridian",
    details: [
      "Zero-injection tolerance: system persona overrides blocked",
      "Explicit bracket citations: [Source: Hampi, Karnataka]",
      "Automatic excerpt generation for UI source cards",
    ],
  },
  {
    step: "05",
    title: "SSE Token Streaming & Proactive Suggestions",
    subtitle: "Low-Latency Real-Time Travel Guidance",
    description:
      "The response is streamed via Server-Sent Events (SSE) word by word, alongside structured events delivering authoritative source citations and context-aware follow-up suggestions.",
    icon: Sparkles,
    color: "from-terracotta/20 to-terracotta/5",
    accent: "text-terracotta",
    details: [
      "Server-Sent Events streaming with ~35ms latency",
      "Emits structured 'sources' and 'suggestions' JSON payloads",
      "Graceful offline grounded fallback if API key is unconfigured",
    ],
  },
];

export default function AboutPage() {
  const [activeStage, setActiveStage] = useState(0);

  return (
    <div className="pt-24 pb-24 min-h-screen bg-ivory-100 dark:bg-obsidian-900 transition-colors">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-20">
        {/* Header Hero */}
        <div className="text-center max-w-3xl mx-auto space-y-4">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-terracotta/10 text-terracotta text-xs font-bold uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4" />
            <span>Architecture, Provenance & Transparency</span>
          </div>
          <h1 className="font-serif text-3xl sm:text-5xl font-bold text-obsidian-900 dark:text-ivory-100 tracking-tight">
            How Incredible Journeys Works
          </h1>
          <p className="text-sm sm:text-base text-obsidian-600 dark:text-ivory-300 font-light leading-relaxed">
            A look under the hood of our verified Retrieval-Augmented Generation (RAG) pipeline,
            zero-hallucination policies, and open-data provenance across India's 36 administrative territories.
          </p>
        </div>

        {/* 1. INTERACTIVE VISUAL RAG PIPELINE DIAGRAM */}
        <div id="rag-architecture" className="space-y-8 scroll-mt-24">
          <div className="text-center sm:text-left">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Interactive Architecture Blueprint
            </span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
              The 5-Stage RAG Pipeline
            </h2>
            <p className="text-xs text-obsidian-500 dark:text-ivory-400 mt-1">
              Click any stage in the flow to inspect its architectural specifications.
            </p>
          </div>

          {/* Stepper Tabs Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            {PIPELINE_STAGES.map((stg, i) => {
              const Icon = stg.icon;
              const isActive = activeStage === i;
              return (
                <button
                  key={stg.step}
                  onClick={() => setActiveStage(i)}
                  className={`p-4 rounded-2xl text-left transition-all border ${
                    isActive
                      ? "bg-white dark:bg-obsidian-800 border-terracotta shadow-editorial-lg scale-[1.02]"
                      : "bg-ivory-200/70 dark:bg-obsidian-850 border-ivory-300 dark:border-obsidian-750 hover:border-terracotta/40"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-mono text-xs font-bold text-obsidian-400 dark:text-ivory-400">
                      {stg.step}
                    </span>
                    <Icon className={`w-4 h-4 ${stg.accent}`} />
                  </div>
                  <h3 className="font-serif text-xs font-bold text-obsidian-900 dark:text-ivory-100 line-clamp-2">
                    {stg.title}
                  </h3>
                </button>
              );
            })}
          </div>

          {/* Active Stage Detailed Card */}
          <div className="rounded-3xl p-8 sm:p-10 bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 shadow-editorial">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-7 space-y-4">
                <div className="inline-flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-terracotta">
                  <span>Stage {PIPELINE_STAGES[activeStage].step}</span>
                  <span>•</span>
                  <span>{PIPELINE_STAGES[activeStage].subtitle}</span>
                </div>
                <h3 className="font-serif text-2xl sm:text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
                  {PIPELINE_STAGES[activeStage].title}
                </h3>
                <p className="text-sm text-obsidian-700 dark:text-ivory-200 leading-relaxed font-light">
                  {PIPELINE_STAGES[activeStage].description}
                </p>

                <div className="pt-4 space-y-2 border-t border-ivory-200 dark:border-obsidian-700">
                  <span className="text-xs font-bold text-obsidian-500 dark:text-ivory-400 uppercase tracking-wider block mb-2">
                    Key Engineering Specifications:
                  </span>
                  {PIPELINE_STAGES[activeStage].details.map((detail, idx) => (
                    <div key={idx} className="flex items-center space-x-2 text-xs text-obsidian-800 dark:text-ivory-200">
                      <CheckCircle2 className="w-4 h-4 text-viridian flex-shrink-0" />
                      <span>{detail}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Graphical Blueprint Visualizer */}
              <div className="lg:col-span-5 rounded-2xl bg-ivory-100 dark:bg-obsidian-900 p-6 border border-ivory-200 dark:border-obsidian-750 font-mono text-xs space-y-3">
                <div className="flex items-center justify-between text-obsidian-500 pb-2 border-b border-ivory-200 dark:border-obsidian-800">
                  <span>PIPELINE TELEMETRY</span>
                  <span className="text-viridian font-bold">STATUS: OK</span>
                </div>
                <div className="text-obsidian-700 dark:text-ivory-300 space-y-1.5 text-[11px]">
                  <div>&gt; COLLECTION: india_places</div>
                  <div>&gt; VECTOR_COUNT: 700 vectors</div>
                  <div>&gt; SIMILARITY_METRIC: Cosine (HNSW)</div>
                  <div>&gt; THRESHOLD: 0.35 Cosine Similarity</div>
                  <div>&gt; COVERAGE: 28 States & 8 UTs</div>
                  <div>&gt; MULTILINGUAL: EN + HI Tokenized</div>
                  <div>&gt; STREAMING_CADENCE: ~20ms / token</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 2. ZERO-HALLUCINATION POLICY STATEMENT */}
        <div id="transparency" className="rounded-3xl p-8 sm:p-10 bg-ivory-200/60 dark:bg-obsidian-850 border border-ivory-300 dark:border-obsidian-750 space-y-6 scroll-mt-24">
          <div className="flex items-center space-x-3 text-terracotta">
            <ShieldCheck className="w-8 h-8" />
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
              Zero-Hallucination Engineering Standard
            </h2>
          </div>

          <p className="text-sm text-obsidian-700 dark:text-ivory-200 leading-relaxed font-light">
            AI travel guides often suffer from catastrophic hallucination—inventing non-existent train schedules,
            fabricating entry ticket prices, or imagining heritage ruins in places where none exist. Incredible Journeys
            enforces an uncompromising anti-hallucination architecture:
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            <div className="p-5 rounded-2xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 space-y-2">
              <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100">
                1. Explicit Null Coordinates
              </h4>
              <p className="text-xs text-obsidian-600 dark:text-ivory-300 leading-relaxed">
                If decimal coordinates for a remote hill pass or tribal sanctuary are not definitively verified by official geocodes, they remain strictly <code className="bg-ivory-200 dark:bg-obsidian-900 px-1 py-0.5 rounded text-[10px]">null</code> and are never guessed.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 space-y-2">
              <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100">
                2. Price & Timing Safeguards
              </h4>
              <p className="text-xs text-obsidian-600 dark:text-ivory-300 leading-relaxed">
                The model is barred from fabricating currency ticket amounts or timetable hours. It instructs travelers to consult the Archaeological Survey of India (ASI) or official state tourism desks.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 space-y-2">
              <h4 className="font-serif text-sm font-bold text-obsidian-900 dark:text-ivory-100">
                3. Grounded Citation Traceability
              </h4>
              <p className="text-xs text-obsidian-600 dark:text-ivory-300 leading-relaxed">
                Every generated assertion is grounded in retrieved text passages with direct clickable references back to canonical Wikimedia encyclopedic entries.
              </p>
            </div>
          </div>
        </div>

        {/* 3. OPEN DATA & CC-BY-SA 4.0 LICENSING DISCLOSURE */}
        <div id="licensing" className="space-y-6 scroll-mt-24 border-t border-ivory-300 dark:border-obsidian-800 pt-12">
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
              Intellectual Property & Licensing
            </span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-obsidian-900 dark:text-ivory-100">
              Open Data Provenance Disclosures
            </h2>
            <p className="text-sm text-obsidian-600 dark:text-ivory-300 font-light">
              We proudly celebrate and credit the global open-knowledge contributors who make subcontinental travel documentation possible.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-2xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 space-y-3">
              <h4 className="font-serif text-base font-bold text-obsidian-900 dark:text-ivory-100 flex items-center justify-between">
                <span>Wikipedia & Wikivoyage (Wikimedia)</span>
                <span className="text-xs font-sans text-gold font-bold">CC BY-SA 4.0</span>
              </h4>
              <p className="text-xs text-obsidian-600 dark:text-ivory-300 leading-relaxed">
                All narrative texts, historical digests, and regional travel contexts in our starter dataset are derived from Wikipedia and Wikivoyage articles, used in accordance with the Creative Commons Attribution-ShareAlike 4.0 International license.
              </p>
              <a
                href="https://creativecommons.org/licenses/by-sa/4.0/"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-1 text-xs text-terracotta font-semibold hover:underline"
              >
                <span>Read License Deed</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>

            <div className="p-6 rounded-2xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 space-y-3">
              <h4 className="font-serif text-base font-bold text-obsidian-900 dark:text-ivory-100 flex items-center justify-between">
                <span>OpenStreetMap & Cartography</span>
                <span className="text-xs font-sans text-viridian font-bold">ODbL</span>
              </h4>
              <p className="text-xs text-obsidian-600 dark:text-ivory-300 leading-relaxed">
                Interactive geographical maps rendered on destination deep dives are provided via OpenStreetMap. Map data is licensed under the Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation (OSMF).
              </p>
              <a
                href="https://www.openstreetmap.org/copyright"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-1 text-xs text-terracotta font-semibold hover:underline"
              >
                <span>Read OSM Copyright</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        {/* CTA Banner */}
        <div className="text-center py-12 rounded-3xl bg-obsidian-950 text-white p-8 space-y-4">
          <h3 className="font-serif text-2xl sm:text-3xl font-bold">
            Ready to Discover Incredible India?
          </h3>
          <p className="text-xs sm:text-sm text-ivory-300 max-w-md mx-auto font-light">
            Start by consulting our AI Tour Guide or browse the curated atlas of all 28 states and 8 union territories.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Link
              href="/explore"
              className="px-6 py-2.5 rounded-full bg-white text-obsidian-950 font-semibold text-xs uppercase tracking-wider hover:bg-ivory-200 transition-colors"
            >
              Browse Atlas
            </Link>
            <Link
              href="/guide"
              className="px-6 py-2.5 rounded-full bg-terracotta text-white font-semibold text-xs uppercase tracking-wider hover:bg-terracotta-600 transition-colors"
            >
              Consult AI Guide
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
