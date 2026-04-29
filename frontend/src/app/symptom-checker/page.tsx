import SymptomForm from "@/components/SymptomForm";
import { Activity, Info } from "lucide-react";

export const metadata = {
  title: "Symptom Checker — MediGuide AI",
  description: "Enter your symptoms and get an AI-powered health assessment with risk level and next steps.",
};

export default function SymptomCheckerPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-600 rounded-2xl mb-4">
          <Activity className="w-7 h-7 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Symptom Checker</h1>
        <p className="text-gray-500 max-w-lg mx-auto">
          Describe your symptoms and receive an AI-assisted risk assessment with possible conditions
          and recommended next steps.
        </p>
      </div>

      {/* Info banner */}
      <div className="flex items-start gap-3 bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 text-sm text-blue-800">
        <Info className="w-5 h-5 mt-0.5 flex-shrink-0 text-blue-600" />
        <p>
          <strong>This tool does not diagnose.</strong> It suggests possible conditions and recommends whether to
          monitor at home, see a doctor, or seek emergency care. For emergencies, call 112 or 911 immediately.
        </p>
      </div>

      <SymptomForm />
    </div>
  );
}
