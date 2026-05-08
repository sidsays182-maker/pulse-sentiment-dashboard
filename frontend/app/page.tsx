"use client";
import { useEffect, useState } from "react";

type Snap = { topic: string; volume: number; sentiment: number };

export default function Home() {
  const [snap, setSnap] = useState<Snap[]>([]);
  useEffect(() => {
    const ws = new WebSocket(
      process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws"
    );
    ws.onmessage = (e) => setSnap(JSON.parse(e.data));
    return () => ws.close();
  }, []);

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
      <h1 className="text-2xl font-semibold mb-6">Pulse · Live sentiment</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {snap.map((s) => (
          <div
            key={s.topic}
            className="rounded-2xl border border-zinc-800 p-4 bg-zinc-900/60"
          >
            <div className="text-sm uppercase text-zinc-400">{s.topic}</div>
            <div className="text-3xl font-semibold mt-1">
              {s.sentiment > 0 ? "+" : ""}
              {s.sentiment.toFixed(2)}
            </div>
            <div className="text-xs text-zinc-500 mt-1">
              volume {s.volume}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
