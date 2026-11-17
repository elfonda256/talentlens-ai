import type { Recommendation, ScoreComponent } from "@/lib/api";

/** Indonesian labels for values that the API returns as codes. */

export const RECOMMENDATION_LABEL: Record<Recommendation, string> = {
  SHORTLIST: "Lolos",
  REVIEW: "Perlu ditinjau",
  REJECT: "Tidak lolos",
};

export const COMPONENT_LABEL: Record<ScoreComponent, string> = {
  skills: "Keterampilan",
  experience: "Pengalaman relevan",
  semantic: "Kesesuaian isi CV dengan lowongan",
  education: "Pendidikan",
};

export const COMPONENT_ORDER: ScoreComponent[] = ["skills", "experience", "semantic", "education"];

export const EMBEDDING_LABEL: Record<string, string> = {
  "multilingual-e5-small": "multilingual-e5-small (model lokal)",
  tfidf: "TF-IDF (cadangan, tanpa model)",
};

export function formatYears(months: number): string {
  return `${(months / 12).toFixed(1)} tahun`;
}
