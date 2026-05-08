# pulse-sentiment-dashboard

> Real-time sentiment analytics over streaming text data. A Python streaming pipeline pushes scored events into a Next.js dashboard with live charts.

`Python` · `Kafka-style stream` · `Transformers` · `FastAPI` · `WebSockets` · `Next.js` · `Recharts` · `Tailwind`

## What it does

1. Pulls a stream of short text items (headlines, comments, reviews) from a configurable source.
2. Scores each item with a multilingual transformer sentiment model.
3. Aggregates rolling windows (1m / 5m / 1h) by topic.
4. Pushes updates over WebSocket to a Next.js dashboard.

## Architecture

```
Source (RSS / API / CSV) ──► Producer ──► in-memory queue
                                            │
                                            ▼
                          Worker (HF transformer) ──► scored events
                                            │
                            ┌───────────────┴────────────────┐
                            ▼                                ▼
                     Postgres (history)                 WebSocket /ws
                                                             │
                                                             ▼
                                                     Next.js dashboard
```

## Features

- **Plug-and-play sources** — generic HTTP API, RSS, or replay from CSV
- **Topic tagging** — keyword + zero-shot classifier
- **Rolling aggregates** — net sentiment, volume, top entities
- **Live dashboard** — sparkline per topic, leaderboard, anomaly markers
- **Backfill mode** — replay historical CSV to validate pipeline

## Quickstart

### Backend
```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python -m pulse.replay data/sample.csv     # demo source
uvicorn pulse.api:app --reload             # ws://localhost:8000/ws
```

### Frontend
```bash
cd frontend
npm install
npm run dev                                # http://localhost:3000
```

## Project layout

```
backend/
  pulse/
    sources/       # http_api.py, rss.py, replay.py
    score.py       # HF sentiment model wrapper
    aggregate.py   # rolling-window stats
    api.py         # FastAPI + WebSocket
  data/sample.csv
frontend/
  app/page.tsx     # dashboard
  components/
    Sparkline.tsx
    Leaderboard.tsx
    TopicCard.tsx
```

## Roadmap

- [ ] Anomaly detection (z-score on volume × sentiment)
- [ ] Per-language models (Tamil, Hindi)
- [ ] Export to Parquet for offline analysis

## License

MIT
