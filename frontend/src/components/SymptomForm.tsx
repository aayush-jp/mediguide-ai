"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import {
  Thermometer, Clock, User, Activity, ChevronRight, ChevronLeft,
  Loader2, AlertTriangle,
} from "lucide-react";
import { clsx } from "clsx";
import type { SymptomFormData, SymptomCheckResult } from "@/types";
import { checkSymptoms } from "@/lib/api";
import RiskMeter from "./RiskMeter";
import ConditionCard from "./ConditionCard";
import EmergencyBanner from "./EmergencyBanner";

const COMMON_SYMPTOMS = [
  "Fever", "Headache", "Cough", "Sore throat", "Body aches",
  "Fatigue", "Runny nose", "Nausea", "Vomiting", "Diarrhea",
  "Stomach pain", "Chest pain", "Shortness of breath", "Dizziness",
  "Rash", "Joint pain", "Back pain", "Loss of appetite", "Chills",
  "Night sweats", "Swollen glands", "Eye redness", "Ear pain",
];

const COMMON_CONDITIONS = [
  "Diabetes", "Hypertension", "Asthma", "Heart disease", "COPD",
  "Kidney disease", "Liver disease", "HIV/AIDS", "Cancer", "Pregnancy",
  "Thyroid disorder", "Lupus",
];

const STEPS = [
  { id: 1, title: "Symptoms",        icon: Activity },
  { id: 2, title: "Details",         icon: Thermometer },
  { id: 3, title: "Profile",         icon: User },
  { id: 4, title: "Medical History", icon: Clock },
];

export default function SymptomForm() {
  const [step, setStep] = useState(1);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [selectedConditions, setSelectedConditions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SymptomCheckResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors }, watch, getValues } = useForm<SymptomFormData>({
    defaultValues: { symptoms: [], customSymptoms: "", existing_conditions: [], allergies: "", medicines: "" },
  });

  const toggleSymptom = (s: string) => {
    setSelectedSymptoms((prev) =>
      prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]
    );
  };

  const toggleCondition = (c: string) => {
    setSelectedConditions((prev) =>
      prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
    );
  };

  const onSubmit = async (data: SymptomFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await checkSymptoms({
        ...data,
        symptoms: selectedSymptoms,
        existing_conditions: selectedConditions,
      });
      setResult(result);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "An error occurred";
      setError("Failed to analyze symptoms. Please check your connection and try again. " + msg);
    } finally {
      setIsLoading(false);
    }
  };

  if (result) {
    return (
      <div className="space-y-6 animate-fade-in">
        <EmergencyBanner show={result.is_emergency} triggers={result.emergency_triggers} />

        <RiskMeter
          level={result.risk_level}
          score={result.risk_score}
          color={result.risk_color}
          action={result.referral?.message}
        />

        {/* Referral box */}
        {result.referral && (
          <div className={clsx(
            "card p-5",
            result.is_emergency ? "border-red-200 bg-red-50" :
            result.risk_level === "HIGH" ? "border-orange-200 bg-orange-50" :
            result.risk_level === "MEDIUM" ? "border-yellow-200 bg-yellow-50" :
            "border-green-200 bg-green-50"
          )}>
            <h3 className="font-semibold text-gray-900 mb-1">
              Recommended Action — {result.referral.urgency}
            </h3>
            <p className="text-sm text-gray-700">{result.referral.message}</p>
            {result.referral.referral_type !== "None required currently" && (
              <p className="text-xs text-gray-500 mt-1">
                Facility type: <strong>{result.referral.referral_type}</strong>
              </p>
            )}
          </div>
        )}

        {/* Possible conditions */}
        {result.possible_conditions.length > 0 && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-600" />
              Possible Conditions
              <span className="text-xs text-gray-400 font-normal ml-auto">
                Ordered by symptom match
              </span>
            </h3>
            <div className="space-y-3">
              {result.possible_conditions.map((condition, i) => (
                <ConditionCard key={condition.key} condition={condition} rank={i} />
              ))}
            </div>
          </div>
        )}

        {/* AI Narrative */}
        {result.narrative && (
          <div className="card p-5">
            <h3 className="font-semibold text-gray-900 mb-3">Detailed Assessment</h3>
            <div className="prose-medical text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {result.narrative}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="disclaimer-box">
          <p className="font-semibold mb-1">⚕️ Important Disclaimer</p>
          <p>{result.disclaimer}</p>
        </div>

        <button onClick={() => { setResult(null); setStep(1); }} className="btn-secondary w-full">
          Start New Assessment
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Step indicator */}
      <div className="flex items-center justify-between">
        {STEPS.map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={s.id} className="flex items-center">
              <div className={clsx(
                "flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                step === s.id ? "bg-blue-600 text-white" :
                step > s.id ? "bg-blue-100 text-blue-700" :
                "bg-gray-100 text-gray-400"
              )}>
                <Icon className="w-4 h-4" />
                <span className="hidden sm:inline">{s.title}</span>
              </div>
              {i < STEPS.length - 1 && (
                <div className={clsx("h-0.5 w-8 mx-1", step > s.id ? "bg-blue-300" : "bg-gray-200")} />
              )}
            </div>
          );
        })}
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <AnimatePresence mode="wait">
          {/* Step 1: Symptoms */}
          {step === 1 && (
            <motion.div key="step1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <div className="card p-5 space-y-4">
                <h2 className="text-lg font-semibold text-gray-900">What symptoms are you experiencing?</h2>
                <p className="text-sm text-gray-500">Select all that apply, then add any others in the field below.</p>

                <div className="flex flex-wrap gap-2">
                  {COMMON_SYMPTOMS.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => toggleSymptom(s.toLowerCase())}
                      className={clsx(
                        "px-3 py-1.5 rounded-xl text-sm font-medium border transition-all",
                        selectedSymptoms.includes(s.toLowerCase())
                          ? "bg-blue-600 text-white border-blue-600 shadow-sm"
                          : "bg-white text-gray-700 border-gray-200 hover:border-blue-300 hover:text-blue-700"
                      )}
                    >
                      {s}
                    </button>
                  ))}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">
                    Other symptoms (comma-separated)
                  </label>
                  <input
                    {...register("customSymptoms")}
                    placeholder="e.g., loss of smell, eye pain, swollen feet"
                    className="input-field"
                  />
                </div>

                {selectedSymptoms.length === 0 && (
                  <p className="text-xs text-amber-600 flex items-center gap-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    Please select at least one symptom.
                  </p>
                )}
              </div>

              <div className="mt-4 flex justify-end">
                <button
                  type="button"
                  onClick={() => selectedSymptoms.length > 0 && setStep(2)}
                  disabled={selectedSymptoms.length === 0}
                  className="btn-primary flex items-center gap-2"
                >
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}

          {/* Step 2: Details */}
          {step === 2 && (
            <motion.div key="step2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <div className="card p-5 space-y-5">
                <h2 className="text-lg font-semibold text-gray-900">Tell us more about your symptoms</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">
                      How long? (days)
                    </label>
                    <input
                      type="number"
                      {...register("duration_days", { min: 0, max: 365 })}
                      placeholder="e.g., 2"
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">
                      Severity (1 = mild, 10 = severe)
                    </label>
                    <input
                      type="number"
                      {...register("severity", { min: 1, max: 10 })}
                      placeholder="1–10"
                      className="input-field"
                    />
                  </div>

                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">
                      Body temperature (°F) — leave blank if not measured
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      {...register("temperature_f", { min: 95, max: 110 })}
                      placeholder="e.g., 101.2"
                      className="input-field"
                    />
                  </div>
                </div>

                {/* Selected symptoms summary */}
                <div className="bg-blue-50 rounded-xl p-3">
                  <p className="text-xs font-semibold text-blue-700 mb-1.5">Selected symptoms:</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedSymptoms.map((s) => (
                      <span key={s} className="text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full capitalize">{s}</span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-4 flex gap-3 justify-between">
                <button type="button" onClick={() => setStep(1)} className="btn-secondary flex items-center gap-2">
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button type="button" onClick={() => setStep(3)} className="btn-primary flex items-center gap-2">
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}

          {/* Step 3: Profile */}
          {step === 3 && (
            <motion.div key="step3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <div className="card p-5 space-y-4">
                <h2 className="text-lg font-semibold text-gray-900">Personal information</h2>
                <p className="text-sm text-gray-500">Helps us give a more accurate risk assessment. All optional.</p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">Age</label>
                    <input type="number" {...register("age", { min: 0, max: 120 })} placeholder="e.g., 28" className="input-field" />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">Gender</label>
                    <select {...register("gender")} className="input-field">
                      <option value="">Prefer not to say</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="mt-4 flex gap-3 justify-between">
                <button type="button" onClick={() => setStep(2)} className="btn-secondary flex items-center gap-2">
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button type="button" onClick={() => setStep(4)} className="btn-primary flex items-center gap-2">
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}

          {/* Step 4: Medical History + Submit */}
          {step === 4 && (
            <motion.div key="step4" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <div className="card p-5 space-y-5">
                <h2 className="text-lg font-semibold text-gray-900">Medical history</h2>
                <p className="text-sm text-gray-500">Important for accurate risk assessment. All optional.</p>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Existing medical conditions
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {COMMON_CONDITIONS.map((c) => (
                      <button
                        key={c}
                        type="button"
                        onClick={() => toggleCondition(c)}
                        className={clsx(
                          "px-3 py-1.5 rounded-xl text-sm font-medium border transition-all",
                          selectedConditions.includes(c)
                            ? "bg-orange-100 text-orange-800 border-orange-300"
                            : "bg-white text-gray-700 border-gray-200 hover:border-orange-300"
                        )}
                      >
                        {c}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">
                    Allergies (comma-separated)
                  </label>
                  <input {...register("allergies")} placeholder="e.g., penicillin, peanuts, sulfa drugs" className="input-field" />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">
                    Current medications (comma-separated)
                  </label>
                  <input {...register("medicines")} placeholder="e.g., metformin, lisinopril, atorvastatin" className="input-field" />
                </div>

                <div className="disclaimer-box">
                  <p className="font-semibold mb-1">⚕️ Before we analyze</p>
                  <p>
                    This assessment is for informational purposes only. It is not a medical diagnosis.
                    Always consult a qualified healthcare professional. If you have an emergency, call 112 or 911.
                  </p>
                </div>
              </div>

              {error && (
                <div className="mt-4 bg-red-50 border border-red-200 rounded-xl p-3 text-sm text-red-700">
                  {error}
                </div>
              )}

              <div className="mt-4 flex gap-3 justify-between">
                <button type="button" onClick={() => setStep(3)} className="btn-secondary flex items-center gap-2">
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button type="submit" disabled={isLoading} className="btn-primary flex items-center gap-2 min-w-[160px] justify-center">
                  {isLoading ? (
                    <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing…</>
                  ) : (
                    <><Activity className="w-4 h-4" /> Analyze Symptoms</>
                  )}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </form>
    </div>
  );
}
