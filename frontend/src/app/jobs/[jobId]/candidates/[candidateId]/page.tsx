"use client";

import { useParams, useSearchParams } from "next/navigation";
import { Suspense, useCallback } from "react";

import { AiSummary } from "@/components/ai-summary";
import { AssessmentPanels } from "@/components/assessment-panels";
import { CandidateBadges } from "@/components/candidate-badges";
import { DecisionExplainer } from "@/components/decision-explainer";
import { CvEvidence } from "@/components/cv-evidence";
import { MatchBreakdown } from "@/components/match-breakdown";
import { Meter } from "@/components/meter";
import { PageShell } from "@/components/page-shell";
import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreComposition, ScoreLegend } from "@/components/score-composition";
import { ScoreExplainer } from "@/components/score-explainer";
import { ScoreRing } from "@/components/score-ring";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { errorMessage, useApi } from "@/hooks/use-api";
import { getCandidateDetail, type CandidateDetail } from "@/lib/api";
import { formatFields, formatNumber, readable } from "@/lib/labels";

export default function CandidatePage() {
  // Next.js needs a Suspense boundary around components that read the URL on the client.
  return (
    <Suspense>
      <CandidateView />
    </Suspense>
  );
}

function CandidateView() {
  const { jobId, candidateId } = useParams<{
    jobId: string;
    candidateId: string;
  }>();
  const reveal = useSearchParams().get("reveal") === "1";
  const detail = useApi(
    useCallback(
      () => getCandidateDetail(jobId, candidateId, reveal),
      [jobId, candidateId, reveal],
    ),
  );
  const back = { href: `/jobs/${jobId}`, label: "Peringkat kandidat" };

  if (detail.error !== undefined) {
    return (
      <PageShell title="Kandidat tidak tersedia" back={back}>
        <Notice tone="error">{errorMessage(detail.error)}</Notice>
      </PageShell>
    );
  }
  if (!detail.data) {
    return (
      <PageShell title={<Skeleton className="h-9 w-56" />} back={back}>
        <div
          className="grid gap-6 lg:grid-cols-[1fr_20rem]"
          role="status"
          aria-label="Memuat rincian kandidat"
        >
          <Skeleton className="h-72" />
          <Skeleton className="h-72" />
        </div>
      </PageShell>
    );
  }

  const { result, breakdown, identity, assessment } = detail.data;
  const contact = [identity.email, identity.phone].filter(Boolean).join(", ");
  return (
    <PageShell
      title={identity.name ?? `Kandidat ${candidateId}`}
      description={
        contact ||
        `Peringkat ${result.rank}. Nama disembunyikan agar penilaian tidak bias.`
      }
      back={back}
    >
      {result.unassessed.length > 0 && (
        <Notice tone="warning">
          <strong className="font-semibold">
            CV ini tidak terbaca lengkap.
          </strong>{" "}
          Bagian {sectionNames(result.unassessed)} tidak dikenali, sehingga
          belum dinilai dan tidak dianggap sebagai kekurangan kandidat. Skor
          bersifat sementara; periksa CV aslinya sebelum memutuskan.
        </Notice>
      )}
      <Card aria-label="Skor AI dan keputusan">
        <CardContent className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center">
          <ScoreRing
            score={result.score}
            recommendation={result.recommendation}
            size="lg"
            provisional={result.unassessed.length > 0}
          />
          <div className="flex min-w-0 flex-1 flex-col gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <RecommendationBadge value={result.recommendation} />
              <CandidateBadges
                rank={result.rank}
                recommendation={result.recommendation}
                assessment={assessment}
              />
            </div>
            <p className="text-xl font-semibold leading-snug">
              Peringkat {result.rank} untuk posisi ini
            </p>
            <ScoreComposition components={breakdown.components} size="lg" />
            <ScoreLegend components={breakdown.components} />
          </div>
        </CardContent>
      </Card>
      <AiSummary jobId={jobId} candidateId={candidateId} />
      <DecisionExplainer
        result={result}
        extractionMethod={detail.data.extraction_method}
        extractionConfidence={detail.data.extraction_confidence}
      />
      <AssessmentPanels assessment={assessment} />
      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <div className="flex min-w-0 flex-col gap-6">
          <ScoreExplainer
            components={breakdown.components}
            score={result.score}
          />
          <MatchBreakdown breakdown={breakdown} />
          <CvEvidence detail={detail.data} />
        </div>
        <aside
          className="order-first flex flex-col gap-6 lg:sticky lg:top-6 lg:order-none"
          aria-label="Ringkasan kecocokan"
        >
          <InsightCard detail={detail.data} />
          <ReadingCard detail={detail.data} />
        </aside>
      </div>
    </PageShell>
  );
}

const SECTION_NAME: Record<string, string> = {
  experience: "pengalaman kerja",
  education: "pendidikan",
  skills: "keterampilan",
  summary: "ringkasan",
};

function sectionNames(keys: string[]): string {
  return keys.map((key) => SECTION_NAME[key] ?? key).join(" dan ");
}

/** The four match percentages. They are the scoring values themselves, shown as percentages. */
function InsightCard({ detail }: { detail: CandidateDetail }) {
  const { result, breakdown } = detail;
  const { experience } = breakdown;
  const mustFound = breakdown.must_have_skills.filter(
    (skill) => skill.status !== "missing",
  ).length;
  const mustImplied = breakdown.must_have_skills.filter(
    (skill) => skill.status === "implied",
  ).length;
  return (
    <Card aria-labelledby="judul-insight">
      <CardHeader className="pb-4">
        <CardTitle id="judul-insight">Tingkat kecocokan</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <Meter
          label="Keseluruhan"
          percent={result.score}
          emphasis
          hint={`Skor ${formatNumber(result.score)} dari 100${result.unassessed.length > 0 ? " (sementara)" : ""}, peringkat ${result.rank}`}
        />
        <div className="flex flex-col gap-4 border-t border-border pt-4">
          <Meter
            label="Keterampilan"
            percent={result.breakdown.skills * 100}
            hint={`${mustFound} dari ${breakdown.must_have_skills.length} keterampilan wajib${mustImplied > 0 ? ` (${mustImplied} tersirat, dinilai sebagian)` : ""}`}
          />
          <Meter
            label="Pengalaman"
            percent={result.breakdown.experience * 100}
            assessed={experience.assessed}
            hint={
              experience.assessed
                ? `${formatNumber(experience.relevant_years)} tahun relevan, syarat ${experience.required_years} tahun`
                : "Bagian pengalaman kerja tidak terbaca"
            }
          />
          <Meter
            label="Pendidikan"
            percent={result.breakdown.education * 100}
            assessed={breakdown.education.status !== "unknown"}
            hint={
              formatFields(breakdown.education.found_fields) ||
              (breakdown.education.status === "unknown"
                ? "Bagian pendidikan tidak terbaca"
                : "Bidang studi tidak disebutkan")
            }
          />
        </div>
      </CardContent>
    </Card>
  );
}

const SECTIONS_SHOWN = ["experience", "education", "skills"] as const;

/** One CV section and how well it was read: found and structured, partly, or not found. */
function SectionReading({
  name,
  confidence,
}: {
  name: string;
  confidence: number | undefined;
}) {
  const label =
    confidence === undefined
      ? "Tidak diukur"
      : confidence === 0
        ? "Tidak ditemukan"
        : confidence < 0.6
          ? "Ditemukan, isinya tidak terbaca"
          : `Terbaca ${formatNumber(confidence * 100, 0)}%`;
  return (
    <>
      <dt className="text-muted-foreground">Bagian {name}</dt>
      <dd
        className={
          confidence !== undefined && confidence < 0.6
            ? "text-right font-medium text-warning-ink"
            : "text-right font-medium tabular-nums"
        }
      >
        {label}
      </dd>
    </>
  );
}

/** How well the document itself was read, so HR knows how far to trust the result. */
function ReadingCard({ detail }: { detail: CandidateDetail }) {
  return (
    <Card aria-labelledby="judul-pembacaan">
      <CardHeader className="pb-4">
        <CardTitle id="judul-pembacaan">Pembacaan dokumen</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3 text-sm">
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
          <dt className="text-muted-foreground">Jenis dokumen</dt>
          <dd className="text-right font-medium">
            {detail.extraction_method === "ocr"
              ? "Hasil pindai"
              : "Dokumen digital"}
          </dd>
          {SECTIONS_SHOWN.map((key) => (
            <SectionReading
              key={key}
              name={SECTION_NAME[key]}
              confidence={detail.section_confidence[key]}
            />
          ))}
          <dt className="text-muted-foreground">Pendidikan selesai</dt>
          <dd className="text-right font-medium">
            {readable(detail.education.map((item) => item.degree).join("; ")) ||
              "Tidak ada yang terbaca"}
          </dd>
          {detail.education_in_progress.length > 0 && (
            <>
              <dt className="text-muted-foreground">Masih ditempuh</dt>
              <dd className="text-right font-medium">
                {readable(
                  detail.education_in_progress
                    .map((item) => item.degree)
                    .join("; "),
                )}
              </dd>
            </>
          )}
        </dl>
        <p className="text-xs text-muted-foreground">
          Bagian yang tidak ditemukan tidak dinilai, bukan dianggap nol.
        </p>
        {detail.warnings.map((warning) => (
          <Notice key={warning} tone="info">
            {warning}
          </Notice>
        ))}
      </CardContent>
    </Card>
  );
}
