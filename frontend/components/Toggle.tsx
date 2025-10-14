export default function Toggle({ checked, onChange, label }: { checked: boolean; onChange: (b:boolean)=>void; label?: string }) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className={`flex items-center gap-2 text-sm ${checked ? "text-brand" : "text-mute"}`}
    >
      <span className={`w-10 h-6 rounded-full border border-white/10 relative ${checked ? "bg-brand/30" : "bg-card"}`}>
        <span className={`absolute top-0.5 transition-all ${checked ? "left-5" : "left-1"} w-5 h-5 rounded-full bg-white/80`} />
      </span>
      {label}
    </button>
  );
}
