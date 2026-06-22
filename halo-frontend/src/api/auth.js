import { apiFetch } from "./client";

/** POST /login -> { access_token, token_type } */
export function login(email, password) {
  return apiFetch("/login", { method: "POST", body: { email, password } });
}

/**
 * POST /signup -> { access_token, token_type }
 * @param {{first_name, last_name, email, password, phone_number?}} payload
 */
export function signup(payload) {
  return apiFetch("/signup", { method: "POST", body: payload });
}
