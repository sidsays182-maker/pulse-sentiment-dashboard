"""Rolling-window aggregator keyed by topic."""
import os
import time
from collections import defaultdict, deque
from typing import Iterable

WINDOW = int(os.getenv("WINDOW_SECONDS", "60"))


class RollingAggregator:
    def __init__(self, topics: Iterable[str], window: int = WINDOW):
        self.topics = list(topics)
        self.window = window
        self.buf: dict[str, deque] = defaultdict(deque)

    def _topic_for(self, text: str) -> str | None:
        t = text.lower()
        for kw in self.topics:
            if kw in t:
                return kw
        return None

    def add(self, text: str, polarity: float, ts: float | None = None):
        ts = ts or time.time()
        topic = self._topic_for(text)
        if topic is None:
            return None
        self.buf[topic].append((ts, polarity))
        self._evict(topic, ts)
        return topic

    def _evict(self, topic: str, now: float):
        cutoff = now - self.window
        q = self.buf[topic]
        while q and q[0][0] < cutoff:
            q.popleft()

    def snapshot(self) -> list[dict]:
        now = time.time()
        out = []
        for topic in self.topics:
            self._evict(topic, now)
            q = self.buf[topic]
            n = len(q)
            mean = sum(p for _, p in q) / n if n else 0.0
            out.append({"topic": topic, "volume": n, "sentiment": round(mean, 3)})
        return out
