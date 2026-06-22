import styles from "./ui.module.css";

export function Toast({ message }) {
  if (!message) return null;
  return <div className={styles.toast}>{message}</div>;
}
