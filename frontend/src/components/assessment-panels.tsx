import {
  CircleCheck,
  CircleX,
  Eye,
  Gauge,
  ShieldAlert,
  type LucideIcon,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Assessment, ConfidenceLevel, Recommendation } from "@/lib/api";
import { CONFIDENCE_LABEL } from "@/lib/labels";
import { cn } from "@/lib/utils";

const DECISION: Record<Recommendation, { icon: LucideIcon; tone: string }> = {
  SHORTLIST: { icon: CircleCheck, tone: "text-success" },
  REVIEW: { icon: Eye, tone: "text-warning" },
  REJECT: { icon: CircleX, tone: "text-destructive" },
};
const BARS: Record<ConfidenceLevel, number> = { high: 3, medium: 2, low: 1 };
const BAR_TONE: Record<ConfidenceLevel, string> = {
  high: "bg-success",
  medium: "bg-warning",
  low: "bg-destructive",
};

/** Next step, how firm the assessment is, and what to check first: one row of three cards. */
export function AssessmentPanels({ assessment }: { assessment: Assessment }) {
  return (
    <div className="grid gap-6 md:grid-cols-3">
      <HiringPanel hiring={assessment.hiring} />
      <ConfidencePanel confidence={assessment.confidence} />
      <RisksPanel risks={assessment.risks} />
    </div>
  );
}

function HiringPanel({ hiring }: { hiring: Assessment["hiring"] }) {
  const { icon: Icon, tone } = DECISION[hiring.decision];
  return (
    <Card aria-labelledby="judul-tindak-lanjut">
      <CardHeader className="pb-3">
        <CardTitle
          id="judul-tindak-lanjut"
          className="text-sm text-muted-foreground"
        >
          Rekomendasi tindak lanjut
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <p className="flex items-center gap-2 text-lg font-semibold leading-snug">
          <Icon className={cn("size-5 shrink-0", tone)} aria-hidden="true" />
          {hiring.title}
        </p>
        <p className="text-sm text-muted-foreground">{hiring.summary}</p>
        <ol className="flex list-decimal flex-col gap-1.5 pl-5 text-sm marker:text-muted-foreground">
          {hiring.next_steps.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}

function ConfidencePanel({
  confidence,
}: {
  confidence: Assessment["confidence"];
}) {
  const filled = BARS[confidence.level];
  return (
    <Card aria-labelledby="judul-keyakinan">
      <CardHeader className="pb-3">
        <CardTitle
          id="judul-keyakinan"
          className="text-sm text-muted-foreground"
        >
          Keyakinan AI
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <p className="flex items-center gap-3 text-lg font-semibold">
          <Gauge className="size-5 text-primary" aria-hidden="true" />
          {CONFIDENCE_LABEL[confidence.level]}
          <span className="flex items-end gap-1" aria-hidden="true">
            {[1, 2, 3].map((bar) => (
              <span
                key={bar}
                className={cn(
                  "w-1.5 rounded-sm",
                  bar === 1 ? "h-2" : bar === 2 ? "h-3" : "h-4",
                  bar <= filled ? BAR_TONE[confidence.level] : "bg-secondary",
                )}
              />
            ))}
          </span>
        </p>
        <ul className="flex list-disc flex-col gap-1.5 pl-5 text-sm marker:text-muted-foreground">
          {confidence.reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
        <p className="text-xs text-muted-foreground">
          Diukur dari kelengkapan pembacaan CV dan jarak skor dari batas
          keputusan.
        </p>
      </CardContent>
    </Card>
  );
}

function RisksPanel({ risks }: { risks: string[] }) {
  return (
    <Card aria-labelledby="judul-risiko">
      <CardHeader className="pb-3">
        <CardTitle id="judul-risiko" className="text-sm text-muted-foreground">
          Potensi risiko
        </CardTitle>
      </CardHeader>
      <CardContent>
        {risks.length === 0 ? (
          <p className="flex items-center gap-2 text-sm">
            <CircleCheck className="size-4 text-success" aria-hidden="true" />
            Tidak ada risiko khusus yang terlihat dari CV.
          </p>
        ) : (
          <ul className="flex flex-col gap-2.5 text-sm">
            {risks.map((risk) => (
              <li key={risk} className="flex items-start gap-2">
                <ShieldAlert
                  className="mt-0.5 size-4 shrink-0 text-warning"
                  aria-hidden="true"
                />
                {risk}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
