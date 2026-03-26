/**
 * src/lib/api.ts — LagnaMaster Session 25
 * Typed fetch client for the FastAPI backend.
 * All calls go through /api/* which Next.js proxies to FastAPI.
 */

const BASE = '/api'

// ── types ─────────────────────────────────────────────────────────────────────

export interface BirthDataRequest {
  year: number
  month: number
  day: number
  hour: number
  lat: number
  lon: number
  tz_offset?: number
  ayanamsha?: 'lahiri' | 'raman' | 'krishnamurti'
  name?: string
}

export interface PlanetOut {
  name: string
  sign: string
  sign_index: number
  degree_in_sign: number
  longitude: number
  is_retrograde: boolean
  speed: number
}

export interface ChartOut {
  id: number
  lagna_sign: string
  lagna_sign_index: number
  lagna_degree: number
  ayanamsha_name: string
  ayanamsha_value: number
  jd_ut: number
  planets: Record<string, PlanetOut>
}

export interface HouseScoreOut {
  house: number
  domain: string
  bhavesh: string
  bhavesh_house: number
  final_score: number
  raw_score: number
  rating: 'Excellent' | 'Strong' | 'Moderate' | 'Weak' | 'Very Weak'
  rules: RuleOut[]
}

export interface RuleOut {
  rule: string
  description: string
  score: number
  is_wc: boolean
  triggered: boolean
}

export interface ChartScoresOut {
  chart_id: number
  lagna_sign: string
  houses: Record<string, HouseScoreOut>
}

export interface YogaOut {
  name: string
  category: string
  nature: 'benefic' | 'malefic' | 'mixed'
  planets: string[]
  description: string
}

export interface TokenOut {
  access_token: string
  refresh_token: string
  token_type: string
  access_expires_in: number
  refresh_expires_in: number
}

export interface UserOut {
  id: number
  username: string
  email: string
  created_at: string
  is_active: boolean
}

export interface HealthOut {
  status: string
  version: string
  db: { backend: string; ok: boolean }
  cache: { backend: string; ok: boolean }
}

// ── New types (S167-S190) ──────────────────────────────────────────────────

export interface SVGRequest {
  style?: 'north_indian' | 'south_indian'
  color_scheme?: 'color' | 'bw'
  show_degrees?: boolean
  title?: string
}

export interface SVGOut {
  chart_id: number
  style: string
  svg: string
}

export interface GuidanceRequest {
  domain?: string
  depth?: 'L1' | 'L2' | 'L3'
  on_date?: string
  school?: string
  l3_opted_in?: boolean
}

export interface GuidanceOut {
  chart_id: number
  domain: string
  heading: string
  summary: string
  signal_bars: number
  signal_display: string
  timing_label: string
  confidence_label: string
  confidence_note: string
  disclaimer: string
  factors: string[]
  timing_note: string
  domain_context: string
  technical_detail: Record<string, unknown>
  depth_returned: string
}

export interface ConfidenceOut {
  chart_id: number
  lagna_boundary_margin_deg: number
  lagna_boundary_warning: boolean
  moon_nakshatra_boundary: boolean
  overall_reliability: string
  uncertainty_sources: string[]
  house_confidence: Record<string, { label: string; interval: number }>
}

export interface ChartV3Out {
  chart_id: number
  lagna_sign: string
  engine_version: string
  d1_scores: Record<string, number>
  cl_scores: Record<string, number>
  sl_scores: Record<string, number>
  d9_scores: Record<string, number>
  d10_scores: Record<string, number>
  raja_yogas: string[]
  viparita_yogas: string[]
  neecha_bhanga: string[]
}

export interface MundaneRequest {
  year: number
  month: number
  day: number
  hour?: number
  lat: number
  lon: number
  tz_offset?: number
  chart_type?: 'ingress' | 'nation' | 'lunar_new_year' | 'swearing_in'
  event_description?: string
  location?: string
}

export interface MundaneOut {
  chart_type: string
  event_description: string
  date: string
  location: string | null
  key_themes: string[]
  challenges: string[]
  house_significations: Record<string, string>
  compressed_dasha: Array<Record<string, unknown>> | null
}

// ── auth token storage ────────────────────────────────────────────────────────

let _accessToken: string | null = null

export function setAccessToken(token: string | null) {
  _accessToken = token
}

export function getAccessToken(): string | null {
  return _accessToken
}

// ── fetch helper ──────────────────────────────────────────────────────────────

async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }
  if (_accessToken) {
    headers['Authorization'] = `Bearer ${_accessToken}`
  }
  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return null as T
  return res.json()
}

// ── auth ──────────────────────────────────────────────────────────────────────

export const auth = {
  register: (username: string, email: string, password: string) =>
    apiFetch<UserOut>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    }),

  login: (username: string, password: string) =>
    apiFetch<TokenOut>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),

  refresh: (refresh_token: string) =>
    apiFetch<TokenOut>('/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token }),
    }),

  me: () => apiFetch<UserOut>('/auth/me'),

  logout: () => apiFetch<null>('/auth/logout', { method: 'POST' }),
}

// ── charts ────────────────────────────────────────────────────────────────────

export const charts = {
  create: (data: BirthDataRequest) =>
    apiFetch<ChartOut>('/charts', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  list: (limit = 20) =>
    apiFetch<ChartOut[]>(`/charts?limit=${limit}`),

  get: (id: number) =>
    apiFetch<ChartOut>(`/charts/${id}`),

  scores: (id: number) =>
    apiFetch<ChartScoresOut>(`/charts/${id}/scores`),

  yogas: (id: number) =>
    apiFetch<YogaOut[]>(`/charts/${id}/yogas`),

  report: async (id: number): Promise<Blob> => {
    const res = await fetch(`${BASE}/charts/${id}/report`, {
      headers: _accessToken ? { Authorization: `Bearer ${_accessToken}` } : {},
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.blob()
  },

  svg: (id: number, req: SVGRequest = {}) =>
    apiFetch<SVGOut>(`/charts/${id}/svg`, {
      method: 'POST',
      body: JSON.stringify(req),
    }),

  pdf: async (id: number): Promise<Blob> => {
    const res = await fetch(`${BASE}/charts/${id}/pdf`, {
      method: 'POST',
      headers: _accessToken ? { Authorization: `Bearer ${_accessToken}` } : {},
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.blob()
  },

  confidence: (id: number) =>
    apiFetch<ConfidenceOut>(`/charts/${id}/confidence`),

  scoresV3: (id: number) =>
    apiFetch<ChartV3Out>(`/charts/${id}/scores/v3`),

  guidance: (id: number, req: GuidanceRequest = {}) =>
    apiFetch<GuidanceOut>(`/charts/${id}/guidance`, {
      method: 'POST',
      body: JSON.stringify(req),
    }),
}

// ── health ────────────────────────────────────────────────────────────────────

export const health = {
  check: () => apiFetch<HealthOut>('/health'),
}

// ── mundane ───────────────────────────────────────────────────────────────────

export const mundane = {
  analyze: (req: MundaneRequest) =>
    apiFetch<MundaneOut>('/mundane/analyze', {
      method: 'POST',
      body: JSON.stringify(req),
    }),
}
