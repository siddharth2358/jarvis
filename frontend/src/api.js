import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function sendText(message) {
  const res = await axios.post(
    `${API_BASE}/chat`,
    null,
    { params: { message } }
  );
  return res.data;
}

export async function sendVoice(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob);

  const res = await axios.post(
    `${API_BASE}/voice-chat`,
    formData
  );
  return res.data;
}
