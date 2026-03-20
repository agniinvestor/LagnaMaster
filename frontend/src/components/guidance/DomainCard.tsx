// frontend/src/components/guidance/DomainCard.tsx — Session 80
// Bloomberg-style domain guidance panel — no raw scores visible
'use client'
import { useState } from 'react'
import { SignalBar } from './SignalBar'

interface GuidanceResponse {
  domain: string; heading: string; summary: string;
  signal_bars: number; signal_display: string; timing_label: string;
  confidence_label: string; confidence_note: string; disclaimer: string;
  factors?: string[]; timing_note?: string; domain_context?: string;
  technical_detail?: Record<string, unknown>; depth_returned: string;
}

interface DomainCardProps { chartId: string; domain: string; label: string }

const CONFIDENCE_DOT: Record<string, string> = {
  High: 'bg-emerald-400', Moderate: 'bg-yellow-400',
  Low: 'bg-orange-400', Uncertain: 'bg-slate-500',
}

export function DomainCard({ chartId, domain, label }: DomainCardProps) {
  const [data, setData] = useState<GuidanceResponse | null>(null)
  const [depth, setDepth] = useState<'L1' | 'L2' | 'L3'>('L1')
  const [loading, setLoading] = useState(false)
  const [l3Confirmed, setL3Confirmed] = useState(false)

  const fetchGuidance = async (d: 'L1' | 'L2' | 'L3' = depth) => {
    setLoading(true)
    try {
      const res = await fetch('/api/guidance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chartId, domain, depth: d,
                               l3OptedIn: d === 'L3' && l3Confirmed }),
      })
      setData(await res.json())
    } finally { setLoading(false) }
  }

  if (!data && !loading) {
    return (
      <button onClick={() => fetchGuidance('L1')}
        className="w-full p-4 bg-slate-900 border border-slate-800 rounded-lg
                   text-left hover:border-slate-700 transition-colors">
        <div className="text-slate-400 text-xs uppercase tracking-widest mb-1">{label}</div>
        <div className="text-slate-500 text-sm">Click to load guidance</div>
      </button>
    )
  }

  return (
    <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg space-y-3">
      <div className="flex items-start justify-between">
        <div>
          <div className="text-slate-400 text-xs uppercase tracking-widest mb-1">{label}</div>
          {data && <SignalBar bars={data.signal_bars} label={data.timing_label} />}
        </div>
        {data && (
          <div className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${CONFIDENCE_DOT[data.confidence_label] || 'bg-slate-600'}`} />
            <span className="text-xs text-slate-500">{data.confidence_label}</span>
          </div>
        )}
      </div>

      {loading && <div className="text-slate-500 text-sm animate-pulse">Loading…</div>}

      {data && (
        <>
          <p className="text-slate-200 text-sm leading-relaxed">{data.summary}</p>

          {depth === 'L1' && (
            <button onClick={() => { setDepth('L2'); fetchGuidance('L2') }}
              className="text-blue-400 text-xs hover:text-blue-300 transition-colors">
              Why? →
            </button>
          )}

          {data.factors && data.factors.length > 0 && (
            <ul className="space-y-1">
              {data.factors.map((f, i) => (
                <li key={i} className="text-slate-400 text-xs flex gap-2">
                  <span className="text-slate-600 mt-0.5">·</span>
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          )}

          {data.timing_note && (
            <p className="text-slate-500 text-xs border-l border-slate-700 pl-3">
              {data.timing_note}
            </p>
          )}

          {depth === 'L2' && !l3Confirmed && (
            <button onClick={() => {
              if (confirm('Show advanced technical detail? This is intended for practitioners and advanced students.')) {
                setL3Confirmed(true); setDepth('L3'); fetchGuidance('L3')
              }
            }} className="text-slate-500 text-xs hover:text-slate-400 transition-colors">
              Show technical detail →
            </button>
          )}

          {data.technical_detail && Object.keys(data.technical_detail).length > 0 && (
            <div className="mt-2 p-3 bg-slate-950 rounded border border-slate-800">
              <div className="text-slate-500 text-xs uppercase tracking-widest mb-2">
                Advanced technical view
              </div>
              <pre className="text-slate-400 text-xs overflow-auto max-h-40">
                {JSON.stringify(data.technical_detail, null, 2)}
              </pre>
            </div>
          )}

          <p className="text-slate-600 text-xs">{data.disclaimer}</p>
        </>
      )}
    </div>
  )
}
