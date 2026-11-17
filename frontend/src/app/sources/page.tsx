import {
  ArrowDown,
  ArrowRight,
  BadgeCheck,
  BriefcaseBusiness,
  ChevronRight,
  CircleCheck,
  FileUp,
  FolderOpen,
  Globe,
  Mail,
  Search,
  ShieldCheck,
  UsersRound,
  type LucideIcon,
} from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

import { PageShell } from "@/components/page-shell";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export const metadata: Metadata = { title: "Pengumpulan CV · TalentLens AI" };

const FUTURE = "Production Integration (Future Phase)";

type Source = { icon: LucideIcon; name: string; how: string; needs: string };

const COMPANY_CHANNELS: Source[] = [
  {
    icon: Globe,
    name: "Situs karier perusahaan",
    how: "Formulir lamaran di situs karier mengirim CV langsung ke lowongan yang dipilih pelamar.",
    needs: "Formulir lamaran yang terhubung ke API TalentLens.",
  },
  {
    icon: Mail,
    name: "Kotak masuk email",
    how: "Lampiran CV di kotak masuk rekrutmen dibaca dari Microsoft 365 atau Gmail.",
    needs: "Kotak masuk khusus rekrutmen dan izin akses dari admin TI.",
  },
  {
    icon: FolderOpen,
    name: "Folder bersama",
    how: "Folder SharePoint, OneDrive, atau Google Drive dipantau; CV baru masuk sebagai kandidat.",
    needs: "Satu folder per lowongan dan izin baca untuk TalentLens.",
  },
];

const JOB_PORTALS: Source[] = [
  {
    icon: UsersRound,
    name: "LinkedIn",
    how: "Lamaran dari lowongan LinkedIn diteruskan beserta CV-nya.",
    needs: "Persetujuan program mitra integrasi ATS dari LinkedIn.",
  },
  {
    icon: BriefcaseBusiness,
    name: "Jobstreet",
    how: "Pelamar dari iklan Jobstreet diteruskan ke lowongan yang sama.",
    needs: "Akun pemberi kerja dan akses integrasi resmi dari Jobstreet.",
  },
  {
    icon: BadgeCheck,
    name: "Kalibrr",
    how: "Pelamar dari iklan Kalibrr diteruskan ke lowongan yang sama.",
    needs: "Akun pemberi kerja dan akses integrasi resmi dari Kalibrr.",
  },
  {
    icon: Search,
    name: "Indeed",
    how: "Lamaran dari iklan Indeed diteruskan ke lowongan yang sama.",
    needs: "Akun pemberi kerja dan akses integrasi resmi dari Indeed.",
  },
];

const INTEGRATION_STEPS = [
  "Konektor resmi per sumber",
  "Validasi format dan ukuran berkas",
  "Penggabungan kandidat yang melamar dua kali",
  "Pencatatan asal setiap CV",
];

const ENGINE_STEPS = [
  "Pembacaan CV dan penyamaran data pribadi",
  "Pencocokan dengan syarat lowongan",
  "Skor, peringkat, dan rekomendasi",
  "Ringkasan AI untuk hiring manager",
];

const PRINCIPLES = [
  {
    title: "Satu jalur penilaian",
    text: "Parser dan aturan skor yang sama untuk semua sumber, sehingga kandidat dari mana pun dibandingkan dengan adil.",
  },
  {
    title: "Hanya lewat akses resmi",
    text: "Tidak ada scraping situs. Setiap portal dihubungkan lewat program integrasi atau API yang disediakan pemiliknya.",
  },
  {
    title: "Data pribadi tetap terlindungi",
    text: "Nama dan kontak disamarkan sebelum dinilai dan sebelum dikirim ke AI, apa pun sumbernya.",
  },
  {
    title: "Asal kandidat tercatat",
    text: "HR dapat melihat dari saluran mana setiap kandidat datang dan menilai saluran yang paling efektif.",
  },
];

export default function SourcesPage() {
  return (
    <PageShell
      section="sources"
      title="Pengumpulan CV"
      description="Semua sumber lamaran mengalir ke satu proses penyaringan yang sama. Saat ini CV masuk lewat unggahan manual; sumber lain disiapkan sebagai integrasi tahap berikutnya."
    >
      <ActiveSource />
      <Architecture />
      <SourceGroup
        id="saluran-perusahaan"
        title="Saluran perusahaan"
        description="Lamaran yang datang langsung ke perusahaan. Belum terhubung; belum ada CV yang diambil dari saluran ini."
        sources={COMPANY_CHANNELS}
      />
      <SourceGroup
        id="portal-lowongan"
        title="Portal lowongan"
        description="Lamaran dari iklan lowongan di portal kerja. Belum terhubung; belum ada CV yang diambil dari portal ini."
        sources={JOB_PORTALS}
        wide
      />
      <Principles />
    </PageShell>
  );
}

function ActiveSource() {
  return (
    <Card className="flex flex-col gap-4 border-success/40 p-5 sm:flex-row sm:items-center sm:p-6">
      <span className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-success-soft text-success-ink">
        <FileUp className="size-5" aria-hidden="true" />
      </span>
      <div className="flex min-w-0 flex-1 flex-col gap-1">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="font-semibold">Unggah manual</h2>
          <Badge variant="success">
            <CircleCheck aria-hidden="true" />
            Aktif
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground">
          HR mengunggah CV dalam PDF, DOCX, atau TXT di halaman lowongan,
          beberapa berkas sekaligus. Ini satu-satunya jalur yang berjalan saat
          ini.
        </p>
      </div>
      <Link
        href="/"
        className="inline-flex shrink-0 items-center gap-1 self-start rounded-md text-sm font-medium text-primary hover:underline sm:self-center"
      >
        Buka dashboard rekrutmen
        <ChevronRight className="size-4" aria-hidden="true" />
      </Link>
    </Card>
  );
}

/** Sources → integration layer (future) → the screening engine that runs today. */
function Architecture() {
  return (
    <section aria-labelledby="judul-arsitektur" className="flex flex-col gap-3">
      <div className="flex flex-col gap-1">
        <h2 id="judul-arsitektur" className="text-base font-semibold">
          Arsitektur integrasi
        </h2>
        <p className="max-w-3xl text-sm text-muted-foreground">
          Setiap sumber masuk lewat lapisan integrasi, lalu diproses oleh mesin
          penyaringan yang sama. Mesin penyaringan sudah berjalan; lapisan
          integrasi adalah tahap berikutnya.
        </p>
      </div>
      <Card className="p-4 sm:p-6">
        <ol className="grid items-stretch gap-3 lg:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)_auto_minmax(0,1fr)]">
          <Stage title="Sumber lamaran">
            <ul className="flex flex-wrap gap-1.5">
              <li>
                <Badge variant="success">Unggah manual</Badge>
              </li>
              {[...COMPANY_CHANNELS, ...JOB_PORTALS].map((source) => (
                <li key={source.name}>
                  <Badge variant="outline">{source.name}</Badge>
                </li>
              ))}
            </ul>
          </Stage>
          <Flow />
          <Stage title="Lapisan integrasi" future>
            <StepList steps={INTEGRATION_STEPS} />
          </Stage>
          <Flow />
          <Stage title="Mesin penyaringan TalentLens" active>
            <StepList steps={ENGINE_STEPS} />
          </Stage>
        </ol>
        <p className="mt-4 border-t border-border pt-4 text-sm text-muted-foreground">
          Saat ini unggahan manual langsung masuk ke mesin penyaringan. Lapisan
          integrasi akan meneruskan sumber lain ke jalur yang sama, tanpa
          mengubah cara CV dibaca maupun aturan penilaian.
        </p>
      </Card>
    </section>
  );
}

type StageProps = {
  title: string;
  future?: boolean;
  active?: boolean;
  children: ReactNode;
};

function Stage({ title, future, active, children }: StageProps) {
  return (
    <li
      className={cn(
        "flex flex-col gap-3 rounded-lg border p-4",
        future && "border-dashed border-brand/40 bg-brand-soft/40",
        active && "border-success/40 bg-success-soft/40",
        !future && !active && "border-border bg-secondary/40",
      )}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-semibold">{title}</h3>
        {future && <Badge variant="brand">{FUTURE}</Badge>}
        {active && <Badge variant="success">Sudah berjalan</Badge>}
      </div>
      {children}
    </li>
  );
}

function Flow() {
  return (
    <li
      aria-hidden="true"
      className="flex items-center justify-center text-muted-foreground"
    >
      <ArrowDown className="size-5 lg:hidden" />
      <ArrowRight className="hidden size-5 lg:block" />
    </li>
  );
}

function StepList({ steps }: { steps: string[] }) {
  return (
    <ol className="flex flex-col gap-2 text-sm">
      {steps.map((step, index) => (
        <li key={step} className="flex gap-2.5">
          <span className="flex size-5 shrink-0 items-center justify-center rounded-full bg-card text-xs font-medium tabular-nums text-muted-foreground ring-1 ring-border">
            {index + 1}
          </span>
          {step}
        </li>
      ))}
    </ol>
  );
}

type SourceGroupProps = {
  id: string;
  title: string;
  description: string;
  sources: Source[];
  /** Four cards per row on large screens instead of three. */
  wide?: boolean;
};

function SourceGroup({
  id,
  title,
  description,
  sources,
  wide,
}: SourceGroupProps) {
  return (
    <section aria-labelledby={id} className="flex flex-col gap-3">
      <div className="flex flex-col gap-1">
        <h2 id={id} className="text-base font-semibold">
          {title}
        </h2>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      <ul
        className={cn(
          "grid gap-4 md:grid-cols-2",
          wide ? "lg:grid-cols-4" : "lg:grid-cols-3",
        )}
      >
        {sources.map((source) => (
          <li key={source.name}>
            <SourceCard source={source} />
          </li>
        ))}
      </ul>
    </section>
  );
}

function SourceCard({
  source: { icon: Icon, name, how, needs },
}: {
  source: Source;
}) {
  return (
    <Card className="flex h-full flex-col gap-4 p-5">
      <div className="flex items-center gap-3">
        <span className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-secondary text-primary">
          <Icon className="size-5" aria-hidden="true" />
        </span>
        <h3 className="font-semibold">{name}</h3>
      </div>
      <p className="text-sm">{how}</p>
      <p className="text-sm text-muted-foreground">
        <span className="font-medium text-foreground">Kebutuhan: </span>
        {needs}
      </p>
      <div className="mt-auto border-t border-border pt-4">
        <Badge variant="brand" className="whitespace-normal">
          {FUTURE}
        </Badge>
      </div>
    </Card>
  );
}

function Principles() {
  return (
    <section aria-labelledby="judul-prinsip" className="flex flex-col gap-3">
      <h2 id="judul-prinsip" className="text-base font-semibold">
        Prinsip integrasi
      </h2>
      <Card className="p-5 sm:p-6">
        <ul className="grid gap-x-8 gap-y-5 md:grid-cols-2">
          {PRINCIPLES.map((principle) => (
            <li key={principle.title} className="flex gap-3">
              <ShieldCheck
                className="mt-0.5 size-5 shrink-0 text-success"
                aria-hidden="true"
              />
              <span className="flex flex-col gap-1">
                <span className="text-sm font-semibold">{principle.title}</span>
                <span className="text-sm text-muted-foreground">
                  {principle.text}
                </span>
              </span>
            </li>
          ))}
        </ul>
      </Card>
    </section>
  );
}
