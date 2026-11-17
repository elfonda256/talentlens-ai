"use client";

import {
  CircleAlert,
  LoaderCircle,
  MessagesSquare,
  ShieldAlert,
  Sparkles,
  ThumbsUp,
  type LucideIcon,
} from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
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
import { errorMessage } from "@/hooks/use-api";
import { createHRSummary, type HRSummary } from "@/lib/api";

type AiSummaryProps = { jobId: string; candidateId: string };

/** Recruiter-style note on request. The AI words the explanation; it never changes the score. */
export function AiSummary({ jobId, candidateId }: AiSummaryProps) {
  const [summary, setSummary] = useState<HRSummary | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setBusy(true);
    setError("");
    try {
      // A second click asks for a fresh note instead of the stored one.
      setSummary(await createHRSummary(jobId, candidateId, summary !== null));
    } catch (summaryError) {
      setError(errorMessage(summaryError));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card aria-labelledby="judul-ringkasan">
      <CardHeader className="flex-row flex-wrap items-start justify-between gap-4">
        <div className="flex min-w-0 flex-1 flex-col gap-1">
          <CardTitle id="judul-ringkasan">Catatan recruiter</CardTitle>
          <CardDescription>
            Ditulis AI dari hasil yang sudah dihitung. Skor dan peringkat tidak
            diubah, dan data pribadi kandidat tidak dikirim.
          </CardDescription>
        </div>
        <Button
          onClick={handleGenerate}
          disabled={busy}
          variant={summary ? "outline" : "default"}
          aria-busy={busy}
        >
          {busy ? (
            <LoaderCircle className="animate-spin" aria-hidden="true" />
          ) : (
            <Sparkles aria-hidden="true" />
          )}
          {busy ? "Menulis…" : summary ? "Tulis ulang" : "Buat catatan"}
        </Button>
      </CardHeader>

      <CardContent className="flex flex-col gap-5" aria-live="polite">
        {error && <Notice tone="error">{error}</Notice>}
        {busy && !summary && (
          <div
            className="flex flex-col gap-3"
            role="status"
            aria-label="Sedang menulis catatan"
          >
            <Skeleton className="h-6 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-24 w-full" />
          </div>
        )}
        {!busy && !summary && !error && (
          <p className="text-sm text-muted-foreground">
            Catatan berisi kekuatan, kekurangan, risiko, dan hal yang perlu
            digali saat wawancara.
          </p>
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
                icon={ShieldAlert}
                tone="text-destructive"
                title="Risiko"
                items={summary.risks}
                empty="Tidak ada risiko khusus yang terdeteksi."
              />
              <NoteList
                icon={MessagesSquare}
                tone="text-primary"
                title="Yang perlu digali saat wawancara"
                items={summary.interview_focus}
                empty="Tidak disarankan lanjut ke wawancara."
              />
            </div>
            <div className="flex flex-col gap-2 border-t border-border pt-4">
              <p className="text-sm">
                <span className="font-medium">Alasan rekomendasi: </span>
                {summary.recommendation_reason}
              </p>
              <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                <Badge
                  variant={
                    summary.source === "gemini" ? "secondary" : "outline"
                  }
                >
                  {summary.source === "gemini"
                    ? `Ditulis oleh Gemini (${summary.model})`
                    : "Ditulis dengan templat bawaan"}
                </Badge>
                {summary.note && <span>{summary.note}</span>}
              </div>
            </div>
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
