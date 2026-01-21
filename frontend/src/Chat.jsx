import { useState } from "react";
import { sendText } from "./api";
import Message from "./Message";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function handleSend() {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);

    setInput("");

    try {
      const res = await sendText(input);

      const assistantMessage = {
        role: "assistant",
        text: res.response
      };

      // Add assistant message AFTER response
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "assistant", text: "⚠️ Error talking to backend" }
      ]);
    }
  }

  return (
    <div>
      <div style={{ height: "55vh", overflowY: "auto", padding: "10px" }}>
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}
      </div>

      <div>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask Jarvis..."
          style={{ width: "75%", padding: "10px" }}
        />
        <button onClick={handleSend} style={{ marginLeft: "10px" }}>
          Send
        </button>
      </div>
    </div>
  );
}
