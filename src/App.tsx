import { useState } from "react";
import { NavBar } from "./components/NavBar";
import { Hero } from "./components/Hero";
import { FilterBar } from "./components/FilterBar";
import { ResultsGrid } from "./components/ResultsGrid";
import { DetailPanel } from "./components/DetailPanel";
import { Footer } from "./components/Footer";
import { useListings } from "./hooks/useListings";

export default function App() {
  const {
    mode,
    setMode,
    search,
    setSearch,
    sort,
    setSort,
    stayFilters,
    setStayFilters,
    eatFilters,
    setEatFilters,
    fastFoodFilters,
    setFastFoodFilters,
    listings,
    allAreas,
    loading,
    error,
    retryFetch,
  } = useListings();

  const [activeItem, setActiveItem] = useState<any | null>(null);

  return (
    <div className="flex flex-col min-h-screen justify-between">
      <div>
        <NavBar />
        <Hero
          mode={mode}
          onModeChange={setMode}
          search={search}
          onSearchChange={setSearch}
          stayCount={mode === "stay" ? listings.length : 6}
          eatCount={mode === "eat" ? listings.length : 5}
        />
        <FilterBar
          mode={mode}
          allAreas={allAreas}
          stayFilters={stayFilters}
          onStayFiltersChange={setStayFilters}
          eatFilters={eatFilters}
          onEatFiltersChange={setEatFilters}
          fastFoodFilters={fastFoodFilters}
          onFastFoodFiltersChange={setFastFoodFilters}
          sort={sort}
          onSortChange={setSort}
        />
        <ResultsGrid
          mode={mode}
          listings={listings}
          totalCount={listings.length}
          loading={loading}
          error={error}
          onRetry={retryFetch}
          onCardClick={setActiveItem}
        />
      </div>

      <DetailPanel
        mode={mode}
        item={activeItem}
        onClose={() => setActiveItem(null)}
      />
      <Footer />
    </div>
  );
}
