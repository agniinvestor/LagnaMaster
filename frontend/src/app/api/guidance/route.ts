// frontend/src/app/api/guidance/route.ts — Session 79-74
// Next.js API route — proxies to Python FastAPI guidance endpoint
import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const { chartId, domain = 'default', depth = 'L1', date, l3OptedIn = false } = body

  if (!chartId) {
    return NextResponse.json({ error: 'chartId required' }, { status: 400 })
  }

  const res = await fetch(`${BACKEND_URL}/guidance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
                'Authorization': req.headers.get('Authorization') || '' },
    body: JSON.stringify({ chart_id: chartId, domain, depth,
                           on_date: date, l3_opted_in: l3OptedIn }),
  })
  const data = await res.json()
  return NextResponse.json(data, { status: res.status })
}
