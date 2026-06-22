import { ChatBubble, Trash } from "../ui/Icons";
import styles from "./chat.module.css";

export function ConversationList({ conversations, activeId, onSelect, onDelete }) {
  if (conversations.length === 0) {
    return (
      <div className={styles.convEmpty}>
        No conversations yet. Start a new chat to get help from Aria.
      </div>
    );
  }

  return (
    <>
      {conversations.map((c) => {
        const active = c.id === activeId;
        return (
          <div
            key={c.id}
            className={`${styles.convRow} ${active ? styles.convRowActive : ""}`}
            onClick={() => onSelect(c.id)}
          >
            <ChatBubble size={15} color="#8A7FC2" style={{ flex: "none" }} />
            <span className={styles.convTitle}>{c.title}</span>
            <span
              className={styles.convDelete}
              onClick={(e) => {
                e.stopPropagation();
                onDelete(c.id);
              }}
              aria-label="Delete conversation"
            >
              <Trash size={14} />
            </span>
          </div>
        );
      })}
    </>
  );
}
