import { ChevronLeft } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

const NAV = [
  { section: "dashboard", href: "/", label: "Dashboard" },
  { section: "sources", href: "/sources", label: "Pengumpulan CV" },
] as const;

type Section = (typeof NAV)[number]["section"];

type PageShellProps = {
  title: ReactNode;
  description?: ReactNode;
  back?: { href: string; label: string };
  actions?: ReactNode;
  /** The header link to mark as current. Job and candidate pages belong to the dashboard. */
  section?: Section;
  children: ReactNode;
};

/** Shared page frame: product header, optional back link, page title and page-level actions. */
export function PageShell({
  title,
  description,
  back,
  actions,
  section = "dashboard",
  children,
}: PageShellProps) {
  return (
    <>
      <a
        href="#konten"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:text-sm"
      >
        Lewati ke konten
      </a>
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex w-full max-w-6xl items-center gap-3 px-4 py-3 sm:px-6">
          <Link href="/" className="flex shrink-0 items-center rounded-md">
            <Image
              src="/brand/talentlens-logo.png"
              alt="TalentLens AI"
              width={155}
              height={32}
              priority
              className="h-7 w-auto sm:h-8"
            />
          </Link>
          <span className="hidden border-l border-border pl-3 text-sm text-muted-foreground sm:inline">
            Platform rekrutmen berbasis AI
          </span>
          <nav
            aria-label="Navigasi utama"
            className="ml-auto flex items-center gap-1"
          >
            {NAV.map((item) => (
              <Link
                key={item.section}
                href={item.href}
                aria-current={item.section === section ? "page" : undefined}
                className={cn(
                  "whitespace-nowrap rounded-md px-2 py-2 text-sm font-medium sm:px-3 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground",
                  item.section === section && "bg-secondary text-foreground",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main
        id="konten"
        className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8"
      >
        <div className="flex flex-col gap-3">
          {back && (
            <Link
              href={back.href}
              className="inline-flex items-center gap-1 self-start rounded-md text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              <ChevronLeft className="size-4" aria-hidden="true" />
              {back.label}
            </Link>
          )}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="flex min-w-0 flex-col gap-1.5">
              <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                {title}
              </h1>
              {description && (
                <div className="max-w-2xl text-muted-foreground">
                  {description}
                </div>
              )}
            </div>
            {actions}
          </div>
        </div>
        {children}
      </main>
      <footer className="border-t border-border">
        <p className="mx-auto w-full max-w-6xl px-4 py-4 text-xs text-muted-foreground sm:px-6">
          Skor dihitung dengan aturan yang tetap dan dapat diperiksa. AI hanya
          membantu menjelaskan; keputusan akhir ada pada HR.
        </p>
      </footer>
    </>
  );
}
