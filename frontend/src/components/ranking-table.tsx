import Link from "next/link";

import { RecommendationBadge } from "@/components/recommendation-badge";
import { ScoreBar } from "@/components/score-bar";
import type { RankingRow } from "@/lib/api";

type RankingTableProps = { jobId: string; rows: RankingRow[]; reveal: boolean };

export function RankingTable({ jobId, rows, reveal }: RankingTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border text-left text-muted-foreground">
            <th className="w-10 py-2 font-medium">#</th>
            <th className="py-2 font-medium">Kandidat</th>
            <th className="w-16 py-2 font-medium">Skor</th>
            <th className="w-40 py-2 font-medium" aria-label="Grafik skor" />
            <th className="w-36 py-2 font-medium">Rekomendasi</th>
            <th className="py-2 font-medium">Alasan utama</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.candidate_id} className="border-b border-border last:border-0">
              <td className="py-3 text-muted-foreground">{row.rank}</td>
              <td className="py-3 pr-4">
                <Link
                  href={`/jobs/${jobId}/candidates/${row.candidate_id}${reveal ? "?reveal=1" : ""}`}
                  className="font-medium text-primary underline-offset-4 hover:underline"
                >
                  {row.name || row.candidate_id}
                </Link>
                {row.extraction_method === "ocr" && (
                  <span className="ml-2 text-xs text-muted-foreground">OCR</span>
                )}
              </td>
              <td className="py-3 font-semibold tabular-nums">{row.score.toFixed(1)}</td>
              <td className="py-3 pr-4">
                <ScoreBar fraction={row.score / 100} />
              </td>
              <td className="py-3">
                <RecommendationBadge value={row.recommendation} />
              </td>
              <td className="py-3 text-muted-foreground">{row.knockout_flags[0] ?? row.reasons[0]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
