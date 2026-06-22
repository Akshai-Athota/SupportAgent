import styles from "./ui.module.css";

export function Spinner({ size = 16, borderWidth }) {
  return (
    <span
      className={styles.spinner}
      style={{ width: size, height: size, borderWidth }}
    />
  );
}
