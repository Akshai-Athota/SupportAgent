import { createContext, useContext, useState, useEffect, useCallback } from "react";
import * as authApi from "../api/auth";
import { ApiError } from "../api/client";
import { decodeJwt, isExpired } from "../lib/jwt";
import { tokenStore } from "../lib/storage";

const AuthContext = createContext(null);

function userFromToken(token) {
  const payload = decodeJwt(token);
  return { id: payload.sub || "", email: payload.email || "" };
}

const NETWORK_MESSAGE =
  "Couldn't reach the support service. Check your connection and try again.";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Restore session on first load.
  useEffect(() => {
    const stored = tokenStore.get();
    if (stored && !isExpired(decodeJwt(stored))) {
      setToken(stored);
      setUser(userFromToken(stored));
    } else if (stored) {
      tokenStore.clear();
    }
    setReady(true);
  }, []);

  const persist = useCallback((accessToken) => {
    tokenStore.set(accessToken);
    setToken(accessToken);
    setUser(userFromToken(accessToken));
    setError("");
  }, []);

  const login = useCallback(
    async (email, password) => {
      setLoading(true);
      setError("");
      try {
        const { access_token } = await authApi.login(email, password);
        persist(access_token);
        return true;
      } catch (err) {
        setError(err instanceof ApiError ? err.detail || "Invalid email or password." : NETWORK_MESSAGE);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [persist]
  );

  const signup = useCallback(
    async (payload) => {
      setLoading(true);
      setError("");
      try {
        const { access_token } = await authApi.signup(payload);
        persist(access_token);
        return true;
      } catch (err) {
        setError(err instanceof ApiError ? err.detail || "Could not create your account." : NETWORK_MESSAGE);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [persist]
  );

  const logout = useCallback(() => {
    tokenStore.clear();
    setToken(null);
    setUser(null);
    setError("");
  }, []);

  const clearError = useCallback(() => setError(""), []);

  const value = { token, user, ready, error, loading, login, signup, logout, clearError };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within <AuthProvider>");
  return ctx;
}
