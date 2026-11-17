"use client";

import { LoaderCircle, Upload } from "lucide-react";
import { useRef } from "react";

import { Button } from "@/components/ui/button";

type FilePickerProps = {
  label: string;
  multiple?: boolean;
  busy?: boolean;
  onFiles: (files: File[]) => void;
};

/** A button that opens the file dialog. Accepts the formats the parser can read. */
export function FilePicker({ label, multiple = false, busy = false, onFiles }: FilePickerProps) {
  const input = useRef<HTMLInputElement>(null);

  return (
    <>
      <input
        ref={input}
        type="file"
        accept=".pdf,.docx,.txt"
        multiple={multiple}
        className="hidden"
        onChange={(event) => {
          const files = Array.from(event.target.files ?? []);
          event.target.value = ""; // lets the same file be chosen again
          if (files.length > 0) onFiles(files);
        }}
      />
      <Button onClick={() => input.current?.click()} disabled={busy}>
        {busy ? <LoaderCircle className="animate-spin" /> : <Upload />}
        {label}
      </Button>
    </>
  );
}
