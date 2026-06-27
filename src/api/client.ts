const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000";

export async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  // Automatically extract "value" array if response is wrapped
  if (data && typeof data === "object" && "value" in data && Array.isArray(data.value)) {
    return data.value as unknown as T;
  }
  return data as T;
}
