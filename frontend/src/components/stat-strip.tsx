import {
  CircleCheck,
  CircleX,
  Eye,
  Users,
  type LucideIcon,
} from "lucide-react";

import type { Recommendation } from "@/lib/api";
import { cn } from "@/lib/utils";

export type RankingFilter = Recommendation | "ALL";

type StatStripProps = {
  counts: Record<RankingFilter, number>;
  active: RankingFilter;
  onSelect: (filter: RankingFilter) => void;
};

const STATS: {
  key: RankingFilter;
  label: string;
  icon: LucideIcon;
  tone: string;
}[] = [
  { key: "ALL", label: "Total kandidat", icon: Users, tone: "text-primary" },
  {
    key: "SHORTLIST",
    label: "Direkomendasikan",
    icon: CircleCheck,
    tone: "text-success",
  },
  { key: "REVIEW", label: "Perlu ditinjau", icon: Eye, tone: "text-warning" },
  {
    key: "REJECT",
    label: "Tidak lolos",
    icon: CircleX,
    tone: "text-destructive",
  },
];

/** Screening totals. Each figure also filters the ranking below it. */
export function StatStrip({ counts, active, onSelect }: StatStripProps) {
  return (
    <div
      role="group"
      aria-label="Ringkasan hasil dan penyaring peringkat"
      className="grid grid-cols-2 overflow-hidden rounded-xl border border-border bg-card lg:grid-cols-4"
    >
      {STATS.map(({ key, label, icon: Icon, tone }) => (
        <button
          key={key}
          type="button"
          aria-pressed={active === key}
          onClick={() => onSelect(key)}
          className={cn(
            "flex cursor-pointer items-center gap-3 border-border p-4 text-left transition-colors hover:bg-secondary/70 sm:px-5",
            "border-b even:border-l lg:border-b-0 lg:border-l lg:first:border-l-0",
            active === key && "bg-secondary",
          )}
        >
          <Icon className={cn("size-5 shrink-0", tone)} aria-hidden="true" />
          <span className="flex flex-col">
            <span className="text-2xl font-semibold leading-none tabular-nums">
              {counts[key]}
            </span>
            <span className="mt-1 text-sm text-muted-foreground">{label}</span>
          </span>
        </button>
      ))}
    </div>
  );
}
