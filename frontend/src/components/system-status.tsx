"use client";

import { CircleAlert, CircleCheck, LoaderCircle, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { API_BASE_URL, getHealth, type HealthResponse } from "@/lib/api";

type Status =
  | { state: "checking" }
  | { state: "online"; health: HealthResponse }
  | { state: "offline"; reason: string };

/** Asks the API for its health and turns any failure into an "offline" status. */
async function fetchStatus(): Promise<Status> {
  try {
    return { state: "online", health: await getHealth() };
  } catch (error) {
    return { state: "offline", reason: error instanceof Error ? error.message : "Unknown error" };
  }
}

export function SystemStatus() {
  const [status, setStatus] = useState<Status>({ state: "checking" });

  useEffect(() => {
    let active = true;
    void fetchStatus().then((next) => {
      if (active) setStatus(next);
    });
    return () => {
      active = false;
    };
  }, []);

  const handleCheckAgain = async () => {
    setStatus({ state: "checking" });
    setStatus(await fetchStatus());
  };

  return (
    <Card>
      <CardHeader className="flex-row items-start justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <CardTitle>Backend API</CardTitle>
          <CardDescription>{API_BASE_URL}</CardDescription>
        </div>
        <StatusBadge status={status} />
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <StatusDetails status={status} />
        <Button variant="outline" size="sm" className="self-start" onClick={handleCheckAgain} disabled={status.state === "checking"}>
          <RefreshCw />
          Check again
        </Button>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: Status }) {
  if (status.state === "online") {
    return (
      <Badge variant="success">
        <CircleCheck />
        Online
      </Badge>
    );
  }
  if (status.state === "offline") {
    return (
      <Badge variant="destructive">
        <CircleAlert />
        Offline
      </Badge>
    );
  }
  return (
    <Badge>
      <LoaderCircle className="animate-spin" />
      Checking
    </Badge>
  );
}

function StatusDetails({ status }: { status: Status }) {
  if (status.state === "checking") {
    return <p className="text-sm text-muted-foreground">Contacting the API…</p>;
  }
  if (status.state === "offline") {
    return (
      <p className="text-sm text-muted-foreground">
        The API could not be reached ({status.reason}). Start the backend, then check again.
      </p>
    );
  }
  const { health } = status;
  const rows = [
    ["Application", health.app_name],
    ["Version", health.version],
    ["Environment", health.environment],
    ["Server time", new Date(health.timestamp).toLocaleString()],
  ];
  return (
    <dl className="grid grid-cols-[8rem_1fr] gap-y-2 text-sm">
      {rows.map(([label, value]) => (
        <div key={label} className="contents">
          <dt className="text-muted-foreground">{label}</dt>
          <dd className="font-medium">{value}</dd>
        </div>
      ))}
    </dl>
  );
}
