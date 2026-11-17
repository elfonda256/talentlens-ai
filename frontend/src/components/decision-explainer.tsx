import { CircleCheck, CircleX, Info, Scale } from "lucide-react";

import { RecommendationBadge } from "@/components/recommendation-badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Recommendation, ScreeningResult } from "@/lib/api";
import { THRESHOLDS, decisionChecks, decisionReason } from "@/lib/decision";
import { formatNumber } from "@/lib/labels";
import { cn } from "@/lib/utils";

const ZONES = [
  {
    key: "REJECT",
    label: "Tidak lolos",
    range: `di bawah ${THRESHOLDS.reject}`,
    from: 0,
    to: THRESHOLDS.reject,
    tone: "bg-destructive-soft",
    dot: "bg-destructive",
  },
  {
    key: "REVIEW",
    label: "Perlu ditinjau",
    range: `${THRESHOLDS.reject} sampai di bawah ${THRESHOLDS.shortlist}`,
    from: THRESHOLDS.reject,
    to: THRESHOLDS.shortlist,
    tone: "bg-warning-soft",
    dot: "bg-warning",
  },
  {
    key: "SHORTLIST",
    label: "Direkomendasikan",
    range: `${THRESHOLDS.shortlist} ke atas`,
    from: THRESHOLDS.shortlist,
    to: 100,
    tone: "bg-success-soft",
    dot: "bg-success",
  },
] as const satisfies readonly {
  key: Recommendation;
  label: string;
  range: string;
  from: number;
  to: number;
  tone: string;
  dot: string;
}[];

type Marker = { score: number; label: string; recommendation: Recommendation };

/** The 0-100 score line with the three decision zones and a dot per candidate. */
function ZoneScale({ markers }: { markers: Marker[] }) {
  return (
    <div className="flex flex-col gap-2">
      <div
        role="img"
        aria-label={markers
          .map((m) => `${m.label}: skor ${formatNumber(m.score)}`)
          .join(", ")}
        className="relative h-3 rounded-full"
      >
        <div className="flex h-full overflow-hidden rounded-full">
          {ZONES.map((zone) => (
            <span
              key={zone.key}
              className={zone.tone}
              style={{ width: `${zone.to - zone.from}%` }}
            />
          ))}
        </div>
        {markers.map((marker) => (
          <span
            key={marker.label}
            title={`${marker.label}: ${formatNumber(marker.score)}`}
            className={cn(
              "absolute top-1/2 size-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full ring-2 ring-card",
              ZONES.find((z) => z.key === marker.recommendation)?.dot,
            )}
            style={{ left: `${Math.min(Math.max(marker.score, 0), 100)}%` }}
          />
        ))}
      </div>
      <div className="hidden text-xs text-muted-foreground sm:flex">
        {ZONES.map((zone) => (
          <span
            key={zone.key}
            className="flex flex-col gap-0.5 border-l border-border pl-1.5 first:border-l-0 first:pl-0"
            style={{ width: `${zone.to - zone.from}%` }}
          >
            <span className="font-medium text-foreground">{zone.label}</span>
            <span className="tabular-nums">{zone.range}</span>
          </span>
        ))}
      </div>
      <ul className="flex flex-col gap-1 text-xs text-muted-foreground sm:hidden">
        {ZONES.map((zone) => (
          <li key={zone.key} className="flex items-center gap-2">
            <span
              className={cn("size-2 rounded-full", zone.dot)}
              aria-hidden="true"
            />
            <span className="font-medium text-foreground">{zone.label}</span>
            {zone.range}
          </li>
        ))}
      </ul>
    </div>
  );
}

type DecisionExplainerProps = {
  result: ScreeningResult;
  extractionMethod: string;
  extractionConfidence: number;
};

/** Candidate page: the decision rule, checked item by item against this candidate. */
export function DecisionExplainer({
  result,
  extractionMethod,
  extractionConfidence,
}: DecisionExplainerProps) {
  const document = {
    method: extractionMethod,
    confidence: extractionConfidence,
  };
  const checks = decisionChecks(result, document);
  return (
    <Card aria-labelledby="judul-keputusan">
      <CardHeader className="flex-row flex-wrap items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          <CardTitle id="judul-keputusan" className="flex items-center gap-2">
            <Scale className="size-4 text-primary" aria-hidden="true" />
            Mengapa keputusannya seperti ini
          </CardTitle>
          <CardDescription>
            Aturan yang sama untuk setiap kandidat. AI tidak ikut menentukan
            keputusan.
          </CardDescription>
        </div>
        <RecommendationBadge value={result.recommendation} />
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <p className="font-medium">{decisionReason(result, document)}</p>
        <ZoneScale
          markers={[
            {
              score: result.score,
              label: "Kandidat ini",
              recommendation: result.recommendation,
            },
          ]}
        />
        <ul className="flex flex-col gap-3 text-sm">
          {checks.map((check) => (
            <li key={check.label} className="flex gap-2.5">
              {check.passed ? (
                <CircleCheck
                  className="mt-0.5 size-4 shrink-0 text-success"
                  aria-label="Terpenuhi"
                />
              ) : (
                <CircleX
                  className="mt-0.5 size-4 shrink-0 text-warning"
                  aria-label="Belum terpenuhi"
                />
              )}
              <span className="flex flex-col gap-0.5">
                <span className="font-medium">{check.label}</span>
                {check.details.map((detail) => (
                  <span key={detail} className="text-muted-foreground">
                    {detail}
                  </span>
                ))}
              </span>
            </li>
          ))}
          {result.missing_must_skills.length > 0 && (
            <li className="flex gap-2.5">
              <Info
                className="mt-0.5 size-4 shrink-0 text-muted-foreground"
                aria-hidden="true"
              />
              <span className="flex flex-col gap-0.5">
                <span className="font-medium">
                  Keterampilan wajib yang belum terlihat di CV:{" "}
                  {result.missing_must_skills.join(", ")}
                </span>
                <span className="text-muted-foreground">
                  Ini mengurangi skor keterampilan, tetapi bukan syarat gugur.
                  Pastikan saat wawancara.
                </span>
              </span>
            </li>
          )}
        </ul>
      </CardContent>
    </Card>
  );
}

type DecisionRulesProps = {
  results: Pick<ScreeningResult, "rank" | "score" | "recommendation">[];
  counts: Record<Recommendation, number>;
};

/** Job page: how decisions are made, with every candidate placed on the same scale. */
export function DecisionRules({ results, counts }: DecisionRulesProps) {
  return (
    <Card
      aria-labelledby="judul-aturan"
      className="flex flex-col gap-4 p-5 sm:p-6"
    >
      <div className="flex flex-col gap-1">
        <h2 id="judul-aturan" className="flex items-center gap-2 font-semibold">
          <Scale className="size-4 text-primary" aria-hidden="true" />
          Cara keputusan dibuat
        </h2>
        <p className="text-sm text-muted-foreground">
          Setiap titik adalah satu kandidat pada skala skor 0–100. Skor tinggi
          tetap masuk tinjauan bila ada syarat gugur (pengalaman minimal, bidang
          atau jenjang pendidikan) atau bagian CV yang belum terbaca.
        </p>
      </div>
      <ZoneScale
        markers={results.map((row) => ({
          score: row.score,
          label: `Peringkat ${row.rank}`,
          recommendation: row.recommendation,
        }))}
      />
      {counts.REJECT === 0 && (
        <p className="text-sm text-muted-foreground">
          Tidak ada kandidat pada lowongan ini yang skornya di bawah{" "}
          {THRESHOLDS.reject}, sehingga belum ada yang masuk{" "}
          <span className="font-medium text-foreground">Tidak lolos</span>.
          &ldquo;Tidak lolos&rdquo; pun selalu berupa rekomendasi dengan alasan
          tertulis; keputusan akhir tetap pada HR.
        </p>
      )}
    </Card>
  );
}
