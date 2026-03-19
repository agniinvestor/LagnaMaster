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
}

// ── health ────────────────────────────────────────────────────────────────────

export const health = {
  check: () => apiFetch<HealthOut>('/health'),
}
