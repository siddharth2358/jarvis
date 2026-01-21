import Chat from "./Chat";
import VoiceChat from "./VoiceChat";

export default function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🧠 Jarvis AI Assistant</h1>
      <Chat />
      <VoiceChat />
    </div>
  );
}
