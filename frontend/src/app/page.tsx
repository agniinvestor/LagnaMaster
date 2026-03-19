/**
 * frontend/src/app/page.tsx — LagnaMaster Session 25
 * Home page — birth data form + chart display.
 */
'use client'

import { useState } from 'react'
import { charts, ChartOut, ChartScoresOut, setAccessToken } from '@/lib/api'

const INDIA_1947 = {
  year: 1947, month: 8, day: 15, hour: 0,
  lat: 28.6139, lon: 77.209, tz_offset: 5.5, ayanamsha: 'lahiri' as const,
  name: 'India Independence',
}

const RATING_COLOR: Record<string, string> = {
  Excellent: 'bg-green-100 text-green-800',
  Strong: 'bg-emerald-100 text-emerald-800',
  Moderate: 'bg-yellow-100 text-yellow-800',
  Weak: 'bg-orange-100 text-orange-800',
  'Very Weak': 'bg-red-100 text-red-800',
}

export default function Home() {
  const [form, setForm] = useState({
    year: 1990, month: 1, day: 1, hour: 12,
    lat: 28.6139, lon: 77.209, tz_offset: 5.5,
    ayanamsha: 'lahiri', name: '',
  })
  const [chart, setChart] = useState<ChartOut | null>(null)
  const [scores, setScores] = useState<ChartScoresOut | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const compute = async () => {
    setLoading(true); setError(null)
    try {
      const c = await charts.create({
        ...form,
        ayanamsha: form.ayanamsha as 'lahiri' | 'raman' | 'krishnamurti',
      })
      const s = await charts.scores(c.id)
      setChart(c); setScores(s)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const demo = () => {
    setForm({ ...INDIA_1947, ayanamsha: 'lahiri', name: 'India Independence' })
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-indigo-900 text-white px-6 py-4 flex items-center gap-3">
        <span className="text-2xl">🪐</span>
        <h1 className="text-xl font-semibold">LagnaMaster</h1>
        <span className="text-indigo-300 text-sm ml-2">Vedic Jyotish Chart Engine</span>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Birth data form */}
        <div className="bg-white rounded-xl shadow p-6 space-y-4">
          <h2 className="font-semibold text-gray-800">Birth Data</h2>

          <div className="grid grid-cols-3 gap-2">
            {(['year','month','day'] as const).map(f => (
              <div key={f}>
                <label className="text-xs text-gray-500 capitalize">{f}</label>
                <input type="number" value={form[f]}
                  onChange={e => setForm({...form, [f]: +e.target.value})}
                  className="w-full border rounded px-2 py-1 text-sm mt-1"/>
              </div>
            ))}
          </div>

          <div>
            <label className="text-xs text-gray-500">Hour (decimal)</label>
            <input type="number" step="0.1" value={form.hour}
              onChange={e => setForm({...form, hour: +e.target.value})}
              className="w-full border rounded px-2 py-1 text-sm mt-1"/>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-xs text-gray-500">Latitude °N</label>
              <input type="number" step="0.0001" value={form.lat}
                onChange={e => setForm({...form, lat: +e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"/>
            </div>
            <div>
              <label className="text-xs text-gray-500">Longitude °E</label>
              <input type="number" step="0.0001" value={form.lon}
                onChange={e => setForm({...form, lon: +e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"/>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-xs text-gray-500">Timezone offset</label>
              <input type="number" step="0.5" value={form.tz_offset}
                onChange={e => setForm({...form, tz_offset: +e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"/>
            </div>
            <div>
              <label className="text-xs text-gray-500">Ayanamsha</label>
              <select value={form.ayanamsha}
                onChange={e => setForm({...form, ayanamsha: e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1">
                <option value="lahiri">Lahiri</option>
                <option value="raman">Raman</option>
                <option value="krishnamurti">Krishnamurti</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-xs text-gray-500">Label (optional)</label>
            <input type="text" value={form.name}
              onChange={e => setForm({...form, name: e.target.value})}
              className="w-full border rounded px-2 py-1 text-sm mt-1"
              placeholder="e.g. My Chart"/>
          </div>

          <button onClick={demo}
            className="w-full border border-indigo-300 text-indigo-700 rounded-lg py-2 text-sm hover:bg-indigo-50 transition">
            🇮🇳 Demo: India 1947
          </button>

          <button onClick={compute} disabled={loading}
            className="w-full bg-indigo-700 text-white rounded-lg py-2 text-sm font-medium hover:bg-indigo-800 disabled:opacity-50 transition">
            {loading ? 'Computing…' : '⚡ Compute Chart'}
          </button>

          {error && (
            <p className="text-red-600 text-sm bg-red-50 rounded p-2">{error}</p>
          )}
        </div>

        {/* Chart result */}
        {chart && (
          <div className="lg:col-span-2 space-y-6">

            {/* Lagna + planets */}
            <div className="bg-white rounded-xl shadow p-6">
              <h2 className="font-semibold text-gray-800 mb-3">
                {chart.lagna_sign} Lagna — {chart.lagna_degree.toFixed(2)}°
                <span className="text-xs text-gray-400 ml-2">
                  {chart.ayanamsha_name} · JD {chart.jd_ut.toFixed(4)}
                </span>
              </h2>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs text-gray-500 border-b">
                      <th className="pb-1">Planet</th>
                      <th>Sign</th>
                      <th>Degree</th>
                      <th>Rx</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.values(chart.planets).map(p => (
                      <tr key={p.name} className="border-b border-gray-50">
                        <td className="py-1 font-medium">{p.name}</td>
                        <td>{p.sign}</td>
                        <td>{p.degree_in_sign.toFixed(2)}°</td>
                        <td>{p.is_retrograde ? '℞' : ''}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Domain scores */}
            {scores && (
              <div className="bg-white rounded-xl shadow p-6">
                <h2 className="font-semibold text-gray-800 mb-3">Domain Scores</h2>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {Object.values(scores.houses).map(h => (
                    <div key={h.house}
                      className="border rounded-lg p-2 text-sm">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-gray-700">H{h.house}</span>
                        <span className={`text-xs px-1.5 py-0.5 rounded-full font-medium ${RATING_COLOR[h.rating] ?? ''}`}>
                          {h.rating}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">{h.domain}</div>
                      <div className="text-base font-bold text-indigo-700 mt-0.5">
                        {h.final_score > 0 ? '+' : ''}{h.final_score.toFixed(1)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  )
}
