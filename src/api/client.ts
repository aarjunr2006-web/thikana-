const getApiBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl && envUrl !== "http://localhost:8000") {
    return envUrl;
  }
  if (typeof window !== "undefined") {
    const { protocol, hostname } = window.location;
    // If accessed via network IP address (e.g., 192.168.x.x), dynamically use that IP for backend
    if (hostname !== "localhost" && hostname !== "127.0.0.1" && !hostname.endsWith("vercel.app")) {
      return `${protocol}//${hostname}:8000`;
    }
  }
  return "http://localhost:8000";
};

const BASE_URL = getApiBaseUrl();

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
