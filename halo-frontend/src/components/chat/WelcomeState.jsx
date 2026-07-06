import { Spark } from "../ui/Icons";
import styles from "./chat.module.css";
import { SampleData } from "./SampleData";

const SUGGESTIONS = [
  "Where is my order?",
  "I'd like to request a refund",
  "What's the status of my latest delivery?",
  "I'd like to talk to a human agent",
];

const SHORT_LABELS = {
  "What's the status of my latest delivery?": "Track my latest delivery",
  "I'd like to talk to a human agent": "Talk to a human agent",
};

export function WelcomeState({ onPick }) {
  return (
    <div className={styles.welcome}>
      <div className={styles.welcomeIcon}>
        <Spark size={34} color="#fff" />
      </div>
      <h2 className={styles.welcomeTitle}>Hi, I'm Aria — how can I help?</h2>
      <p className={styles.welcomeText}>
        Ask me about your orders, refunds, deliveries or anything else. I'll
        look things up and bring in a human if you need one.
      </p>
      <SampleData token={token} onPick={onPick} />
      <div className={styles.suggestGrid}>
        {SUGGESTIONS.map((text) => (
          <div key={text} className={styles.suggestCard} onClick={() => onPick(text)}>
            <span className={styles.suggestIcon}>
              <Spark size={15} color="#6C47FF" />
            </span>
            <span className={styles.suggestText}>{SHORT_LABELS[text] || text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
