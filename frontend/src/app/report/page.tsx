import ReportUpload from "@/components/ReportUpload";
import { FileText, Info } from "lucide-react";

export const metadata = {
  title: "Health Report Analysis — MediGuide AI",
  description: "Upload your blood test, urine test, or lab report for AI-powered interpretation.",
};

export default function ReportPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-600 rounded-2xl mb-4">
          <FileText className="w-7 h-7 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Health Report Analysis</h1>
        <p className="text-gray-500 max-w-lg mx-auto">
          Upload a photo or image of your medical report. Our AI will extract the values,
          compare them to normal ranges, and explain what they mean in plain language.
        </p>
      </div>

      {/* Supported types */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: "Blood Test", emoji: "🩸" },
          { label: "Urine Test", emoji: "🧪" },
          { label: "Prescription", emoji: "💊" },
          { label: "Discharge Summary", emoji: "📋" },
        ].map(({ label, emoji }) => (
          <div key={label} className="card p-3 text-center">
            <div className="text-2xl mb-1">{emoji}</div>
            <p className="text-xs font-medium text-gray-600">{label}</p>
          </div>
        ))}
      </div>

      {/* Info banner */}
      <div className="flex items-start gap-3 bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 text-sm text-blue-800">
        <Info className="w-5 h-5 mt-0.5 flex-shrink-0 text-blue-600" />
        <p>
          <strong>How it works:</strong> Claude Vision AI reads your report image, extracts all test values,
          compares them to standard reference ranges, and generates a plain-language explanation.
          No data is stored.
        </p>
      </div>

      <ReportUpload />
    </div>
  );
}
