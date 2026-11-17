"use client";

import { BriefcaseBusiness, ChevronRight } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { FilePicker } from "@/components/file-picker";
import { PageShell } from "@/components/page-shell";
import { SystemStatus } from "@/components/system-status";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
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
      description="Unggah deskripsi lowongan, lalu unggah CV pelamar untuk disaring dan diperingkat."
    >
      <SystemStatus />

      <Card>
        <CardHeader>
          <CardTitle>Unggah deskripsi lowongan</CardTitle>
          <CardDescription>
            PDF, DOCX, atau TXT. Sistem membaca syarat minimal, bidang pendidikan, dan keterampilan.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <div>
            <FilePicker label="Pilih berkas lowongan" busy={uploading} onFiles={handleJobFile} />
          </div>
          {uploadError && <p className="text-sm text-destructive">{uploadError}</p>}
        </CardContent>
      </Card>

      <section className="flex flex-col gap-3">
        <h2 className="text-base font-semibold">Lowongan tersimpan</h2>
        {jobs.loading && <p className="text-sm text-muted-foreground">Memuat…</p>}
        {jobs.error !== undefined && (
          <p className="text-sm text-destructive">{errorMessage(jobs.error)}</p>
        )}
        {jobs.data?.length === 0 && (
          <p className="text-sm text-muted-foreground">Belum ada lowongan. Unggah satu untuk memulai.</p>
        )}
        {jobs.data?.map((job) => (
          <Link key={job.job_id} href={`/jobs/${job.job_id}`}>
            <Card className="transition-colors hover:bg-secondary">
              <CardContent className="flex items-center gap-4 p-4">
                <BriefcaseBusiness className="size-5 text-muted-foreground" />
                <div className="flex flex-1 flex-col">
                  <span className="font-medium">{job.title}</span>
                  <span className="text-sm text-muted-foreground">{job.candidate_count} kandidat</span>
                </div>
                <Badge variant={job.screened ? "success" : "secondary"}>
                  {job.screened ? "Sudah disaring" : "Belum disaring"}
                </Badge>
                <ChevronRight className="size-4 text-muted-foreground" />
              </CardContent>
            </Card>
          </Link>
        ))}
      </section>
    </PageShell>
  );
}
