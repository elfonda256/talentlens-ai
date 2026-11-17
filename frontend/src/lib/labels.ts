import type { ComponentKey, ConfidenceLevel, Recommendation } from "@/lib/api";

/** Indonesian labels and colours for values that the API returns as codes. */

export const RECOMMENDATION_LABEL: Record<Recommendation, string> = {
  SHORTLIST: "Direkomendasikan",
  REVIEW: "Perlu ditinjau",
  REJECT: "Tidak lolos",
};

export const COMPONENT_LABEL: Record<ComponentKey, string> = {
  must_skills: "Keterampilan wajib",
  bonus_skills: "Keterampilan tambahan",
  experience: "Pengalaman relevan",
  education: "Pendidikan",
  semantic: "Kesesuaian isi CV",
};

/** Tailwind background class of each score component; the same colour everywhere it appears. */
export const COMPONENT_COLOR: Record<ComponentKey, string> = {
  must_skills: "bg-part-must",
  bonus_skills: "bg-part-bonus",
  experience: "bg-part-experience",
  education: "bg-part-education",
  semantic: "bg-part-semantic",
};

export const CONFIDENCE_LABEL: Record<ConfidenceLevel, string> = {
  high: "Tinggi",
  medium: "Sedang",
  low: "Rendah",
};

const FIELD_LABEL: Record<string, string> = {
  architecture: "Arsitektur",
  "interior design": "Desain interior",
  "civil engineering": "Teknik sipil",
  "urban planning": "Perencanaan kota",
  "product design": "Desain produk",
  "visual communication design": "Desain komunikasi visual",
  "computer science": "Ilmu komputer",
  accounting: "Akuntansi",
  management: "Manajemen",
};

/** "architecture, interior design" -> "Arsitektur, Desain interior" */
export function formatFields(fields: string[]): string {
  return fields.map((field) => FIELD_LABEL[field] ?? field).join(", ");
}

/** Replaces the redaction placeholders left in CV text with readable wording. */
export function readable(text: string): string {
  return text
    .replaceAll("[INSTITUSI]", "(nama kampus disamarkan)")
    .replaceAll("[NAMA]", "(nama disamarkan)")
    .replaceAll("[EMAIL]", "(email disamarkan)")
    .replaceAll("[TELEPON]", "(telepon disamarkan)");
}

/** 3.2 -> "3,2" (Indonesian decimal comma). */
export function formatNumber(value: number, digits = 1): string {
  return value.toFixed(digits).replace(".", ",");
}

export function formatYears(years: number): string {
  return `${formatNumber(years)} tahun`;
}
