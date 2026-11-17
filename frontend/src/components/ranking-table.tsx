import { ChevronRight } from "lucide-react";
import Link from "next/link";

import { CandidateBadges } from "@/components/candidate-badges";
import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreComposition } from "@/components/score-composition";
import { ScoreRing } from "@/components/score-ring";
import type { RankingRow } from "@/lib/api";
import { CONFIDENCE_LABEL, formatYears } from "@/lib/labels";
import { cn } from "@/lib/utils";

type RankingTableProps = { jobId: string; rows: RankingRow[]; reveal: boolean };

/** Ranked candidates. Each row links to the full explanation of that candidate's score. */
export function RankingTable({ jobId, rows, reveal }: RankingTableProps) {
  return (
    <ol className="flex flex-col divide-y divide-border">
      {rows.map((row) => {
        const { highlights, assessment } = row;
        const experienceRead = !row.unassessed.includes("experience");
        const experienceMet =
          highlights.relevant_years >= highlights.required_years;
        return (
          <li key={row.candidate_id}>
            <Link
              href={`/jobs/${jobId}/candidates/${row.candidate_id}${reveal ? "?reveal=1" : ""}`}
              className="group grid grid-cols-[4rem_minmax(0,1fr)] items-center gap-x-4 gap-y-3 px-4 py-4 transition-colors hover:bg-secondary/60 sm:px-6 lg:grid-cols-[1.25rem_4rem_minmax(0,1.25fr)_minmax(0,1fr)_10.5rem_1rem]"
            >
              <span
                className="hidden text-sm tabular-nums text-muted-foreground lg:block"
                aria-label={`Peringkat ${row.rank}`}
              >
                {row.rank}
              </span>
              <ScoreRing
                score={row.score}
                recommendation={row.recommendation}
                provisional={row.unassessed.length > 0}
              />
              <span className="flex min-w-0 flex-col gap-1.5">
                <span className="flex flex-wrap items-center gap-x-2 gap-y-1.5">
                  <span className="truncate font-medium group-hover:underline">
                    <span className="text-muted-foreground lg:hidden">
                      #{row.rank}{" "}
                    </span>
                    {row.name || `Kandidat ${row.candidate_id}`}
                  </span>
                  <CandidateBadges
                    rank={row.rank}
                    recommendation={row.recommendation}
                    assessment={assessment}
                  />
                </span>
                <span className="text-sm text-muted-foreground">
                  {headline(row)}
                </span>
                <span className="lg:hidden">
                  <RecommendationBadge value={row.recommendation} />
                </span>
              </span>

              <span className="col-span-2 flex flex-col gap-2 lg:col-span-1">
                <ScoreComposition components={highlights.components} />
                <span className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
                  <Fact
                    label="Keterampilan wajib"
                    value={`${highlights.must_matched}/${highlights.must_total}`}
                    weak={highlights.must_matched < highlights.must_total / 2}
                  />
                  <Fact
                    label="Pengalaman"
                    value={
                      experienceRead
                        ? formatYears(highlights.relevant_years)
                        : "belum dinilai"
                    }
                    weak={experienceRead && !experienceMet}
                  />
                  <Fact
                    label="Keyakinan AI"
                    value={CONFIDENCE_LABEL[assessment.confidence.level]}
                    weak={assessment.confidence.level === "low"}
                  />
                </span>
              </span>
              <span className="hidden lg:block">
                <RecommendationBadge value={row.recommendation} />
              </span>
              <ChevronRight
                className="hidden size-4 text-muted-foreground transition-transform group-hover:translate-x-0.5 lg:block"
                aria-hidden="true"
              />
            </Link>
          </li>
        );
      })}
    </ol>
  );
}

/** The one thing HR should know about this candidate before opening the detail. */
function headline(row: RankingRow): string {
  const { highlights } = row;
  const missing = highlights.must_total - highlights.must_matched;
  if (row.unassessed.length > 0) {
    return "CV tidak terbaca lengkap, periksa manual";
  }
  if (highlights.relevant_years < highlights.required_years) {
    return "Pengalaman di bawah syarat minimal";
  }
  if (row.knockout_flags.length > 0) return row.knockout_flags[0];
  if (missing > 0) return `${missing} keterampilan wajib belum terlihat di CV`;
  return "Semua syarat wajib terpenuhi";
}

function Fact({
  label,
  value,
  weak,
}: {
  label: string;
  value: string;
  weak: boolean;
}) {
  return (
    <span>
      {label}{" "}
      <span
        className={cn(
          "font-medium tabular-nums text-foreground",
          weak && "text-destructive-ink",
        )}
      >
        {value}
      </span>
    </span>
  );
}
