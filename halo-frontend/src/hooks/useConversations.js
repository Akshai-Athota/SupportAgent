import { useState, useEffect, useCallback, useRef } from "react";
import * as conversationsApi from "../api/conversations";
import { clearMessages } from "../lib/storage";

/**
 * Manages the list of conversations for the signed-in user.
 * Optimistic add/remove with server sync.
 */
export function useConversations(token, { onUnauthorized, onError } = {}) {
  const [conversations, setConversations] = useState([]);
  const tokenRef = useRef(token);
  tokenRef.current = token;

  const reload = useCallback(async () => {
    if (!tokenRef.current) return;
    try {
      const list = await conversationsApi.listConversations(tokenRef.current);
      list.sort((a, b) => new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0));
      setConversations(list);
    } catch (err) {
      if (err?.status === 401) onUnauthorized?.();
    }
  }, [onUnauthorized]);

  useEffect(() => {
    if (token) reload();
    else setConversations([]);
  }, [token, reload]);

  /** Insert (or move to top) a conversation locally. */
  const upsert = useCallback((conv) => {
    setConversations((prev) => [
      conv,
      ...prev.filter((c) => c.id !== conv.id),
    ]);
  }, []);

  const remove = useCallback(
    async (id) => {
      setConversations((prev) => prev.filter((c) => c.id !== id));
      clearMessages(id);
      try {
        await conversationsApi.deleteConversation(tokenRef.current, id);
      } catch (err) {
        if (err?.status === 401) onUnauthorized?.();
        else if (err?.status !== 404) onError?.("Could not delete the conversation on the server.");
      }
    },
    [onUnauthorized, onError]
  );

  return { conversations, reload, upsert, remove };
}
