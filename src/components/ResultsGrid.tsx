import type { DirectoryMode, Accommodation, FoodService, FastFoodSpot } from "../types";
import { AccommodationCard } from "./AccommodationCard";
import { FoodServiceCard } from "./FoodServiceCard";
import { FastFoodCard } from "./FastFoodCard";

interface ResultsGridProps {
  mode: DirectoryMode;
  listings: any[];
  totalCount: number;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  onCardClick: (item: any) => void;
}

export function ResultsGrid({
  mode,
  listings,
  totalCount,
  loading,
  error,
  onRetry,
  onCardClick,
}: ResultsGridProps) {
  const noun =
    mode === "stay" ? "hostels & PGs" : mode === "eat" ? "food spots" : "fast food joints";

  if (error) {
    return (
      <section className="results">
        <div className="results-inner text-center py-16">
          <div className="inline-block p-6 rounded-xl border border-red-500/20 bg-red-950/20 max-w-md mx-auto">
            <span className="text-3xl" role="img" aria-label="Error Warning">⚠️</span>
            <h3 className="font-display text-lg text-[#FFD166] mt-4 mb-2">Connection Registry Offline</h3>
            <p className="text-sm text-[#F7EFE0]/80 mb-6 font-body leading-relaxed">{error}</p>
            <button
              onClick={onRetry}
              className="px-6 py-2.5 rounded-lg font-bold font-display text-sm bg-[#E8932B] text-[#0E2138] hover:bg-[#FFD166] active:scale-95 transition-all outline-none focus-visible:ring-2 focus-visible:ring-[#FFD166]"
            >
              Retry Connection
            </button>
          </div>
        </div>
      </section>
    );
  }

  if (loading) {
    return (
      <section className="results">
        <div className="results-inner">
          <p className="results-count font-mono opacity-50">Syncing registry directories...</p>
          <div className="grid">
            {Array.from({ length: 6 }).map((_, idx) => (
              <div
                key={idx}
                className="card animate-pulse h-48 opacity-60 pointer-events-none bg-[#EFE0C0]/90 border border-transparent"
                style={{
                  animationDuration: "1.5s",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                }}
              >
                <div className="h-4 bg-[#1B3349]/20 rounded w-1/3"></div>
                <div className="h-6 bg-[#1B3349]/20 rounded w-3/4 my-2"></div>
                <div className="h-4 bg-[#1B3349]/20 rounded w-1/2"></div>
                <div className="h-8 bg-[#1B3349]/10 rounded w-full mt-4"></div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="results">
      <div className="results-inner">
        <p className="results-count">
          {listings.length} of {totalCount} {noun}
        </p>

        {listings.length === 0 ? (
          <p className="mono" style={{ color: "rgba(247, 239, 224, 0.6)", fontSize: "0.85rem" }}>
            No matches. Try widening a filter.
          </p>
        ) : (
          <div className="grid">
            {listings.map((item, index) => {
              if (mode === "stay") {
                return (
                  <AccommodationCard
                    key={item.id}
                    item={item as Accommodation}
                    index={index}
                    onClick={() => onCardClick(item)}
                  />
                );
              } else if (mode === "eat") {
                return (
                  <FoodServiceCard
                    key={item.id}
                    item={item as FoodService}
                    onClick={() => onCardClick(item)}
                  />
                );
              } else {
                return (
                  <FastFoodCard
                    key={item.id}
                    item={item as FastFoodSpot}
                    onClick={() => onCardClick(item)}
                  />
                );
              }
            })}
          </div>
        )}
      </div>
    </section>
  );
}
