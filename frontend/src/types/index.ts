export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "EMERGENCY" | "UNKNOWN";
export type RiskColor = "green" | "yellow" | "orange" | "red" | "gray";

export interface PossibleCondition {
  key: string;
  name: string;
  confidence: number;
  risk_level: RiskLevel;
  description: string;
  when_to_see_doctor: string[];
  home_care: string[];
  typical_duration: string;
}

export interface ReferralInfo {
  referral_needed: boolean;
  urgency: string;
  message: string;
  referral_type: string;
}

export interface SymptomCheckResult {
  narrative: string;
  risk_level: RiskLevel;
  risk_score: number;
  risk_color: RiskColor;
  is_emergency: boolean;
  emergency_triggers: string[];
  possible_conditions: PossibleCondition[];
  referral: ReferralInfo;
  disclaimer: string;
}

export interface SymptomFormData {
  symptoms: string[];
  customSymptoms: string;
  age?: number;
  gender?: string;
  duration_days?: number;
  severity?: number;
  temperature_f?: number;
  existing_conditions: string[];
  allergies: string;
  medicines: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  is_emergency?: boolean;
  timestamp: Date;
}

export interface LabValue {
  test: string;
  value: number;
  status: "NORMAL" | "LOW" | "HIGH" | "unknown";
  severity?: string;
  normal_range?: string;
  unit?: string;
  interpretation?: string;
}

export interface ReportAnalysisResult {
  narrative: string;
  interpreted_values: LabValue[];
  report_type: string;
}
