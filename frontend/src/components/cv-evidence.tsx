import { TriangleAlert } from "lucide-react";

import { HighlightedText } from "@/components/highlighted-text";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { CandidateDetail, ExperienceRelevance } from "@/lib/api";
import { formatNumber, readable } from "@/lib/labels";

const RELEVANCE = {
  relevant: { text: "Relevan", variant: "success" },
  partial: { text: "Sebagian relevan", variant: "warning" },
  not_relevant: { text: "Tidak dihitung", variant: "outline" },
} as const;

/** The CV itself, with the words that matched the job marked, next to what is still unmet. */
export function CvEvidence({ detail }: { detail: CandidateDetail }) {
  const { breakdown, result } = detail;
  const allTerms = [
    ...breakdown.must_have_skills,
    ...breakdown.bonus_skills,
  ].flatMap((skill) => skill.terms);

  return (
    <Card aria-labelledby="judul-bukti">
      <CardHeader>
        <CardTitle id="judul-bukti">Bukti dari CV</CardTitle>
        <CardDescription>
          Kata yang cocok dengan syarat lowongan{" "}
          <mark>ditandai seperti ini</mark>.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-6">
        {breakdown.unmet_requirements.length > 0 && (
          <div className="rounded-lg border border-warning/40 bg-warning-soft p-4">
            <h3 className="flex items-center gap-2 text-sm font-semibold text-warning-ink">
              <TriangleAlert className="size-4" aria-hidden="true" />
              Syarat yang belum terpenuhi
            </h3>
            <ul className="mt-2 flex list-disc flex-col gap-1 pl-5 text-sm text-warning-ink">
              {breakdown.unmet_requirements.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex flex-col gap-3">
          <h3 className="text-sm font-semibold">Riwayat pekerjaan</h3>
          {breakdown.experiences.length === 0 && (
            <p className="text-sm text-muted-foreground">
              Bagian pengalaman kerja tidak terbaca dari CV ini.
            </p>
          )}
          {breakdown.experiences.map((role) => (
            <Role key={`${role.title}-${role.start}`} role={role} />
          ))}
        </div>

        <div className="flex flex-col gap-3">
          <h3 className="text-sm font-semibold">
            Kalimat CV yang paling mendukung tiap syarat
          </h3>
          <ul className="flex flex-col gap-3">
            {result.evidence.slice(0, 4).map((item) => (
              <li
                key={item.requirement}
                className="flex flex-col gap-1 border-l-2 border-border pl-3 text-sm"
              >
                <span className="text-muted-foreground">
                  {item.requirement}
                </span>
                <span>
                  <HighlightedText
                    text={readable(item.best_match)}
                    terms={allTerms}
                  />
                </span>
                <span className="text-xs text-muted-foreground">
                  Kemiripan makna {formatNumber(item.similarity * 100, 0)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}

function Role({ role }: { role: ExperienceRelevance }) {
  const { text, variant } = RELEVANCE[role.relevance];
  const period = `${role.start} sampai ${role.end === "present" ? "sekarang" : role.end}`;
  return (
    <article className="rounded-lg border border-border p-4">
      <div className="flex flex-wrap items-start justify-between gap-x-4 gap-y-1">
        <div className="min-w-0">
          <p className="font-medium">
            <HighlightedText
              text={role.title || "Jabatan tidak terbaca"}
              terms={role.terms}
            />
          </p>
          <p className="text-sm text-muted-foreground">
            {[role.company, period].filter(Boolean).join(", ")}
          </p>
        </div>
        <Badge variant={variant}>{text}</Badge>
      </div>
      {role.description && (
        <ul className="mt-3 flex list-disc flex-col gap-1 pl-5 text-sm marker:text-muted-foreground">
          {role.description.split("\n").map((line) => (
            <li key={line}>
              <HighlightedText text={line} terms={role.terms} />
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}
