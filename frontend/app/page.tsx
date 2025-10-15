"use client";

import { useEffect, useState } from "react";
import Card from "@/components/Card";
import Table from "@/components/Table";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [exchange, setExchange] = useState("US");
  const [query, setQuery] = useState("");
  const [filtered, setFiltered] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // För text i rubrik beroende på börs
  const formatExchange = (ex: string) =>
    ex === "ST" ? "🇸🇪 Svenska marknaden" : "🇺🇸 Amerikanska marknaden";

  // Hämta data från API
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/screener?exchange=${exchange}&limit=20`
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json.top || []);
      setFiltered(json.top || []);
    } catch (err: any) {
      console.error(err);
      setError("Kunde inte hämta data från API");
    } finally {
      setLoading(false);
    }
  };

  // Kör vid laddning eller när börs ändras
  useEffect(() => {
    fetchData();
  }, [exchange]);

  // Filtrering för sök
  useEffect(() => {
    if (!query) {
      setFiltered(data);
    } else {
      const q = query.toLowerCase();
      setFiltered(
        data.filter(
          (s) =>
            s.symbol.toLowerCase().includes(q) ||
            (s.name && s.name.toLowerCase().includes(q))
        )
      );
    }
  }, [query, data]);

  return (
    <main className="p-6 bg-neutral-950 min-h-screen text-neutral-100">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-neutral-100">
          se <span className="text-green-400">tintel</span>{" "}
          <span className="text-sm text-neutral-400">
            trader intelligence
          </span>
          <br />
          <span className="text-xs text-neutral-500">
            Top 20 – högst Tintel-score just nu ({formatExchange(exchange)}).
          </span>
        </h2>

        <div className="flex items-center gap-2">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Sök aktie"
            className="px-3 py-2 rounded-lg bg-neutral-900 text-sm text-neutral-200 placeholder-neutral-500 focus:outline-none border border-neutral-800 w-56"
          />
          <select
            value={exchange}
            onChange={(e) => setExchange(e.target.value)}
            className="bg-neutral-900 border border-neutral-800 rounded-lg text-sm p-2"
          >
            <option value="US">🇺🇸 US</option>
            <option value="ST">🇸🇪 ST</option>
          </select>
        </div>
      </div>

      {loading && <div className="text-neutral-400">Laddar data...</div>}
      {error && <div className="text-red-500">{error}</div>}

      {!loading && !error && (
        <>
          {/* Cards – top 10 */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.slice(0, 10).map((stock) => (
              <Card key={stock.symbol} stock={stock} />
            ))}
          </div>

          {/* Table – alla */}
          <h3 className="text-neutral-400 mt-6 mb-2">
            {exchange === "ST" ? "🇸🇪" : "🇺🇸"} Top 20
          </h3>
          <Table data={filtered} />
        </>
      )}
    </main>
  );
}
