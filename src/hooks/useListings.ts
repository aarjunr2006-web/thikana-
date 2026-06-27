import { useState, useEffect, useMemo } from "react";
import { fetchAccommodations } from "../api/accommodations";
import { fetchFoodServices } from "../api/foodServices";
import { fetchFastFoodSpots } from "../api/fastFood";
import type {
  DirectoryMode,
  AccommodationFilters,
  FoodServiceFilters,
  FastFoodFilters,
  SortOption,
  FoodService,
} from "../types";

export function useListings() {
  const [mode, setMode] = useState<DirectoryMode>("stay");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortOption>("distance");

  const [stayFilters, setStayFilters] = useState<AccommodationFilters>({
    target_audience: "all",
    max_distance_km: 2.5,
    area: "all",
  });

  const [eatFilters, setEatFilters] = useState<FoodServiceFilters>({
    type: "all",
    budget_type: "all",
    area: "all",
  });

  const [fastFoodFilters, setFastFoodFilters] = useState<FastFoodFilters>({
    area: "all",
    max_cost_for_two: 400,
  });

  const [rawListings, setRawListings] = useState<any[]>([]);
  const [allAreas, setAllAreas] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Trigger state compile for unique areas
  useEffect(() => {
    let active = true;
    const fetchAllAreas = async () => {
      try {
        let res: any[] = [];
        if (mode === "stay") {
          res = await fetchAccommodations({ target_audience: "all", max_distance_km: 2.5, area: "all" });
        } else if (mode === "eat") {
          res = await fetchFoodServices({ type: "all", area: "all", budget_type: "all" });
        } else {
          res = await fetchFastFoodSpots({ area: "all", max_cost_for_two: 400 });
        }
        if (active) {
          const areas = Array.from(new Set(res.map((item) => item.area))).sort();
          setAllAreas(areas);
        }
      } catch (err) {
        if (active) {
          // Sensible fallbacks of seeded Jodhpur areas if API is offline
          setAllAreas([
            "Sector-A Shastri Nagar",
            "Sector-G Shastri Nagar",
            "Kalpatru Shopping Centre",
            "Pratap Nagar",
            "Kamla Nehru Nagar",
            "Sardarpura",
            "Ratanada",
            "P.W.D Colony",
            "Chopasni Housing Board",
            "Basni",
            "Jaljog Choraha",
            "Jaljog"
          ]);
        }
      }
    };
    fetchAllAreas();
    return () => {
      active = false;
    };
  }, [mode]);

  // Set default sort option based on mode
  useEffect(() => {
    if (mode === "stay") {
      setSort("distance");
    } else if (mode === "eat") {
      setSort("name");
    } else {
      setSort("name");
    }
  }, [mode]);

  // Reset filters when switching mode
  const handleSetMode = (newMode: DirectoryMode) => {
    setMode(newMode);
    setSearch("");
    setRawListings([]); // Clear raw listings immediately on mode transition to prevent render crashes
    if (newMode === "stay") {
      setStayFilters({
        target_audience: "all",
        max_distance_km: 2.5,
        area: "all",
      });
    } else if (newMode === "eat") {
      setEatFilters({
        type: "all",
        budget_type: "all",
        area: "all",
      });
    } else {
      setFastFoodFilters({
        area: "all",
        max_cost_for_two: 400,
      });
    }
  };

  // Debounced API fetching
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);

    const performFetch = async () => {
      try {
        let results: any[] = [];
        if (mode === "stay") {
          results = await fetchAccommodations(stayFilters);
        } else if (mode === "eat") {
          results = await fetchFoodServices(eatFilters);
        } else {
          results = await fetchFastFoodSpots(fastFoodFilters);
        }
        if (active) {
          setRawListings(results);
          setLoading(false);
        }
      } catch (err: any) {
        if (active) {
          setError(err.message || "Failed to connect to directory registry.");
          setLoading(false);
        }
      }
    };

    const delayDebounceFn = setTimeout(() => {
      performFetch();
    }, 300);

    return () => {
      active = false;
      clearTimeout(delayDebounceFn);
    };
  }, [
    mode,
    stayFilters,
    eatFilters.type,
    eatFilters.area,
    fastFoodFilters.area,
    fastFoodFilters.max_cost_for_two,
  ]);

  // Client-side filters (search text, budget type, and sort)
  const listings = useMemo(() => {
    let result = [...rawListings];

    // Client-side budget filter for food services (since backend API has no budget parameter)
    if (mode === "eat" && eatFilters.budget_type !== "all") {
      result = result.filter((item: FoodService) => item.budget_type === eatFilters.budget_type);
    }

    // Client-side free text query search (searches name, area, USP, features, address, and specialties)
    if (search.trim() !== "") {
      const q = search.toLowerCase();
      result = result.filter((item) => {
        const name = (item.name || "").toLowerCase();
        const area = (item.area || "").toLowerCase();
        const address = (item.address || "").toLowerCase();
        const features = item.features ? item.features.join(" ").toLowerCase() : "";
        const specialties = item.specialties ? item.specialties.join(" ").toLowerCase() : "";
        const usp = item.usp ? item.usp.toLowerCase() : "";
        
        // Search top_items dictionary keys too
        const menuItems = item.top_items
          ? Object.keys(item.top_items).join(" ").toLowerCase()
          : "";

        return (
          name.includes(q) ||
          area.includes(q) ||
          address.includes(q) ||
          features.includes(q) ||
          specialties.includes(q) ||
          menuItems.includes(q) ||
          usp.includes(q)
        );
      });
    }

    // Client-side sorting
    result.sort((a, b) => {
      if (mode === "stay") {
        if (sort === "distance") {
          return a.distance_from_college_km - b.distance_from_college_km;
        }
        return a.name.localeCompare(b.name);
      } else if (mode === "eat") {
        if (sort === "area") {
          return a.area.localeCompare(b.area);
        }
        return a.name.localeCompare(b.name);
      } else {
        // Fast Food sort option: cost or name
        if (sort === "cost") {
          return a.average_cost_for_two - b.average_cost_for_two;
        }
        return a.name.localeCompare(b.name);
      }
    });

    return result;
  }, [rawListings, mode, search, sort, eatFilters.budget_type]);

  const retryFetch = () => {
    // Re-trigger fetch by updating state object references
    setStayFilters((prev) => ({ ...prev }));
    setEatFilters((prev) => ({ ...prev }));
    setFastFoodFilters((prev) => ({ ...prev }));
  };

  return {
    mode,
    setMode: handleSetMode,
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
  };
}
