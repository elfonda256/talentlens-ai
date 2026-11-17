"use client";

import { Notice } from "@/components/ui/notice";
import { useApi } from "@/hooks/use-api";
import { getHealth } from "@/lib/api";

/** Says so only when the screening service cannot be reached; otherwise shows nothing. */
export function SystemStatus() {
  const { error } = useApi(getHealth);
  if (error === undefined) return null;
  return (
    <Notice tone="error">
      Layanan penyaringan tidak terhubung. Coba muat ulang halaman ini beberapa
      saat lagi.
    </Notice>
  );
}
