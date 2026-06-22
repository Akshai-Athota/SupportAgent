/**
 * Decode a JWT payload (no verification — display only).
 * The backend signs tokens with { sub, email, exp }.
 */
export function decodeJwt(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(escape(window.atob(base64)));
    return JSON.parse(json);
  } catch {
    return {};
  }
}

/** Returns true if the token's `exp` claim is in the past. */
export function isExpired(payload) {
  return !!(payload && payload.exp && payload.exp * 1000 < Date.now());
}
