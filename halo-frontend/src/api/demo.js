import { apiFetch } from "./client";

/**
 * POST /demo/seed-orders?count=N
 * Seeds up to `count` (1–5) sample orders for the signed-in customer so a
 * brand-new account has something for Aria to look up.
 * -> { created, orders: [{ order_id, status, total }] }
 * Throws ApiError(409) once the customer already has the max sample orders.
 */
export function seedOrders(token, count = 4) {
  const safe = Math.max(1, Math.min(count, 5));
  return apiFetch("/demo/seed-orders?count=" + safe, { method: "POST", token });
}
