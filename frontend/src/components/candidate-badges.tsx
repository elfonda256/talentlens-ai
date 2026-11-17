import { Star, Trophy } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import type { Assessment, Recommendation } from "@/lib/api";

type CandidateBadgesProps = {
  rank: number;
  recommendation: Recommendation;
  assessment: Assessment;
};

/**
 * Highlights on top of the decision.
 * "Paling cocok": the top-ranked candidate, if recommended.
 * "Sangat direkomendasikan": recommended with a clear margin and a firm assessment.
 */
export function CandidateBadges({
  rank,
  recommendation,
  assessment,
}: CandidateBadgesProps) {
  const bestMatch = rank === 1 && recommendation === "SHORTLIST";
  if (!bestMatch && !assessment.highly_recommended) return null;
  return (
    <span className="flex flex-wrap gap-1.5">
      {bestMatch && (
        <Badge variant="brand">
          <Trophy aria-hidden="true" />
          Paling cocok
        </Badge>
      )}
      {assessment.highly_recommended && (
        <Badge variant="success">
          <Star aria-hidden="true" />
          Sangat direkomendasikan
        </Badge>
      )}
    </span>
  );
}
