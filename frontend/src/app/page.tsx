import Link from "next/link";
import {
  Activity, MessageCircle, FileText, ArrowRight,
  Shield, Brain, Zap, Globe, AlertTriangle, CheckCircle,
} from "lucide-react";

const FEATURES = [
  {
    href: "/symptom-checker",
    icon: Activity,
    color: "blue",
    title: "Symptom Checker",
    description:
      "Enter your symptoms with age, duration, and severity. Get AI-assessed possible conditions, risk level, and what to do next.",
    badges: ["Possible conditions", "Risk meter", "Home care tips"],
  },
  {
    href: "/chat",
    icon: MessageCircle,
    color: "purple",
    title: "AI Medical Chat",
    description:
      "Have a natural conversation about your health. The AI asks follow-up questions, detects emergency signs, and guides you step by step.",
    badges: ["Multi-turn chat", "Voice input", "Emergency detection"],
  },
  {
    href: "/report",
    icon: FileText,
    color: "green",
    title: "Report Analysis",
    description:
      "Upload a photo of your blood test, urine test, or lab report. AI Vision extracts values, checks normal ranges, and explains everything clearly.",
    badges: ["Blood test", "Urine test", "Lab interpretation"],
  },
];

const COLOR_MAP: Record<string, { bg: string; light: string; text: string; border: string }> = {
  blue:   { bg: "bg-blue-600",   light: "bg-blue-50",   text: "text-blue-600",   border: "border-blue-100" },
  purple: { bg: "bg-purple-600", light: "bg-purple-50", text: "text-purple-600", border: "border-purple-100" },
  green:  { bg: "bg-green-600",  light: "bg-green-50",  text: "text-green-600",  border: "border-green-100" },
};

const RISK_LEVELS = [
  { label: "Low Risk",   color: "bg-green-100 text-green-800 border-green-200",  desc: "Home care · self-monitor" },
  { label: "Medium",     color: "bg-yellow-100 text-yellow-800 border-yellow-200", desc: "See doctor within 48 hrs" },
  { label: "High Risk",  color: "bg-orange-100 text-orange-800 border-orange-200", desc: "See doctor today" },
  { label: "Emergency",  color: "bg-red-100 text-red-800 border-red-200",        desc: "Call 911 immediately" },
];

const HIGHLIGHTS = [
  { icon: Brain,   title: "Claude AI Engine",      desc: "Powered by Anthropic's Claude — state-of-the-art medical reasoning." },
  { icon: Shield,  title: "Safety First",          desc: "Emergency red-flag detection. Never prescribes drugs or makes diagnoses." },
  { icon: Zap,     title: "MCP Agent Architecture", desc: "Medical tools exposed via Model Context Protocol for structured AI reasoning." },
  { icon: Globe,   title: "Multilingual Ready",     desc: "Architecture supports English, Hindi, Tamil, Kannada, Telugu, Malayalam." },
];

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-20">

      {/* Hero */}
      <section className="text-center space-y-6">
        <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200 rounded-full px-4 py-1.5 text-sm text-blue-700 font-medium">
          <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
          Clinical Support Assistant · Not a Doctor Replacement
        </div>
        <h1 className="text-4xl sm:text-5xl font-black text-gray-900 leading-tight">
          MediGuide <span className="text-blue-600">AI</span>
        </h1>
        <p className="text-xl text-gray-500 max-w-2xl mx-auto">
          Understand your symptoms · Interpret your lab reports · Know your next safe step.
          <br />Powered by Claude AI + MCP medical tools architecture.
        </p>

        <div className="flex flex-wrap justify-center gap-3">
          <Link href="/symptom-checker" className="btn-primary flex items-center gap-2 text-base px-6 py-3">
            <Activity className="w-5 h-5" />
            Check My Symptoms
          </Link>
          <Link href="/chat" className="btn-secondary flex items-center gap-2 text-base px-6 py-3">
            <MessageCircle className="w-5 h-5" />
            Chat with AI
          </Link>
        </div>

        {/* Emergency notice */}
        <div className="inline-flex items-center gap-2 bg-red-50 border border-red-200 rounded-xl px-4 py-2 text-sm text-red-700">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          Medical emergency? Call <strong className="ml-1">112</strong> (India) or <strong className="ml-1">911</strong> (US) immediately.
        </div>
      </section>

      {/* Risk level guide */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-6">Risk Assessment Output</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {RISK_LEVELS.map(({ label, color, desc }) => (
            <div key={label} className={`rounded-2xl border p-4 text-center ${color}`}>
              <p className="font-bold text-base mb-1">{label}</p>
              <p className="text-xs opacity-80">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Feature cards */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Core Modules</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {FEATURES.map(({ href, icon: Icon, color, title, description, badges }) => {
            const c = COLOR_MAP[color];
            return (
              <Link
                key={href}
                href={href}
                className="card p-6 hover:shadow-md transition-shadow group flex flex-col"
              >
                <div className={`w-12 h-12 ${c.light} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className={`w-6 h-6 ${c.text}`} />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
                <p className="text-sm text-gray-500 mb-4 flex-1">{description}</p>
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {badges.map((b) => (
                    <span key={b} className={`text-xs font-medium px-2 py-0.5 rounded-full ${c.light} ${c.text} border ${c.border}`}>
                      {b}
                    </span>
                  ))}
                </div>
                <div className={`flex items-center gap-1.5 text-sm font-semibold ${c.text} group-hover:gap-2.5 transition-all`}>
                  Open <ArrowRight className="w-4 h-4" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* How it works */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">How It Works</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { step: "1", title: "Enter Symptoms", desc: "Select symptoms and answer a few questions about duration, severity, and medical history." },
            { step: "2", title: "AI Analyzes", desc: "Claude AI uses MCP medical tools to check for emergencies, match conditions, and calculate risk." },
            { step: "3", title: "Risk Assessment", desc: "You get a color-coded risk meter: Low, Medium, High, or Emergency — with clear reasoning." },
            { step: "4", title: "Next Safe Step", desc: "Home care tips for low risk, doctor referral for medium/high, emergency services for critical." },
          ].map(({ step, title, desc }) => (
            <div key={step} className="card p-5 relative">
              <div className="w-9 h-9 bg-blue-600 text-white font-bold rounded-xl flex items-center justify-center text-sm mb-3">
                {step}
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
              <p className="text-sm text-gray-500">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture highlights */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Technology Stack</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {HIGHLIGHTS.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card p-5 flex items-start gap-4">
              <div className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <Icon className="w-5 h-5 text-slate-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-0.5">{title}</h3>
                <p className="text-sm text-gray-500">{desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Stack badges */}
        <div className="mt-6 flex flex-wrap gap-2 justify-center">
          {[
            "Next.js 15", "FastAPI", "Claude claude-sonnet-4-6", "MCP Protocol",
            "Anthropic Tool Use", "Claude Vision OCR", "Tailwind CSS", "Framer Motion",
          ].map((t) => (
            <span key={t} className="bg-slate-100 text-slate-700 text-xs font-medium px-3 py-1.5 rounded-full border border-slate-200">
              {t}
            </span>
          ))}
        </div>
      </section>

      {/* Safety statement */}
      <section className="bg-blue-600 rounded-3xl p-8 text-center text-white">
        <CheckCircle className="w-10 h-10 mx-auto mb-4 text-blue-200" />
        <h2 className="text-2xl font-bold mb-3">Built for Safety</h2>
        <p className="text-blue-100 max-w-2xl mx-auto text-base">
          MediGuide AI never prescribes medications, never makes a final diagnosis, and always
          escalates emergencies automatically. Every response ends with a safety disclaimer.
          It's designed to support — never replace — your healthcare provider.
        </p>
      </section>

    </div>
  );
}
