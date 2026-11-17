import { formatNumber } from "@/lib/labels";
import { cn } from "@/lib/utils";

type MeterProps = {
  label: string;
  percent: number;
  hint?: string;
  emphasis?: boolean;
};

/** A labelled percentage with a bar. Tone follows the value so weak areas stand out. */
export function Meter({ label, percent, hint, emphasis = false }: MeterProps) {
  const value = Math.min(Math.max(percent, 0), 100);
  const tone =
    value >= 70 ? "bg-success" : value >= 45 ? "bg-warning" : "bg-destructive";
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-baseline justify-between gap-3">
        <span
          className={cn(
            "text-sm",
            emphasis ? "font-semibold" : "text-muted-foreground",
          )}
        >
          {label}
        </span>
        <span
          className={cn(
            "tabular-nums",
            emphasis ? "text-lg font-semibold" : "text-sm font-medium",
          )}
        >
          {formatNumber(value, 0)}%
        </span>
      </div>
      <div
        role="meter"
        aria-label={label}
        aria-valuenow={Math.round(value)}
        aria-valuemin={0}
        aria-valuemax={100}
        className={cn(
          "w-full overflow-hidden rounded-full bg-secondary",
          emphasis ? "h-2.5" : "h-1.5",
        )}
      >
        <div
          className={cn("h-full origin-left animate-grow rounded-full", tone)}
          style={{ width: `${value}%` }}
        />
      </div>
      {hint && <span className="text-xs text-muted-foreground">{hint}</span>}
    </div>
  );
}
