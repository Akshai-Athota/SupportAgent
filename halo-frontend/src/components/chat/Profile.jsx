import { useState, useEffect, useRef } from "react";
import { Logout, Chevron } from "../ui/Icons";
import styles from "./chat.module.css";

/** Bottom-of-sidebar account pill with a logout popover. */
export function Profile({ user, onLogout }) {
  const [open, setOpen] = useState(false);
  const wrapRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onDocClick = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, [open]);

  const email = user?.email || "guest";
  const initial = (email.trim()[0] || "U").toUpperCase();
  const meta = user?.id ? `Customer #${user.id}` : "Signed in";

  return (
    <div className={styles.profileWrap} ref={wrapRef}>
      {open && (
        <div className={styles.popover}>
          <div className={styles.popHead}>
            <div className={styles.popEmail}>{email}</div>
            <div className={styles.popMeta}>{meta}</div>
          </div>
          <button className={styles.popLogout} onClick={onLogout}>
            <Logout size={16} />
            Log out
          </button>
        </div>
      )}

      <button className={styles.profileBtn} onClick={() => setOpen((v) => !v)}>
        <div className={styles.avatar}>{initial}</div>
        <div className={styles.profileMeta}>
          <div className={styles.profileEmail}>{email}</div>
          <div className={styles.profileSub}>{meta}</div>
        </div>
        <Chevron size={16} color="#B6AECB" style={{ flex: "none" }} />
      </button>
    </div>
  );
}
