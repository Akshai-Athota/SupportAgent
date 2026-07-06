import { useEffect, useRef } from "react";
import { Message } from "./Message";
import { WelcomeState } from "./WelcomeState";
import styles from "./chat.module.css";

/** Scrollable transcript. Shows the welcome state when empty. */
export function MessageList({ token, messages, sending, showActivity, onPickSuggestion }) {
  const endRef = useRef(null);
  const scrollRef = useRef(null);

  // Keep the latest message in view as content streams in.
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, sending]);

  return (
    <div className={styles.messages} ref={scrollRef}>
      {messages.length === 0 ? (
        <WelcomeState token={token} onPick={onPickSuggestion} />
      ) : (
        messages.map((message, i) => (
          <Message key={i} message={message} showActivity={showActivity} />
        ))
      )}
      <div ref={endRef} style={{ height: 6 }} />
    </div>
  );
}
