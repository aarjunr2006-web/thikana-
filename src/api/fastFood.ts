import { request } from "./client";
import type { FastFoodSpot, FastFoodFilters } from "../types";

export async function fetchFastFoodSpots(filters: FastFoodFilters): Promise<FastFoodSpot[]> {
  const params = new URLSearchParams();
  if (filters.area && filters.area !== "all") {
    params.append("area", filters.area);
  }
  if (filters.max_cost_for_two) {
    params.append("max_cost_for_two", filters.max_cost_for_two.toString());
  }
  params.append("limit", "100");
  
  const queryStr = params.toString() ? `?${params.toString()}` : "";
  return request<FastFoodSpot[]>(`/api/v1/fast-food-spots/${queryStr}`);
}
