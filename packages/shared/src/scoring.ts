export function fairEVSales(sector: string | null | undefined, yoy: number | null | undefined) {
  const g = (yoy ?? 0);
  let lo = 1.0, hi = 2.0;
  if (g < 0)        { lo = 0.8; hi = 1.2; }
  else if (g < 0.1) { lo = 1.0; hi = 1.8; }
  else if (g < 0.3) { lo = 1.5; hi = 2.5; }
  else              { lo = 2.0; hi = 3.5; }

  const s = (sector || "").toLowerCase();
  let mult = 1.0;
  if (/(software|ai|saas)/.test(s)) mult = 1.2;
  if (/(energy|materials|mining)/.test(s)) mult = 0.8;

  return { lo: +(lo*mult).toFixed(2), hi: +(hi*mult).toFixed(2) };
}

export function fairPriceFromEVS(
  evSalesCur: number | null | undefined,
  mcap: number | null | undefined,
  price: number | null | undefined,
  sector: string | null | undefined,
  yoy: number | null | undefined
) {
  if (!evSalesCur || !mcap || !price) return null;
  const band = fairEVSales(sector, yoy);
  const mid = (band.lo + band.hi) / 2;
  // Antag EV ≈ Market Cap för penny names (skuld/kassa ofta okänd) => price scales med EV/Sales
  const fairPriceMid = +(price * (mid / evSalesCur)).toFixed(2);
  const fairPriceLo  = +(price * (band.lo / evSalesCur)).toFixed(2);
  const fairPriceHi  = +(price * (band.hi / evSalesCur)).toFixed(2);
  const upsideMid = +(((fairPriceMid / price) - 1) * 100).toFixed(0);
  return { band, fairPriceLo, fairPriceMid, fairPriceHi, upsideMid };
}
