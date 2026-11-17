import { cva, type VariantProps } from "class-variance-authority";
import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-medium [&_svg]:size-3.5 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        secondary: "bg-secondary text-secondary-foreground",
        outline: "border border-border text-foreground",
        brand: "bg-brand-soft text-brand-ink",
        success: "bg-success-soft text-success-ink",
        warning: "bg-warning-soft text-warning-ink",
        destructive: "bg-destructive-soft text-destructive-ink",
      },
    },
    defaultVariants: { variant: "secondary" },
  },
);

type BadgeProps = ComponentProps<"span"> & VariantProps<typeof badgeVariants>;

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
