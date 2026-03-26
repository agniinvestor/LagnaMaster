/**
 * frontend/src/lib/api.test.ts — Session 25 unit tests for API client
 */

import { setAccessToken, getAccessToken, auth, charts as chartsApi, health, mundane as mundaneApi } from './api'
const charts = chartsApi

// Mock global fetch
const mockFetch = jest.fn()
global.fetch = mockFetch

function mockResponse(body: unknown, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText: status === 200 ? 'OK' : 'Error',
    json: () => Promise.resolve(body),
    blob: () => Promise.resolve(new Blob([JSON.stringify(body)])),
  } as Response
}

beforeEach(() => {
  mockFetch.mockReset()
  setAccessToken(null)
})

describe('Token management', () => {
  it('stores and retrieves access token', () => {
    setAccessToken('test-token')
    expect(getAccessToken()).toBe('test-token')
  })

  it('clears access token', () => {
    setAccessToken('test-token')
    setAccessToken(null)
    expect(getAccessToken()).toBeNull()
  })
})

describe('auth.login', () => {
  it('POSTs to /api/auth/login', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      access_token: 'acc', refresh_token: 'ref',
      token_type: 'bearer', access_expires_in: 900, refresh_expires_in: 604800,
    }))
    const result = await auth.login('alice', 'password123')
    expect(mockFetch).toHaveBeenCalledWith('/api/auth/login', expect.objectContaining({
      method: 'POST',
    }))
    expect(result.access_token).toBe('acc')
  })

  it('throws on 401', async () => {
    mockFetch.mockResolvedValue(mockResponse({ detail: 'Invalid credentials' }, 401))
    await expect(auth.login('alice', 'wrong')).rejects.toThrow('Invalid credentials')
  })
})

describe('auth.me', () => {
  it('includes Authorization header when token set', async () => {
    setAccessToken('my-token')
    mockFetch.mockResolvedValue(mockResponse({
      id: 1, username: 'alice', email: 'a@x.com',
      created_at: '2026-01-01', is_active: true,
    }))
    await auth.me()
    const [, opts] = mockFetch.mock.calls[0]
    expect((opts as RequestInit).headers).toMatchObject({
      Authorization: 'Bearer my-token',
    })
  })
})

describe('charts.create', () => {
  it('POSTs birth data to /api/charts', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      id: 1, lagna_sign: 'Taurus', lagna_sign_index: 1,
      lagna_degree: 7.73, ayanamsha_name: 'lahiri',
      ayanamsha_value: 23.15, jd_ut: 2432412.27, planets: {},
    }))
    const result = await charts.create({
      year: 1947, month: 8, day: 15, hour: 0,
      lat: 28.6139, lon: 77.209,
    })
    expect(result.lagna_sign).toBe('Taurus')
    expect(mockFetch).toHaveBeenCalledWith('/api/charts', expect.objectContaining({
      method: 'POST',
    }))
  })
})

describe('charts.scores', () => {
  it('GETs /api/charts/:id/scores', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_id: 1, lagna_sign: 'Taurus', houses: {},
    }))
    await charts.scores(1)
    expect(mockFetch).toHaveBeenCalledWith('/api/charts/1/scores', expect.any(Object))
  })
})

describe('health.check', () => {
  it('returns health object', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      status: 'ok', version: '0.2.0',
      db: { backend: 'sqlite', ok: true },
      cache: { backend: 'redis', ok: false },
    }))
    const h = await health.check()
    expect(h.status).toBe('ok')
    expect(h.db.backend).toBe('sqlite')
  })
})

describe('charts.svg', () => {
  it('POSTs to /api/charts/:id/svg', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_id: 1, style: 'north_indian', svg: '<svg></svg>',
    }))
    const result = await chartsApi.svg(1, { style: 'north_indian' })
    expect(mockFetch).toHaveBeenCalledWith('/api/charts/1/svg', expect.objectContaining({
      method: 'POST',
    }))
    expect(result.svg).toBe('<svg></svg>')
  })
})

describe('charts.confidence', () => {
  it('GETs /api/charts/:id/confidence', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_id: 1,
      lagna_boundary_margin_deg: 5.2,
      lagna_boundary_warning: false,
      moon_nakshatra_boundary: false,
      overall_reliability: 'High',
      uncertainty_sources: [],
      house_confidence: {},
    }))
    const result = await chartsApi.confidence(1)
    expect(mockFetch).toHaveBeenCalledWith('/api/charts/1/confidence', expect.any(Object))
    expect(result.overall_reliability).toBe('High')
  })
})

describe('charts.scoresV3', () => {
  it('GETs /api/charts/:id/scores/v3', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_id: 1, lagna_sign: 'Taurus', engine_version: 'v3.0.0',
      d1_scores: { '1': 2.5 }, cl_scores: {}, sl_scores: {},
      d9_scores: {}, d10_scores: {},
      raja_yogas: [], viparita_yogas: [], neecha_bhanga: [],
    }))
    const result = await chartsApi.scoresV3(1)
    expect(mockFetch).toHaveBeenCalledWith('/api/charts/1/scores/v3', expect.any(Object))
    expect(result.d1_scores['1']).toBe(2.5)
  })
})

describe('charts.guidance', () => {
  it('POSTs to /api/charts/:id/guidance', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_id: 1, domain: 'career', heading: 'Strong period',
      summary: 'Career looks good', signal_bars: 4, signal_display: '●●●●○',
      timing_label: 'Active', confidence_label: 'High',
      confidence_note: 'Birth time reliable', disclaimer: 'For guidance only',
      factors: [], timing_note: '', domain_context: '',
      technical_detail: {}, depth_returned: 'L1',
    }))
    const result = await chartsApi.guidance(1, { domain: 'career', depth: 'L1' })
    expect(mockFetch).toHaveBeenCalledWith('/api/charts/1/guidance', expect.objectContaining({
      method: 'POST',
    }))
    expect(result.signal_bars).toBe(4)
  })
})

describe('mundane.analyze', () => {
  it('POSTs to /api/mundane/analyze', async () => {
    mockFetch.mockResolvedValue(mockResponse({
      chart_type: 'ingress', event_description: 'Solar ingress',
      date: '2026-03-20', location: 'Greenwich',
      key_themes: ['New cycle'], challenges: ['Instability'],
      house_significations: { '1': 'National identity' },
      compressed_dasha: null,
    }))
    const result = await mundaneApi.analyze({
      year: 2026, month: 3, day: 20, lat: 51.477, lon: 0.0,
    })
    expect(mockFetch).toHaveBeenCalledWith('/api/mundane/analyze', expect.objectContaining({
      method: 'POST',
    }))
    expect(result.key_themes[0]).toBe('New cycle')
  })
})
