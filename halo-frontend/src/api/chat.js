import { API_BASE, authHeaders, ApiError } from "./client";

function chatQuery(conversationId) {
  return conversationId
    ? "?conversation_id=" + encodeURIComponent(conversationId)
    : "";
}

/**
 * POST /chat -> { response, tools_used, conversation_id }
 * Non-streaming: returns the full answer at once, including tools used.
 */
export async function sendChat({ token, conversationId, query }) {
  const res = await fetch(API_BASE + "/chat" + chatQuery(conversationId), {
    method: "POST",
    headers: { ...authHeaders(token), "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new ApiError(res.status);
  return res.json();
}

/**
 * POST /chat/stream -> Server-Sent Events.
 * Each event is `data: <json-encoded-token>`; the stream ends with `data: [DONE]`.
 * The new conversation id (if any) arrives in the `X-Conversation-Id` header.
 *
 * @param {object} opts
 * @param {(accumulatedText:string)=>void} opts.onToken - called with the full text so far
 * @param {(conversationId:string)=>void} [opts.onConversationId]
 */
export async function streamChat({ token, conversationId, query, onToken, onConversationId }) {
  const res = await fetch(API_BASE + "/chat/stream" + chatQuery(conversationId), {
    method: "POST",
    headers: { ...authHeaders(token), "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new ApiError(res.status);

  const cid = res.headers.get("X-Conversation-Id");
  if (cid && onConversationId) onConversationId(cid);

  // Fallback for environments without a readable stream.
  if (!res.body || !res.body.getReader) {
    onToken(await res.text());
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let accumulated = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let boundary;
    while ((boundary = buffer.indexOf("\n\n")) >= 0) {
      const line = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      const match = line.match(/^data: ([\s\S]*)$/);
      if (!match) continue;

      const payload = match[1];
      if (payload === "[DONE]") return;
      try {
        accumulated += JSON.parse(payload);
        onToken(accumulated);
      } catch {
        // ignore keep-alive / non-JSON lines
      }
    }
  }
}
