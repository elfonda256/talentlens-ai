"use client";

import { useParams, useSearchParams } from "next/navigation";
import { Suspense, useCallback } from "react";

import { AiSummary } from "@/components/ai-summary";
import { PageShell } from "@/components/page-shell";
import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreBar } from "@/components/score-bar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { errorMessage, useApi } from "@/hooks/use-api";
import { getCandidateDetail, type CandidateDetail } from "@/lib/api";
import { COMPONENT_LABEL, COMPONENT_ORDER, formatYears } from "@/lib/labels";

export default function CandidatePage() {
  // Next.js needs a Suspense boundary around components that read the URL on the client.
  return (
    <Suspense>
      <CandidateView />
    </Suspense>
  );
}

function CandidateView() {
  const { jobId, candidateId } = useParams<{ jobId: string; candidateId: string }>();
  const reveal = useSearchParams().get("reveal") === "1";
  const detail = useApi(
    useCallback(() => getCandidateDetail(jobId, candidateId, reveal), [jobId, candidateId, reveal]),
  );
  const back = { href: `/jobs/${jobId}`, label: "Peringkat kandidat" };

  if (detail.error !== undefined) {
    return (
      <PageShell title="Kandidat tidak tersedia" back={back}>
        <p className="text-sm text-destructive">{errorMessage(detail.error)}</p>
      </PageShell>
    );
  }
  if (!detail.data) {
    return <PageShell title="Memuat…" back={back}>{null}</PageShell>;
  }

  const { result, identity } = detail.data;
  return (
    <PageShell
      title={identity.name ?? candidateId}
      description={[identity.email, identity.phone].filter(Boolean).join(" · ") || undefined}
      back={back}
    >
      <ScoreCard detail={detail.data} />
      <AiSummary jobId={jobId} candidateId={candidateId} />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Alasan</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="flex list-disc flex-col gap-2 pl-5 text-sm">
              {result.reasons.map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Bukti dari CV</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4 text-sm">
            {result.evidence.slice(0, 4).map((item) => (
              <div key={item.requirement} className="flex flex-col gap-1">
                <span className="text-muted-foreground">Syarat: {item.requirement}</span>
                <span>“{item.best_match}”</span>
                <span className="text-xs text-muted-foreground">
                  Kemiripan {(item.similarity * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <ProfileCard detail={detail.data} />
    </PageShell>
  );
}

function ScoreCard({ detail }: { detail: CandidateDetail }) {
  const { result } = detail;
  return (
    <Card>
      <CardContent className="flex flex-col gap-6 p-6 md:flex-row md:items-center">
        <div className="flex flex-col gap-2 md:w-48">
          <span className="text-sm text-muted-foreground">Peringkat {result.rank}</span>
          <span className="text-5xl font-semibold tabular-nums">{result.score.toFixed(1)}</span>
          <div>
            <RecommendationBadge value={result.recommendation} />
          </div>
        </div>
        <div className="flex flex-1 flex-col gap-3">
          {COMPONENT_ORDER.map((component) => (
            <div key={component} className="grid grid-cols-[15rem_1fr_5rem] items-center gap-3 text-sm">
              <span className="text-muted-foreground">{COMPONENT_LABEL[component]}</span>
              <ScoreBar fraction={result.breakdown[component]} />
              <span className="text-right font-medium tabular-nums">
                {result.contributions[component].toFixed(1)} poin
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function ProfileCard({ detail }: { detail: CandidateDetail }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Profil hasil parsing</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-5 text-sm">
        <p className="text-muted-foreground">
          Total pengalaman {formatYears(detail.total_experience_months)} · dibaca dengan{" "}
          {detail.extraction_method === "ocr" ? "OCR" : "ekstraksi teks"} · keyakinan{" "}
          {(detail.extraction_confidence * 100).toFixed(0)}%
        </p>
        {detail.warnings.map((warning) => (
          <p key={warning} className="text-warning">
            {warning}
          </p>
        ))}
        <div className="flex flex-col gap-2">
          <span className="font-medium">Pengalaman</span>
          {detail.experiences.map((experience) => (
            <div key={`${experience.title}-${experience.start}`} className="flex justify-between gap-4">
              <span>
                {experience.title}
                {experience.company && <span className="text-muted-foreground"> · {experience.company}</span>}
              </span>
              <span className="shrink-0 text-muted-foreground">
                {experience.start}–{experience.end === "present" ? "sekarang" : experience.end}
              </span>
            </div>
          ))}
        </div>
        <div className="flex flex-col gap-2">
          <span className="font-medium">Pendidikan</span>
          {detail.education.map((education) => (
            <span key={education.degree}>{education.degree}</span>
          ))}
        </div>
        <div className="flex flex-col gap-2">
          <span className="font-medium">Keterampilan terdeteksi</span>
          <div className="flex flex-wrap gap-2">
            {detail.skills.map((skill) => (
              <Badge key={skill} variant="outline">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
