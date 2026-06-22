/**
 * Browser-side persistence.
 *
 * The backend keeps conversation memory server-side (LangGraph threads) but
 * exposes no "get messages" endpoint, so we cache rendered messages per
 * conversation locally to restore history on reload / when switching chats.
 */
const TOKEN_KEY = "halo_token";
const STREAM_KEY = "halo_streaming";
const MSG_PREFIX = "halo_msgs_";

export const tokenStore = {
  get() {
    try {
      return localStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },
  set(token) {
    try {
      localStorage.setItem(TOKEN_KEY, token);
    } catch {}
  },
  clear() {
    try {
      localStorage.removeItem(TOKEN_KEY);
    } catch {}
  },
};

export const streamingPref = {
  get(fallback = true) {
    try {
      const v = localStorage.getItem(STREAM_KEY);
      return v === null ? fallback : v === "1";
    } catch {
      return fallback;
    }
  },
  set(on) {
    try {
      localStorage.setItem(STREAM_KEY, on ? "1" : "0");
    } catch {}
  },
};

export function loadMessages(conversationId) {
  if (!conversationId) return [];
  try {
    const raw = localStorage.getItem(MSG_PREFIX + conversationId);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveMessages(conversationId, messages) {
  if (!conversationId) return;
  try {
    localStorage.setItem(MSG_PREFIX + conversationId, JSON.stringify(messages));
  } catch {}
}

export function clearMessages(conversationId) {
  try {
    localStorage.removeItem(MSG_PREFIX + conversationId);
  } catch {}
}
