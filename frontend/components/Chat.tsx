"use client";
import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function Chat({ symbol }: { symbol: string }) {
  const [messages, setMessages] = useState<any[]>([]);
  const [body, setBody] = useState("");

  // hämta historik
  async function load() {
    const { data } = await supabase
      .from("messages")
      .select("*")
      .eq("symbol", symbol.toUpperCase())
      .order("created_at", { ascending: false })
      .limit(50);
    setMessages(data || []);
  }

  // realtime sub
  useEffect(() => {
    load();
    const sub = supabase
      .channel("room_" + symbol)
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "messages", filter: `symbol=eq.${symbol}` },
        (payload) => setMessages((prev) => [payload.new, ...prev])
      )
      .subscribe();
    return () => supabase.removeChannel(sub);
  }, [symbol]);

  async function sendMessage() {
    if (!body.trim()) return;
    await supabase.from("messages").insert([
      {
        symbol: symbol.toUpperCase(),
        username: "anon",
        body,
      },
    ]);
    setBody("");
  }

  return (
    <div className="space-y-2">
      <div className="border rounded-lg p-2 h-64 overflow-y-auto bg-black/10">
        {messages.map((m) => (
          <div key={m.id} className="text-sm border-b border-white/5 py-1">
            <span className="text-blue-400 font-semibold">{m.username || "anon"}</span>: {m.body}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Write something..."
          className="flex-1 border rounded-md px-2 py-1 bg-black/20"
        />
        <button
          onClick={sendMessage}
          className="bg-green-500 px-3 py-1 rounded-md text-sm text-white hover:bg-green-600"
        >
          Send
        </button>
      </div>
    </div>
  );
}
