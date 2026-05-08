"""FastAPI app exposing /ws and /snapshot."""
import asyncio
import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .aggregate import RollingAggregator
from .score import score
from .sources.replay import stream

TOPICS = os.getenv("TOPICS", "fed,inflation,ai").split(",")
agg = RollingAggregator(TOPICS)
clients: set[WebSocket] = set()


async def producer():
    async for text in stream("data/sample.csv", speed=10.0):
        s = score(text)
        agg.add(text, s["polarity"])
        snap = agg.snapshot()
        dead = []
        for ws in clients:
            try:
                await ws.send_text(json.dumps(snap))
            except Exception:
                dead.append(ws)
        for ws in dead:
            clients.discard(ws)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(producer())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/snapshot")
def snapshot():
    return agg.snapshot()


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.discard(ws)
