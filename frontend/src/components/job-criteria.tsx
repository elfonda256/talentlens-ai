import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { JobProfile } from "@/lib/api";

/** What the system understood from the job description. Shown so HR can check it. */
export function JobCriteria({ job }: { job: JobProfile }) {
  const must = job.skills.filter((skill) => skill.priority === "must");
  const nice = job.skills.filter((skill) => skill.priority === "nice");

  return (
    <Card>
      <CardHeader>
        <CardTitle>Kriteria yang terbaca dari lowongan</CardTitle>
        <CardDescription>Inilah dasar penilaian. Periksa sebelum menjalankan screening.</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4 text-sm">
        <dl className="grid grid-cols-[11rem_1fr] gap-y-2">
          <dt className="text-muted-foreground">Pengalaman minimal</dt>
          <dd className="font-medium">
            {job.min_years_experience > 0 ? `${job.min_years_experience} tahun` : "Tidak disyaratkan"}
          </dd>
          <dt className="text-muted-foreground">Bidang pendidikan</dt>
          <dd className="font-medium">{job.degree_fields.join(", ") || "Tidak disyaratkan"}</dd>
        </dl>
        <SkillGroup title="Keterampilan wajib" skills={must.map((s) => s.label)} variant="secondary" />
        <SkillGroup title="Nilai tambah" skills={nice.map((s) => s.label)} variant="outline" />
      </CardContent>
    </Card>
  );
}

type SkillGroupProps = { title: string; skills: string[]; variant: "secondary" | "outline" };

function SkillGroup({ title, skills, variant }: SkillGroupProps) {
  if (skills.length === 0) return null;
  return (
    <div className="flex flex-col gap-2">
      <span className="text-muted-foreground">{title}</span>
      <div className="flex flex-wrap gap-2">
        {skills.map((skill) => (
          <Badge key={skill} variant={variant}>
            {skill}
          </Badge>
        ))}
      </div>
    </div>
  );
}
