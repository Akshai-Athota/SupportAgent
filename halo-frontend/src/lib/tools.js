/**
 * Friendly labels for the agent tools the backend reports in `tools_used`.
 * Keep these in sync with app/tools/tools.py on the backend.
 */
export const TOOL_LABELS = {
  check_my_refund_eligibility: "Checked refund eligibility",
  get_my_order_status: "Looked up order status",
  get_my_orders: "Fetched your orders",
  get_current_customer: "Verified your account",
  search_knowledge_base: "Searched the help center",
  save_memory: "Saved a note for next time",
  escalate_to_human: "Escalated to a human agent",
  get_my_tickets_of_order: "Checked your support tickets",
};

/** Map a raw `tools_used` array into de-duplicated, labelled chips. */
export function mapTools(toolNames) {
  if (!Array.isArray(toolNames) || toolNames.length === 0) return [];
  const seen = new Set();
  const out = [];
  for (const name of toolNames) {
    if (seen.has(name)) continue;
    seen.add(name);
    const label = TOOL_LABELS[name];
    if (label) out.push({ name, label });
  }
  return out;
}
