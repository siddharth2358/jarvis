export default function Message({ role, text }) {
  return (
    <div style={{ textAlign: role === "user" ? "right" : "left" }}>
      <span
        style={{
          background: role === "user" ? "#2563eb" : "#374151",
          color: "white",
          padding: "10px 14px",
          borderRadius: "14px",
          display: "inline-block",
          margin: "6px 0",
          maxWidth: "70%"
        }}
      >
        {text}
      </span>
    </div>
  );
}
