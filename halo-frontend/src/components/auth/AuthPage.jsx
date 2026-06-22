import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { LoginForm } from "./LoginForm";
import { SignupForm } from "./SignupForm";
import { Spark } from "../ui/Icons";
import styles from "./auth.module.css";

export function AuthPage() {
  const { clearError } = useAuth();
  const [mode, setMode] = useState("login");

  const switchMode = (next) => {
    clearError();
    setMode(next);
  };

  return (
    <div className={styles.page}>
      <div className={styles.formSide}>
        <div className={styles.formWrap}>
          <div className={styles.brand}>
            <div className={styles.brandMark}>
              <Spark size={22} color="#fff" />
            </div>
            <span className={styles.brandName}>Halo</span>
          </div>

          {mode === "login" ? (
            <LoginForm onSwitch={() => switchMode("signup")} />
          ) : (
            <SignupForm onSwitch={() => switchMode("login")} />
          )}
        </div>
      </div>

      <DecorativePanel />
    </div>
  );
}

function DecorativePanel() {
  return (
    <div className={styles.deco}>
      <div className={`${styles.blob} ${styles.blob1}`} />
      <div className={`${styles.blob} ${styles.blob2}`} />
      <div className={styles.decoInner}>
        <h2 className={styles.decoTitle}>
          Friendly help,
          <br />
          any time of day.
        </h2>
        <p className={styles.decoText}>
          Aria can check your orders, sort out refunds, search our help center,
          and loop in a human whenever you need one.
        </p>
        <div className={styles.previewCard}>
          <div className={styles.pvUserRow}>
            <div className={styles.pvUserBubble}>Where's my order #4821?</div>
          </div>
          <div className={styles.pvBotRow}>
            <div className={styles.pvAvatar}>A</div>
            <div className={styles.pvBotBubble}>
              It's out for delivery and should arrive today by 6pm. Want me to
              send tracking updates?
            </div>
          </div>
          <div className={styles.pvChips}>
            <span className={styles.pvChip}>Looked up order status</span>
          </div>
        </div>
      </div>
    </div>
  );
}
