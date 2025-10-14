export default function FactorTooltip({ factors, why }: { factors: any; why: string }) {
  return (
    <div className="mt-3 text-xs text-mute">
      <div className="flex gap-4">
        <span>mom {(factors.mom*100).toFixed(0)}</span>
        <span>qual {(factors.qual*100).toFixed(0)}</span>
        <span>cat {(factors.cat*100).toFixed(0)}</span>
        <span>val {(factors.val*100).toFixed(0)}</span>
      </div>
      <div className="mt-1">{why}</div>
    </div>
  );
}
