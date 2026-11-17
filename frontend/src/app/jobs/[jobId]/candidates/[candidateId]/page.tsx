"use client";

import { useParams, useSearchParams } from "next/navigation";
import { Suspense, useCallback } from "react";

import { AiSummary } from "@/components/ai-summary";
import { CvEvidence } from "@/components/cv-evidence";
import { MatchBreakdown } from "@/components/match-breakdown";
import { Meter } from "@/components/meter";
import { PageShell } from "@/components/page-shell";
import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreExplainer } from "@/components/score-explainer";
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

  const { result, breakdown, identity } = detail.data;
  const contact = [identity.email, identity.phone].filter(Boolean).join(", ");
  return (
    <PageShell
      title={identity.name ?? `Kandidat ${candidateId}`}
      description={
        contact ||
        `Peringkat ${result.rank}. Nama disembunyikan agar penilaian tidak bias.`
      }
      back={back}
      actions={<RecommendationBadge value={result.recommendation} />}
    >
      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <div className="flex min-w-0 flex-col gap-6">
          <AiSummary jobId={jobId} candidateId={candidateId} />
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

/** The four match percentages. They are the scoring values themselves, shown as percentages. */
function InsightCard({ detail }: { detail: CandidateDetail }) {
  const { result, breakdown } = detail;
  const { experience } = breakdown;
  const mustFound = breakdown.must_have_skills.filter(
    (skill) => skill.status !== "missing",
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
          hint={`Skor ${formatNumber(result.score)} dari 100, peringkat ${result.rank}`}
        />
        <div className="flex flex-col gap-4 border-t border-border pt-4">
          <Meter
            label="Keterampilan"
            percent={result.breakdown.skills * 100}
            hint={`${mustFound} dari ${breakdown.must_have_skills.length} keterampilan wajib`}
          />
          <Meter
            label="Pengalaman"
            percent={result.breakdown.experience * 100}
            hint={`${formatNumber(experience.relevant_years)} tahun relevan, syarat ${experience.required_years} tahun`}
          />
          <Meter
            label="Pendidikan"
            percent={result.breakdown.education * 100}
            hint={
              formatFields(breakdown.education.found_fields) ||
              "Bidang tidak terbaca"
            }
          />
        </div>
      </CardContent>
    </Card>
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
          <dt className="text-muted-foreground">Cara baca</dt>
          <dd className="text-right font-medium">
            {detail.extraction_method === "ocr"
              ? "OCR (hasil scan)"
              : "Teks langsung"}
          </dd>
          <dt className="text-muted-foreground">Keyakinan</dt>
          <dd className="text-right font-medium tabular-nums">
            {formatNumber(detail.extraction_confidence * 100, 0)}%
          </dd>
          <dt className="text-muted-foreground">Pendidikan</dt>
          <dd className="text-right font-medium">
            {readable(detail.education.map((item) => item.degree).join("; ")) ||
              "Tidak terbaca"}
          </dd>
        </dl>
        {detail.warnings.map((warning) => (
          <Notice key={warning} tone="info">
            {warning}
          </Notice>
        ))}
      </CardContent>
    </Card>
  );
}
