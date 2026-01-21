import { useRef, useState } from "react";
import { sendVoice } from "./api";

export default function VoiceChat() {
  const recorder = useRef(null);
  const chunks = useRef([]);
  const [recording, setRecording] = useState(false);

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder.current = new MediaRecorder(stream);
    recorder.current.start();
    setRecording(true);

    recorder.current.ondataavailable = e => chunks.current.push(e.data);

    recorder.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: "audio/wav" });
      chunks.current = [];

      const res = await sendVoice(blob);
      new Audio(`http://localhost:8000${res.audio_url}`).play();
    };
  }

  function stopRecording() {
    recorder.current.stop();
    setRecording(false);
  }

  return (
    <button
      onMouseDown={startRecording}
      onMouseUp={stopRecording}
      style={{
        background: recording ? "red" : "green",
        color: "white",
        padding: "16px",
        borderRadius: "50%",
        marginTop: "15px"
      }}
    >
      🎤
    </button>
  );
}
