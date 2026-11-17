"use client";

import { FileUp, LoaderCircle, Play, SearchX } from "lucide-react";
import { useParams } from "next/navigation";
import { Suspense, useCallback, useState } from "react";

import { CvUploadButton, UploadReport } from "@/components/cv-upload";
import { JobCriteria } from "@/components/job-criteria";
import { PageShell } from "@/components/page-shell";
import { RankingTable } from "@/components/ranking-table";
import { ScoreLegend } from "@/components/score-composition";
import { StatStrip, type RankingFilter } from "@/components/stat-strip";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { errorMessage, useApi } from "@/hooks/use-api";
import {
  ApiError,
  getJob,
  getRanking,
  listCandidates,
  runScreening,
  type UploadOutcome,
} from "@/lib/api";

const NOT_SCREENED = 409;

export default function JobPage() {
  // Next.js needs a Suspense boundary around components that read the URL on the client.
  return (
    <Suspense>
      <JobView />
    </Suspense>
  );
}

function JobView() {
  const { jobId } = useParams<{ jobId: string }>();
  const [reveal, setReveal] = useState(false);
  const [filter, setFilter] = useState<RankingFilter>("ALL");
  const [screening, setScreening] = useState(false);
  const [screenError, setScreenError] = useState("");
  const [uploads, setUploads] = useState<UploadOutcome[]>([]);

  const job = useApi(useCallback(() => getJob(jobId), [jobId]));
  const candidates = useApi(useCallback(() => listCandidates(jobId), [jobId]));
  const ranking = useApi(
    useCallback(() => getRanking(jobId, reveal), [jobId, reveal]),
  );

  const candidateCount = candidates.data?.length ?? 0;
  const notScreened =
    ranking.error instanceof ApiError && ranking.error.status === NOT_SCREENED;
  const rows = ranking.data?.results ?? [];
  const counts = {
    ALL: rows.length,
    SHORTLIST: rows.filter((row) => row.recommendation === "SHORTLIST").length,
    REVIEW: rows.filter((row) => row.recommendation === "REVIEW").length,
    REJECT: rows.filter((row) => row.recommendation === "REJECT").length,
  };
  const visible =
    filter === "ALL"
      ? rows
      : rows.filter((row) => row.recommendation === filter);

  const handleScreen = async () => {
    setScreening(true);
    setScreenError("");
    try {
      await runScreening(jobId);
      setFilter("ALL");
      ranking.reload();
    } catch (error) {
      setScreenError(errorMessage(error));
    } finally {
      setScreening(false);
    }
  };

  const back = { href: "/", label: "Semua lowongan" };
  if (job.error !== undefined) {
    return (
      <PageShell title="Lowongan tidak ditemukan" back={back}>
        <Notice tone="error">{errorMessage(job.error)}</Notice>
      </PageShell>
    );
  }

  const needsScreening = candidateCount > 0 && (notScreened || ranking.loading);
  return (
    <PageShell
      title={job.data?.title ?? <Skeleton className="h-9 w-64" />}
      description={
        candidates.loading
          ? undefined
          : candidateCount === 0
            ? "Belum ada CV untuk lowongan ini."
            : `${candidateCount} kandidat${ranking.data ? ", sudah disaring" : ", belum disaring"}`
      }
      back={back}
      actions={
        <div className="flex flex-wrap items-center gap-2">
          <CvUploadButton
            jobId={jobId}
            primary={candidateCount === 0}
            onError={(error) => setScreenError(errorMessage(error))}
            onUploaded={(outcomes) => {
              setUploads(outcomes);
              setScreenError("");
              candidates.reload();
              ranking.reload();
            }}
          />
          <Button
            onClick={handleScreen}
            disabled={screening || candidateCount === 0}
            variant={needsScreening ? "default" : "outline"}
            aria-busy={screening}
          >
            {screening ? (
              <LoaderCircle className="animate-spin" aria-hidden="true" />
            ) : (
              <Play aria-hidden="true" />
            )}
            {screening
              ? "Menyaring…"
              : ranking.data
                ? "Saring ulang"
                : "Jalankan screening"}
          </Button>
        </div>
      }
    >
      {job.data ? (
        <JobCriteria job={job.data} />
      ) : (
        <Skeleton className="h-14" />
      )}
      {uploads.length > 0 && (
        <UploadReport outcomes={uploads} onDismiss={() => setUploads([])} />
      )}
      {screenError && <Notice tone="error">{screenError}</Notice>}
      {ranking.error !== undefined && !notScreened && (
        <Notice tone="error">{errorMessage(ranking.error)}</Notice>
      )}

      {screening && (
        <div
          className="flex flex-col gap-3"
          aria-label="Sedang menyaring kandidat"
          role="status"
        >
          <Skeleton className="h-[86px]" />
          <Skeleton className="h-64" />
        </div>
      )}

      {!screening && notScreened && candidateCount === 0 && (
        <EmptyState icon={FileUp} title="Unggah CV pelamar">
          Pilih beberapa berkas sekaligus (PDF, DOCX, atau TXT). Data pribadi
          dipisahkan dari isi CV sebelum penilaian, supaya tidak memengaruhi
          skor.
        </EmptyState>
      )}
      {!screening && notScreened && candidateCount > 0 && (
        <EmptyState icon={Play} title={`${candidateCount} CV siap disaring`}>
          Jalankan screening untuk mencocokkan setiap CV dengan kriteria
          lowongan dan menyusun peringkatnya. Mengunggah CV baru menghapus
          peringkat lama.
        </EmptyState>
      )}

      {!screening && ranking.data && (
        <>
          <StatStrip counts={counts} active={filter} onSelect={setFilter} />
          <Card>
            <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-3 border-b border-border p-4 sm:px-6">
              <div className="flex flex-col gap-2">
                <h2 className="text-base font-semibold">Peringkat kandidat</h2>
                <ScoreLegend
                  components={rows[0]?.highlights.components ?? []}
                />
              </div>
              <label className="flex cursor-pointer items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  className="size-4 accent-primary"
                  checked={reveal}
                  onChange={(event) => setReveal(event.target.checked)}
                />
                Tampilkan nama kandidat
              </label>
            </div>
            {visible.length > 0 ? (
              <RankingTable jobId={jobId} rows={visible} reveal={reveal} />
            ) : (
              <div className="p-6">
                <EmptyState
                  icon={SearchX}
                  title="Tidak ada kandidat pada kelompok ini"
                >
                  Pilih kelompok lain pada ringkasan di atas untuk melihat
                  kandidat lainnya.
                </EmptyState>
              </div>
            )}
            <p className="border-t border-border px-4 py-3 text-xs text-muted-foreground sm:px-6">
              Skor AI menggabungkan keterampilan, pengalaman, pendidikan, dan
              kesesuaian isi CV dengan lowongan. Bilah menunjukkan sumbangan
              tiap komponen; keputusan akhir tetap ada pada HR.
            </p>
          </Card>
        </>
      )}
    </PageShell>
  );
}
