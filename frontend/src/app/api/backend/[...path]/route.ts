/**
 * Server-side relay to the backend API.
 *
 * The browser only ever calls this app. This handler runs on the server, adds the shared API
 * key and forwards the request, so neither the key nor the backend address reaches the browser.
 */
import type { NextRequest } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";
const BACKEND_API_KEY = process.env.BACKEND_API_KEY ?? "";

const REQUEST_HEADERS = ["accept", "content-type", "x-request-id"];
const RESPONSE_HEADERS = ["content-type", "x-request-id"];

type Context = { params: Promise<{ path: string[] }> };

async function relay(request: NextRequest, { params }: Context) {
  const { path } = await params;
  if (path.some((segment) => segment === "." || segment === "..")) {
    return Response.json({ detail: "Alamat tidak valid" }, { status: 400 });
  }
  const target = new URL(
    `/api/v1/${path.map(encodeURIComponent).join("/")}`,
    BACKEND_URL,
  );
  target.search = request.nextUrl.search;

  const headers = new Headers();
  for (const name of REQUEST_HEADERS) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  if (BACKEND_API_KEY) headers.set("x-api-key", BACKEND_API_KEY);

  const init: RequestInit & { duplex?: "half" } = {
    method: request.method,
    headers,
    cache: "no-store",
  };
  if (request.method === "POST") {
    init.body = request.body;
    init.duplex = "half"; // required by Node to stream an upload through
  }

  let upstream: Response;
  try {
    upstream = await fetch(target, init);
  } catch {
    return Response.json(
      { detail: "Layanan penyaringan tidak dapat dihubungi." },
      { status: 502 },
    );
  }

  const forwarded = new Headers();
  for (const name of RESPONSE_HEADERS) {
    const value = upstream.headers.get(name);
    if (value) forwarded.set(name, value);
  }
  return new Response(upstream.body, {
    status: upstream.status,
    headers: forwarded,
  });
}

export { relay as GET, relay as POST };
