import { apiFetch } from "./client";

/** GET /conversation/ -> { conversations: [{ conversation_id, title, updated_at }] } */
export async function listConversations(token) {
  const data = await apiFetch("/conversation/", { token });
  return (data?.conversations || []).map((c) => ({
    id: c.conversation_id,
    title: c.title || "New chat",
    updatedAt: c.updated_at,
  }));
}

/** POST /conversation/create?title= -> { conversation_id, title } */
export function createConversation(token, title) {
  const qs = "?title=" + encodeURIComponent(title || "");
  return apiFetch("/conversation/create" + qs, { method: "POST", token });
}

/** DELETE /conversation/{id} -> { deleted, conversation_id } */
export function deleteConversation(token, id) {
  return apiFetch(`/conversation/${id}`, { method: "DELETE", token });
}
