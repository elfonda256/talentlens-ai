import { CircleCheck, CircleX, Eye } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import type { Recommendation } from "@/lib/api";
import { RECOMMENDATION_LABEL } from "@/lib/labels";

const STYLE = {
  SHORTLIST: { variant: "success", icon: CircleCheck },
  REVIEW: { variant: "warning", icon: Eye },
  REJECT: { variant: "destructive", icon: CircleX },
} as const;

/** The system's verdict. Icon and wording carry the meaning, not colour alone. */
export function RecommendationBadge({ value }: { value: Recommendation }) {
  const { variant, icon: Icon } = STYLE[value];
  return (
    <Badge variant={variant}>
      <Icon aria-hidden="true" />
      {RECOMMENDATION_LABEL[value]}
    </Badge>
  );
}
