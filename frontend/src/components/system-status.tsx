"use client";

import { CircleAlert, CircleCheck, LoaderCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { useApi } from "@/hooks/use-api";
import { API_BASE_URL, API_DOCS_URL, getHealth } from "@/lib/api";

const EMBEDDING_MODE: Record<string, string> = {
  auto: "otomatis (E5, cadangan TF-IDF)",
  e5: "multilingual-e5-small",
  tfidf: "TF-IDF",
};

/** One-line health strip: is the API reachable, and which AI components are configured. */
export function SystemStatus() {
  const { data: health, error, loading } = useApi(getHealth);

  if (loading) {
    return (
      <Badge className="self-start">
        <LoaderCircle className="animate-spin" />
        Menghubungi API
      </Badge>
    );
  }
  if (error || !health) {
    return (
      <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
        <Badge variant="destructive">
          <CircleAlert />
          API tidak terhubung
        </Badge>
        <span>Jalankan backend di {API_BASE_URL}, lalu muat ulang halaman.</span>
      </div>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-muted-foreground">
      <Badge variant="success">
        <CircleCheck />
        API terhubung
      </Badge>
      <span>Embedding: {EMBEDDING_MODE[health.embedding_backend] ?? health.embedding_backend}</span>
      <span>Ringkasan AI: {health.llm_summary ? "Gemini aktif" : "templat (kunci Gemini belum diatur)"}</span>
      <a href={API_DOCS_URL} target="_blank" rel="noreferrer" className="underline underline-offset-4">
        Dokumentasi API
      </a>
    </div>
  );
}
