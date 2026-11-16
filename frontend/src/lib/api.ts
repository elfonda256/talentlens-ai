/** Single place where the frontend talks to the backend. */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const API_V1 = `${API_BASE_URL}/api/v1`;

export const API_DOCS_URL = `${API_BASE_URL}/docs`;

export type HealthResponse = {
  status: "ok";
  app_name: string;
  version: string;
  environment: string;
  timestamp: string;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_V1}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API responded with ${response.status} for ${path}`);
  }
  return (await response.json()) as T;
}

export function getHealth(): Promise<HealthResponse> {
  return getJson<HealthResponse>("/health");
}
