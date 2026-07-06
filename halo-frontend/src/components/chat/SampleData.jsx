import { useState } from "react";
import { seedOrders } from "../../api/demo";
import { ApiError } from "../../api/client";
import { Spark, Plus, Check } from "../ui/Icons";
import styles from "./chat.module.css";

const STATUS_META = {
  processing: { label: "Processing", cls: "statusProcessing" },
  shipped: { label: "Shipped", cls: "statusShipped" },
  delivered: { label: "Delivered", cls: "statusDelivered" },
  cancelled: { label: "Cancelled", cls: "statusCancelled" },
};
const COUNTS = [1, 2, 3, 4, 5];
const money = (n) => "€" + Number(n).toFixed(2);

/**
 * First-run helper on the welcome screen: lets a new customer seed sample
 * orders via POST /demo/seed-orders, then surfaces them for Aria to explore.
 * `onPick(text)` reuses the welcome-suggestion handler to ask Aria a question.
 */
export function SampleData({ token, onPick }) {
  const [count, setCount] = useState(3);
  const [status, setStatus] = useState("idle"); // idle | loading | done | full | error
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");

  const generate = async () => {
    if (status === "loading") return;
    setStatus("loading");
    setError("");
    try {
      const res = await seedOrders(token, count);
      const created = (res?.orders || []).map((o) => ({
        id: o.order_id,
        status: o.status,
        total: o.total,
      }));
      setOrders((prev) => [...created, ...prev]);
      setStatus("done");
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        setStatus("full");
      } else {
        setError(err?.detail || "Couldn't create sample orders. Please try again.");
        setStatus((s) => (orders.length ? "done" : "error"));
      }
    }
  };

  const hasOrders = orders.length > 0;
  const first = !hasOrders;

  return (
    <div className={styles.sampleCard}>
      <div className={styles.sampleHead}>
        <span className={styles.sampleIcon}>
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none">
            <path d="M21 8.2l-9-5-9 5v7.6l9 5 9-5V8.2z" stroke="#6c47ff" strokeWidth="1.7" strokeLinejoin="round" />
            <path d="M3.2 8.2l8.8 4.9 8.8-4.9M12 22V13.1" stroke="#6c47ff" strokeWidth="1.7" strokeLinejoin="round" />
          </svg>
        </span>
        <div className={styles.sampleHeadText}>
          <div className={styles.sampleTitle}>
            {first ? "Explore with sample orders" : "Your sample orders"}
          </div>
          <div className={styles.sampleSub}>
            {status === "full"
              ? "That's the full set. Ask Aria about any of them below."
              : first
              ? "You don't have any orders yet. Generate a few and Aria can look them up, track deliveries and process refunds."
              : "All set. Ask Aria about any of these below."}
          </div>
        </div>
      </div>

      {hasOrders && (
        <div className={styles.orderList}>
          {orders.map((o) => {
            const meta = STATUS_META[o.status] || { label: o.status, cls: "statusProcessing" };
            return (
              <div className={styles.orderRow} key={o.id}>
                <span className={styles.orderId}>#{o.id}</span>
                <span className={`${styles.statusBadge} ${styles[meta.cls]}`}>
                  <span className={styles.statusDot} />
                  {meta.label}
                </span>
                <span className={styles.orderTotal}>{money(o.total)}</span>
              </div>
            );
          })}
        </div>
      )}

      {hasOrders && onPick && (
        <>
          <div className={styles.sampleLabel}>Now try asking Aria</div>
          <div className={styles.tryChips}>
            {[
              `Where is order #${orders[0].id}?`,
              `Refund for order #${orders[0].id}`,
              "Track my latest delivery",
            ].map((t) => (
              <button key={t} className={styles.tryChip} onClick={() => onPick(t)}>
                <Spark size={13} color="#6C47FF" />
                {t}
              </button>
            ))}
          </div>
        </>
      )}

      {status !== "full" && status !== "loading" && (
        <>
          {first && (
            <>
              <div className={styles.sampleLabel}>How many orders?</div>
              <div className={styles.countRow}>
                {COUNTS.map((n) => (
                  <button
                    key={n}
                    className={`${styles.countBtn} ${n === count ? styles.countBtnOn : ""}`}
                    onClick={() => setCount(n)}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </>
          )}
          <button className={hasOrders ? styles.sampleMore : styles.sampleBtn} onClick={generate}>
            {hasOrders ? (
              <>
                <Plus size={16} color="#6c47ff" />
                Generate a few more
              </>
            ) : (
              <>
                <Spark size={18} color="#fff" />
                Generate sample orders
              </>
            )}
          </button>
        </>
      )}

      {status === "loading" && (
        <div className={styles.sampleLoading}>
          <span className={styles.sampleSpin} />
          Creating your sample orders…
        </div>
      )}

      {status === "full" && (
        <div className={styles.sampleFull}>
          <Check size={14} color="#2fae74" />
          You've reached the maximum of 10 sample orders.
        </div>
      )}

      {error && <div className={styles.sampleError}>{error}</div>}
    </div>
  );
}
