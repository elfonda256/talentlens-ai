import type { ComponentScore } from "@/lib/api";
import { COMPONENT_COLOR, COMPONENT_LABEL, formatNumber } from "@/lib/labels";
import { cn } from "@/lib/utils";

type ScoreCompositionProps = {
  components: ComponentScore[];
  size?: "sm" | "lg";
};

/**
 * How the 0-100 score is built. Each segment is as wide as the points that component can give;
 * the filled part is what the candidate earned. The whole bar therefore reads as the final score.
 */
export function ScoreComposition({
  components,
  size = "sm",
}: ScoreCompositionProps) {
  const summary = components
    .map(
      (part) =>
        `${COMPONENT_LABEL[part.key]} ${formatNumber(part.points)} dari ${formatNumber(part.max_points, 0)}`,
    )
    .join(", ");
  return (
    <div
      role="img"
      aria-label={`Susunan skor: ${summary}`}
      className={cn("flex w-full gap-0.5", size === "lg" ? "h-3.5" : "h-2")}
    >
      {components.map((part) => (
        <div
          key={part.key}
          title={`${COMPONENT_LABEL[part.key]}: ${formatNumber(part.points)} dari ${formatNumber(part.max_points, 0)} poin`}
          className="overflow-hidden rounded-sm bg-secondary"
          style={{ width: `${part.max_points}%` }}
        >
          <div
            className={cn(
              "h-full origin-left animate-grow",
              COMPONENT_COLOR[part.key],
            )}
            style={{ width: `${Math.min(part.score_percent, 100)}%` }}
          />
        </div>
      ))}
    </div>
  );
}

/** Colour key for the composition bar. */
export function ScoreLegend({ components }: { components: ComponentScore[] }) {
  return (
    <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
      {components.map((part) => (
        <li key={part.key} className="flex items-center gap-1.5">
          <span
            className={cn("size-2.5 rounded-sm", COMPONENT_COLOR[part.key])}
            aria-hidden="true"
          />
          {COMPONENT_LABEL[part.key]}
        </li>
      ))}
    </ul>
  );
}
