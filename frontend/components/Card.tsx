import { ReactNode } from "react";

export default function Card({ children }: { children: ReactNode }) {
  return (
    <div className="bg-card/80 rounded-2xl p-4 border border-white/5 shadow-sm">
      {children}
    </div>
  );
}
