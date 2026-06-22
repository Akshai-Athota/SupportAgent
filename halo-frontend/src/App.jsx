import { useAuth } from "./context/AuthContext";
import { AuthPage } from "./components/auth/AuthPage";
import { ChatApp } from "./components/chat/ChatApp";

export default function App() {
  const { ready, token } = useAuth();

  // Brief splash while we restore the session from localStorage.
  if (!ready) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#FBFAFF",
        }}
      >
        <div
          style={{
            width: 46,
            height: 46,
            borderRadius: 14,
            background: "linear-gradient(135deg,#6C47FF,#B453E6)",
            boxShadow: "0 10px 30px rgba(108,71,255,.3)",
            animation: "haloFloat 1.6s ease-in-out infinite",
          }}
        />
      </div>
    );
  }

  return token ? <ChatApp /> : <AuthPage />;
}
