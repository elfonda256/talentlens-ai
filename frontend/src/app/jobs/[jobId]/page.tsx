"use client";

import { LoaderCircle, Play } from "lucide-react";
import { useParams } from "next/navigation";
import { Suspense, useCallback, useState } from "react";

import { CvUpload } from "@/components/cv-upload";
import { JobCriteria } from "@/components/job-criteria";
import { PageShell } from "@/components/page-shell";
import { RankingTable } from "@/components/ranking-table";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { errorMessage, useApi } from "@/hooks/use-api";
import { ApiError, getJob, getRanking, listCandidates, runScreening } from "@/lib/api";
import { EMBEDDING_LABEL } from "@/lib/labels";

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
  const [screening, setScreening] = useState(false);
  const [screenError, setScreenError] = useState("");

  const job = useApi(useCallback(() => getJob(jobId), [jobId]));
  const candidates = useApi(useCallback(() => listCandidates(jobId), [jobId]));
  const ranking = useApi(useCallback(() => getRanking(jobId, reveal), [jobId, reveal]));

  const candidateCount = candidates.data?.length ?? 0;
  const notScreened = ranking.error instanceof ApiError && ranking.error.status === NOT_SCREENED;

  const handleScreen = async () => {
    setScreening(true);
    setScreenError("");
    try {
      await runScreening(jobId);
      ranking.reload();
    } catch (error) {
      setScreenError(errorMessage(error));
    } finally {
      setScreening(false);
    }
  };

  if (job.error !== undefined) {
    return (
      <PageShell title="Lowongan tidak ditemukan" back={{ href: "/", label: "Semua lowongan" }}>
        <p className="text-sm text-destructive">{errorMessage(job.error)}</p>
      </PageShell>
    );
  }

  return (
    <PageShell title={job.data?.title ?? "Memuat…"} back={{ href: "/", label: "Semua lowongan" }}>
      {job.data && <JobCriteria job={job.data} />}

      <CvUpload
        jobId={jobId}
        candidateCount={candidateCount}
        onUploaded={() => {
          candidates.reload();
          ranking.reload();
        }}
      />

      <Card>
        <CardHeader className="flex-row items-start justify-between gap-4">
          <div className="flex flex-col gap-1.5">
            <CardTitle>Peringkat kandidat</CardTitle>
            <CardDescription>
              {ranking.data
                ? `Embedding: ${EMBEDDING_LABEL[ranking.data.embedding_backend] ?? ranking.data.embedding_backend}. Skor dihitung secara deterministik, bukan oleh LLM.`
                : "Jalankan screening setelah CV diunggah. Mengunggah CV baru menghapus peringkat lama."}
            </CardDescription>
          </div>
          <Button onClick={handleScreen} disabled={screening || candidateCount === 0}>
            {screening ? <LoaderCircle className="animate-spin" /> : <Play />}
            Jalankan screening
          </Button>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          {screenError && <p className="text-sm text-destructive">{screenError}</p>}
          {ranking.error !== undefined && !notScreened && (
            <p className="text-sm text-destructive">{errorMessage(ranking.error)}</p>
          )}
          {notScreened && (
            <p className="text-sm text-muted-foreground">Belum ada hasil screening untuk lowongan ini.</p>
          )}
          {ranking.data && (
            <>
              <label className="flex items-center gap-2 self-start text-sm">
                <input
                  type="checkbox"
                  checked={reveal}
                  onChange={(event) => setReveal(event.target.checked)}
                />
                Tampilkan identitas kandidat
              </label>
              <RankingTable jobId={jobId} rows={ranking.data.results} reveal={reveal} />
            </>
          )}
        </CardContent>
      </Card>
    </PageShell>
  );
}
