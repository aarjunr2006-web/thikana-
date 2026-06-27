import type {
  DirectoryMode,
  AccommodationFilters,
  FoodServiceFilters,
  FastFoodFilters,
  SortOption,
  TargetAudience,
  FoodServiceType,
  BudgetType,
} from "../types";

interface FilterBarProps {
  mode: DirectoryMode;
  allAreas: string[];
  stayFilters: AccommodationFilters;
  onStayFiltersChange: (filters: AccommodationFilters) => void;
  eatFilters: FoodServiceFilters;
  onEatFiltersChange: (filters: FoodServiceFilters) => void;
  fastFoodFilters: FastFoodFilters;
  onFastFoodFiltersChange: (filters: FastFoodFilters) => void;
  sort: SortOption;
  onSortChange: (sort: SortOption) => void;
}

export function FilterBar({
  mode,
  allAreas,
  stayFilters,
  onStayFiltersChange,
  eatFilters,
  onEatFiltersChange,
  fastFoodFilters,
  onFastFoodFiltersChange,
  sort,
  onSortChange,
}: FilterBarProps) {
  // Chip configuration for other modes
  const stayChips: { value: TargetAudience | "all"; label: string; color: string }[] = [
    { value: "all", label: "All", color: "" },
    { value: "Boys", label: "Boys", color: "var(--indigo-600)" },
    { value: "Girls", label: "Girls", color: "var(--rose)" },
    { value: "Co-ed", label: "Co-ed", color: "var(--olive)" },
  ];

  const eatChips: { value: FoodServiceType | "all"; label: string; color: string }[] = [
    { value: "all", label: "All", color: "" },
    { value: "Tiffin", label: "Tiffin", color: "var(--indigo-600)" },
    { value: "Dhaba", label: "Dhaba", color: "var(--rose)" },
    { value: "Bhojnalaya", label: "Bhojnalaya", color: "var(--olive)" },
  ];

  const handleChipClick = (value: string) => {
    if (mode === "stay") {
      onStayFiltersChange({
        ...stayFilters,
        target_audience: value as TargetAudience | "all",
      });
    } else {
      onEatFiltersChange({
        ...eatFilters,
        type: value as FoodServiceType | "all",
      });
    }
  };

  const currentChipValue = mode === "stay" ? stayFilters.target_audience : eatFilters.type;
  const chips = mode === "stay" ? stayChips : eatChips;

  return (
    <section className="filters">
      <div className="filters-inner">
        {/* Chip Row - hidden for fast food */}
        {mode !== "fast_food" ? (
          <div className="chip-row" id="chipRow">
            {chips.map((chip) => {
              const isActive = currentChipValue === chip.value;
              return (
                <button
                  key={chip.value}
                  className={`chip ${isActive ? "active" : ""}`}
                  onClick={() => handleChipClick(chip.value)}
                  aria-pressed={isActive}
                >
                  {chip.value !== "all" && (
                    <span
                      className="dot"
                      style={{ backgroundColor: chip.color }}
                    ></span>
                  )}
                  {chip.label}
                </button>
              );
            })}
          </div>
        ) : (
          <div className="chip-row text-xs font-mono tracking-widest text-[rgba(247,239,224,0.55)] uppercase">
            🍔 Fast Food & Snacks
          </div>
        )}

        {/* Dropdowns */}
        <div className="select-row">
          {/* Area select */}
          <select
            id="areaSelect"
            aria-label="Filter by area"
            value={
              mode === "stay"
                ? stayFilters.area
                : mode === "eat"
                ? eatFilters.area
                : fastFoodFilters.area
            }
            onChange={(e) => {
              const area = e.target.value;
              if (mode === "stay") {
                onStayFiltersChange({ ...stayFilters, area });
              } else if (mode === "eat") {
                onEatFiltersChange({ ...eatFilters, area });
              } else {
                onFastFoodFiltersChange({ ...fastFoodFilters, area });
              }
            }}
          >
            <option value="all">All areas</option>
            {allAreas.map((area) => (
              <option key={area} value={area}>
                {area}
              </option>
            ))}
          </select>

          {/* Secondary select (distance/budget/cost) */}
          {mode === "stay" ? (
            <select
              id="secondarySelect"
              aria-label="Filter by distance"
              value={stayFilters.max_distance_km}
              onChange={(e) => {
                onStayFiltersChange({
                  ...stayFilters,
                  max_distance_km: parseFloat(e.target.value),
                });
              }}
            >
              <option value="2.5">Any distance</option>
              <option value="1">Under 1 km</option>
              <option value="1.5">Under 1.5 km</option>
              <option value="2">Under 2 km</option>
            </select>
          ) : mode === "eat" ? (
            <select
              id="secondarySelect"
              aria-label="Filter by budget"
              value={eatFilters.budget_type}
              onChange={(e) => {
                onEatFiltersChange({
                  ...eatFilters,
                  budget_type: e.target.value as BudgetType | "all",
                });
              }}
            >
              <option value="all">Any budget</option>
              <option value="Budget">Budget</option>
              <option value="Mid-range">Mid-range</option>
            </select>
          ) : (
            <select
              id="secondarySelect"
              aria-label="Filter by cost"
              value={fastFoodFilters.max_cost_for_two}
              onChange={(e) => {
                onFastFoodFiltersChange({
                  ...fastFoodFilters,
                  max_cost_for_two: parseInt(e.target.value),
                });
              }}
            >
              <option value="400">Any budget</option>
              <option value="200">Under ₹200 for two</option>
              <option value="300">Under ₹300 for two</option>
            </select>
          )}

          {/* Sort Select */}
          <select
            id="sortSelect"
            aria-label="Sort results"
            value={sort}
            onChange={(e) => onSortChange(e.target.value as SortOption)}
          >
            {mode === "stay" ? (
              <>
                <option value="distance">Closest first</option>
                <option value="name">Name (A–Z)</option>
              </>
            ) : mode === "eat" ? (
              <>
                <option value="name">Name (A–Z)</option>
                <option value="area">Area (A–Z)</option>
              </>
            ) : (
              <>
                <option value="name">Name (A–Z)</option>
                <option value="cost">Cheapest first</option>
              </>
            )}
          </select>
        </div>
      </div>
    </section>
  );
}
