import { Check } from "../ui/Icons";
import styles from "./chat.module.css";

function TypingDots() {
  return (
    <span className={styles.dots}>
      <span className={styles.dot} style={{ animationDelay: "0s" }} />
      <span className={styles.dot} style={{ animationDelay: "0.18s" }} />
      <span className={styles.dot} style={{ animationDelay: "0.36s" }} />
    </span>
  );
}

/**
 * A single chat message — user bubble, or assistant bubble with optional
 * typing dots, streaming caret, and agent tool chips.
 */
export function Message({ message, showActivity }) {
  if (message.role === "user") {
    return (
      <div className={styles.userRow}>
        <div className={styles.userBubble}>{message.text}</div>
      </div>
    );
  }

  const isEmpty = message.streaming && !message.text;
  const tools = showActivity ? message.tools || [] : [];

  return (
    <div className={styles.botRow}>
      <div className={styles.botAvatar}>A</div>
      <div className={styles.botCol}>
        <div className={styles.botName}>Aria</div>
        <div className={styles.botBubble}>
          {isEmpty ? (
            <TypingDots />
          ) : (
            <>
              <span>{message.text}</span>
              {message.streaming && <span className={styles.caret} />}
            </>
          )}
        </div>
        {tools.length > 0 && (
          <div className={styles.chips}>
            {tools.map((tool, i) => (
              <span key={tool.name || i} className={styles.chip}>
                <Check size={11} color="#6C47FF" />
                {tool.label}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
