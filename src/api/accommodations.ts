import { request } from "./client";
import type { Accommodation, AccommodationFilters } from "../types";

export async function fetchAccommodations(filters: AccommodationFilters): Promise<Accommodation[]> {
  const params = new URLSearchParams();
  if (filters.target_audience && filters.target_audience !== "all") {
    params.append("target_audience", filters.target_audience);
  }
  if (filters.max_distance_km) {
    params.append("max_distance_km", filters.max_distance_km.toString());
  }
  if (filters.area && filters.area !== "all") {
    params.append("area", filters.area);
  }
  params.append("limit", "100");
  
  const queryStr = params.toString() ? `?${params.toString()}` : "";
  return request<Accommodation[]>(`/api/v1/accommodations/${queryStr}`);
}
