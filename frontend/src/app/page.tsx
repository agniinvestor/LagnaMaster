/**
 * frontend/src/app/page.tsx — LagnaMaster Session 25
 * Home page — birth data form + chart display.
 */
'use client'

import { useState } from 'react'
import {
  charts, ChartOut, ChartScoresOut, ChartV3Out, ConfidenceOut,
  GuidanceOut, MundaneOut, mundane,
} from '@/lib/api'

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

  // Tab
  const [tab, setTab] = useState<'chart' | 'mundane'>('chart')

  // New chart-result state
  const [svg, setSvg] = useState<string | null>(null)
  const [svgStyle, setSvgStyle] = useState<'north_indian' | 'south_indian'>('north_indian')
  const [confidence, setConfidence] = useState<ConfidenceOut | null>(null)
  const [v3, setV3] = useState<ChartV3Out | null>(null)
  const [v3Open, setV3Open] = useState(false)
  const [guidance, setGuidance] = useState<GuidanceOut | null>(null)
  const [guidanceDomain, setGuidanceDomain] = useState('career')
  const [guidanceDepth, setGuidanceDepth] = useState<'L1' | 'L2' | 'L3'>('L1')
  const [guidanceLoading, setGuidanceLoading] = useState(false)

  // Mundane tab state
  const [mundaneForm, setMundaneForm] = useState<{
    year: number; month: number; day: number; hour: number;
    lat: number; lon: number; tz_offset: number;
    chart_type: 'ingress' | 'nation' | 'lunar_new_year' | 'swearing_in';
    event_description: string; location: string;
  }>({
    year: 2026, month: 3, day: 20, hour: 0,
    lat: 51.477, lon: 0.0, tz_offset: 0.0,
    chart_type: 'ingress',
    event_description: '', location: '',
  })
  const [mundaneResult, setMundaneResult] = useState<MundaneOut | null>(null)
  const [mundaneLoading, setMundaneLoading] = useState(false)
  const [mundaneError, setMundaneError] = useState<string | null>(null)

  const compute = async () => {
    setLoading(true); setError(null)
    setSvg(null); setConfidence(null); setV3(null); setGuidance(null)
    try {
      const c = await charts.create({
        ...form,
        ayanamsha: form.ayanamsha as 'lahiri' | 'raman' | 'krishnamurti',
      })
      const [s, svgRes, conf, v3Res] = await Promise.all([
        charts.scores(c.id),
        charts.svg(c.id, { style: svgStyle }),
        charts.confidence(c.id),
        charts.scoresV3(c.id),
      ])
      setChart(c); setScores(s)
      setSvg(svgRes.svg); setConfidence(conf); setV3(v3Res)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const demo = () => {
    setForm({ ...INDIA_1947, ayanamsha: 'lahiri', name: 'India Independence' })
  }

  const fetchGuidance = async () => {
    if (!chart) return
    setGuidanceLoading(true)
    try {
      const g = await charts.guidance(chart.id, {
        domain: guidanceDomain,
        depth: guidanceDepth,
      })
      setGuidance(g)
    } catch {
      // guidance errors are non-fatal; panel stays blank
    } finally {
      setGuidanceLoading(false)
    }
  }

  const toggleSvgStyle = async (style: 'north_indian' | 'south_indian') => {
    if (!chart) return
    setSvgStyle(style)
    try {
      const res = await charts.svg(chart.id, { style })
      setSvg(res.svg)
    } catch {
      // keep existing svg on error
    }
  }

  const analyzeMundane = async () => {
    setMundaneLoading(true); setMundaneError(null)
    try {
      const result = await mundane.analyze({
        year: mundaneForm.year,
        month: mundaneForm.month,
        day: mundaneForm.day,
        hour: mundaneForm.hour,
        lat: mundaneForm.lat,
        lon: mundaneForm.lon,
        tz_offset: mundaneForm.tz_offset,
        chart_type: mundaneForm.chart_type,
        event_description: mundaneForm.event_description || undefined,
        location: mundaneForm.location || undefined,
      })
      setMundaneResult(result)
    } catch (e: unknown) {
      setMundaneError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setMundaneLoading(false)
    }
  }

  // suppress unused-variable warnings for state setters used by future tasks
  void guidance; void guidanceDomain; void guidanceDepth; void guidanceLoading
  void fetchGuidance

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-indigo-900 text-white px-6 py-4 flex items-center gap-3">
        <span className="text-2xl">🪐</span>
        <h1 className="text-xl font-semibold">LagnaMaster</h1>
        <span className="text-indigo-300 text-sm ml-2">Vedic Jyotish Chart Engine</span>
      </header>

      {/* Tab bar */}
      <div className="bg-white border-b px-6 flex gap-6">
        {(['chart', 'mundane'] as const).map(t => (
          <button key={t}
            onClick={() => setTab(t)}
            className={`py-3 text-sm font-medium border-b-2 transition ${
              tab === t
                ? 'border-indigo-700 text-indigo-700'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t === 'chart' ? 'Birth Chart' : 'Mundane'}
          </button>
        ))}
      </div>

      {/* Birth Chart tab */}
      {tab === 'chart' && (
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

              {/* SVG chart */}
              {svg && (
                <div className="bg-white rounded-xl shadow p-6">
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="font-semibold text-gray-800">Chart Diagram</h2>
                    <div className="flex items-center gap-2">
                      <div className="flex rounded-lg border overflow-hidden text-xs">
                        {(['north_indian', 'south_indian'] as const).map(s => (
                          <button key={s}
                            onClick={() => toggleSvgStyle(s)}
                            className={`px-2 py-1 transition ${svgStyle === s ? 'bg-indigo-700 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>
                            {s === 'north_indian' ? 'North' : 'South'}
                          </button>
                        ))}
                      </div>
                      <button
                        onClick={async () => {
                          const blob = await charts.pdf(chart.id)
                          const url = URL.createObjectURL(blob)
                          const a = document.createElement('a')
                          a.href = url; a.download = `lagnamaster_${chart.id}.pdf`
                          a.click(); URL.revokeObjectURL(url)
                        }}
                        className="border border-gray-300 text-gray-600 rounded px-2 py-1 text-xs hover:bg-gray-50 transition">
                        ⬇ PDF
                      </button>
                    </div>
                  </div>
                  <div dangerouslySetInnerHTML={{ __html: svg }}
                    className="w-full overflow-x-auto"/>
                </div>
              )}

              {/* Confidence badge */}
              {confidence && (
                <div className={`rounded-xl shadow p-4 text-sm ${
                  confidence.lagna_boundary_warning
                    ? 'bg-amber-50 border border-amber-200'
                    : 'bg-white'
                }`}>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-700">Reliability:</span>
                    <span className="font-semibold text-indigo-700">{confidence.overall_reliability}</span>
                    {confidence.lagna_boundary_warning && (
                      <span className="text-amber-700 ml-2">
                        ⚠ Lagna within {confidence.lagna_boundary_margin_deg.toFixed(1)}° of sign boundary — birth time sensitive
                      </span>
                    )}
                    {confidence.moon_nakshatra_boundary && (
                      <span className="text-amber-600 ml-2 text-xs">Moon near nakshatra boundary</span>
                    )}
                  </div>
                </div>
              )}

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

              {/* V3 multi-axis scores (collapsible) */}
              {v3 && (
                <div className="bg-white rounded-xl shadow">
                  <button
                    onClick={() => setV3Open(!v3Open)}
                    className="w-full flex items-center justify-between px-6 py-4 text-sm font-semibold text-gray-800 hover:bg-gray-50 rounded-xl transition">
                    <span>Multi-axis Scores <span className="text-xs font-normal text-gray-400 ml-1">(heuristic estimate — {v3.engine_version})</span></span>
                    <span className="text-gray-400">{v3Open ? '▲' : '▼'}</span>
                  </button>

                  {v3Open && (
                    <div className="px-6 pb-6 space-y-4">
                      {/* D1, D9, D10 grids */}
                      {([['D1 (Rashi)', v3.d1_scores], ['D9 (Navamsha)', v3.d9_scores], ['D10 (Dasamsha)', v3.d10_scores]] as [string, Record<string, number>][]).map(([label, scores]) => (
                        <div key={label}>
                          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">{label}</h3>
                          <div className="grid grid-cols-4 sm:grid-cols-6 gap-1">
                            {Object.entries(scores).map(([h, s]) => (
                              <div key={h} className="border rounded p-1 text-center text-xs">
                                <div className="text-gray-500">H{h}</div>
                                <div className={`font-bold ${s >= 0 ? 'text-emerald-700' : 'text-red-600'}`}>
                                  {s > 0 ? '+' : ''}{s.toFixed(1)}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}

                      {/* Yoga lists */}
                      {v3.raja_yogas.length > 0 && (
                        <div>
                          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Raja Yogas</h3>
                          <div className="flex flex-wrap gap-1">
                            {v3.raja_yogas.map((y, i) => (
                              <span key={i} className="bg-emerald-100 text-emerald-800 text-xs px-2 py-0.5 rounded-full">{y}</span>
                            ))}
                          </div>
                        </div>
                      )}

                      {v3.viparita_yogas.length > 0 && (
                        <div>
                          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Viparita Yogas</h3>
                          <div className="flex flex-wrap gap-1">
                            {v3.viparita_yogas.map((y, i) => (
                              <span key={i} className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">{y}</span>
                            ))}
                          </div>
                        </div>
                      )}

                      {v3.neecha_bhanga.length > 0 && (
                        <div>
                          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Neecha Bhanga</h3>
                          <div className="flex flex-wrap gap-1">
                            {v3.neecha_bhanga.map((y, i) => (
                              <span key={i} className="bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded-full">{y}</span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* PLACEHOLDER_GUIDANCE */}

            </div>
          )}
        </div>
      )}

      {/* Mundane tab */}
      {tab === 'mundane' && (
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
          <div className="bg-white rounded-xl shadow p-6 space-y-4">
            <h2 className="font-semibold text-gray-800">Mundane Analysis</h2>
            <p className="text-xs text-gray-500">Nation charts, solar ingresses, swearing-in events. Source: PVRNR Ch.35.</p>

            <div className="grid grid-cols-3 gap-2">
              {(['year','month','day'] as const).map(f => (
                <div key={f}>
                  <label className="text-xs text-gray-500 capitalize">{f}</label>
                  <input type="number" value={mundaneForm[f]}
                    onChange={e => setMundaneForm({...mundaneForm, [f]: +e.target.value})}
                    className="w-full border rounded px-2 py-1 text-sm mt-1"/>
                </div>
              ))}
            </div>

            <div>
              <label className="text-xs text-gray-500">Hour (decimal)</label>
              <input type="number" step="0.1" value={mundaneForm.hour}
                onChange={e => setMundaneForm({...mundaneForm, hour: +e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"/>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs text-gray-500">Latitude °N</label>
                <input type="number" step="0.0001" value={mundaneForm.lat}
                  onChange={e => setMundaneForm({...mundaneForm, lat: +e.target.value})}
                  className="w-full border rounded px-2 py-1 text-sm mt-1"/>
              </div>
              <div>
                <label className="text-xs text-gray-500">Longitude °E</label>
                <input type="number" step="0.0001" value={mundaneForm.lon}
                  onChange={e => setMundaneForm({...mundaneForm, lon: +e.target.value})}
                  className="w-full border rounded px-2 py-1 text-sm mt-1"/>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs text-gray-500">Timezone offset</label>
                <input type="number" step="0.5" value={mundaneForm.tz_offset}
                  onChange={e => setMundaneForm({...mundaneForm, tz_offset: +e.target.value})}
                  className="w-full border rounded px-2 py-1 text-sm mt-1"/>
              </div>
              <div>
                <label className="text-xs text-gray-500">Chart Type</label>
                <select value={mundaneForm.chart_type}
                  onChange={e => setMundaneForm({...mundaneForm, chart_type: e.target.value as 'ingress' | 'nation' | 'lunar_new_year' | 'swearing_in'})}
                  className="w-full border rounded px-2 py-1 text-sm mt-1">
                  <option value="ingress">Solar Ingress</option>
                  <option value="nation">Nation Chart</option>
                  <option value="lunar_new_year">Lunar New Year</option>
                  <option value="swearing_in">Swearing-In</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500">Event Description (optional)</label>
              <input type="text" value={mundaneForm.event_description}
                onChange={e => setMundaneForm({...mundaneForm, event_description: e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"
                placeholder="e.g. Aries ingress 2026"/>
            </div>

            <div>
              <label className="text-xs text-gray-500">Location (optional)</label>
              <input type="text" value={mundaneForm.location}
                onChange={e => setMundaneForm({...mundaneForm, location: e.target.value})}
                className="w-full border rounded px-2 py-1 text-sm mt-1"
                placeholder="e.g. New Delhi"/>
            </div>

            <button onClick={analyzeMundane} disabled={mundaneLoading}
              className="w-full bg-indigo-700 text-white rounded-lg py-2 text-sm font-medium hover:bg-indigo-800 disabled:opacity-50 transition">
              {mundaneLoading ? 'Analyzing…' : '🌍 Analyze'}
            </button>

            {mundaneError && (
              <p className="text-red-600 text-sm bg-red-50 rounded p-2">{mundaneError}</p>
            )}
          </div>

          {mundaneResult && (
            <div className="bg-white rounded-xl shadow p-6 space-y-4">
              <h2 className="font-semibold text-gray-800">
                {mundaneResult.chart_type} · {mundaneResult.date}
                {mundaneResult.location && <span className="text-gray-500 text-sm ml-2">{mundaneResult.location}</span>}
              </h2>

              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Key Themes</h3>
                <ul className="list-disc list-inside text-sm space-y-0.5">
                  {mundaneResult.key_themes.map((t, i) => <li key={i}>{t}</li>)}
                </ul>
              </div>

              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Challenges</h3>
                <ul className="list-disc list-inside text-sm space-y-0.5">
                  {mundaneResult.challenges.map((c, i) => <li key={i}>{c}</li>)}
                </ul>
              </div>

              {Object.keys(mundaneResult.house_significations).length > 0 && (
                <div>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">House Significations</h3>
                  <table className="w-full text-sm">
                    <tbody>
                      {Object.entries(mundaneResult.house_significations).map(([h, sig]) => (
                        <tr key={h} className="border-b border-gray-50">
                          <td className="py-1 font-medium w-8">H{h}</td>
                          <td className="text-gray-600">{sig}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {mundaneResult.compressed_dasha && mundaneResult.compressed_dasha.length > 0 && (
                <div>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase mb-1">Dasha Periods</h3>
                  <div className="text-sm space-y-0.5">
                    {mundaneResult.compressed_dasha.map((d, i) => (
                      <div key={i} className="text-gray-600">{JSON.stringify(d)}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </main>
  )
}
