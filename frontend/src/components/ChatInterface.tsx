"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Mic, AlertTriangle, Bot, User, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { clsx } from "clsx";
import type { ChatMessage } from "@/types";
import { sendChatMessage } from "@/lib/api";

const SUGGESTED_QUERIES = [
  "I have a fever and sore throat for 2 days",
  "I have a headache and nausea",
  "My stomach has been hurting since yesterday",
  "I feel very tired and weak",
];

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm MediGuide AI, your clinical support assistant.\n\nI can help you understand your symptoms, suggest what might be causing them, and guide you on the next safe step — whether that's home care or seeing a doctor.\n\n**Please tell me:** What symptoms are you experiencing today?\n\n---\n⚕️ *I'm not a doctor. For emergencies, call 112 or 911 immediately.*",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isEmergency, setIsEmergency] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const messageText = (text ?? input).trim();
    if (!messageText || isLoading) return;

    const userMsg: ChatMessage = {
      role: "user",
      content: messageText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      const result = await sendChatMessage(messageText, history);

      if (result.is_emergency) setIsEmergency(true);

      const assistantMsg: ChatMessage = {
        role: "assistant",
        content: result.response,
        is_emergency: result.is_emergency,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I encountered an error. Please check your connection and try again. " +
            "If you have a medical emergency, call 112 or 911 immediately.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoice = () => {
    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      alert("Voice input is not supported in your browser. Please type your symptoms.");
      return;
    }
    const SpeechRecognition =
      (window as unknown as { SpeechRecognition?: { new(): SpeechRecognition } }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: { new(): SpeechRecognition } }).webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      inputRef.current?.focus();
    };
    recognition.start();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-3xl mx-auto">
      {/* Emergency alert bar */}
      <AnimatePresence>
        {isEmergency && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            className="bg-red-600 text-white px-4 py-3 flex items-center gap-2 rounded-t-2xl"
          >
            <AlertTriangle className="w-5 h-5 flex-shrink-0 animate-pulse" />
            <p className="text-sm font-semibold">
              Emergency detected — Call <a href="tel:112" className="underline">112</a> or{" "}
              <a href="tel:911" className="underline">911</a> immediately.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white rounded-2xl border border-gray-100 shadow-sm">
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={clsx("flex gap-3", msg.role === "user" ? "flex-row-reverse" : "flex-row")}
          >
            {/* Avatar */}
            <div
              className={clsx(
                "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                msg.role === "user" ? "bg-blue-600" : msg.is_emergency ? "bg-red-600" : "bg-slate-700"
              )}
            >
              {msg.role === "user" ? (
                <User className="w-4 h-4 text-white" />
              ) : (
                <Bot className="w-4 h-4 text-white" />
              )}
            </div>

            {/* Bubble */}
            <div
              className={clsx(
                "max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-none"
                  : msg.is_emergency
                  ? "bg-red-50 border border-red-200 text-red-900 rounded-tl-none"
                  : "bg-gray-50 border border-gray-100 text-gray-800 rounded-tl-none prose-medical"
              )}
            >
              {msg.role === "assistant" ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                msg.content
              )}
              <p
                className={clsx(
                  "text-xs mt-2",
                  msg.role === "user" ? "text-blue-200" : "text-gray-400"
                )}
              >
                {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </p>
            </div>
          </motion.div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
            <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-gray-50 border border-gray-100 rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-2">
              <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />
              <span className="text-sm text-gray-500">Analyzing your symptoms…</span>
            </div>
          </motion.div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Suggested queries */}
      {messages.length <= 1 && (
        <div className="flex flex-wrap gap-2 mt-3">
          {SUGGESTED_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => handleSend(q)}
              className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1.5 rounded-full border border-blue-200 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Input area */}
      <div className="mt-3 bg-white border border-gray-200 rounded-2xl shadow-sm flex items-end gap-2 p-2">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe your symptoms… (Press Enter to send)"
          rows={1}
          className="flex-1 resize-none bg-transparent px-3 py-2 text-sm text-gray-800 placeholder-gray-400 focus:outline-none max-h-32"
          style={{ minHeight: "40px" }}
        />
        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            onClick={handleVoice}
            title="Voice input"
            className={clsx(
              "p-2 rounded-xl transition-colors",
              isListening
                ? "bg-red-100 text-red-600 animate-pulse"
                : "text-gray-400 hover:text-blue-600 hover:bg-blue-50"
            )}
          >
            <Mic className="w-5 h-5" />
          </button>
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className="btn-primary !py-2 !px-4 flex items-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
