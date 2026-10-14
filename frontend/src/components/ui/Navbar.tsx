"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Sparkles, Moon, Sun, Menu, X, Landmark, Info } from "lucide-react";

export function Navbar() {
  const pathname = usePathname();
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);

    // Initial dark mode check
    if (
      localStorage.theme === "dark" ||
      (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      document.documentElement.classList.add("dark");
      setDarkMode(true);
    } else {
      document.documentElement.classList.remove("dark");
      setDarkMode(false);
    }

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const toggleDarkMode = () => {
    if (darkMode) {
      document.documentElement.classList.remove("dark");
      localStorage.theme = "light";
      setDarkMode(false);
    } else {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
      setDarkMode(true);
    }
  };

  const navLinks = [
    { href: "/explore", label: "Atlas & Destinations", icon: Compass },
    { href: "/guide", label: "AI Tour Guide", icon: Sparkles },
    { href: "/about", label: "Transparency & RAG", icon: Info },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        isScrolled
          ? "bg-ivory-100/90 dark:bg-obsidian-900/90 backdrop-blur-md border-b border-ivory-300/60 dark:border-obsidian-700/60 shadow-sm py-3.5"
          : "bg-transparent py-5"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo & Identity */}
          <Link href="/" className="group flex items-center space-x-3 text-left">
            <div className="w-10 h-10 rounded-full bg-terracotta text-ivory-50 flex items-center justify-center font-serif text-lg font-bold shadow-md group-hover:scale-105 transition-transform duration-200">
              <Landmark className="w-5 h-5 text-ivory-100" />
            </div>
            <div>
              <span className="font-serif text-xl sm:text-2xl font-bold tracking-tight text-obsidian-900 dark:text-ivory-100 group-hover:text-terracotta transition-colors">
                Incredible Journeys
              </span>
              <p className="text-[10px] tracking-widest uppercase font-medium text-terracotta dark:text-saffron">
                Discover India with AI
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`text-sm font-medium tracking-wide transition-colors flex items-center space-x-1.5 ${
                    isActive
                      ? "text-terracotta dark:text-saffron font-semibold"
                      : "text-obsidian-700 dark:text-ivory-300 hover:text-terracotta dark:hover:text-saffron"
                  }`}
                >
                  <Icon className="w-4 h-4 opacity-75" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Action CTAs */}
          <div className="hidden md:flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-full text-obsidian-700 dark:text-ivory-300 hover:bg-ivory-300/50 dark:hover:bg-obsidian-800 transition-colors"
              aria-label="Toggle visual theme"
            >
              {darkMode ? <Sun className="w-4 h-4 text-saffron" /> : <Moon className="w-4 h-4" />}
            </button>

            <Link
              href="/guide"
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-terracotta hover:bg-terracotta-600 text-white text-xs font-semibold tracking-wider uppercase transition-all shadow-md hover:shadow-lg active:scale-95"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Ask AI Guide</span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center space-x-2">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-full text-obsidian-700 dark:text-ivory-300"
              aria-label="Toggle visual theme"
            >
              {darkMode ? <Sun className="w-4 h-4 text-saffron" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-obsidian-800 dark:text-ivory-100 hover:bg-ivory-300/40 dark:hover:bg-obsidian-800"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-ivory-100 dark:bg-obsidian-900 border-b border-ivory-300 dark:border-obsidian-800 px-4 pt-3 pb-6 space-y-3">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                  isActive
                    ? "bg-terracotta/10 text-terracotta dark:text-saffron"
                    : "text-obsidian-800 dark:text-ivory-200 hover:bg-ivory-200 dark:hover:bg-obsidian-800"
                }`}
              >
                <Icon className="w-4 h-4 text-terracotta dark:text-saffron" />
                <span>{link.label}</span>
              </Link>
            );
          })}
          <div className="pt-2">
            <Link
              href="/guide"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center space-x-2 px-4 py-2.5 rounded-full bg-terracotta text-white text-xs font-semibold uppercase tracking-wider shadow-md"
            >
              <Sparkles className="w-4 h-4" />
              <span>Launch AI Tour Guide</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
