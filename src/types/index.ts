export type TargetAudience = "Boys" | "Girls" | "Co-ed";
export type FoodServiceType = "Tiffin" | "Dhaba" | "Bhojnalaya";
export type BudgetType = "Budget" | "Mid-range";

export interface Accommodation {
  id: string;
  name: string;
  area: string;
  address: string;
  contact_number: string;
  target_audience: TargetAudience;
  features: string[];
  distance_from_college_km: number;
  latitude?: number;
  longitude?: number;
}

export interface FoodService {
  id: string;
  name: string;
  type: FoodServiceType;
  area: string;
  address: string;
  contact_number: string;
  timings: string;
  budget_type: BudgetType;
  usp: string;
}

export interface FastFoodSpot {
  id: string;
  name: string;
  area: string;
  address: string;
  contact_number: string;
  specialties: string[];
  average_cost_for_two: number;
  top_items: Record<string, number>;
}

export type DirectoryMode = "stay" | "eat" | "fast_food";

export interface AccommodationFilters {
  target_audience: TargetAudience | "all";
  max_distance_km: number;
  area: string;
}

export interface FoodServiceFilters {
  type: FoodServiceType | "all";
  budget_type: BudgetType | "all";
  area: string;
}

export interface FastFoodFilters {
  area: string;
  max_cost_for_two: number;
}

export type StaySortOption = "distance" | "name";
export type EatSortOption = "name" | "area";
export type FastFoodSortOption = "name" | "cost";
export type SortOption = StaySortOption | EatSortOption | FastFoodSortOption;
