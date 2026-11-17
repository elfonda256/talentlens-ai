"use client";

import { CircleAlert, CircleCheck, Copy, X } from "lucide-react";
import { useState } from "react";

import { FilePicker } from "@/components/file-picker";
import { Button } from "@/components/ui/button";
import { uploadCandidates, type UploadOutcome } from "@/lib/api";

const STATUS = {
  parsed: { text: "Terbaca", icon: CircleCheck, tone: "text-success-ink" },
  duplicate: { text: "Sudah ada", icon: Copy, tone: "text-muted-foreground" },
  failed: {
    text: "Gagal dibaca",
    icon: CircleAlert,
    tone: "text-destructive-ink",
  },
} as const;

type CvUploadButtonProps = {
  jobId: string;
  primary: boolean;
  onUploaded: (outcomes: UploadOutcome[]) => void;
  onError: (error: unknown) => void;
};

/** Uploads one or more CVs and hands the per-file outcomes to the page. */
export function CvUploadButton({
  jobId,
  primary,
  onUploaded,
  onError,
}: CvUploadButtonProps) {
  const [busy, setBusy] = useState(false);

  const handleFiles = async (files: File[]) => {
    setBusy(true);
    try {
      onUploaded(await uploadCandidates(jobId, files));
    } catch (error) {
      onError(error);
    } finally {
      setBusy(false);
    }
  };

  return (
    <FilePicker
      label="Unggah CV"
      busyLabel="Membaca CV…"
      multiple
      busy={busy}
      variant={primary ? "default" : "outline"}
      onFiles={handleFiles}
    />
  );
}

type UploadReportProps = { outcomes: UploadOutcome[]; onDismiss: () => void };

/** What happened to each uploaded file. One unreadable CV never hides the others. */
export function UploadReport({ outcomes, onDismiss }: UploadReportProps) {
  const parsed = outcomes.filter(
    (outcome) => outcome.status === "parsed",
  ).length;
  return (
    <div
      className="rounded-xl border border-border bg-card p-4 sm:px-6"
      role="status"
    >
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm font-medium">
          {parsed} dari {outcomes.length} berkas berhasil dibaca
        </p>
        <Button
          variant="ghost"
          size="sm"
          onClick={onDismiss}
          aria-label="Tutup laporan unggahan"
        >
          <X aria-hidden="true" />
        </Button>
      </div>
      <ul className="mt-2 grid gap-x-8 gap-y-1.5 text-sm sm:grid-cols-2">
        {outcomes.map((outcome, position) => {
          const { text, icon: Icon, tone } = STATUS[outcome.status];
          return (
            <li
              key={`${outcome.file_name}-${position}`}
              className="flex min-w-0 flex-wrap items-center gap-x-3"
            >
              <span
                className={`flex w-28 shrink-0 items-center gap-1.5 font-medium ${tone}`}
              >
                <Icon className="size-4" aria-hidden="true" />
                {text}
              </span>
              <span className="min-w-0 truncate">{outcome.file_name}</span>
              {outcome.status === "failed" && (
                <span className="basis-full text-muted-foreground">
                  {outcome.detail}
                </span>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
