"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload, FileImage, Loader2, CheckCircle, AlertCircle,
  TrendingUp, TrendingDown, Minus,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { clsx } from "clsx";
import type { ReportAnalysisResult, LabValue } from "@/types";
import { analyzeReport } from "@/lib/api";

function LabValueRow({ item }: { item: LabValue }) {
  const status = item.status;
  return (
    <div className={clsx(
      "flex items-center gap-3 p-3 rounded-xl border",
      status === "NORMAL" ? "bg-green-50 border-green-200" :
      status === "LOW"    ? "bg-blue-50 border-blue-200" :
      status === "HIGH"   ? "bg-red-50 border-red-200" :
      "bg-gray-50 border-gray-200"
    )}>
      <div className={clsx(
        "flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center",
        status === "NORMAL" ? "bg-green-100" :
        status === "LOW"    ? "bg-blue-100" :
        status === "HIGH"   ? "bg-red-100" :
        "bg-gray-100"
      )}>
        {status === "NORMAL" ? <Minus className="w-4 h-4 text-green-600" /> :
         status === "LOW"    ? <TrendingDown className="w-4 h-4 text-blue-600" /> :
         status === "HIGH"   ? <TrendingUp className="w-4 h-4 text-red-600" /> :
         <AlertCircle className="w-4 h-4 text-gray-500" />}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-semibold text-gray-900 capitalize">
            {item.test.replace(/_/g, " ")}
          </span>
          <span className={clsx(
            "text-xs font-bold px-2 py-0.5 rounded-full",
            status === "NORMAL" ? "bg-green-100 text-green-700" :
            status === "LOW"    ? "bg-blue-100 text-blue-700" :
            status === "HIGH"   ? "bg-red-100 text-red-700" :
            "bg-gray-100 text-gray-600"
          )}>
            {status}
          </span>
        </div>
        <div className="text-xs text-gray-500 mt-0.5">
          <strong>Value:</strong> {item.value} {item.unit || ""}
          {item.normal_range && <> · <strong>Normal:</strong> {item.normal_range}</>}
        </div>
        {item.severity && item.severity !== "none" && (
          <p className="text-xs text-gray-600 mt-0.5 italic">Severity: {item.severity}</p>
        )}
      </div>
    </div>
  );
}

export default function ReportUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [gender, setGender] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ReportAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const f = acceptedFiles[0];
    if (!f) return;
    setFile(f);
    setResult(null);
    setError(null);
    const url = URL.createObjectURL(f);
    setPreview(url);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [".jpg", ".jpeg", ".png", ".webp"] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
  });

  const handleAnalyze = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);
    try {
      const res = await analyzeReport(file, gender || undefined);
      setResult(res);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Unknown error";
      setError("Failed to analyze report. " + msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={clsx(
          "border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200",
          isDragActive
            ? "border-blue-500 bg-blue-50"
            : file
            ? "border-green-400 bg-green-50"
            : "border-gray-300 hover:border-blue-400 hover:bg-blue-50/30 bg-white"
        )}
      >
        <input {...getInputProps()} />
        {file ? (
          <div className="space-y-2">
            <CheckCircle className="w-10 h-10 text-green-500 mx-auto" />
            <p className="font-semibold text-green-700">{file.name}</p>
            <p className="text-sm text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB · Click to change</p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto">
              <Upload className="w-7 h-7 text-blue-500" />
            </div>
            <div>
              <p className="font-semibold text-gray-700">
                {isDragActive ? "Drop your report here" : "Drag & drop your report"}
              </p>
              <p className="text-sm text-gray-400 mt-1">or click to browse</p>
            </div>
            <div className="flex flex-wrap justify-center gap-2 text-xs text-gray-400">
              {["Blood Test", "Urine Test", "Prescription", "Discharge Summary"].map((t) => (
                <span key={t} className="bg-gray-100 px-2 py-1 rounded-full">{t}</span>
              ))}
            </div>
            <p className="text-xs text-gray-400">Supports JPEG, PNG, WebP · Max 10 MB</p>
          </div>
        )}
      </div>

      {/* Image preview */}
      {preview && (
        <div className="card p-3">
          <div className="flex items-center gap-2 mb-2">
            <FileImage className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-medium text-gray-700">Report Preview</span>
          </div>
          <img src={preview} alt="Report preview" className="w-full max-h-64 object-contain rounded-xl bg-gray-50" />
        </div>
      )}

      {/* Gender selector */}
      {file && !result && (
        <div className="card p-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Patient gender <span className="text-gray-400 font-normal">(optional — for accurate ranges)</span>
          </label>
          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            className="input-field"
          >
            <option value="">Not specified</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-red-500" />
          {error}
        </div>
      )}

      {/* Analyze button */}
      {file && !result && (
        <button
          onClick={handleAnalyze}
          disabled={isLoading}
          className="btn-primary w-full flex items-center justify-center gap-2 py-3"
        >
          {isLoading ? (
            <><Loader2 className="w-5 h-5 animate-spin" /> Analyzing with AI Vision…</>
          ) : (
            <><FileImage className="w-5 h-5" /> Analyze Report</>
          )}
        </button>
      )}

      {/* Results */}
      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
            {/* Report type badge */}
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="font-semibold text-gray-900">Analysis Complete</span>
              <span className="ml-auto text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                {result.report_type}
              </span>
            </div>

            {/* Lab values */}
            {result.interpreted_values.length > 0 && (
              <div className="card p-5 space-y-3">
                <h3 className="font-semibold text-gray-900">Interpreted Values</h3>
                {result.interpreted_values.map((item, i) => (
                  <LabValueRow key={i} item={item} />
                ))}
              </div>
            )}

            {/* Narrative */}
            {result.narrative && (
              <div className="card p-5">
                <h3 className="font-semibold text-gray-900 mb-3">AI Summary</h3>
                <div className="prose-medical text-sm text-gray-700 leading-relaxed">
                  <ReactMarkdown>{result.narrative}</ReactMarkdown>
                </div>
              </div>
            )}

            <div className="disclaimer-box">
              <p className="font-semibold mb-1">⚕️ Disclaimer</p>
              <p>
                This report analysis is for general informational purposes only. Interpretation of
                medical test results requires clinical context. Always consult your doctor or
                pathologist for professional guidance.
              </p>
            </div>

            <button
              onClick={() => { setResult(null); setFile(null); setPreview(null); }}
              className="btn-secondary w-full"
            >
              Analyze Another Report
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
