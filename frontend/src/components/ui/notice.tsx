import { CircleAlert, CircleCheck, Info } from "lucide-react";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

const STYLE = {
  error: {
    box: "border-destructive/30 bg-destructive-soft text-destructive-ink",
    icon: CircleAlert,
  },
  success: {
    box: "border-success/30 bg-success-soft text-success-ink",
    icon: CircleCheck,
  },
  info: { box: "border-border bg-secondary text-foreground", icon: Info },
} as const;

type NoticeProps = {
  tone: keyof typeof STYLE;
  children: ReactNode;
  className?: string;
};

/** Inline message for an error, a confirmation or a hint. Errors are announced to screen readers. */
export function Notice({ tone, children, className }: NoticeProps) {
  const { box, icon: Icon } = STYLE[tone];
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      className={cn(
        "flex items-start gap-2.5 rounded-md border px-3.5 py-2.5 text-sm",
        box,
        className,
      )}
    >
      <Icon className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
      <div className="min-w-0">{children}</div>
    </div>
  );
}
