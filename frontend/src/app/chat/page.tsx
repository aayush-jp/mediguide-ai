import ChatInterface from "@/components/ChatInterface";
import { MessageCircle, Shield } from "lucide-react";

export const metadata = {
  title: "AI Medical Chat — MediGuide AI",
  description: "Chat with our AI clinical support assistant about your symptoms.",
};

export default function ChatPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
          <MessageCircle className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-gray-900">AI Medical Chat</h1>
          <p className="text-sm text-gray-500">Describe your symptoms naturally — I'll ask follow-up questions</p>
        </div>
        <div className="ml-auto flex items-center gap-1.5 text-xs text-green-700 bg-green-50 border border-green-200 rounded-full px-3 py-1">
          <Shield className="w-3.5 h-3.5" />
          Safe & Private
        </div>
      </div>

      <ChatInterface />
    </div>
  );
}
