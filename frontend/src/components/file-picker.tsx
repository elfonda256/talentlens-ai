"use client";

import { LoaderCircle, Upload } from "lucide-react";
import { useRef } from "react";

import { Button } from "@/components/ui/button";

type FilePickerProps = {
  label: string;
  busyLabel: string;
  multiple?: boolean;
  busy?: boolean;
  variant?: "default" | "outline";
  onFiles: (files: File[]) => void;
};

/** A button that opens the file dialog. Accepts the formats the parser can read. */
export function FilePicker({
  label,
  busyLabel,
  multiple = false,
  busy = false,
  variant = "default",
  onFiles,
}: FilePickerProps) {
  const input = useRef<HTMLInputElement>(null);

  return (
    <>
      <input
        ref={input}
        type="file"
        accept=".pdf,.docx,.txt"
        multiple={multiple}
        className="hidden"
        tabIndex={-1}
        aria-hidden="true"
        onChange={(event) => {
          const files = Array.from(event.target.files ?? []);
          event.target.value = ""; // lets the same file be chosen again
          if (files.length > 0) onFiles(files);
        }}
      />
      <Button
        variant={variant}
        onClick={() => input.current?.click()}
        disabled={busy}
        aria-busy={busy}
      >
        {busy ? (
          <LoaderCircle className="animate-spin" aria-hidden="true" />
        ) : (
          <Upload aria-hidden="true" />
        )}
        {busy ? busyLabel : label}
      </Button>
    </>
  );
}
