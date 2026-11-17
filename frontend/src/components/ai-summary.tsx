"use client";

import { LoaderCircle, Sparkles } from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { errorMessage } from "@/hooks/use-api";
import { createHRSummary, type HRSummary } from "@/lib/api";

type AiSummaryProps = { jobId: string; candidateId: string };

/** HR summary on request. The LLM words the explanation; it never changes the score. */
export function AiSummary({ jobId, candidateId }: AiSummaryProps) {
  const [summary, setSummary] = useState<HRSummary | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setBusy(true);
    setError("");
    try {
      // A second click asks for a fresh text instead of the stored one.
      setSummary(await createHRSummary(jobId, candidateId, summary !== null));
    } catch (summaryError) {
      setError(errorMessage(summaryError));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card>
      <CardHeader className="flex-row items-start justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <CardTitle>Ringkasan AI untuk HR</CardTitle>
          <CardDescription>
            Gemini hanya merangkai penjelasan dari fakta yang sudah dihitung. Skor dan peringkat tidak
            diubah, dan data pribadi kandidat tidak dikirim.
          </CardDescription>
        </div>
        <Button onClick={handleGenerate} disabled={busy}>
          {busy ? <LoaderCircle className="animate-spin" /> : <Sparkles />}
          {summary ? "Buat ulang" : "Buat ringkasan"}
        </Button>
      </CardHeader>
      {(summary || error) && (
        <CardContent className="flex flex-col gap-3">
          {error && <p className="text-sm text-destructive">{error}</p>}
          {summary && (
            <>
              <p className="leading-relaxed">{summary.text}</p>
              <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                <Badge variant={summary.source === "gemini" ? "success" : "secondary"}>
                  {summary.source === "gemini" ? `Gemini · ${summary.model}` : "Templat deterministik"}
                </Badge>
                {summary.note && <span>{summary.note}</span>}
              </div>
            </>
          )}
        </CardContent>
      )}
    </Card>
  );
}
