"use client";

import { CircleCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Notice } from "@/components/ui/notice";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { API_BASE_URL, getHealth } from "@/lib/api";

const EMBEDDING_MODE: Record<string, string> = {
  auto: "model E5 (cadangan TF-IDF)",
  e5: "model E5",
  tfidf: "TF-IDF",
};

/** One-line health strip: is the service reachable, and which AI components are switched on. */
export function SystemStatus() {
  const { data: health, error, loading } = useApi(getHealth);

  if (loading) return <Skeleton className="h-6 w-72" />;
  if (error || !health) {
    return (
      <Notice tone="error">
        Layanan tidak terhubung. Jalankan backend di {API_BASE_URL}, lalu muat
        ulang halaman ini.
      </Notice>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-muted-foreground">
      <Badge variant="success">
        <CircleCheck aria-hidden="true" />
        Layanan terhubung
      </Badge>
      <span>
        Pencocokan makna:{" "}
        {EMBEDDING_MODE[health.embedding_backend] ?? health.embedding_backend}
      </span>
      <span>
        Ringkasan AI: {health.llm_summary ? "Gemini aktif" : "templat bawaan"}
      </span>
    </div>
  );
}
