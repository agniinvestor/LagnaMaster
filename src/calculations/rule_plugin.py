"""
src/calculations/rule_plugin.py — Session 108

Dynamic Rule Plugin Architecture.
Allows custom yogas, rules, and scoring modifiers to be registered
without modifying the core engine.

Use cases:
  - Regional traditional rules (Kerala, Bengal, Tamil traditions)
  - Practitioner-specific custom rules
  - B.V. Raman's supplementary rules
  - Experimental rules for empirical testing

API:
  @register_yoga("My Custom Yoga")
  def my_yoga(chart) -> bool: ...

  @register_scorer("My Score Modifier")
  def my_scorer(chart, house) -> float: ...

  results = apply_all_plugins(chart)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
import functools

_YOGA_REGISTRY: dict[str, dict] = {}
_SCORER_REGISTRY: dict[str, dict] = {}


@dataclass
class PluginYogaResult:
    name: str
    source: str
    present: bool
    score: float
    description: str
    plugin_note: str = "Custom/extended rule — not core classical engine"


@dataclass
class PluginScoreResult:
    name: str
    house: int
    modifier: float
    description: str


def register_yoga(name: str, source: str = "Custom",
                   score_if_present: float = 1.0):
    """Decorator to register a custom yoga detection function."""
    def decorator(fn: Callable) -> Callable:
        _YOGA_REGISTRY[name] = {
            "fn": fn, "source": source,
            "score": score_if_present,
        }
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def register_scorer(name: str, description: str = ""):
    """Decorator to register a custom house score modifier."""
    def decorator(fn: Callable) -> Callable:
        _SCORER_REGISTRY[name] = {"fn": fn, "description": description}
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def apply_all_plugins(chart) -> list[PluginYogaResult]:
    """Run all registered yoga plugins against a chart."""
    results = []
    for name, reg in _YOGA_REGISTRY.items():
        try:
            present = reg["fn"](chart)
            results.append(PluginYogaResult(
                name=name, source=reg["source"],
                present=bool(present),
                score=reg["score"] if present else 0.0,
                description=f"Plugin yoga: {name}",
            ))
        except Exception as e:
            results.append(PluginYogaResult(
                name=name, source=reg["source"], present=False, score=0.0,
                description=f"Plugin error: {e}",
            ))
    return results


def apply_score_plugins(chart, house: int) -> list[PluginScoreResult]:
    """Run all registered score modifier plugins for a house."""
    results = []
    for name, reg in _SCORER_REGISTRY.items():
        try:
            modifier = reg["fn"](chart, house)
            if modifier != 0.0:
                results.append(PluginScoreResult(
                    name=name, house=house, modifier=float(modifier),
                    description=reg["description"],
                ))
        except Exception:
            pass
    return results


def list_plugins() -> dict:
    """List all registered plugins."""
    return {
        "yogas":   list(_YOGA_REGISTRY.keys()),
        "scorers": list(_SCORER_REGISTRY.keys()),
    }


def clear_plugins() -> None:
    """Clear all registered plugins (for testing)."""
    _YOGA_REGISTRY.clear()
    _SCORER_REGISTRY.clear()


# ── Built-in example plugin: B.V. Raman's Gajakesari strict version ──────────
@register_yoga("Gajakesari (BVR strict)", "B.V. Raman Three Hundred Combinations", 2.0)
def _gajakesari_bvr(chart) -> bool:
    """
    BVR's strict Gajakesari: Jupiter in kendra from Moon AND Jupiter strong.
    Classical: Jupiter in 1st/4th/7th/10th from Moon.
    BVR adds: Jupiter must not be combust or debilitated.
    """
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    moon_h = ph.get("Moon", 0)
    jup_h  = ph.get("Jupiter", 0)
    if moon_h == 0 or jup_h == 0:
        return False
    diff = abs(jup_h - moon_h) % 12
    in_kendra = diff in {0, 3, 6, 9}
    try:
        from src.calculations.dignity import compute_all_dignities
        dig = compute_all_dignities(chart).get("Jupiter")
        not_afflicted = not (dig and dig.combust)
    except Exception:
        not_afflicted = True
    return in_kendra and not_afflicted
