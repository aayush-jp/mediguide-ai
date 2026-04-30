import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import {
  Activity,
  AlertTriangle,
  Bot,
  Brain,
  FileText,
  Globe2,
  HeartPulse,
  History,
  LogOut,
  Menu,
  Mic,
  ShieldCheck,
  Stethoscope,
  Upload,
  UserPlus,
} from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";
const AuthContext = createContext(null);

function api(path, options = {}) {
  const token = localStorage.getItem("mediguide_token");
  return fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  }).then(async (response) => {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed");
    return data;
  });
}

function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("mediguide_user");
    return stored ? JSON.parse(stored) : null;
  });

  useEffect(() => {
    if (!localStorage.getItem("mediguide_token")) return;
    api("/api/auth/me").then(setUser).catch(() => logout());
  }, []);

  function saveAuth(auth) {
    localStorage.setItem("mediguide_token", auth.access_token);
    localStorage.setItem("mediguide_user", JSON.stringify(auth.user));
    setUser(auth.user);
  }

  function logout() {
    localStorage.removeItem("mediguide_token");
    localStorage.removeItem("mediguide_user");
    setUser(null);
  }

  const value = useMemo(() => ({ user, saveAuth, logout, isAuthed: Boolean(user) }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function useAuth() {
  return useContext(AuthContext);
}

function ProtectedRoute({ children }) {
  const { isAuthed } = useAuth();
  return isAuthed ? children : <Navigate to="/login" replace />;
}

function Landing() {
  const features = [
    ["Symptom Checker", "Follow-up questions and AI-guided risk review.", Activity],
    ["Disease Prediction", "ML-style predictions shown as educational probabilities.", Brain],
    ["Medical Chatbot", "Protected chatbot with safety-first medical guardrails.", Bot],
    ["OCR Analysis", "Upload reports and prescriptions for AI-assisted summaries.", FileText],
  ];

  return (
    <main>
      <nav className="topbar">
        <Link className="brand" to="/"><span><HeartPulse size={22} /></span>MediGuide AI</Link>
        <div className="nav-actions">
          <Link className="btn secondary" to="/login">Login</Link>
          <Link className="btn primary" to="/signup">Sign Up</Link>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-copy">
          <div className="pill"><ShieldCheck size={16} /> AI-assisted clinical support</div>
          <h1>MediGuide AI</h1>
          <p>
            A secure healthcare assistant for symptom analysis, disease prediction, report OCR,
            risk triage, health history, and doctor escalation guidance.
          </p>
          <div className="hero-actions">
            <Link className="btn primary large" to="/signup"><UserPlus size={18} /> Start Securely</Link>
            <Link className="btn secondary large" to="/login">Login</Link>
          </div>
          <div className="disclaimer">
            MediGuide AI provides AI-assisted health information only and is not a replacement for a licensed medical professional.
          </div>
        </div>
        <div className="hero-panel">
          <div className="metric-card teal"><span>Risk AI</span><strong>Low - Emergency</strong></div>
          <div className="metric-card blue"><span>Architecture</span><strong>Agent + MCP + Skills</strong></div>
          <div className="metric-card navy"><span>Security</span><strong>JWT protected tools</strong></div>
        </div>
      </section>

      <section className="preview-grid">
        {features.map(([title, desc, Icon]) => (
          <article className="preview-card" key={title}>
            <Icon />
            <h3>{title}</h3>
            <p>{desc}</p>
            <span>Login required</span>
          </article>
        ))}
      </section>
    </main>
  );
}

function AuthPage({ mode }) {
  const isSignup = mode === "signup";
  const navigate = useNavigate();
  const { saveAuth, isAuthed } = useAuth();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthed) navigate("/dashboard");
  }, [isAuthed, navigate]);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const auth = await api(`/api/auth/${isSignup ? "signup" : "login"}`, {
        method: "POST",
        body: JSON.stringify(isSignup ? form : { email: form.email, password: form.password }),
      });
      saveAuth(auth);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <Link className="brand" to="/"><span><HeartPulse size={22} /></span>MediGuide AI</Link>
      <form className="auth-card" onSubmit={submit}>
        <h1>{isSignup ? "Create your account" : "Welcome back"}</h1>
        <p>Authentication is required before accessing dashboard tools.</p>
        {isSignup && (
          <label>Name<input required minLength="2" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
        )}
        <label>Email<input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
        <label>Password<input required minLength="8" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
        {error && <div className="error">{error}</div>}
        <button className="btn primary full" disabled={loading}>{loading ? "Please wait..." : isSignup ? "Sign Up" : "Login"}</button>
        <Link to={isSignup ? "/login" : "/signup"}>{isSignup ? "Already have an account? Login" : "Need an account? Sign up"}</Link>
      </form>
    </main>
  );
}

function DashboardLayout() {
  const { user, logout } = useAuth();
  const [active, setActive] = useState("overview");
  const sections = [
    ["overview", "Dashboard", Menu],
    ["symptoms", "Symptom Checker", Activity],
    ["prediction", "Disease Prediction", Brain],
    ["chat", "Medical Chatbot", Bot],
    ["report", "Report OCR", Upload],
    ["history", "Health History", History],
    ["risk", "Risk Tracker", AlertTriangle],
    ["language", "Language + Voice", Globe2],
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/dashboard"><span><HeartPulse size={22} /></span>MediGuide AI</Link>
        <div className="user-box">Logged in as<strong>{user?.name}</strong></div>
        {sections.map(([key, label, Icon]) => (
          <button key={key} className={active === key ? "active" : ""} onClick={() => setActive(key)}>
            <Icon size={18} /> {label}
          </button>
        ))}
        <button onClick={logout}><LogOut size={18} /> Logout</button>
      </aside>
      <main className="dashboard">
        <div className="dash-header">
          <div>
            <p>Secure dashboard</p>
            <h1>{sections.find(([key]) => key === active)?.[1]}</h1>
          </div>
          <span className="secure-badge"><ShieldCheck size={16} /> Protected by JWT</span>
        </div>
        <ToolPanel active={active} />
        <div className="disclaimer">
          MediGuide AI provides AI-assisted health information only and is not a replacement for a licensed medical professional.
        </div>
      </main>
    </div>
  );
}

function ToolPanel({ active }) {
  if (active === "overview") return <Overview />;
  if (active === "symptoms") return <SymptomTool />;
  if (active === "prediction") return <PredictionTool />;
  if (active === "chat") return <ChatTool />;
  if (active === "report") return <ReportTool />;
  if (active === "history") return <HistoryTool />;
  if (active === "risk") return <RiskTool />;
  return <LanguageVoiceTool />;
}

function Overview() {
  const cards = [
    ["Symptom Checker", "Follow-up questions, risk levels, and safe next steps.", Activity],
    ["Disease Prediction", "ML prediction API with no final diagnosis claims.", Brain],
    ["Medical Chatbot", "Guardrailed assistant for health questions.", Bot],
    ["Medical Report OCR", "Validated uploads and report summarization.", FileText],
    ["Voice Input", "Speech-ready endpoint and browser voice support path.", Mic],
    ["Doctor Alerts", "Escalates only serious, unclear, persistent, or approval cases.", Stethoscope],
  ];
  return <div className="card-grid">{cards.map(([t, d, Icon]) => <article className="tool-card" key={t}><Icon /><h3>{t}</h3><p>{d}</p></article>)}</div>;
}

function ResultBox({ data }) {
  if (!data) return <div className="empty">No result yet. Submit the form to run the protected AI API.</div>;
  return <pre className="result">{JSON.stringify(data, null, 2)}</pre>;
}

function SymptomTool() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      setData(await api("/api/ai/symptom-analysis", {
        method: "POST",
        body: JSON.stringify({
          symptoms: form.get("symptoms").split(",").map((s) => s.trim()).filter(Boolean),
          age: Number(form.get("age")) || null,
          duration_days: Number(form.get("duration")) || null,
          severity: Number(form.get("severity")) || 4,
          language: form.get("language"),
        }),
      }));
    } catch (err) { setError(err.message); }
  }
  return <FormTool title="Symptom checker with follow-up questions" onSubmit={submit} error={error}>
    <input name="symptoms" placeholder="fever, cough, headache" required />
    <div className="row"><input name="age" placeholder="Age" /><input name="duration" placeholder="Duration days" /><input name="severity" placeholder="Severity 1-10" /></div>
    <select name="language"><option>English</option><option>Hindi</option><option>Tamil</option><option>Kannada</option><option>Telugu</option><option>Malayalam</option></select>
    <button className="btn primary">Analyze symptoms</button><ResultBox data={data} />
  </FormTool>;
}

function PredictionTool() {
  const [data, setData] = useState(null);
  async function submit(event) {
    event.preventDefault();
    const symptoms = new FormData(event.currentTarget).get("symptoms").split(",").map((s) => s.trim()).filter(Boolean);
    setData(await api("/api/ai/disease-prediction", { method: "POST", body: JSON.stringify({ symptoms }) }));
  }
  return <FormTool title="ML-based disease prediction" onSubmit={submit}><input name="symptoms" required placeholder="sore throat, fever" /><button className="btn primary">Predict</button><ResultBox data={data} /></FormTool>;
}

function ChatTool() {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    const message = form.get("message");
    event.currentTarget.reset();
    try {
      const result = await api("/api/ai/chat", { method: "POST", body: JSON.stringify({ message, language: form.get("language") || "English" }) });
      setMessages((prev) => [...prev, { message, result }]);
    } catch (err) { setError(err.message); }
  }
  return <FormTool title="Medical chatbot" onSubmit={submit} error={error}><textarea name="message" required placeholder="Ask a medical support question..." /><select name="language"><option>English</option><option>Hindi</option><option>Tamil</option></select><button className="btn primary">Send</button><ResultBox data={messages} /></FormTool>;
}

function ReportTool() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    setError("");
    const form = new FormData();
    form.append("file", event.currentTarget.file.files[0]);
    try { setData(await api("/api/ai/report-ocr", { method: "POST", body: form })); } catch (err) { setError(err.message); }
  }
  return <FormTool title="Medical report OCR analysis" onSubmit={submit} error={error}><input type="file" name="file" accept="image/png,image/jpeg,image/webp,application/pdf" required /><button className="btn primary">Upload and analyze</button><ResultBox data={data} /></FormTool>;
}

function HistoryTool() {
  const [items, setItems] = useState(null);
  const [message, setMessage] = useState("");
  async function load() { setItems(await api("/api/health-history")); }
  async function save() {
    await api("/api/health-history", { method: "POST", body: JSON.stringify({ title: "Demo symptom review", category: "Symptom Checker", risk_level: "Low", risk_score: 24, summary: "Saved secure health history entry." }) });
    setMessage("Saved sample history item.");
    load();
  }
  useEffect(() => { load().catch(() => setItems([])); }, []);
  return <section className="panel"><h2>Health history save/fetch</h2><p>{message || "Your history is empty until analyses are saved."}</p><button className="btn primary" onClick={save}>Save sample history</button><ResultBox data={items} /></section>;
}

function RiskTool() {
  const [data, setData] = useState(null);
  async function submit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setData(await api("/api/ai/risk-score", { method: "POST", body: JSON.stringify({ symptoms: form.get("symptoms").split(","), severity: Number(form.get("severity")), duration_days: Number(form.get("duration")), age: Number(form.get("age")) || null }) }));
  }
  return <FormTool title="Risk score tracker" onSubmit={submit}><input name="symptoms" placeholder="symptoms" required /><div className="row"><input name="severity" placeholder="Severity" required /><input name="duration" placeholder="Duration" required /><input name="age" placeholder="Age" /></div><button className="btn primary">Calculate risk</button><ResultBox data={data} /></FormTool>;
}

function LanguageVoiceTool() {
  const [data, setData] = useState(null);
  return <section className="panel"><h2>Multi-language support + voice input</h2><p>Frontend supports language selection. Backend exposes a protected voice transcription endpoint for Whisper/Web Speech/Hugging Face integration.</p><button className="btn primary" onClick={() => api("/api/ai/voice-transcription", { method: "POST" }).then(setData)}>Check voice API</button><ResultBox data={data} /></section>;
}

function FormTool({ title, onSubmit, error, children }) {
  return <section className="panel"><h2>{title}</h2><form className="tool-form" onSubmit={onSubmit}>{children}</form>{error && <div className="error">{error}</div>}</section>;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/signup" element={<AuthPage mode="signup" />} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App />);
