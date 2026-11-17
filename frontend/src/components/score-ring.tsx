import type { Recommendation } from "@/lib/api";
import { formatNumber } from "@/lib/labels";
import { cn } from "@/lib/utils";

const TONE: Record<Recommendation, string> = {
  SHORTLIST: "text-success",
  REVIEW: "text-warning",
  REJECT: "text-destructive",
};
const RADIUS = 42;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

type ScoreRingProps = {
  score: number;
  recommendation: Recommendation;
  size?: "sm" | "lg";
  provisional?: boolean;
};

/** The AI score as a ring. The colour follows the decision; the number carries the meaning. */
export function ScoreRing({
  score,
  recommendation,
  size = "sm",
  provisional = false,
}: ScoreRingProps) {
  const filled = (Math.min(Math.max(score, 0), 100) / 100) * CIRCUMFERENCE;
  const large = size === "lg";
  return (
    <div
      className={cn("relative shrink-0", large ? "size-32" : "size-16")}
      role="img"
      aria-label={`Skor AI ${formatNumber(score)} dari 100${provisional ? ", sementara" : ""}`}
    >
      <svg viewBox="0 0 100 100" className="size-full -rotate-90">
        <circle
          cx="50"
          cy="50"
          r={RADIUS}
          fill="none"
          strokeWidth="8"
          className="stroke-secondary"
        />
        <circle
          cx="50"
          cy="50"
          r={RADIUS}
          fill="none"
          strokeWidth="8"
          strokeLinecap="round"
          stroke="currentColor"
          strokeDasharray={`${filled} ${CIRCUMFERENCE}`}
          className={cn(
            "transition-[stroke-dasharray] duration-700",
            TONE[recommendation],
          )}
        />
      </svg>
      <span
        className="absolute inset-0 flex flex-col items-center justify-center leading-none"
        aria-hidden="true"
      >
        <span
          className={cn(
            "font-semibold tabular-nums tracking-tight",
            large ? "text-4xl" : "text-base",
          )}
        >
          {formatNumber(score)}
        </span>
        {large && (
          <span className="mt-1.5 text-xs text-muted-foreground">
            {provisional ? "skor sementara" : "Skor AI"}
          </span>
        )}
      </span>
    </div>
  );
}
