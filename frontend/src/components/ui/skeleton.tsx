import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

/** Grey placeholder shown while content loads. Hidden from screen readers. */
export function Skeleton({ className, ...props }: ComponentProps<"div">) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "animate-shimmer rounded-md bg-[linear-gradient(90deg,var(--muted)_25%,var(--border)_50%,var(--muted)_75%)] bg-[length:200%_100%]",
        className,
      )}
      {...props}
    />
  );
}
