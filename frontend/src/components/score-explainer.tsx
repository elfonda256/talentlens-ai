import { ScoreComposition } from "@/components/score-composition";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { ComponentScore } from "@/lib/api";
import { COMPONENT_COLOR, COMPONENT_LABEL, formatNumber } from "@/lib/labels";
import { cn } from "@/lib/utils";

type ScoreExplainerProps = { components: ComponentScore[]; score: number };

/** Explainable AI: where every point of the final score comes from, and why. */
export function ScoreExplainer({ components, score }: ScoreExplainerProps) {
  const provisional = components.some((part) => !part.assessed);
  return (
    <Card aria-labelledby="judul-skor">
      <CardHeader>
        <CardTitle id="judul-skor">Dari mana skor ini berasal</CardTitle>
        <CardDescription>
          Skor akhir adalah jumlah lima komponen. Setiap komponen punya batas
          poin sendiri, dan dihitung dengan aturan yang sama untuk semua
          kandidat.
          {provisional &&
            " Komponen yang bagian CV-nya tidak terbaca tidak ikut dihitung; bobotnya dibagi ke komponen lain, sehingga skor ini bersifat sementara."}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <ScoreComposition components={components} size="lg" />
        <table className="w-full text-sm">
          <caption className="sr-only">Rincian skor per komponen</caption>
          <thead>
            <tr className="border-b border-border text-left text-xs text-muted-foreground">
              <th scope="col" className="pb-2 font-medium">
                Komponen
              </th>
              <th scope="col" className="hidden pb-2 font-medium sm:table-cell">
                Mengapa
              </th>
              <th scope="col" className="pb-2 text-right font-medium">
                Poin
              </th>
            </tr>
          </thead>
          <tbody>
            {components.map((part) => (
              <tr key={part.key} className="border-b border-border align-top">
                <th scope="row" className="py-3 pr-4 text-left font-medium">
                  <span className="flex items-center gap-2">
                    <span
                      className={cn(
                        "size-2.5 shrink-0 rounded-sm",
                        COMPONENT_COLOR[part.key],
                      )}
                      aria-hidden="true"
                    />
                    {COMPONENT_LABEL[part.key]}
                  </span>
                  <span className="mt-1 block font-normal text-muted-foreground sm:hidden">
                    {part.explanation}
                  </span>
                </th>
                <td className="hidden py-3 pr-4 text-muted-foreground sm:table-cell">
                  {part.explanation}
                </td>
                <td className="whitespace-nowrap py-3 text-right tabular-nums">
                  {part.assessed ? (
                    <>
                      <span className="font-semibold">
                        {formatNumber(part.points)}
                      </span>
                      <span className="text-muted-foreground">
                        {" "}
                        dari {formatNumber(part.max_points)}
                      </span>
                    </>
                  ) : (
                    <span className="text-muted-foreground">Belum dinilai</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <th scope="row" className="pt-3 text-left font-semibold">
                {provisional ? "Skor sementara" : "Skor akhir"}
              </th>
              <td className="hidden sm:table-cell" />
              <td className="whitespace-nowrap pt-3 text-right tabular-nums">
                <span className="text-lg font-semibold">
                  {formatNumber(score)}
                </span>
                <span className="text-muted-foreground">
                  {" "}
                  dari 100{provisional && " (sementara)"}
                </span>
              </td>
            </tr>
          </tfoot>
        </table>
      </CardContent>
    </Card>
  );
}
