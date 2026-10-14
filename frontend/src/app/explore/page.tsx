"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Search,
  Filter,
  Award,
  ChevronLeft,
  ChevronRight,
  Compass,
  X,
  RefreshCw,
} from "lucide-react";
import { DestinationCard } from "@/components/ui/DestinationCard";
import { FoodCard } from "@/components/ui/FoodCard";
import { Destination, RegionDivision, FoodItem } from "@/lib/types";
import { fetchDestinations, fetchRegions, fetchFoods } from "@/lib/api";

const CATEGORIES = [
  "All",
  "Heritage",
  "Fort",
  "Temple",
  "Nature",
  "Wildlife",
  "Hill Station",
  "Beach",
  "Food",
  "Festival",
];

function ExploreContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Read URL query parameters
  const paramSearch = searchParams.get("search") || "";
  const paramState = searchParams.get("state") || "All";
  const paramCategory = searchParams.get("category") || "All";
  const paramUnesco = searchParams.get("unesco") === "true";
  const paramPage = parseInt(searchParams.get("page") || "1", 10);

  const [searchTerm, setSearchTerm] = useState(paramSearch);
  const [selectedState, setSelectedState] = useState(paramState);
  const [selectedCategory, setSelectedCategory] = useState(paramCategory);
  const [unescoOnly, setUnescoOnly] = useState(paramUnesco);
  const [currentPage, setCurrentPage] = useState(paramPage);

  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [foods, setFoods] = useState<FoodItem[]>([]);
  const [regions, setRegions] = useState<RegionDivision[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  // Sync state with URL params
  useEffect(() => {
    setSearchTerm(paramSearch);
    setSelectedState(paramState);
    setSelectedCategory(paramCategory);
    setUnescoOnly(paramUnesco);
    setCurrentPage(paramPage);
  }, [paramSearch, paramState, paramCategory, paramUnesco, paramPage]);

  // Load regions once
  useEffect(() => {
    fetchRegions().then((res) => {
      setRegions(res.divisions);
    });
  }, []);

  // Fetch destinations or foods when parameters change
  useEffect(() => {
    let isCancelled = false;
    setLoading(true);

    if (paramCategory.toLowerCase() === "food") {
      fetchFoods({
        search: paramSearch,
        state: paramState,
      })
        .then((res) => {
          if (!isCancelled) {
            setFoods(res.foods);
            setDestinations([]);
            setTotal(res.total);
            setTotalPages(1);
          }
        })
        .finally(() => {
          if (!isCancelled) setLoading(false);
        });
    } else {
      setFoods([]);
      fetchDestinations({
        search: paramSearch,
        state: paramState,
        category: paramCategory,
        unesco: paramUnesco ? true : undefined,
        page: paramPage,
        limit: 16,
      })
        .then((res) => {
          if (!isCancelled) {
            setDestinations(res.destinations);
            setTotal(res.total);
            setTotalPages(res.total_pages || 1);
          }
        })
        .finally(() => {
          if (!isCancelled) setLoading(false);
        });
    }

    return () => {
      isCancelled = true;
    };
  }, [paramSearch, paramState, paramCategory, paramUnesco, paramPage]);

  // Update URL parameters
  const updateQueryParams = (updates: {
    search?: string;
    state?: string;
    category?: string;
    unesco?: boolean;
    page?: number;
  }) => {
    const q = new URLSearchParams();

    const newSearch = updates.search !== undefined ? updates.search : searchTerm;
    const newState = updates.state !== undefined ? updates.state : selectedState;
    const newCategory = updates.category !== undefined ? updates.category : selectedCategory;
    const newUnesco = updates.unesco !== undefined ? updates.unesco : unescoOnly;
    const newPage = updates.page !== undefined ? updates.page : 1; // reset page on filter change unless specified

    if (newSearch) q.set("search", newSearch);
    if (newState && newState !== "All") q.set("state", newState);
    if (newCategory && newCategory !== "All") q.set("category", newCategory);
    if (newUnesco) q.set("unesco", "true");
    if (newPage > 1) q.set("page", newPage.toString());

    router.push(`/explore?${q.toString()}`);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateQueryParams({ search: searchTerm, page: 1 });
  };

  const handleResetFilters = () => {
    setSearchTerm("");
    setSelectedState("All");
    setSelectedCategory("All");
    setUnescoOnly(false);
    setCurrentPage(1);
    router.push("/explore");
  };

  return (
    <div className="pt-24 pb-20 min-h-screen max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header Banner */}
      <div className="mb-10 text-center sm:text-left border-b border-ivory-300 dark:border-obsidian-800 pb-8">
        <span className="text-xs font-bold uppercase tracking-widest text-terracotta dark:text-saffron">
          Curated Subcontinental Atlas
        </span>
        <h1 className="font-serif text-3xl sm:text-5xl font-bold text-obsidian-900 dark:text-ivory-100 mt-1">
          Explore Destinations of India
        </h1>
        <p className="text-sm text-obsidian-600 dark:text-ivory-300 max-w-2xl mt-2 font-light">
          Search, filter, and discover over 600 verified destinations, temples, hill stations, and culinary traditions across all 36 administrative territories.
        </p>
      </div>

      {/* Filter Control Bar */}
      <div className="bg-white dark:bg-obsidian-800 rounded-2xl p-5 border border-ivory-300 dark:border-obsidian-700 shadow-editorial mb-10 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3.5 items-center">
          {/* Keyword Search */}
          <form onSubmit={handleSearchSubmit} className="md:col-span-5 relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search destination, city, or keywords..."
              className="w-full px-4 py-2.5 pl-10 rounded-xl bg-ivory-100 dark:bg-obsidian-900 border border-ivory-300 dark:border-obsidian-700 text-xs sm:text-sm text-obsidian-900 dark:text-ivory-100 focus:outline-none focus:ring-1 focus:ring-terracotta"
            />
            <Search className="w-4 h-4 text-obsidian-400 absolute left-3.5 top-3" />
            {searchTerm && (
              <button
                type="button"
                onClick={() => {
                  setSearchTerm("");
                  updateQueryParams({ search: "", page: 1 });
                }}
                className="absolute right-3 top-3 text-obsidian-400 hover:text-obsidian-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </form>

          {/* State/UT Dropdown */}
          <div className="md:col-span-4">
            <select
              value={selectedState}
              onChange={(e) => {
                setSelectedState(e.target.value);
                updateQueryParams({ state: e.target.value, page: 1 });
              }}
              className="w-full px-3 py-2.5 rounded-xl bg-ivory-100 dark:bg-obsidian-900 border border-ivory-300 dark:border-obsidian-700 text-xs sm:text-sm text-obsidian-900 dark:text-ivory-100 focus:outline-none focus:ring-1 focus:ring-terracotta"
            >
              <option value="All">All 28 States & 8 Union Territories</option>
              {regions.map((reg) => (
                <option key={reg.name} value={reg.name}>
                  {reg.name} ({reg.count} sights)
                </option>
              ))}
            </select>
          </div>

          {/* UNESCO Toggle */}
          <div className="md:col-span-3 flex items-center justify-between sm:justify-end space-x-2">
            <button
              onClick={() => {
                const nextVal = !unescoOnly;
                setUnescoOnly(nextVal);
                updateQueryParams({ unesco: nextVal, page: 1 });
              }}
              className={`flex-1 sm:flex-initial inline-flex items-center justify-center space-x-1.5 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all border ${
                unescoOnly
                  ? "bg-gold text-obsidian-950 border-gold shadow-sm"
                  : "bg-ivory-100 dark:bg-obsidian-900 text-obsidian-700 dark:text-ivory-300 border-ivory-300 dark:border-obsidian-700 hover:border-gold"
              }`}
            >
              <Award className="w-3.5 h-3.5" />
              <span>UNESCO Only</span>
            </button>

            {(searchTerm || selectedState !== "All" || selectedCategory !== "All" || unescoOnly) && (
              <button
                onClick={handleResetFilters}
                className="p-2.5 rounded-xl bg-ivory-200 dark:bg-obsidian-700 text-obsidian-600 dark:text-ivory-300 hover:bg-terracotta hover:text-white transition-colors"
                title="Reset all filters"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Category Filter Chips */}
        <div className="pt-2 border-t border-ivory-200 dark:border-obsidian-700/60 flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-none">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-obsidian-500 dark:text-ivory-400 flex items-center space-x-1 mr-1">
            <Filter className="w-3 h-3 text-terracotta" />
            <span>Theme:</span>
          </span>
          {CATEGORIES.map((cat) => {
            const isSelected = selectedCategory.toLowerCase() === cat.toLowerCase();
            return (
              <button
                key={cat}
                onClick={() => {
                  setSelectedCategory(cat);
                  updateQueryParams({ category: cat, page: 1 });
                }}
                className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                  isSelected
                    ? "bg-terracotta text-white shadow-sm"
                    : "bg-ivory-100 dark:bg-obsidian-900 text-obsidian-700 dark:text-ivory-300 hover:bg-ivory-200 dark:hover:bg-obsidian-700"
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Results Count & Current Filter Indicators */}
      <div className="flex items-center justify-between text-xs text-obsidian-500 dark:text-ivory-400 mb-6">
        <span>
          Showing {destinations.length} of <strong>{total}</strong> verified records
        </span>
        {total > 0 && (
          <span>
            Page <strong>{currentPage}</strong> of <strong>{totalPages}</strong>
          </span>
        )}
      </div>

      {/* Destinations Grid or Skeleton / Empty State */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="rounded-2xl overflow-hidden bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 p-4 space-y-3 animate-pulse"
            >
              <div className="aspect-[16/11] bg-ivory-200 dark:bg-obsidian-700 rounded-xl" />
              <div className="h-4 bg-ivory-200 dark:bg-obsidian-700 rounded w-3/4" />
              <div className="h-3 bg-ivory-200 dark:bg-obsidian-700 rounded w-1/2" />
              <div className="h-3 bg-ivory-200 dark:bg-obsidian-700 rounded w-full" />
            </div>
          ))}
        </div>
      ) : foods.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {foods.map((food) => (
            <FoodCard key={food.id} food={food} />
          ))}
        </div>
      ) : destinations.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {destinations.map((dest) => (
            <DestinationCard key={dest.id || dest.slug} destination={dest} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-white dark:bg-obsidian-800 rounded-3xl border border-ivory-300 dark:border-obsidian-700 p-8">
          <Compass className="w-12 h-12 text-terracotta mx-auto mb-3 opacity-60" />
          <h3 className="font-serif text-xl font-bold text-obsidian-900 dark:text-ivory-100">
            No Destinations Found
          </h3>
          <p className="text-xs text-obsidian-500 dark:text-ivory-400 max-w-sm mx-auto mt-1 mb-6">
            We couldn't match any verified records for your current filters. Try relaxing your search term or exploring another state.
          </p>
          <button
            onClick={handleResetFilters}
            className="px-5 py-2.5 rounded-full bg-terracotta text-white text-xs font-semibold uppercase tracking-wider shadow-md hover:bg-terracotta-600 transition-colors"
          >
            Clear All Filters
          </button>
        </div>
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="mt-12 flex items-center justify-center space-x-3">
          <button
            disabled={currentPage <= 1}
            onClick={() => updateQueryParams({ page: currentPage - 1 })}
            className="p-2 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-700 dark:text-ivory-200 disabled:opacity-40 hover:border-terracotta transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>

          <span className="text-xs font-medium px-4 py-2 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-800 dark:text-ivory-200">
            Page {currentPage} of {totalPages}
          </span>

          <button
            disabled={currentPage >= totalPages}
            onClick={() => updateQueryParams({ page: currentPage + 1 })}
            className="p-2 rounded-xl bg-white dark:bg-obsidian-800 border border-ivory-300 dark:border-obsidian-700 text-obsidian-700 dark:text-ivory-200 disabled:opacity-40 hover:border-terracotta transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}

export default function ExplorePage() {
  return (
    <Suspense fallback={<div className="min-h-screen pt-32 text-center text-sm">Loading Indian Travel Atlas...</div>}>
      <ExploreContent />
    </Suspense>
  );
}
