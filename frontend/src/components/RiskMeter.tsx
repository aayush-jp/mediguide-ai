"use client";

import { motion } from "framer-motion";
import type { RiskLevel, RiskColor } from "@/types";

interface RiskMeterProps {
  level: RiskLevel;
  score: number;
  color: RiskColor;
  action?: string;
}

const RISK_CONFIG: Record<
  RiskLevel,
  { label: string; bg: string; text: string; bar: string; icon: string; description: string }
> = {
  LOW: {
    label: "Low Risk",
    bg: "bg-green-50 border-green-200",
    text: "text-green-800",
    bar: "bg-green-500",
    icon: "✅",
    description: "Your symptoms appear mild. Home care is likely appropriate.",
  },
  MEDIUM: {
    label: "Medium Risk",
    bg: "bg-yellow-50 border-yellow-200",
    text: "text-yellow-800",
    bar: "bg-yellow-400",
    icon: "⚠️",
    description: "Some symptoms warrant attention. Consider seeing a doctor soon.",
  },
  HIGH: {
    label: "High Risk",
    bg: "bg-orange-50 border-orange-200",
    text: "text-orange-800",
    bar: "bg-orange-500",
    icon: "🔶",
    description: "Your symptoms are concerning. Medical attention is recommended today.",
  },
  EMERGENCY: {
    label: "Emergency",
    bg: "bg-red-50 border-red-300",
    text: "text-red-800",
    bar: "bg-red-600",
    icon: "🚨",
    description: "Potential emergency. Call 911 or go to the ER immediately.",
  },
  UNKNOWN: {
    label: "Assessing…",
    bg: "bg-gray-50 border-gray-200",
    text: "text-gray-700",
    bar: "bg-gray-400",
    icon: "⏳",
    description: "Gathering information to assess risk level.",
  },
};

export default function RiskMeter({ level, score, color: _color, action }: RiskMeterProps) {
  const cfg = RISK_CONFIG[level] ?? RISK_CONFIG.UNKNOWN;

  return (
    <div className={`rounded-2xl border p-5 ${cfg.bg}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{cfg.icon}</span>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">Risk Level</p>
            <p className={`text-xl font-bold ${cfg.text}`}>{cfg.label}</p>
          </div>
        </div>
        <div className={`text-3xl font-black ${cfg.text}`}>{score}%</div>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-white/60 rounded-full h-3 mb-3 overflow-hidden">
        <motion.div
          className={`h-3 rounded-full ${cfg.bar}`}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </div>

      {/* Scale labels */}
      <div className="flex justify-between text-xs text-gray-400 mb-3">
        <span>Low</span>
        <span>Medium</span>
        <span>High</span>
        <span>Emergency</span>
      </div>

      <p className={`text-sm font-medium ${cfg.text}`}>{cfg.description}</p>

      {action && (
        <div className="mt-3 bg-white/70 rounded-xl p-3 text-sm text-gray-700 border border-white">
          <span className="font-semibold">Next step: </span>{action}
        </div>
      )}
    </div>
  );
}
