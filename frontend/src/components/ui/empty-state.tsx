import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

type EmptyStateProps = { icon: LucideIcon; title: string; children: ReactNode };

/** Shown where a list or result will appear; tells the user what to do next. */
export function EmptyState({ icon: Icon, title, children }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-2 rounded-lg border border-dashed border-border px-6 py-10 text-center">
      <span className="flex size-10 items-center justify-center rounded-full bg-secondary text-muted-foreground">
        <Icon className="size-5" aria-hidden="true" />
      </span>
      <p className="font-medium">{title}</p>
      <p className="max-w-md text-sm text-muted-foreground">{children}</p>
    </div>
  );
}
