import { Fragment } from "react";

type HighlightedTextProps = { text: string; terms: string[] };

function escapeForRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Renders text with every occurrence of the given keywords marked. */
export function HighlightedText({ text, terms }: HighlightedTextProps) {
  const unique = [...new Set(terms.filter(Boolean))].sort(
    (a, b) => b.length - a.length,
  );
  if (unique.length === 0) return <>{text}</>;

  // Splitting on a capturing group keeps the matches: odd positions are keywords.
  // Whole words only, so "Architect" is not marked inside "Architecture".
  const alternatives = unique.map(escapeForRegExp).join("|");
  const pattern = new RegExp(
    `(?<![\\p{L}\\p{N}])(${alternatives})(?![\\p{L}\\p{N}])`,
    "giu",
  );
  return (
    <>
      {text
        .split(pattern)
        .map((piece, position) =>
          position % 2 === 1 ? (
            <mark key={position}>{piece}</mark>
          ) : (
            <Fragment key={position}>{piece}</Fragment>
          ),
        )}
    </>
  );
}
