import clsx from "classnames";

export default function Badge({ children, tone = "default" }: { children: any; tone?: "default"|"green"|"red" }) {
  return (
    <span className={clsx(
      "text-xs px-2 py-0.5 rounded-full border",
      tone === "green" && "border-emerald-400/30 text-emerald-300",
      tone === "red" && "border-rose-400/30 text-rose-300",
      tone === "default" && "border-white/10 text-mute"
    )}>{children}</span>
  );
}
