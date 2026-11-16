import { BookOpenText, ScanSearch } from "lucide-react";

import { SystemStatus } from "@/components/system-status";
import { API_DOCS_URL } from "@/lib/api";

export default function HomePage() {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-8 px-6 py-16">
      <header className="flex flex-col gap-3">
        <div className="flex items-center gap-3">
          <span className="flex size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <ScanSearch className="size-5" />
          </span>
          <h1 className="text-2xl font-semibold tracking-tight">TalentLens AI</h1>
        </div>
        <p className="text-muted-foreground">
          Enterprise AI Recruitment Copilot. This page confirms that the frontend and the API can
          talk to each other.
        </p>
      </header>

      <SystemStatus />

      <a
        href={API_DOCS_URL}
        target="_blank"
        rel="noreferrer"
        className="inline-flex items-center gap-2 self-start text-sm font-medium text-primary underline-offset-4 hover:underline"
      >
        <BookOpenText className="size-4" />
        Open the API documentation (Swagger)
      </a>
    </main>
  );
}
