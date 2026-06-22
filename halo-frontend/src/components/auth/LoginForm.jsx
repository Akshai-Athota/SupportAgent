import { useAuth } from "../../context/AuthContext";
import { Spinner } from "../ui/Spinner";
import styles from "./auth.module.css";

export function LoginForm({ onSwitch }) {
  const { login, loading, error } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    login((data.get("email") || "").trim(), data.get("password") || "");
  };

  return (
    <>
      <h1 className={styles.title}>Welcome back</h1>
      <p className={styles.subtitle}>
        Log in to pick up your conversations with Aria, your support assistant.
      </p>

      <form onSubmit={handleSubmit}>
        <div className={styles.field}>
          <label className={styles.label}>Email</label>
          <input
            className={styles.input}
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Password</label>
          <input
            className={styles.input}
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="Enter your password"
          />
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <button className={styles.submit} type="submit" disabled={loading}>
          {loading ? (
            <>
              <Spinner size={16} /> Please wait…
            </>
          ) : (
            "Log in"
          )}
        </button>
      </form>

      <p className={styles.switchText}>
        New to Halo?{" "}
        <span className={styles.switchLink} onClick={onSwitch}>
          Create an account
        </span>
      </p>
    </>
  );
}
