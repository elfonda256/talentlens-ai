"use client";

import {
  CircleAlert,
  LoaderCircle,
  MessagesSquare,
  RefreshCw,
  Sparkles,
  ThumbsUp,
  type LucideIcon,
} from "lucide-react";
import { useCallback, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { errorMessage, useApi } from "@/hooks/use-api";
import { createHRSummary, type HRSummary } from "@/lib/api";

type AiSummaryProps = { jobId: string; candidateId: string };

/**
 * The recruiter's note, written as soon as the page opens. The AI words the explanation from
 * facts the system already computed; it never changes the score. Risks have their own panel.
 */
export function AiSummary({ jobId, candidateId }: AiSummaryProps) {
  const first = useApi(
    useCallback(
      () => createHRSummary(jobId, candidateId, false),
      [jobId, candidateId],
    ),
  );
  const [rewritten, setRewritten] = useState<HRSummary | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const summary = rewritten ?? first.data;
  const writing = first.loading || busy;

  const handleRewrite = async () => {
    setBusy(true);
    setError("");
    try {
      setRewritten(await createHRSummary(jobId, candidateId, true));
    } catch (rewriteError) {
      setError(errorMessage(rewriteError));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card aria-labelledby="judul-ringkasan">
      <CardHeader className="flex-row flex-wrap items-start justify-between gap-4">
        <div className="flex min-w-0 flex-1 flex-col gap-1">
          <CardTitle id="judul-ringkasan" className="flex items-center gap-2">
            <Sparkles className="size-4 text-brand" aria-hidden="true" />
            Ringkasan AI untuk hiring manager
          </CardTitle>
          <CardDescription>
            Disusun dari fakta CV dan lowongan. Skor dan peringkat tidak diubah,
            dan data pribadi kandidat tidak dikirim.
          </CardDescription>
        </div>
        {summary && (
          <Button
            onClick={handleRewrite}
            disabled={writing}
            variant="outline"
            size="sm"
            aria-busy={busy}
          >
            {busy ? (
              <LoaderCircle className="animate-spin" aria-hidden="true" />
            ) : (
              <RefreshCw aria-hidden="true" />
            )}
            {busy ? "Menyusun…" : "Susun ulang"}
          </Button>
        )}
      </CardHeader>

      <CardContent className="flex flex-col gap-5" aria-live="polite">
        {(error || first.error !== undefined) && (
          <Notice tone="error">{error || errorMessage(first.error)}</Notice>
        )}
        {writing && !summary && (
          <div
            className="flex flex-col gap-3"
            role="status"
            aria-label="Sedang menyusun ringkasan"
          >
            <Skeleton className="h-6 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-24 w-full" />
          </div>
        )}
        {summary && (
          <>
            <div className="flex flex-col gap-1.5">
              <p className="text-lg font-semibold leading-snug">
                {summary.headline}
              </p>
              <p className="max-w-3xl text-muted-foreground">{summary.fit}</p>
            </div>
            <div className="grid gap-x-8 gap-y-5 md:grid-cols-2">
              <NoteList
                icon={ThumbsUp}
                tone="text-success"
                title="Kekuatan"
                items={summary.strengths}
                empty="Tidak ada kekuatan menonjol untuk posisi ini."
              />
              <NoteList
                icon={CircleAlert}
                tone="text-warning"
                title="Kekurangan"
                items={summary.concerns}
                empty="Tidak ada kekurangan yang terlihat dari CV."
              />
              <NoteList
                icon={MessagesSquare}
                tone="text-primary"
                title="Yang perlu digali saat wawancara"
                items={summary.interview_focus}
                empty="Tidak disarankan lanjut ke wawancara."
              />
            </div>
            <p className="border-t border-border pt-4 text-sm">
              <span className="font-medium">Alasan rekomendasi: </span>
              {summary.recommendation_reason}
            </p>
          </>
        )}
      </CardContent>
    </Card>
  );
}

type NoteListProps = {
  icon: LucideIcon;
  tone: string;
  title: string;
  items: string[];
  empty: string;
};

function NoteList({ icon: Icon, tone, title, items, empty }: NoteListProps) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="flex items-center gap-2 text-sm font-semibold">
        <Icon className={`size-4 ${tone}`} aria-hidden="true" />
        {title}
      </h3>
      {items.length > 0 ? (
        <ul className="flex list-disc flex-col gap-1.5 pl-5 text-sm marker:text-muted-foreground">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-muted-foreground">{empty}</p>
      )}
    </div>
  );
}
