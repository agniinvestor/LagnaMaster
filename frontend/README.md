# LagnaMaster — Next.js Frontend (Session 25)

Next.js 14 + TypeScript + Tailwind CSS frontend replacing Streamlit.

## Development

```bash
cd frontend
npm install
npm run dev      # http://localhost:3000
```

Requires FastAPI running on :8000. Set NEXT_PUBLIC_API_URL if API is elsewhere.

## Build

```bash
npm run build && npm start
```

## Test

```bash
npm test
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| NEXT_PUBLIC_API_URL | http://localhost:8000 | FastAPI base URL |

## Structure

```
src/
  app/
    page.tsx       Home — birth data form + chart display
    layout.tsx     Root layout
    globals.css    Tailwind base
  lib/
    api.ts         Typed fetch client for FastAPI
    api.test.ts    Unit tests (Jest + fetch mock)
  components/     (future: Chart SVG, Yoga cards, Dasha timeline)
```
