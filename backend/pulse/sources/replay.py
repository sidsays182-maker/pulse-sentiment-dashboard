"""Replay a CSV of {ts,text} as a live stream."""
import asyncio
import csv
import time
from pathlib import Path


async def stream(path: str, speed: float = 5.0):
    rows = list(csv.DictReader(Path(path).open()))
    if not rows:
        return
    t0 = float(rows[0]["ts"])
    start = time.time()
    for r in rows:
        delay = (float(r["ts"]) - t0) / speed - (time.time() - start)
        if delay > 0:
            await asyncio.sleep(delay)
        yield r["text"]
