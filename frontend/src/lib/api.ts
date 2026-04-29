import axios from "axios";
import type {
  SymptomFormData,
  SymptomCheckResult,
  ReportAnalysisResult,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
});

// ---------------------------------------------------------------------------
// Symptom Checker
// ---------------------------------------------------------------------------
export async function checkSymptoms(
  formData: SymptomFormData
): Promise<SymptomCheckResult> {
  const allSymptoms = [
    ...formData.symptoms,
    ...formData.customSymptoms
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean),
  ];

  const allConditions = formData.existing_conditions.filter(Boolean);

  const payload = {
    symptoms: allSymptoms,
    age: formData.age || undefined,
    gender: formData.gender || undefined,
    duration_days: formData.duration_days || undefined,
    severity: formData.severity || undefined,
    temperature_f: formData.temperature_f || undefined,
    existing_conditions: allConditions.length ? allConditions : undefined,
    allergies: formData.allergies
      ? formData.allergies.split(",").map((s) => s.trim()).filter(Boolean)
      : undefined,
    medicines: formData.medicines
      ? formData.medicines.split(",").map((s) => s.trim()).filter(Boolean)
      : undefined,
  };

  const { data } = await api.post<SymptomCheckResult>("/api/v1/symptom-check", payload);
  return data;
}

// ---------------------------------------------------------------------------
// Medical Chatbot
// ---------------------------------------------------------------------------
export async function sendChatMessage(
  message: string,
  history: Array<{ role: string; content: string }>
): Promise<{ response: string; is_emergency: boolean }> {
  const { data } = await api.post("/api/v1/chat", { message, history });
  return data;
}

// ---------------------------------------------------------------------------
// Report Analysis
// ---------------------------------------------------------------------------
export async function analyzeReport(
  file: File,
  gender?: string
): Promise<ReportAnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);
  if (gender) formData.append("gender", gender);

  const { data } = await api.post<ReportAnalysisResult>(
    "/api/v1/report-analyze",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
}
