/**
 * Low-level HTTP client for the support-agent API.
 * Base URL comes from VITE_API_BASE_URL (see .env.example).
 */
export const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  "https://support-agent-680190152293.europe-west3.run.app"
).replace(/\/+$/, "");

/** Error carrying the HTTP status + parsed `detail` from FastAPI. */
export class ApiError extends Error {
  constructor(status, detail) {
    super(detail || `Request failed (${status})`);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/** Extract a human-readable message from a FastAPI error body. */
async function parseDetail(res) {
  try {
    const data = await res.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail) && data.detail[0]?.msg) return data.detail[0].msg;
  } catch {}
  return undefined;
}

/**
 * JSON request helper.
 * @param {string} path - e.g. "/login"
 * @param {{method?:string, body?:any, token?:string}} options
 */
export async function apiFetch(path, { method = "GET", body, token } = {}) {
  const headers = authHeaders(token);
  if (body !== undefined) headers["Content-Type"] = "application/json";

  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) throw new ApiError(res.status, await parseDetail(res));
  if (res.status === 204) return null;

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}
