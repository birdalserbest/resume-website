import { useState, useRef, useEffect } from "react";
import { API_BASE } from "src/config"; // single source for backend URL

export default function Chat() {
  // Local state for messages in the conversation.
  // Each message has a `role` (user/assistant) and a `content` string. See initial message
  const INITIAL_MESSAGES = [
    {
      role: "assistant",
      content: "Hi! Ask me about Birdal’s experience or projects.",
    },
  ];
  const [messages, setMessages] = useState(INITIAL_MESSAGES);

  // State for the text in the input box
  const [input, setInput] = useState("");
  // Loading flag to disable input and show "Thinking…" bubble
  const [loading, setLoading] = useState(false);

  // Reference to the scrollable chat container so we can auto-scroll on new messages
  const listRef = useRef(null);

  // Auto-scroll whenever messages update
  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  // Called when the user presses “Send” or hits Enter
  async function send() {
    const text = input.trim();
    if (!text || loading) return; // skip empty sends or double clicks

    // Append the user’s message immediately to the chat
    setInput("");
    const next = [...messages, { role: "user", content: text }];
    setMessages(next);
    setLoading(true);

    try {
      // Send all recent messages to backend; we keep only last 8 to limit payload size
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next.slice(-8) }),
      });

      // Parse backend response
      const data = await res.json();
      // Append assistant’s reply
      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.reply ?? "…" },
      ]);
    } catch {
      // If backend can’t be reached, show fallback message
      setMessages((m) => [
        ...m,
        { role: "assistant", content: "Sorry — backend not reachable." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // Handle keyboard input: Enter = send; Shift+Enter = newline
  function onKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  function clearChat() {
    if (loading) return; // don't clear mid-request
    setMessages(INITIAL_MESSAGES); // reset to greeting
    listRef.current?.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Render UI
  return (
    <div className="mx-auto w-[600px] max-w-[90vw] p-4 overflow-x-hidden">
      {/* ---------- Header ---------- */}
      <header className="text-center mb-6">
        <h1 className="text-3xl font-bold">Chat with Birdal’s Resume</h1>
        <p className="opacity-75 text-sm mt-1">
          Try: “Summarize your backend experience.”
        </p>
      </header>

      {/* ---------- Scrollable message list ---------- */}
      <div
        ref={listRef}
        className="bg-neutral-900/50 border border-neutral-800 rounded-2xl
                 h-[55vh] min-h-[320px] max-h-[70vh] flex-shrink-0
                 p-4 overflow-auto space-y-3 w-full"
      >
        {messages.map((m, i) => (
          <div
            key={i}
            className={m.role === "user" ? "text-right" : "text-left"}
          >
            {/* Each chat bubble */}
            <div
              className={`inline-block px-3 py-2 rounded-xl
              max-w-[80%]
              hyphens-auto break-normal whitespace-pre-wrap
              ${
                m.role === "user"
                  ? "bg-blue-600 text-white text-left"
                  : "bg-neutral-800 text-neutral-100"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="text-left">
            <div className="inline-block px-3 py-2 rounded-xl bg-neutral-800 text-neutral-100 animate-pulse">
              Thinking…
            </div>
          </div>
        )}
      </div>

      {/* ---------- Input area + Buttons ---------- */}
      <div className="mt-3 flex gap-2 items-stretch">
        {/* Text input */}
        <textarea
          className="flex-1 resize-none rounded-xl border border-neutral-700 bg-neutral-900 p-3 outline-none focus:ring-2 focus:ring-blue-600"
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKey}
          placeholder="Ask about experience, projects, tech choices…"
        />

        {/* Clear and Send buttons stacked vertically */}
        <div className="flex flex-col gap-2 w-24">
          <button
            onClick={clearChat}
            disabled={loading}
            className="flex-1 rounded-xl border border-neutral-700 hover:bg-neutral-800 disabled:opacity-50 text-sm"
            title="Clear chat"
          >
            Clear
          </button>

          <button
            onClick={send}
            disabled={loading}
            className="flex-1 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium"
          >
            Send
          </button>
        </div>
      </div>

      {/* ---------- Footer hint ---------- */}
      <div className="mt-2 text-xs opacity-60 text-center">
        Powered by a private model adapter (OpenAI/Groq) — demo mode.
      </div>
    </div>
  );
}
