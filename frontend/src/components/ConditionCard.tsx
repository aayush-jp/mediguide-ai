"use client";

import { ChevronDown, ChevronUp, Clock, AlertCircle, Heart } from "lucide-react";
import { useState } from "react";
import type { PossibleCondition } from "@/types";
import { clsx } from "clsx";

interface ConditionCardProps {
  condition: PossibleCondition;
  rank: number;
}

const RISK_STYLES: Record<string, string> = {
  LOW:       "bg-green-100 text-green-800",
  MEDIUM:    "bg-yellow-100 text-yellow-800",
  HIGH:      "bg-orange-100 text-orange-800",
  EMERGENCY: "bg-red-100 text-red-800",
};

export default function ConditionCard({ condition, rank }: ConditionCardProps) {
  const [expanded, setExpanded] = useState(rank === 0);

  const confidenceColor =
    condition.confidence >= 70
      ? "bg-green-500"
      : condition.confidence >= 40
      ? "bg-yellow-400"
      : "bg-gray-300";

  return (
    <div className="card overflow-hidden animate-slide-up">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 p-4 text-left hover:bg-gray-50 transition-colors"
      >
        {/* Rank badge */}
        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white text-sm font-bold rounded-lg flex items-center justify-center">
          {rank + 1}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-gray-900">{condition.name}</span>
            <span className={clsx("text-xs font-semibold px-2 py-0.5 rounded-full", RISK_STYLES[condition.risk_level] ?? RISK_STYLES.LOW)}>
              {condition.risk_level}
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-0.5 truncate">{condition.description}</p>
        </div>

        {/* Confidence bar */}
        <div className="flex-shrink-0 flex flex-col items-end gap-1 min-w-[80px]">
          <span className="text-xs font-semibold text-gray-500">{condition.confidence}% match</span>
          <div className="w-20 h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div
              className={clsx("h-full rounded-full transition-all", confidenceColor)}
              style={{ width: `${condition.confidence}%` }}
            />
          </div>
        </div>

        {expanded ? (
          <ChevronUp className="w-4 h-4 text-gray-400 flex-shrink-0" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-400 flex-shrink-0" />
        )}
      </button>

      {expanded && (
        <div className="border-t border-gray-100 px-4 pb-4 pt-3 space-y-3">
          {/* Duration */}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Clock className="w-4 h-4 text-gray-400" />
            <span><strong>Typical duration:</strong> {condition.typical_duration}</span>
          </div>

          {/* Home care */}
          {condition.home_care.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Heart className="w-4 h-4 text-green-500" />
                <span className="text-sm font-semibold text-gray-700">Home Care Tips</span>
              </div>
              <ul className="space-y-1">
                {condition.home_care.map((tip, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                    <span className="text-green-500 mt-0.5">•</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* When to see doctor */}
          {condition.when_to_see_doctor.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-4 h-4 text-orange-500" />
                <span className="text-sm font-semibold text-gray-700">When to See a Doctor</span>
              </div>
              <ul className="space-y-1">
                {condition.when_to_see_doctor.slice(0, 4).map((sign, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                    <span className="text-orange-400 mt-0.5">→</span>
                    {sign}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <p className="text-xs text-gray-400 italic">
            This is general information, not a diagnosis. Consult a healthcare professional.
          </p>
        </div>
      )}
    </div>
  );
}
