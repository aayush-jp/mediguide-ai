"use client";

import { AlertTriangle, Phone } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface EmergencyBannerProps {
  show: boolean;
  triggers?: string[];
}

export default function EmergencyBanner({ show, triggers }: EmergencyBannerProps) {
  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="bg-red-600 text-white rounded-2xl p-5 shadow-lg border border-red-700"
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-white animate-pulse" />
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-lg mb-1">⚠️ Emergency — Seek Immediate Care</h3>
              <p className="text-red-100 mb-3">
                The symptoms you described may indicate a medical emergency.
                Please call emergency services or go to the nearest emergency room immediately.
              </p>
              {triggers && triggers.length > 0 && (
                <div className="bg-white/10 rounded-xl p-3 mb-3">
                  <p className="text-sm font-medium mb-1 text-red-100">Warning signs detected:</p>
                  <ul className="list-disc list-inside text-sm text-white space-y-0.5">
                    {triggers.slice(0, 4).map((t, i) => (
                      <li key={i} className="capitalize">{t}</li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="flex flex-wrap gap-3">
                <a
                  href="tel:112"
                  className="flex items-center gap-2 bg-white text-red-600 font-bold px-4 py-2 rounded-xl hover:bg-red-50 transition-colors"
                >
                  <Phone className="w-4 h-4" />
                  Call 112 (India)
                </a>
                <a
                  href="tel:911"
                  className="flex items-center gap-2 bg-white/10 text-white font-bold px-4 py-2 rounded-xl hover:bg-white/20 transition-colors border border-white/30"
                >
                  <Phone className="w-4 h-4" />
                  Call 911 (US)
                </a>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
