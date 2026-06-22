import { useAuth } from "../../context/AuthContext";
import { Spinner } from "../ui/Spinner";
import styles from "./auth.module.css";

export function SignupForm({ onSwitch }) {
  const { signup, loading, error } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    signup({
      first_name: (data.get("first_name") || "").trim(),
      last_name: (data.get("last_name") || "").trim(),
      email: (data.get("email") || "").trim(),
      password: data.get("password") || "",
      phone_number: (data.get("phone_number") || "").trim() || null,
    });
  };

  return (
    <>
      <h1 className={styles.title}>Create your account</h1>
      <p className={styles.subtitle}>
        Sign up to start chatting with Aria about orders, refunds and more.
      </p>

      <form onSubmit={handleSubmit}>
        <div className={`${styles.field} ${styles.row2}`}>
          <div>
            <label className={styles.label}>First name</label>
            <input className={styles.input} name="first_name" placeholder="Jane" />
          </div>
          <div>
            <label className={styles.label}>Last name</label>
            <input className={styles.input} name="last_name" placeholder="Doe" />
          </div>
        </div>
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
          <label className={styles.label}>
            Phone <span className={styles.optional}>(optional)</span>
          </label>
          <input className={styles.input} name="phone_number" placeholder="+1 555 000 1234" />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Password</label>
          <input
            className={styles.input}
            name="password"
            type="password"
            autoComplete="new-password"
            placeholder="At least 6 characters"
          />
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <button className={styles.submit} type="submit" disabled={loading}>
          {loading ? (
            <>
              <Spinner size={16} /> Please wait…
            </>
          ) : (
            "Create account"
          )}
        </button>
      </form>

      <p className={styles.switchText}>
        Already have an account?{" "}
        <span className={styles.switchLink} onClick={onSwitch}>
          Log in
        </span>
      </p>
    </>
  );
}
