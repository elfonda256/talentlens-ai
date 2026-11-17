import { Badge } from "@/components/ui/badge";
import type { Recommendation } from "@/lib/api";
import { RECOMMENDATION_LABEL } from "@/lib/labels";

const VARIANT = { SHORTLIST: "success", REVIEW: "warning", REJECT: "destructive" } as const;

export function RecommendationBadge({ value }: { value: Recommendation }) {
  return <Badge variant={VARIANT[value]}>{RECOMMENDATION_LABEL[value]}</Badge>;
}
