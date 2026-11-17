"use client";

import { useState } from "react";

import { FilePicker } from "@/components/file-picker";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { errorMessage } from "@/hooks/use-api";
import { uploadCandidates, type UploadOutcome } from "@/lib/api";

const STATUS_TEXT = { parsed: "Terbaca", duplicate: "Duplikat", failed: "Gagal" } as const;
const STATUS_CLASS = {
  parsed: "text-success",
  duplicate: "text-muted-foreground",
  failed: "text-destructive",
} as const;

type CvUploadProps = { jobId: string; candidateCount: number; onUploaded: () => void };

export function CvUpload({ jobId, candidateCount, onUploaded }: CvUploadProps) {
  const [busy, setBusy] = useState(false);
  const [outcomes, setOutcomes] = useState<UploadOutcome[]>([]);
  const [error, setError] = useState("");

  const handleFiles = async (files: File[]) => {
    setBusy(true);
    setError("");
    try {
      setOutcomes(await uploadCandidates(jobId, files));
      onUploaded();
    } catch (uploadError) {
      setError(errorMessage(uploadError));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Unggah CV</CardTitle>
        <CardDescription>
          {candidateCount} kandidat tersimpan. Pilih beberapa berkas sekaligus (PDF, DOCX, TXT).
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <div>
          <FilePicker label="Pilih berkas CV" multiple busy={busy} onFiles={handleFiles} />
        </div>
        {error && <p className="text-sm text-destructive">{error}</p>}
        {outcomes.length > 0 && (
          <ul className="flex flex-col gap-1 text-sm">
            {outcomes.map((outcome, position) => (
              <li key={`${outcome.file_name}-${position}`} className="flex gap-3">
                <span className={`w-16 shrink-0 font-medium ${STATUS_CLASS[outcome.status]}`}>
                  {STATUS_TEXT[outcome.status]}
                </span>
                <span className="truncate">{outcome.file_name}</span>
                {outcome.detail && <span className="text-muted-foreground">{outcome.detail}</span>}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
