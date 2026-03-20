// frontend/src/components/timing/TimingCalendar.tsx — Session 81
// 90-day timing calendar — colour by activation quality, no "bad day" language
'use client'
import { useState, useEffect } from 'react'

interface DayData { date: string; signal_bars: number; timing_label: string;
                    domains_active: string[] }

const DAY_COLORS: Record<number, string> = {
  5: 'bg-blue-900 border-blue-700 hover:bg-blue-800',
  4: 'bg-blue-950 border-blue-800 hover:bg-blue-900',
  3: 'bg-slate-800 border-slate-700 hover:bg-slate-700',
  2: 'bg-slate-900 border-slate-800 hover:bg-slate-800',
  1: 'bg-amber-950 border-amber-900 hover:bg-amber-900',
  0: 'bg-slate-950 border-slate-900 hover:bg-slate-900',
}

const LABEL_MAP: Record<number, string> = {
  5: 'Clear passage', 4: 'Favourable', 3: 'Mixed', 2: 'Neutral',
  1: 'Navigate carefully', 0: 'Significant resistance',
}

interface Props { chartId: string }

export function TimingCalendar({ chartId }: Props) {
  const [days, setDays] = useState<DayData[]>([])
  const [selected, setSelected] = useState<DayData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Generate placeholder 90-day data (real: fetch from /api/timing)
    const generated: DayData[] = Array.from({ length: 90 }, (_, i) => {
      const d = new Date(); d.setDate(d.getDate() + i)
      const bars = Math.floor(Math.random() * 6)  // replace with real API
      return {
        date: d.toISOString().slice(0, 10),
        signal_bars: bars,
        timing_label: LABEL_MAP[bars],
        domains_active: bars >= 4 ? ['career', 'wealth'] : bars >= 3 ? ['general'] : [],
      }
    })
    setDays(generated)
    setLoading(false)
  }, [chartId])

  if (loading) return <div className="text-slate-500 text-sm animate-pulse">Loading calendar…</div>

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-15 gap-0.5" style={{ gridTemplateColumns: 'repeat(15, 1fr)' }}>
        {days.slice(0, 90).map((day) => (
          <button key={day.date} onClick={() => setSelected(day)}
            title={`${day.date}: ${day.timing_label}`}
            className={`w-full aspect-square rounded-sm border text-[8px] transition-colors
                        ${DAY_COLORS[day.signal_bars]}
                        ${selected?.date === day.date ? 'ring-1 ring-blue-400' : ''}`}>
          </button>
        ))}
      </div>

      {/* Legend */}
      <div className="flex gap-3 flex-wrap">
        {[5,3,1].map(b => (
          <div key={b} className="flex items-center gap-1.5">
            <div className={`w-3 h-3 rounded-sm border ${DAY_COLORS[b]}`} />
            <span className="text-slate-500 text-xs">{LABEL_MAP[b]}</span>
          </div>
        ))}
      </div>

      {/* Day detail */}
      {selected && (
        <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
          <div className="text-slate-300 text-sm font-medium mb-1">{selected.date}</div>
          <div className="text-slate-400 text-xs">{selected.timing_label}</div>
          {selected.domains_active.length > 0 && (
            <div className="text-slate-500 text-xs mt-1">
              Active: {selected.domains_active.join(', ')}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
