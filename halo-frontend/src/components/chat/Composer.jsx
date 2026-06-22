import { useRef } from "react";
import { Send } from "../ui/Icons";
import { Spinner } from "../ui/Spinner";
import styles from "./chat.module.css";

/** Auto-growing message input. Enter sends, Shift+Enter inserts a newline. */
export function Composer({ sending, onSend }) {
  const ref = useRef(null);

  const submit = () => {
    const el = ref.current;
    if (!el) return;
    const text = el.value;
    if (!text.trim()) return;
    el.value = "";
    el.style.height = "auto";
    onSend(text);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
      return;
    }
    const el = e.target;
    requestAnimationFrame(() => {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 140) + "px";
    });
  };

  return (
    <div className={styles.composer}>
      <div className={styles.composerInner}>
        <div className={styles.composerBox}>
          <textarea
            ref={ref}
            className={styles.textarea}
            rows={1}
            placeholder="Message Aria…"
            onKeyDown={handleKeyDown}
          />
          <button className={styles.sendBtn} onClick={submit} aria-label="Send">
            {sending ? <Spinner size={16} /> : <Send size={18} color="#fff" />}
          </button>
        </div>
        <div className={styles.disclaimer}>
          Aria is an AI agent and can make mistakes. Verify important details.
        </div>
      </div>
    </div>
  );
}
