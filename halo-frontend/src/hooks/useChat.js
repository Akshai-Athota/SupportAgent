import { useState, useRef, useCallback } from "react";
import { sendChat, streamChat } from "../api/chat";
import { createConversation } from "../api/conversations";
import { loadMessages, saveMessages } from "../lib/storage";
import { mapTools } from "../lib/tools";

const ERROR_TEXT =
  "Sorry — I couldn't reach the support service just now. Please try again in a moment.";
const RATE_TEXT =
  "You're sending messages a little fast — please wait a moment and try again.";

/**
 * Owns the message list for the active conversation plus send/stream logic.
 *
 * @param {object} deps
 * @param {string} deps.token
 * @param {string|null} deps.activeId
 * @param {(id:string)=>void} deps.setActiveId
 * @param {(conv:{id,title,updatedAt})=>void} deps.onConversationCreated
 * @param {()=>void} deps.reloadConversations
 * @param {(msg:string)=>void} deps.onToast
 * @param {()=>void} deps.onUnauthorized
 */
export function useChat({
  token,
  activeId,
  setActiveId,
  onConversationCreated,
  reloadConversations,
  onToast,
  onUnauthorized,
}) {
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);

  // Refs keep async callbacks free of stale closures.
  const messagesRef = useRef([]);
  const activeRef = useRef(activeId);
  const sendingRef = useRef(false);
  activeRef.current = activeId;

  const apply = useCallback((updater) => {
    setMessages((prev) => {
      const next = typeof updater === "function" ? updater(prev) : updater;
      messagesRef.current = next;
      return next;
    });
  }, []);

  const patchLast = useCallback(
    (patch) =>
      apply((prev) => {
        if (!prev.length) return prev;
        const next = prev.slice();
        next[next.length - 1] = { ...next[next.length - 1], ...patch };
        return next;
      }),
    [apply]
  );

  /** Load persisted messages for a conversation (or clear for a new chat). */
  const openConversation = useCallback(
    (id) => apply(id ? loadMessages(id) : []),
    [apply]
  );

  /** Ensure a conversation exists before the first message; returns its id. */
  const ensureConversation = useCallback(
    async (firstText) => {
      if (activeRef.current) return activeRef.current;
      try {
        const conv = await createConversation(token, firstText.slice(0, 40));
        const id = conv.conversation_id;
        activeRef.current = id;
        setActiveId(id);
        onConversationCreated({
          id,
          title: conv.title || firstText.slice(0, 40),
          updatedAt: new Date().toISOString(),
        });
        return id;
      } catch (err) {
        if (err?.status === 401) onUnauthorized?.();
        return null; // /chat will create one on the backend as a fallback
      }
    },
    [token, setActiveId, onConversationCreated, onUnauthorized]
  );

  const send = useCallback(
    async (rawText, streamingOn) => {
      const text = rawText.trim();
      if (!text || sendingRef.current || !token) return;

      sendingRef.current = true;
      setSending(true);
      apply((prev) => [
        ...prev,
        { role: "user", text },
        { role: "assistant", text: "", streaming: true, tools: [] },
      ]);

      const conversationId = await ensureConversation(text);

      try {
        if (streamingOn) {
          await streamChat({
            token,
            conversationId,
            query: text,
            onToken: (acc) => patchLast({ text: acc }),
            onConversationId: (id) => {
              if (!activeRef.current) {
                activeRef.current = id;
                setActiveId(id);
              }
            },
          });
          patchLast({ streaming: false });
        } else {
          const data = await sendChat({ token, conversationId, query: text });
          if (data.conversation_id && !activeRef.current) {
            activeRef.current = data.conversation_id;
            setActiveId(data.conversation_id);
          }
          patchLast({
            text: data.response || "",
            streaming: false,
            tools: mapTools(data.tools_used),
          });
        }
      } catch (err) {
        if (err?.status === 401) {
          onUnauthorized?.();
        } else if (err?.status === 429) {
          patchLast({ text: RATE_TEXT, streaming: false, isError: true });
        } else {
          patchLast({ text: ERROR_TEXT, streaming: false, isError: true });
          onToast?.("Couldn't reach the support service.");
        }
      } finally {
        sendingRef.current = false;
        setSending(false);
        const id = activeRef.current;
        if (id) saveMessages(id, messagesRef.current);
        reloadConversations?.();
      }
    },
    [token, ensureConversation, patchLast, apply, setActiveId, onToast, onUnauthorized, reloadConversations]
  );

  return { messages, sending, send, openConversation };
}
