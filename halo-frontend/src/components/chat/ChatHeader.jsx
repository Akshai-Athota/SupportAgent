import styles from "./chat.module.css";

/** Top bar: active conversation title + the live-streaming toggle. */
export function ChatHeader({ title, streamingOn, onToggleStreaming }) {
  return (
    <div className={styles.header}>
      <div style={{ minWidth: 0 }}>
        <div className={styles.headerTitle}>{title}</div>
        <div className={styles.headerSub}>Aria · AI support agent</div>
      </div>

      <div className={styles.toggle} onClick={onToggleStreaming} role="switch" aria-checked={streamingOn}>
        <span className={styles.toggleLabel}>Live streaming</span>
        <div className={`${styles.track} ${streamingOn ? styles.trackOn : ""}`}>
          <div className={`${styles.knob} ${streamingOn ? styles.knobOn : ""}`} />
        </div>
        <span className={styles.toggleState}>{streamingOn ? "On" : "Off"}</span>
      </div>
    </div>
  );
}
