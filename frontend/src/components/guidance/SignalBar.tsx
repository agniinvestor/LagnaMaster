// frontend/src/components/guidance/SignalBar.tsx — Session 80
// 5-bar signal indicator — mobile-signal style, no percentages
'use client'
interface SignalBarProps { bars: number; label: string; size?: 'sm' | 'md' | 'lg' }

const LABEL_COLORS: Record<string, string> = {
  'Clear passage': 'text-emerald-400',
  'Favourable': 'text-green-400',
  'Mixed — lean in': 'text-yellow-400',
  'Neutral': 'text-slate-400',
  'Navigate carefully': 'text-orange-400',
  'Significant resistance': 'text-slate-500',
}

export function SignalBar({ bars, label, size = 'md' }: SignalBarProps) {
  const heights = ['h-2', 'h-3', 'h-4', 'h-5', 'h-6']
  const barW = size === 'sm' ? 'w-1.5' : size === 'lg' ? 'w-3' : 'w-2'
  const labelColor = LABEL_COLORS[label] || 'text-slate-400'

  return (
    <div className="flex items-end gap-2">
      <div className="flex items-end gap-0.5">
        {Array.from({ length: 5 }, (_, i) => (
          <div
            key={i}
            className={`${barW} ${heights[i]} rounded-sm transition-colors ${
              i < bars ? 'bg-blue-400' : 'bg-slate-700'
            }`}
          />
        ))}
      </div>
      <span className={`text-xs font-medium ${labelColor}`}>{label}</span>
    </div>
  )
}
