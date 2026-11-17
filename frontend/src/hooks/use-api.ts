"use client";

import { useEffect, useState } from "react";

type ApiState<T> = { data?: T; error?: unknown; loading: boolean };

/**
 * Loads data when the component mounts and whenever `load` changes; `reload` asks again.
 * Pass a `load` function wrapped in `useCallback` so it only changes when its inputs do.
 */
export function useApi<T>(load: () => Promise<T>) {
  const [state, setState] = useState<ApiState<T>>({ loading: true });
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let active = true;
    load().then(
      (data) => active && setState({ data, loading: false }),
      (error: unknown) => active && setState({ error, loading: false }),
    );
    return () => {
      active = false;
    };
  }, [load, version]);

  return { ...state, reload: () => setVersion((current) => current + 1) };
}

export function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "Terjadi galat yang tidak dikenal";
}
