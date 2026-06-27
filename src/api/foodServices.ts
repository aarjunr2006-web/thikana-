import { request } from "./client";
import type { FoodService, FoodServiceFilters } from "../types";

export async function fetchFoodServices(filters: FoodServiceFilters): Promise<FoodService[]> {
  const params = new URLSearchParams();
  if (filters.type && filters.type !== "all") {
    params.append("type", filters.type);
  }
  if (filters.area && filters.area !== "all") {
    params.append("area", filters.area);
  }
  params.append("limit", "100");
  
  const queryStr = params.toString() ? `?${params.toString()}` : "";
  return request<FoodService[]>(`/api/v1/food-services/${queryStr}`);
}
