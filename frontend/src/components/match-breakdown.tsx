import {
  CircleCheck,
  CircleDashed,
  CircleX,
  type LucideIcon,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type {
  MatchBreakdown as Breakdown,
  MatchStatus,
  SkillMatch,
} from "@/lib/api";
import { formatFields, formatYears } from "@/lib/labels";
import { cn } from "@/lib/utils";

const STATUS: Record<
  MatchStatus,
  { icon: LucideIcon; tone: string; text: string }
> = {
  matched: { icon: CircleCheck, tone: "text-success", text: "Ditemukan" },
  implied: { icon: CircleDashed, tone: "text-warning", text: "Tersirat" },
  missing: { icon: CircleX, tone: "text-destructive", text: "Tidak ditemukan" },
};

const EDUCATION_TEXT = {
  match: "Sesuai dengan bidang yang diminta",
  related: "Serumpun dengan bidang yang diminta",
  mismatch: "Berbeda dari bidang yang diminta",
  not_required: "Lowongan tidak mensyaratkan bidang tertentu",
} as const;

/** Requirement by requirement: what the job asked for and what the CV shows. */
export function MatchBreakdown({ breakdown }: { breakdown: Breakdown }) {
  const { experience, education } = breakdown;
  const educationStatus: MatchStatus =
    education.status === "mismatch"
      ? "missing"
      : education.status === "related"
        ? "implied"
        : "matched";

  return (
    <Card aria-labelledby="judul-kecocokan">
      <CardHeader>
        <CardTitle id="judul-kecocokan">
          Kecocokan dengan syarat lowongan
        </CardTitle>
      </CardHeader>
      <CardContent className="grid gap-x-8 gap-y-6 md:grid-cols-2">
        <SkillList
          title="Keterampilan wajib"
          skills={breakdown.must_have_skills}
        />
        <div className="flex flex-col gap-6">
          <SkillList
            title="Keterampilan tambahan"
            skills={breakdown.bonus_skills}
          />
          <Group title="Pengalaman">
            <Line
              status={experience.met ? "matched" : "missing"}
              label={`${formatYears(experience.relevant_years)} pengalaman relevan`}
              detail={
                experience.required_years > 0
                  ? `Syarat minimal ${experience.required_years} tahun. Total masa kerja ${formatYears(experience.total_years)}.`
                  : `Tanpa syarat minimal. Total masa kerja ${formatYears(experience.total_years)}.`
              }
            />
          </Group>
          <Group title="Pendidikan">
            <Line
              status={educationStatus}
              label={
                formatFields(education.found_fields) ||
                "Bidang tidak terbaca dari CV"
              }
              detail={
                EDUCATION_TEXT[education.status] +
                (education.required_fields.length > 0
                  ? ` (${formatFields(education.required_fields)}).`
                  : ".") +
                (education.level_below_requirement
                  ? " Jenjangnya di bawah syarat."
                  : "")
              }
            />
          </Group>
        </div>
      </CardContent>
    </Card>
  );
}

function SkillList({ title, skills }: { title: string; skills: SkillMatch[] }) {
  const found = skills.filter((skill) => skill.status !== "missing").length;
  return (
    <Group
      title={title}
      count={skills.length > 0 ? `${found} dari ${skills.length}` : undefined}
    >
      {skills.length === 0 && (
        <p className="text-sm text-muted-foreground">
          Tidak ada pada lowongan ini.
        </p>
      )}
      {skills.map((skill) => (
        <Line
          key={skill.label}
          status={skill.status}
          label={skill.label}
          detail={
            skill.terms.length > 0
              ? `Tertulis di CV: ${skill.terms.join(", ")}`
              : undefined
          }
        />
      ))}
    </Group>
  );
}

function Group({
  title,
  count,
  children,
}: {
  title: string;
  count?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-2.5">
      <h3 className="flex items-baseline justify-between gap-3 text-sm font-semibold">
        {title}
        {count && (
          <span className="font-normal tabular-nums text-muted-foreground">
            {count}
          </span>
        )}
      </h3>
      <ul className="flex flex-col gap-2.5">{children}</ul>
    </div>
  );
}

function Line({
  status,
  label,
  detail,
}: {
  status: MatchStatus;
  label: string;
  detail?: string;
}) {
  const { icon: Icon, tone, text } = STATUS[status];
  return (
    <li className="flex items-start gap-2.5 text-sm">
      <Icon className={cn("mt-0.5 size-4 shrink-0", tone)} aria-hidden="true" />
      <span className="flex min-w-0 flex-col">
        <span className={cn(status === "missing" && "text-muted-foreground")}>
          {label}
          <span className="sr-only">: {text}</span>
        </span>
        {detail && (
          <span className="text-xs text-muted-foreground">{detail}</span>
        )}
      </span>
    </li>
  );
}
