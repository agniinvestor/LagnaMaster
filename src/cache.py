"""
src/cache.py — LagnaMaster Session 20
Redis 3-tier caching layer.  All tiers are optional; if Redis is unavailable
every get() returns None and set() is a no-op, so the application degrades
gracefully.

Three cache tiers
-----------------
Tier 1  ephemeris   BirthChart objects keyed by (year,month,day,hour,lat,lon,tz,ayanamsha)
                    TTL 7 days  — planet positions are immutable for a given instant
Tier 2  scores      ChartScores keyed by chart_id + scoring_engine_version
                    TTL 1 day   — invalidated when the scoring engine changes
Tier 3  av          AshtakavargaChart keyed by chart_id
                    TTL 1 day   — deterministic given the chart

Environment variables
---------------------
REDIS_URL       Redis connection URL  (default redis://localhost:6379/0)
                Set to empty string to disable Redis entirely.
CACHE_VERSION   Integer bumped whenever the scoring engine changes (default 1)

Public API
----------
    get(tier, key)          → dict | None
    set(tier, key, value)   → None
    delete(tier, key)       → None
    flush_tier(tier)        → int   (keys deleted)
    health_check()          → dict
    make_ephemeris_key(...) → str
    make_scores_key(...)    → str
    make_av_key(...)        → str
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ── optional redis import ──────────────────────────────────────────────────────
try:
    import redis

    _REDIS_AVAILABLE = True
except ImportError:
    _REDIS_AVAILABLE = False

# ── tier configuration ────────────────────────────────────────────────────────
TIER_EPHEMERIS = "eph"
TIER_SCORES = "scr"
TIER_AV = "av"

_TTL: dict[str, int] = {
    TIER_EPHEMERIS: 7 * 24 * 3600,  # 7 days
    TIER_SCORES: 24 * 3600,  # 1 day
    TIER_AV: 24 * 3600,  # 1 day
}

_PREFIX = "lm"  # key namespace: lm:{tier}:{key}

# ── module state ──────────────────────────────────────────────────────────────
_client: Optional["redis.Redis"] = None
_disabled: bool = False


def _get_client() -> Optional["redis.Redis"]:
    global _client, _disabled

    if _disabled:
        return None
    if _client is not None:
        return _client

    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    if not url or not _REDIS_AVAILABLE:
        _disabled = True
        return None

    try:
        _client = redis.Redis.from_url(
            url,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        _client.ping()  # fail fast if unreachable
        logger.info("Redis cache connected: %s", url)
        return _client
    except Exception as exc:
        logger.warning("Redis unavailable (%s) — caching disabled", exc)
        _disabled = True
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Key builders
# ──────────────────────────────────────────────────────────────────────────────


def make_ephemeris_key(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float,
    ayanamsha: str,
) -> str:
    """Stable cache key for an ephemeris computation."""
    raw = f"{year}|{month}|{day}|{hour:.4f}|{lat:.6f}|{lon:.6f}|{tz_offset:.2f}|{ayanamsha}"
    digest = hashlib.sha1(raw.encode()).hexdigest()[:16]
    return digest


def make_scores_key(chart_id: int) -> str:
    """Cache key for a chart's domain scores (includes engine version)."""
    version = os.environ.get("CACHE_VERSION", "1")
    return f"{chart_id}:v{version}"


def make_av_key(chart_id: int) -> str:
    """Cache key for a chart's ashtakavarga tables."""
    return str(chart_id)


def _full_key(tier: str, key: str) -> str:
    return f"{_PREFIX}:{tier}:{key}"


# ──────────────────────────────────────────────────────────────────────────────
# Core operations
# ──────────────────────────────────────────────────────────────────────────────


def get(tier: str, key: str) -> Optional[dict]:
    """Return cached value or None on miss / error."""
    r = _get_client()
    if r is None:
        return None
    try:
        raw = r.get(_full_key(tier, key))
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.debug("Cache get error (%s): %s", tier, exc)
        return None


def set(tier: str, key: str, value: Any) -> None:
    """Serialise *value* to JSON and store with the tier's TTL."""
    r = _get_client()
    if r is None:
        return
    try:
        ttl = _TTL.get(tier, 3600)
        r.setex(_full_key(tier, key), ttl, json.dumps(value))
    except Exception as exc:
        logger.debug("Cache set error (%s): %s", tier, exc)


def delete(tier: str, key: str) -> None:
    """Delete a single cache entry."""
    r = _get_client()
    if r is None:
        return
    try:
        r.delete(_full_key(tier, key))
    except Exception as exc:
        logger.debug("Cache delete error (%s): %s", tier, exc)


def flush_tier(tier: str) -> int:
    """Delete all keys in a tier. Returns number of keys deleted."""
    r = _get_client()
    if r is None:
        return 0
    try:
        pattern = _full_key(tier, "*")
        keys = list(r.scan_iter(pattern, count=100))
        if keys:
            return r.delete(*keys)
        return 0
    except Exception as exc:
        logger.debug("Cache flush error (%s): %s", tier, exc)
        return 0


def health_check() -> dict:
    """Return Redis connectivity status."""
    r = _get_client()
    if r is None:
        return {"backend": "redis", "ok": False, "reason": "disabled or unavailable"}
    try:
        r.ping()
        info = r.info("server")
        return {
            "backend": "redis",
            "ok": True,
            "version": info.get("redis_version", "unknown"),
        }
    except Exception as exc:
        return {"backend": "redis", "ok": False, "reason": str(exc)}
