"use client";

import { BriefcaseBusiness, ChevronRight, FileText } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { FilePicker } from "@/components/file-picker";
import { PageShell } from "@/components/page-shell";
import { SystemStatus } from "@/components/system-status";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { errorMessage, useApi } from "@/hooks/use-api";
import { createJob, listJobs } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const jobs = useApi(listJobs);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");

  const handleJobFile = async ([file]: File[]) => {
    setUploading(true);
    setUploadError("");
    try {
      const job = await createJob(file);
      router.push(`/jobs/${job.job_id}`);
    } catch (error) {
      setUploadError(errorMessage(error));
      setUploading(false);
    }
  };

  return (
    <PageShell
      title="Lowongan"
      description="Mulai dari deskripsi lowongan. Setelah itu unggah CV pelamar, dan sistem menyusun peringkat beserta alasannya."
      actions={
        <FilePicker
          label="Unggah deskripsi lowongan"
          busyLabel="Membaca lowongan…"
          busy={uploading}
          onFiles={handleJobFile}
        />
      }
    >
      <SystemStatus />
      {uploadError && <Notice tone="error">{uploadError}</Notice>}

      <section aria-label="Lowongan tersimpan" className="flex flex-col gap-3">
        {jobs.loading && (
          <>
            <Skeleton className="h-[74px]" />
            <Skeleton className="h-[74px]" />
          </>
        )}
        {jobs.error !== undefined && (
          <Notice tone="error">{errorMessage(jobs.error)}</Notice>
        )}
        {jobs.data?.length === 0 && (
          <EmptyState icon={FileText} title="Belum ada lowongan">
            Unggah berkas deskripsi lowongan (PDF, DOCX, atau TXT). Sistem
            membaca syarat pengalaman, pendidikan, dan keterampilan dari berkas
            itu.
          </EmptyState>
        )}
        {jobs.data?.map((job) => (
          <Link
            key={job.job_id}
            href={`/jobs/${job.job_id}`}
            className="group flex items-center gap-4 rounded-xl border border-border bg-card p-4 transition-colors hover:border-primary/40 hover:bg-secondary/60"
          >
            <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-primary">
              <BriefcaseBusiness className="size-5" aria-hidden="true" />
            </span>
            <span className="flex min-w-0 flex-1 flex-col">
              <span className="truncate font-medium">{job.title}</span>
              <span className="text-sm text-muted-foreground">
                {job.candidate_count === 0
                  ? "Belum ada CV"
                  : `${job.candidate_count} kandidat`}
              </span>
            </span>
            <Badge variant={job.screened ? "success" : "secondary"}>
              {job.screened ? "Sudah disaring" : "Belum disaring"}
            </Badge>
            <ChevronRight
              className="size-4 text-muted-foreground transition-transform group-hover:translate-x-0.5"
              aria-hidden="true"
            />
          </Link>
        ))}
      </section>
    </PageShell>
  );
}
