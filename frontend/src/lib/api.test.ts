/**
 * frontend/src/lib/api.test.ts — Session 25 unit tests for API client
 */

import { setAccessToken, getAccessToken, auth, charts, health } from './api'

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
