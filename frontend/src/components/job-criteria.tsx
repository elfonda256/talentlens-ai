import { ChevronDown } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import type { JobProfile, SkillRequirement } from "@/lib/api";
import { formatFields } from "@/lib/labels";

/** What the system understood from the job description. Collapsed by default; HR can check it. */
export function JobCriteria({ job }: { job: JobProfile }) {
  const must = requirementLabels(job.skills, "must");
  const nice = requirementLabels(job.skills, "nice");

  return (
    <details className="group rounded-xl border border-border bg-card">
      <summary className="flex cursor-pointer list-none flex-wrap items-center gap-x-6 gap-y-2 rounded-xl p-4 sm:px-6 [&::-webkit-details-marker]:hidden">
        <span className="font-semibold">Kriteria penilaian</span>
        <span className="text-sm text-muted-foreground">
          {job.min_years_experience > 0
            ? `Pengalaman minimal ${job.min_years_experience} tahun`
            : "Tanpa syarat pengalaman minimal"}
        </span>
        <span className="text-sm text-muted-foreground">
          {must.length} keterampilan wajib, {nice.length} nilai tambah
        </span>
        <ChevronDown
          className="ml-auto size-4 text-muted-foreground transition-transform group-open:rotate-180"
          aria-hidden="true"
        />
      </summary>
      <div className="flex flex-col gap-4 border-t border-border p-4 text-sm sm:px-6">
        <p className="text-muted-foreground">
          Dibaca otomatis dari berkas lowongan. Inilah dasar penilaian semua
          kandidat.
        </p>
        <dl className="grid gap-x-6 gap-y-2 sm:grid-cols-[11rem_1fr]">
          <dt className="text-muted-foreground">Pengalaman minimal</dt>
          <dd className="font-medium">
            {job.min_years_experience > 0
              ? `${job.min_years_experience} tahun`
              : "Tidak disyaratkan"}
          </dd>
          <dt className="text-muted-foreground">Bidang pendidikan</dt>
          <dd className="font-medium">
            {formatFields(job.degree_fields) || "Tidak disyaratkan"}
          </dd>
        </dl>
        <SkillGroup
          title="Keterampilan wajib"
          skills={must}
          variant="secondary"
        />
        <SkillGroup title="Nilai tambah" skills={nice} variant="outline" />
      </div>
    </details>
  );
}

/** Skills written as alternatives in the vacancy ("A / B") count as one requirement. */
function requirementLabels(
  skills: SkillRequirement[],
  priority: "must" | "nice",
): string[] {
  const labels = new Map<string, string[]>();
  for (const skill of skills.filter((item) => item.priority === priority)) {
    const key = skill.group || skill.skill_id;
    labels.set(key, [...(labels.get(key) ?? []), skill.label]);
  }
  return [...labels.values()].map((group) => group.join(" / "));
}

type SkillGroupProps = {
  title: string;
  skills: string[];
  variant: "secondary" | "outline";
};

function SkillGroup({ title, skills, variant }: SkillGroupProps) {
  if (skills.length === 0) return null;
  return (
    <div className="flex flex-col gap-2">
      <span className="text-muted-foreground">{title}</span>
      <ul className="flex flex-wrap gap-2">
        {skills.map((skill) => (
          <li key={skill}>
            <Badge variant={variant}>{skill}</Badge>
          </li>
        ))}
      </ul>
    </div>
  );
}
