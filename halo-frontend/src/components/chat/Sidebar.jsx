import { Spark, Plus } from "../ui/Icons";
import { ConversationList } from "./ConversationList";
import { Profile } from "./Profile";
import styles from "./chat.module.css";

export function Sidebar({
  conversations,
  activeId,
  onSelect,
  onDelete,
  onNewChat,
  user,
  onLogout,
}) {
  return (
    <div className={styles.sidebar}>
      <div className={styles.sideTop}>
        <div className={styles.brand}>
          <div className={styles.brandMark}>
            <Spark size={17} color="#fff" />
          </div>
          <span className={styles.brandName}>Halo</span>
        </div>
        <button className={styles.newBtn} onClick={onNewChat}>
          <Plus size={16} color="#fff" />
          New chat
        </button>
      </div>

      <div className={styles.convScroll}>
        <div className={styles.convLabel}>Recent chats</div>
        <ConversationList
          conversations={conversations}
          activeId={activeId}
          onSelect={onSelect}
          onDelete={onDelete}
        />
      </div>

      <Profile user={user} onLogout={onLogout} />
    </div>
  );
}
