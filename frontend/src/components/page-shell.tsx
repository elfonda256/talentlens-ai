import { ChevronLeft, ScanSearch } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

type PageShellProps = {
  title: string;
  description?: string;
  back?: { href: string; label: string };
  children: ReactNode;
};

/** Shared page frame: product header, optional back link, page title. */
export function PageShell({ title, description, back, children }: PageShellProps) {
  return (
    <>
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex w-full max-w-5xl items-center gap-3 px-6 py-4">
          <span className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <ScanSearch className="size-5" />
          </span>
          <Link href="/" className="text-lg font-semibold tracking-tight">
            TalentLens AI
          </Link>
          <span className="text-sm text-muted-foreground">AI Recruitment Copilot</span>
        </div>
      </header>
      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-6 py-8">
        <div className="flex flex-col gap-2">
          {back && (
            <Link
              href={back.href}
              className="inline-flex items-center gap-1 self-start text-sm text-muted-foreground hover:text-foreground"
            >
              <ChevronLeft className="size-4" />
              {back.label}
            </Link>
          )}
          <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
          {description && <p className="text-muted-foreground">{description}</p>}
        </div>
        {children}
      </main>
    </>
  );
}
