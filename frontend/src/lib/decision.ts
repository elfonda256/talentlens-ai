import type { Recommendation, ScreeningResult } from "@/lib/api";
import { formatNumber } from "@/lib/labels";

/**
 * The decision zones of the backend rule (`explanation.decide`, SHORTLIST_THRESHOLD and
 * REJECT_THRESHOLD, defaults not overridden on staging). The decision always comes from the
 * backend; these values are only used to explain it.
 */
export const THRESHOLDS = { shortlist: 70, reject: 45 } as const;

export type DecisionCheck = {
  passed: boolean;
  label: string;
  details: string[];
};

type DocumentRead = { method: string; confidence: number };

/** Backend notes use a decimal point ("0.3 tahun"); the interface uses a comma. */
const readable = (text: string) => text.replace(/(\d)\.(\d)/g, "$1,$2");

/** The rule's checks, in the order the backend applies them, for one candidate. */
export function decisionChecks(
  result: ScreeningResult,
  document: DocumentRead,
): DecisionCheck[] {
  const score = formatNumber(result.score);
  const checks: DecisionCheck[] = [
    result.unassessed.length === 0
      ? {
          passed: true,
          label: "Semua bagian CV terbaca dan dinilai",
          details: [],
        }
      : {
          passed: false,
          label: "Ada bagian CV yang belum terbaca",
          details: ["CV seperti ini selalu ditinjau HR, berapa pun skornya."],
        },
    result.score >= THRESHOLDS.shortlist
      ? {
          passed: true,
          label: `Skor ${score} mencapai batas rekomendasi ${THRESHOLDS.shortlist}`,
          details: [],
        }
      : {
          passed: false,
          label: `Skor ${score} di bawah batas rekomendasi ${THRESHOLDS.shortlist}`,
          details: [],
        },
    result.knockout_flags.length === 0
      ? {
          passed: true,
          label: "Tidak ada syarat gugur yang dilanggar",
          details: [
            "Syarat gugur: pengalaman minimal, bidang pendidikan, dan jenjang pendidikan.",
          ],
        }
      : {
          passed: false,
          label: "Ada syarat gugur yang perlu diputuskan HR",
          details: result.knockout_flags.map(readable),
        },
  ];
  if (result.score < THRESHOLDS.reject) {
    const readWell = document.method !== "ocr" && document.confidence >= 0.7;
    checks.push({
      passed: readWell,
      label: readWell
        ? "Dokumen terbaca dengan baik"
        : "Kualitas pembacaan dokumen meragukan",
      details: readWell
        ? []
        : [
            "Skor rendah dari dokumen yang sulit dibaca tidak ditolak otomatis.",
          ],
    });
  }
  return checks;
}

/** One sentence: why the backend's decision came out this way. */
export function decisionReason(
  result: ScreeningResult,
  document: DocumentRead,
): string {
  const { score, knockout_flags: flags, unassessed } = result;
  const reasons: Record<Recommendation, () => string> = {
    SHORTLIST: () =>
      `Direkomendasikan karena skornya mencapai batas ${THRESHOLDS.shortlist} dan tidak ada syarat gugur yang dilanggar.`,
    REJECT: () =>
      `Tidak lolos karena skornya di bawah ${THRESHOLDS.reject} dan dokumennya terbaca dengan baik.`,
    REVIEW: () => {
      if (unassessed.length > 0) {
        return "Perlu ditinjau karena ada bagian CV yang belum terbaca, sehingga skornya belum lengkap.";
      }
      if (score >= THRESHOLDS.shortlist) {
        return "Perlu ditinjau karena skornya tinggi, tetapi ada syarat gugur yang perlu diputuskan HR.";
      }
      if (score >= THRESHOLDS.reject) {
        const extra =
          flags.length > 0
            ? ", dan ada syarat gugur yang perlu diputuskan HR"
            : "";
        return `Perlu ditinjau karena skornya berada di zona tinjau, antara ${THRESHOLDS.reject} dan ${THRESHOLDS.shortlist}${extra}.`;
      }
      const ocr = document.method === "ocr" ? "hasil pindai" : "sulit dibaca";
      return `Perlu ditinjau karena skornya rendah, tetapi dokumennya ${ocr}, sehingga tidak ditolak otomatis.`;
    },
  };
  return reasons[result.recommendation]();
}
