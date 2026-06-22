import { useState, useCallback } from "react";
import { useAuth } from "../../context/AuthContext";
import { useConversations } from "../../hooks/useConversations";
import { useChat } from "../../hooks/useChat";
import { streamingPref } from "../../lib/storage";
import { Sidebar } from "./Sidebar";
import { ChatHeader } from "./ChatHeader";
import { MessageList } from "./MessageList";
import { Composer } from "./Composer";
import { Toast } from "../ui/Toast";
import styles from "./chat.module.css";

const SHOW_AGENT_ACTIVITY = true; // toggle the tool-usage chips globally

/** Authenticated app shell: sidebar + chat. Orchestrates conversation + chat state. */
export function ChatApp() {
  const { token, user, logout } = useAuth();

  const [activeId, setActiveId] = useState(null);
  const [streamingOn, setStreamingOn] = useState(() => streamingPref.get());
  const [toast, setToast] = useState("");

  const showToast = useCallback((message) => {
    setToast(message);
    setTimeout(() => setToast(""), 4000);
  }, []);

  const { conversations, reload, upsert, remove } = useConversations(token, {
    onUnauthorized: logout,
    onError: showToast,
  });

  const { messages, sending, send, openConversation } = useChat({
    token,
    activeId,
    setActiveId,
    onConversationCreated: upsert,
    reloadConversations: reload,
    onToast: showToast,
    onUnauthorized: logout,
  });

  const selectConversation = useCallback(
    (id) => {
      if (sending) return;
      setActiveId(id);
      openConversation(id);
    },
    [sending, openConversation]
  );

  const newChat = useCallback(() => {
    if (sending) return;
    setActiveId(null);
    openConversation(null);
  }, [sending, openConversation]);

  const deleteConversation = useCallback(
    (id) => {
      remove(id);
      if (id === activeId) {
        setActiveId(null);
        openConversation(null);
      }
    },
    [remove, activeId, openConversation]
  );

  const toggleStreaming = useCallback(() => {
    setStreamingOn((prev) => {
      const next = !prev;
      streamingPref.set(next);
      return next;
    });
  }, []);

  const active = conversations.find((c) => c.id === activeId);

  return (
    <div className={styles.app}>
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={selectConversation}
        onDelete={deleteConversation}
        onNewChat={newChat}
        user={user}
        onLogout={logout}
      />

      <div className={styles.main}>
        <ChatHeader
          title={active ? active.title : "New chat"}
          streamingOn={streamingOn}
          onToggleStreaming={toggleStreaming}
        />
        <MessageList
          messages={messages}
          sending={sending}
          showActivity={SHOW_AGENT_ACTIVITY}
          onPickSuggestion={(text) => send(text, streamingOn)}
        />
        <Composer sending={sending} onSend={(text) => send(text, streamingOn)} />
      </div>

      <Toast message={toast} />
    </div>
  );
}
