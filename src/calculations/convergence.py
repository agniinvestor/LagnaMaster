"""src/calculations/convergence.py — Multi-signal convergence layer.

Architecture gap G5.

For each house+direction combination, counts INDEPENDENT confirmations
across evidence channels.  5 weak signals summing to 3.0 ≠ 3 confirmed
signals at 1.0.  Convergence across independent evidence is qualitatively
different from score accumulation.

Evidence channels (independent axes):
  - scoring: structural house quality (26 rules)
  - bphs: BPHS verse-specific predictions
  - saravali: Saravali text confirmations
  - other_text: any other classical text (BhavarthaRatnakara, etc.)
  - yoga: yoga-based confirmations (from signal_group)

Contra-indicators are counted separately — NOT netted against confirmations.
A house with 4 confirmations + 2 contra-indicators is different from a house
with 2 net confirmations.

Public API
----------
  converge(eval_results, ctx) → list[ConvergedPrediction]
  ConvergedPrediction — one house prediction with convergence data
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from src.calculations.chart_context import ChartContext
from src.calculations.unified_engine import EvalResult

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G5", "session": "S328"}


# ---------------------------------------------------------------------------
# Evidence channels
# ---------------------------------------------------------------------------

# D3: Yoga rule detection — categories and tags that identify yoga rules
_YOGA_CATEGORIES = {"raja_yoga", "yoga", "yogakaraka"}

_yoga_rule_ids_cache: set[str] | None = None


def _get_yoga_rule_ids() -> set[str]:
    """Build and cache the set of yoga-related rule_ids from the corpus."""
    global _yoga_rule_ids_cache
    if _yoga_rule_ids_cache is not None:
        return _yoga_rule_ids_cache
    try:
        from src.corpus.combined_corpus import build_corpus
        corpus = build_corpus()
        ids: set[str] = set()
        for r in corpus.all():
            if r.category in _YOGA_CATEGORIES:
                ids.add(r.rule_id)
            elif any("yoga" in t.lower() for t in (r.keyword_tags or [])):
                ids.add(r.rule_id)
        _yoga_rule_ids_cache = ids
    except (ImportError, Exception):
        _yoga_rule_ids_cache = set()
    return _yoga_rule_ids_cache


def _classify_channel(result: EvalResult) -> str:
    """Classify an EvalResult into its evidence channel.

    D3: Yoga detection uses category + tags from corpus, not just signal_group keyword.
    """
    if result.rule_category == "scoring_rule":
        return "scoring"
    # D2: Varga natal channels
    if result.rule_category == "scoring_d9":
        return "d9_natal"
    if result.rule_category == "scoring_d10":
        return "d10_natal"

    # D3: Check if this is a yoga rule (by category/tag lookup)
    if result.rule_id in _get_yoga_rule_ids():
        return "yoga"

    source = result.source.lower()
    if source == "bphs":
        return "bphs"
    if source == "saravali":
        return "saravali"
    if result.signal_group and "yoga" in result.signal_group.lower():
        return "yoga"
    return "other_text"


# ---------------------------------------------------------------------------
# ConvergedPrediction
# ---------------------------------------------------------------------------

@dataclass
class ConfirmationSource:
    """One independent confirmation of a house prediction."""
    channel: str           # scoring|bphs|saravali|other_text|yoga
    rule_id: str
    magnitude: float
    verse: str = ""


@dataclass
class ConvergedPrediction:
    """A house prediction with multi-signal convergence data.

    This is NOT a sum of scores.  It's a count of HOW MANY independent
    evidence channels confirm the same direction for the same house.
    """
    house: int
    direction: str                                    # favorable|unfavorable
    convergence_score: int                            # count of confirming channels
    confirmation_sources: list[ConfirmationSource] = field(default_factory=list)
    contra_indicators: list[ConfirmationSource] = field(default_factory=list)
    contra_score: int = 0                             # count of contra channels
    outcome_domains: list[str] = field(default_factory=list)
    total_magnitude: float = 0.0                      # sum of confirming magnitudes
    total_contra_magnitude: float = 0.0               # sum of contra magnitudes

    @property
    def net_channels(self) -> int:
        """Confirming channels minus contra channels."""
        return self.convergence_score - self.contra_score

    @property
    def strength_label(self) -> str:
        """Human-readable convergence strength."""
        cs = self.convergence_score
        if cs >= 4:
            return "very_strong"
        if cs >= 3:
            return "strong"
        if cs >= 2:
            return "moderate"
        return "weak"


# ---------------------------------------------------------------------------
# Convergence algorithm
# ---------------------------------------------------------------------------

def converge(
    eval_results: list[EvalResult],
    ctx: Optional[ChartContext] = None,
) -> list[ConvergedPrediction]:
    """Synthesize EvalResults into converged predictions.

    Groups results by house + direction, counts independent evidence
    channels, and tracks contra-indicators separately.

    Parameters
    ----------
    eval_results : list[EvalResult]
        Flat list from evaluate_all_rules().
    ctx : ChartContext, optional
        Chart context (reserved for future use — varga overlay, dasha checks).

    Returns
    -------
    list[ConvergedPrediction]
        One per house+direction with convergence data, sorted by
        convergence_score descending.
    """
    # Group by house → direction → channel → results
    # A channel confirms at most ONCE per house+direction (independence)
    house_dir: dict[tuple[int, str], dict[str, list[EvalResult]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for r in eval_results:
        if r.house == 0:
            continue  # skip non-house-specific rules
        if r.direction in ("neutral", "mixed"):
            continue  # only converge clear favorable/unfavorable signals

        channel = _classify_channel(r)
        house_dir[(r.house, r.direction)][channel].append(r)

    # Build ConvergedPrediction for each house
    # For each house, we produce two entries: favorable and unfavorable
    # The "other" direction becomes contra-indicators
    predictions: list[ConvergedPrediction] = []

    # Collect all houses that have any signal
    houses_seen: set[int] = {key[0] for key in house_dir}

    for house in sorted(houses_seen):
        fav_channels = house_dir.get((house, "favorable"), {})
        unfav_channels = house_dir.get((house, "unfavorable"), {})

        # Build favorable prediction (if any confirming channels)
        if fav_channels:
            confirmations: list[ConfirmationSource] = []
            domains: set[str] = set()
            total_mag = 0.0

            for channel, results in fav_channels.items():
                # Pick the strongest result per channel (independence: 1 per channel)
                best = max(results, key=lambda r: abs(r.magnitude))
                confirmations.append(ConfirmationSource(
                    channel=channel,
                    rule_id=best.rule_id,
                    magnitude=best.magnitude,
                    verse=best.verse,
                ))
                total_mag += best.magnitude
                for r in results:
                    domains.update(r.outcome_domains)

            # Contra-indicators: unfavorable channels for this house
            contras: list[ConfirmationSource] = []
            contra_mag = 0.0
            for channel, results in unfav_channels.items():
                best = max(results, key=lambda r: abs(r.magnitude))
                contras.append(ConfirmationSource(
                    channel=channel,
                    rule_id=best.rule_id,
                    magnitude=best.magnitude,
                    verse=best.verse,
                ))
                contra_mag += abs(best.magnitude)

            predictions.append(ConvergedPrediction(
                house=house,
                direction="favorable",
                convergence_score=len(confirmations),
                confirmation_sources=confirmations,
                contra_indicators=contras,
                contra_score=len(contras),
                outcome_domains=sorted(domains),
                total_magnitude=total_mag,
                total_contra_magnitude=contra_mag,
            ))

        # Build unfavorable prediction (if any confirming channels)
        if unfav_channels:
            confirmations = []
            domains = set()
            total_mag = 0.0

            for channel, results in unfav_channels.items():
                best = max(results, key=lambda r: abs(r.magnitude))
                confirmations.append(ConfirmationSource(
                    channel=channel,
                    rule_id=best.rule_id,
                    magnitude=best.magnitude,
                    verse=best.verse,
                ))
                total_mag += abs(best.magnitude)
                for r in results:
                    domains.update(r.outcome_domains)

            # Contra: favorable channels
            contras = []
            contra_mag = 0.0
            for channel, results in fav_channels.items():
                best = max(results, key=lambda r: abs(r.magnitude))
                contras.append(ConfirmationSource(
                    channel=channel,
                    rule_id=best.rule_id,
                    magnitude=best.magnitude,
                    verse=best.verse,
                ))
                contra_mag += abs(best.magnitude)

            predictions.append(ConvergedPrediction(
                house=house,
                direction="unfavorable",
                convergence_score=len(confirmations),
                confirmation_sources=confirmations,
                contra_indicators=contras,
                contra_score=len(contras),
                outcome_domains=sorted(domains),
                total_magnitude=total_mag,
                total_contra_magnitude=contra_mag,
            ))

    # Sort: highest convergence first, then by house
    predictions.sort(key=lambda p: (-p.convergence_score, p.house))

    return predictions
