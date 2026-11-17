"use client";

import {
  BriefcaseBusiness,
  ChevronRight,
  CircleCheck,
  Eye,
  FileUp,
  ListChecks,
  Users,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { FilePicker } from "@/components/file-picker";
import { PageShell } from "@/components/page-shell";
import { SystemStatus } from "@/components/system-status";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { errorMessage, useApi } from "@/hooks/use-api";
import { createJob, listJobs, type JobSummary } from "@/lib/api";
import { cn } from "@/lib/utils";

export default function DashboardPage() {
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
      title="Dasbor rekrutmen"
      description="Pantau lowongan aktif dan hasil penyaringan kandidat di satu tempat."
      actions={
        <FilePicker
          label="Tambah lowongan"
          busyLabel="Membaca lowongan…"
          busy={uploading}
          onFiles={handleJobFile}
        />
      }
    >
      <SystemStatus />
      {uploadError && <Notice tone="error">{uploadError}</Notice>}
      {jobs.error !== undefined && (
        <Notice tone="error">{errorMessage(jobs.error)}</Notice>
      )}

      {jobs.loading && (
        <>
          <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            {[1, 2, 3, 4].map((key) => (
              <Skeleton key={key} className="h-[92px]" />
            ))}
          </div>
          <Skeleton className="h-36" />
        </>
      )}

      {jobs.data && jobs.data.length === 0 && <GettingStarted />}

      {jobs.data && jobs.data.length > 0 && (
        <>
          <Overview jobs={jobs.data} />
          <section
            aria-labelledby="judul-lowongan"
            className="flex flex-col gap-3"
          >
            <h2 id="judul-lowongan" className="text-base font-semibold">
              Lowongan
            </h2>
            <div className="grid gap-4 lg:grid-cols-2">
              {jobs.data.map((job) => (
                <JobCard key={job.job_id} job={job} />
              ))}
            </div>
          </section>
        </>
      )}
    </PageShell>
  );
}

/** Totals across every vacancy: the first thing a recruiter looks at in the morning. */
function Overview({ jobs }: { jobs: JobSummary[] }) {
  const sum = (pick: (job: JobSummary) => number) =>
    jobs.reduce((total, job) => total + pick(job), 0);
  const items: {
    label: string;
    value: number;
    icon: LucideIcon;
    tone: string;
  }[] = [
    {
      label: "Lowongan aktif",
      value: jobs.length,
      icon: BriefcaseBusiness,
      tone: "text-primary",
    },
    {
      label: "Total kandidat",
      value: sum((j) => j.candidate_count),
      icon: Users,
      tone: "text-brand",
    },
    {
      label: "Direkomendasikan",
      value: sum((j) => j.shortlist),
      icon: CircleCheck,
      tone: "text-success",
    },
    {
      label: "Perlu ditinjau",
      value: sum((j) => j.review),
      icon: Eye,
      tone: "text-warning",
    },
  ];
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {items.map(({ label, value, icon: Icon, tone }) => (
        <Card key={label} className="flex items-center gap-4 p-4 sm:p-5">
          <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-secondary">
            <Icon className={cn("size-5", tone)} aria-hidden="true" />
          </span>
          <span className="flex flex-col">
            <span className="text-2xl font-semibold tabular-nums leading-none">
              {value}
            </span>
            <span className="mt-1 text-sm text-muted-foreground">{label}</span>
          </span>
        </Card>
      ))}
    </div>
  );
}

const SEGMENTS = [
  { key: "shortlist", label: "direkomendasikan", color: "bg-success" },
  { key: "review", label: "perlu ditinjau", color: "bg-warning" },
  { key: "reject", label: "tidak lolos", color: "bg-destructive" },
] as const;

function JobCard({ job }: { job: JobSummary }) {
  const screenedTotal = job.shortlist + job.review + job.reject;
  return (
    <Link
      href={`/jobs/${job.job_id}`}
      className="group flex flex-col gap-4 rounded-xl border border-border bg-card p-5 transition-colors hover:border-primary/40 hover:bg-secondary/40"
    >
      <span className="flex items-start gap-4">
        <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-primary">
          <BriefcaseBusiness className="size-5" aria-hidden="true" />
        </span>
        <span className="flex min-w-0 flex-1 flex-col">
          <span className="truncate font-semibold group-hover:underline">
            {job.title}
          </span>
          <span className="text-sm text-muted-foreground">
            {job.candidate_count === 0
              ? "Belum ada CV"
              : `${job.candidate_count} kandidat`}
          </span>
        </span>
        <Badge variant={job.screened ? "success" : "secondary"}>
          {job.screened ? "Sudah disaring" : "Menunggu penyaringan"}
        </Badge>
      </span>

      {job.screened && screenedTotal > 0 ? (
        <span className="flex flex-col gap-2">
          <span
            className="flex h-2 overflow-hidden rounded-full bg-secondary"
            role="img"
            aria-label={SEGMENTS.map((s) => `${job[s.key]} ${s.label}`).join(
              ", ",
            )}
          >
            {SEGMENTS.map((s) => (
              <span
                key={s.key}
                className={s.color}
                style={{ width: `${(job[s.key] / screenedTotal) * 100}%` }}
              />
            ))}
          </span>
          <span className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
            {SEGMENTS.map((s) => (
              <span key={s.key} className="flex items-center gap-1.5">
                <span
                  className={cn("size-2 rounded-full", s.color)}
                  aria-hidden="true"
                />
                <span className="font-medium tabular-nums text-foreground">
                  {job[s.key]}
                </span>
                {s.label}
              </span>
            ))}
          </span>
        </span>
      ) : (
        <span className="text-sm text-muted-foreground">
          {job.candidate_count === 0
            ? "Unggah CV pelamar untuk mulai menyaring."
            : "Jalankan penyaringan untuk melihat peringkat."}
        </span>
      )}

      <span className="flex items-center gap-1 text-sm font-medium text-primary">
        {job.screened ? "Lihat peringkat" : "Buka lowongan"}
        <ChevronRight
          className="size-4 transition-transform group-hover:translate-x-0.5"
          aria-hidden="true"
        />
      </span>
    </Link>
  );
}

const STEPS = [
  {
    icon: FileUp,
    title: "Tambahkan lowongan",
    text: "Unggah deskripsi lowongan. Syarat pengalaman, pendidikan, dan keterampilan dibaca otomatis.",
  },
  {
    icon: Users,
    title: "Unggah CV pelamar",
    text: "Beberapa berkas sekaligus, dalam PDF, DOCX, atau TXT. Data pribadi dipisahkan sebelum dinilai.",
  },
  {
    icon: ListChecks,
    title: "Tinjau peringkat",
    text: "Setiap kandidat mendapat skor, rekomendasi, dan penjelasan yang dapat diperiksa.",
  },
];

function GettingStarted() {
  return (
    <section aria-labelledby="judul-mulai" className="flex flex-col gap-4">
      <h2 id="judul-mulai" className="text-base font-semibold">
        Mulai dalam tiga langkah
      </h2>
      <ol className="grid gap-4 md:grid-cols-3">
        {STEPS.map(({ icon: Icon, title, text }, index) => (
          <li key={title}>
            <Card className="flex h-full flex-col gap-3 p-5">
              <span className="flex items-center gap-3">
                <span className="flex size-9 items-center justify-center rounded-lg bg-brand-soft text-brand-ink">
                  <Icon className="size-4.5" aria-hidden="true" />
                </span>
                <span className="text-sm text-muted-foreground">
                  Langkah {index + 1}
                </span>
              </span>
              <span className="font-semibold">{title}</span>
              <span className="text-sm text-muted-foreground">{text}</span>
            </Card>
          </li>
        ))}
      </ol>
    </section>
  );
}
