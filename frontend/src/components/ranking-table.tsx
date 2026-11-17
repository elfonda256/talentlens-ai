import { ChevronRight } from "lucide-react";
import Link from "next/link";

import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreComposition } from "@/components/score-composition";
import type { RankingRow } from "@/lib/api";
import { formatNumber, formatYears } from "@/lib/labels";
import { cn } from "@/lib/utils";

type RankingTableProps = { jobId: string; rows: RankingRow[]; reveal: boolean };

/** Ranked candidates. Each row links to the full explanation of that candidate's score. */
export function RankingTable({ jobId, rows, reveal }: RankingTableProps) {
  return (
    <ol className="flex flex-col divide-y divide-border">
      {rows.map((row) => {
        const { highlights } = row;
        const experienceMet =
          highlights.relevant_years >= highlights.required_years;
        const experienceRead = !row.unassessed.includes("experience");
        return (
          <li key={row.candidate_id}>
            <Link
              href={`/jobs/${jobId}/candidates/${row.candidate_id}${reveal ? "?reveal=1" : ""}`}
              className="group grid grid-cols-[2rem_1fr_auto] items-center gap-x-4 gap-y-3 px-4 py-4 transition-colors hover:bg-secondary/60 sm:px-6 lg:grid-cols-[2rem_minmax(9rem,1.1fr)_minmax(13rem,1.4fr)_9rem_9rem_9.5rem_1rem]"
            >
              <span
                className="text-sm tabular-nums text-muted-foreground"
                aria-label={`Peringkat ${row.rank}`}
              >
                {row.rank}
              </span>
              <span className="flex min-w-0 flex-col">
                <span className="truncate font-medium group-hover:underline">
                  {row.name || row.candidate_id}
                </span>
                <span className="truncate text-sm text-muted-foreground">
                  {headline(row)}
                </span>
              </span>
              <span className="col-start-3 row-start-1 lg:hidden">
                <RecommendationBadge value={row.recommendation} />
              </span>

              <span className="col-span-3 flex items-center gap-3 lg:col-span-1">
                <span className="w-12 shrink-0 text-xl font-semibold tabular-nums">
                  {formatNumber(row.score)}
                </span>
                <ScoreComposition components={highlights.components} />
              </span>
              <Fact
                label="Keterampilan wajib"
                value={`${highlights.must_matched} dari ${highlights.must_total}`}
                weak={highlights.must_matched < highlights.must_total / 2}
              />
              <Fact
                label="Pengalaman relevan"
                value={
                  experienceRead
                    ? formatYears(highlights.relevant_years)
                    : "Belum dinilai"
                }
                weak={experienceRead && !experienceMet}
              />
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
    <span className="hidden flex-col lg:flex">
      <span
        className={cn(
          "text-sm font-medium tabular-nums",
          weak && "text-destructive-ink",
        )}
      >
        {value}
      </span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </span>
  );
}
