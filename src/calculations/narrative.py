"""src/calculations/narrative.py — Narrative synthesis layer.

Architecture gap G7 (Phase A).

Turns convergence scores and timing windows into structured life-phase
narratives that a practitioner can read, verify against source texts,
and present to a querent.

Predictions are not bullet points.  A life is a story.

Public API
----------
  narrate(timed_predictions, ctx) → NarrativeReport
  NarrativeReport — life phases, interactions, absences, arcs, domains

Replaces the Session 39 LPI-based narrative (generate_narrative) with
pipeline-aware narrative from G1-G6 convergence + temporal data.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


from src.calculations.chart_context import ChartContext
from src.calculations.temporal_projection import TimedPrediction
from src.calculations.vimshottari_dasa import MahaDasha

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G7", "session": "S328"}

# ---------------------------------------------------------------------------
# House domain mapping
# ---------------------------------------------------------------------------

HOUSE_DOMAIN: dict[int, str] = {
    1: "self_vitality",
    2: "wealth_family",
    3: "courage_skills",
    4: "home_happiness",
    5: "intellect_children",
    6: "challenges",
    7: "relationships",
    8: "transformation",
    9: "fortune_dharma",
    10: "career_status",
    11: "gains_income",
    12: "liberation_loss",
}

# Broad life domains that group multiple houses
DOMAIN_GROUPS: dict[str, list[int]] = {
    "career": [2, 6, 10, 11],
    "family": [2, 4, 5, 7],
    "health": [1, 6, 8],
    "spiritual": [5, 9, 12],
}

# Phase labels based on dominant dasha lord character
_PHASE_LABELS: dict[str, str] = {
    "Sun": "authority",
    "Moon": "nurturing",
    "Mars": "action",
    "Rahu": "ambition",
    "Jupiter": "expansion",
    "Saturn": "discipline",
    "Mercury": "learning",
    "Ketu": "detachment",
    "Venus": "enjoyment",
}

# Absence meanings per house
_ABSENCE_MEANINGS: dict[int, str] = {
    1: "stable self-image, no major identity shifts",
    2: "financial status quo, no sudden wealth or loss",
    3: "routine communication, no major ventures with siblings",
    4: "stable home environment, no relocation",
    5: "no significant changes in children or creative output",
    6: "no major health crises or litigation",
    7: "relationship status quo, no marriage or separation",
    8: "no major transformative events or crises",
    9: "no significant spiritual or educational shifts",
    10: "career stability, no major professional changes",
    11: "steady income, no windfall or major loss",
    12: "no foreign settlement or major isolation periods",
}

# Human-readable domain labels
_DOMAIN_LABEL: dict[str, str] = {
    "career_status": "career and status",
    "character_temperament": "character",
    "physical_health": "physical health",
    "mental_health": "mental well-being",
    "physical_appearance": "physical constitution",
    "enemies_litigation": "conflicts and litigation",
    "intelligence_education": "education and intellect",
    "fame_reputation": "fame and reputation",
    "foreign_travel": "foreign connections",
    "property_vehicles": "property and vehicles",
    "progeny": "children",
    "wealth": "wealth",
    "marriage": "marriage",
    "health": "health",
    "longevity": "longevity",
    "relationships": "relationships",
    "character": "character",
    "career": "career",
    "spirituality": "spiritual growth",
}


# ---------------------------------------------------------------------------
# NL template rendering
# ---------------------------------------------------------------------------

def _claim_to_phrase(claim: str) -> str:
    """Convert a snake_case claim to readable English phrase."""
    return claim.replace("_", " ").strip()


def _render_domain_text(ds: "DomainSummary", phase_lord: str) -> str:
    """Render a domain summary into a natural language sentence."""
    domain_label = _DOMAIN_LABEL.get(ds.domain, ds.domain.replace("_", " "))
    dir_word = {"favorable": "supported", "unfavorable": "challenged", "mixed": "mixed signals for"}[ds.direction]

    parts = [f"{domain_label.capitalize()}: {dir_word}"]

    if ds.claims:
        # Use the top 2 claims as evidence
        phrases = [_claim_to_phrase(c) for c in ds.claims[:2]]
        parts.append(f" — {'; '.join(phrases)}")

    if ds.peak_window != (0, 0):
        parts.append(f" (peak {ds.peak_window[0]}-{ds.peak_window[1]})")

    return "".join(parts) + "."


def _render_phase_text(phase: "LifePhase") -> str:
    """Render a life phase into a natural language paragraph."""
    dir_label = {
        "favorable": "a period of growth and opportunity",
        "unfavorable": "a period of challenge and restructuring",
        "mixed": "a period of contrasts — opportunity alongside challenge",
    }[phase.dominant_direction]

    lines = [f"{phase.lord} period ({phase.start_year}-{phase.end_year}): {dir_label}."]

    for ds in phase.domain_summaries[:4]:
        if ds.text:
            lines.append(f"  {ds.text}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Claims extraction from EvalResult
# ---------------------------------------------------------------------------

def _extract_house_claims(
    eval_results: list,
) -> dict[tuple[int, str], list[str]]:
    """Extract claim texts from EvalResult predictions, keyed by (house, domain).

    Returns {(house, domain): [claim_text, ...]} for use in NL templates.
    """
    claims: dict[tuple[int, str], list[str]] = defaultdict(list)
    for er in eval_results:
        if not hasattr(er, "predictions") or not er.predictions:
            continue
        for pred in er.predictions:
            if not isinstance(pred, dict):
                continue
            claim = pred.get("claim", "")
            domain = pred.get("domain", "")
            if claim and er.house > 0:
                claims[(er.house, domain)].append(claim)
    return dict(claims)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class DomainSummary:
    """One domain's prediction within a life phase."""
    domain: str
    direction: str            # favorable|unfavorable|mixed
    convergence: int          # strongest convergence score
    peak_window: tuple[int, int] = (0, 0)
    houses: list[int] = field(default_factory=list)
    claims: list[str] = field(default_factory=list)  # from corpus predictions
    text: str = ""            # NL template rendering


@dataclass
class LifePhase:
    """One dasha period with its activated predictions."""
    lord: str
    label: str                # e.g., "discipline", "expansion"
    start_year: int
    end_year: int
    dominant_direction: str   # overall: favorable|unfavorable|mixed
    domain_summaries: list[DomainSummary] = field(default_factory=list)
    activated_houses: list[int] = field(default_factory=list)
    total_favorable: int = 0
    total_unfavorable: int = 0
    text: str = ""            # NL phase summary


@dataclass
class InteractionEffect:
    """Cross-house interaction within the same dasha period."""
    houses: list[int]
    domains: list[str]
    dasha_lord: str
    period: tuple[int, int]
    description: str


@dataclass
class AbsenceEntry:
    """A dormant house — absence is also a prediction."""
    house: int
    domain: str
    meaning: str
    max_convergence: int
    lord: str = ""            # house lord (for per-lagna meaning)


@dataclass
class DomainNarrative:
    """One life domain traced across all phases."""
    domain: str               # "career", "family", "health", "spiritual"
    phases: list[dict] = field(default_factory=list)
    peak_period: tuple[int, int] = (0, 0)
    overall_direction: str = "neutral"


@dataclass
class NarrativeReport:
    """Complete narrative synthesis — Layer 6 output.

    This is what the practitioner reads instead of "H10 = 3.2".
    """
    life_phases: list[LifePhase]
    interaction_effects: list[InteractionEffect]
    absence_analysis: list[AbsenceEntry]
    overall_arc: str
    per_domain_narratives: dict[str, DomainNarrative]
    lagna_sign: str = ""
    total_predictions: int = 0


# ---------------------------------------------------------------------------
# Life phase extraction
# ---------------------------------------------------------------------------

def _build_life_phases(
    predictions: list[TimedPrediction],
    dashas: list[MahaDasha],
    house_claims: dict[tuple[int, str], list[str]] | None = None,
) -> list[LifePhase]:
    """Build life phases from dasha periods + activated predictions."""
    phases: list[LifePhase] = []
    house_claims = house_claims or {}

    for md in dashas:
        md_start = md.start.year
        md_end = md.end.year

        # Find predictions whose peak window falls WITHIN this dasha
        activated: list[TimedPrediction] = []
        for p in predictions:
            pw = p.peak_window
            if pw == (0, 0):
                continue
            peak_mid = (pw[0] + pw[1]) / 2
            if md_start <= peak_mid <= md_end:
                activated.append(p)

        fav = sum(1 for p in activated if p.direction == "favorable")
        unfav = sum(1 for p in activated if p.direction == "unfavorable")
        dominant = "favorable" if fav > unfav else ("unfavorable" if unfav > fav else "mixed")

        # Group by domain
        domain_preds: dict[str, list[TimedPrediction]] = defaultdict(list)
        houses_seen: set[int] = set()
        for p in activated:
            houses_seen.add(p.house)
            for d in p.outcome_domains:
                domain_preds[d].append(p)
            if not p.outcome_domains:
                domain_preds[HOUSE_DOMAIN.get(p.house, "other")].append(p)

        domain_summaries: list[DomainSummary] = []
        for domain, preds in sorted(domain_preds.items()):
            fav_d = sum(1 for p in preds if p.direction == "favorable")
            unfav_d = sum(1 for p in preds if p.direction == "unfavorable")
            d_dir = "favorable" if fav_d > unfav_d else ("unfavorable" if unfav_d > fav_d else "mixed")

            best_conv = max((p.convergence_score for p in preds), default=0)
            best_pred = max(preds, key=lambda p: p.convergence_score)
            d_houses = sorted({p.house for p in preds})

            # Collect claims from corpus for this domain + houses
            domain_claims: list[str] = []
            for h in d_houses:
                domain_claims.extend(house_claims.get((h, domain), []))
            # Deduplicate while preserving order
            seen_claims: set[str] = set()
            unique_claims: list[str] = []
            for c in domain_claims:
                if c not in seen_claims:
                    seen_claims.add(c)
                    unique_claims.append(c)

            ds = DomainSummary(
                domain=domain,
                direction=d_dir,
                convergence=best_conv,
                peak_window=best_pred.peak_window,
                houses=d_houses,
                claims=unique_claims[:5],  # top 5 claims
            )
            ds.text = _render_domain_text(ds, md.lord)
            domain_summaries.append(ds)

        phase = LifePhase(
            lord=md.lord,
            label=_PHASE_LABELS.get(md.lord, "transition"),
            start_year=md_start,
            end_year=md_end,
            dominant_direction=dominant,
            domain_summaries=sorted(domain_summaries, key=lambda d: -d.convergence),
            activated_houses=sorted(houses_seen),
            total_favorable=fav,
            total_unfavorable=unfav,
        )
        phase.text = _render_phase_text(phase)
        phases.append(phase)

    return phases


# ---------------------------------------------------------------------------
# Interaction effects
# ---------------------------------------------------------------------------

# Known interaction meanings (enriches data-driven detection)
_KNOWN_INTERACTIONS: dict[frozenset[int], str] = {
    frozenset({7, 10}): "spouse connected to career",
    frozenset({5, 7}): "children follow partnership",
    frozenset({4, 10}): "home and career tension",
    frozenset({2, 11}): "wealth from multiple sources",
    frozenset({1, 8}): "deep personal transformation",
    frozenset({9, 12}): "spiritual journey abroad",
    frozenset({3, 10}): "career through communication",
    frozenset({6, 8}): "health crisis and transformation",
    frozenset({5, 9}): "wisdom and progeny linked",
    frozenset({2, 7}): "wealth through partnership",
}


def _detect_interactions(phases: list[LifePhase]) -> list[InteractionEffect]:
    """Detect cross-house interactions — data-driven co-activation.

    Any pair of houses that activate in the same dasha period AND share
    overlapping domains is flagged as an interaction.  Known patterns
    get enriched descriptions; novel co-activations get auto-generated ones.
    """
    effects: list[InteractionEffect] = []
    seen: set[tuple[int, int, str]] = set()

    for phase in phases:
        if len(phase.activated_houses) < 2:
            continue

        # Build house→domains mapping for this phase
        house_domains: dict[int, set[str]] = defaultdict(set)
        for ds in phase.domain_summaries:
            for h in ds.houses:
                house_domains[h].add(ds.domain)

        # Check all pairs of activated houses
        houses = phase.activated_houses
        for i, h1 in enumerate(houses):
            for h2 in houses[i + 1:]:
                key = (min(h1, h2), max(h1, h2), phase.lord)
                if key in seen:
                    continue
                seen.add(key)

                # Shared domains = interaction
                shared = house_domains.get(h1, set()) & house_domains.get(h2, set())
                if not shared:
                    # Even without shared domains, known patterns still count
                    pair = frozenset({h1, h2})
                    if pair not in _KNOWN_INTERACTIONS:
                        continue

                pair = frozenset({h1, h2})
                known = _KNOWN_INTERACTIONS.get(pair)

                if known:
                    desc = known
                else:
                    # Auto-generate description from domain names
                    d1 = HOUSE_DOMAIN.get(h1, f"H{h1}")
                    d2 = HOUSE_DOMAIN.get(h2, f"H{h2}")
                    desc = f"{d1} and {d2} co-activate"

                all_domains = house_domains.get(h1, set()) | house_domains.get(h2, set())

                effects.append(InteractionEffect(
                    houses=sorted({h1, h2}),
                    domains=sorted(all_domains),
                    dasha_lord=phase.lord,
                    period=(phase.start_year, phase.end_year),
                    description=desc,
                ))

    return effects


# ---------------------------------------------------------------------------
# Absence analysis
# ---------------------------------------------------------------------------

def _analyze_absences(
    predictions: list[TimedPrediction],
    ctx: ChartContext | None = None,
) -> list[AbsenceEntry]:
    """Identify relatively dormant houses with per-lagna meanings.

    Uses bottom-quartile threshold. Absence meanings are customized
    using the house lord from ChartContext when available.
    """
    house_max_conv: dict[int, int] = {h: 0 for h in range(1, 13)}
    for p in predictions:
        if p.convergence_score > house_max_conv.get(p.house, 0):
            house_max_conv[p.house] = p.convergence_score

    all_convs = sorted(house_max_conv.values())
    q1_idx = max(0, len(all_convs) // 4 - 1)
    threshold = all_convs[q1_idx] if all_convs else 1

    absences: list[AbsenceEntry] = []
    for house, max_conv in sorted(house_max_conv.items()):
        if max_conv > threshold:
            continue

        domain = HOUSE_DOMAIN.get(house, "unknown")
        generic = _ABSENCE_MEANINGS.get(house, "no significant activation")

        # Per-lagna enrichment: identify the house lord
        lord = ""
        if ctx is not None:
            lord = ctx.house_map.house_lord[house - 1]
            domain_label = _DOMAIN_LABEL.get(domain, domain.replace("_", " "))
            meaning = (
                f"{generic} ({lord} as {house}th lord "
                f"does not strongly activate {domain_label})"
            )
        else:
            meaning = generic

        absences.append(AbsenceEntry(
            house=house,
            domain=domain,
            meaning=meaning,
            max_convergence=max_conv,
            lord=lord,
        ))

    return absences


# ---------------------------------------------------------------------------
# Overall arc
# ---------------------------------------------------------------------------

def _compute_arc(phases: list[LifePhase]) -> str:
    """Compute the overall life trajectory across thirds of the dasha sequence."""
    if not phases:
        return "unknown"

    n = len(phases)
    thirds = [
        phases[:max(1, n // 3)],
        phases[max(1, n // 3):max(2, 2 * n // 3)],
        phases[max(2, 2 * n // 3):],
    ]

    def label(group):
        if not group:
            return "neutral"
        fav = sum(p.total_favorable for p in group)
        unfav = sum(p.total_unfavorable for p in group)
        if fav > unfav * 1.5:
            return "favorable"
        if unfav > fav * 1.5:
            return "challenging"
        return "mixed"

    labels = [label(t) for t in thirds]

    arc_map = {
        ("favorable", "favorable", "favorable"): "sustained prosperity",
        ("challenging", "favorable", "favorable"): "building to harvest",
        ("favorable", "challenging", "favorable"): "challenge then recovery",
        ("favorable", "favorable", "challenging"): "early success, later tests",
        ("challenging", "challenging", "favorable"): "long struggle to late harvest",
        ("favorable", "challenging", "challenging"): "early promise, sustained challenges",
        ("challenging", "favorable", "challenging"): "middle peak",
        ("challenging", "challenging", "challenging"): "persistent challenges",
    }

    return arc_map.get(tuple(labels), f"{labels[0]} early, {labels[1]} middle, {labels[2]} late")


# ---------------------------------------------------------------------------
# Per-domain narratives
# ---------------------------------------------------------------------------

def _build_domain_narratives(phases: list[LifePhase]) -> dict[str, DomainNarrative]:
    """Trace each broad domain across all life phases."""
    narratives: dict[str, DomainNarrative] = {}

    for domain_name, house_list in DOMAIN_GROUPS.items():
        house_set = set(house_list)
        phase_entries: list[dict] = []
        best_conv = 0
        best_peak = (0, 0)
        total_fav = 0
        total_unfav = 0

        for phase in phases:
            relevant = [ds for ds in phase.domain_summaries if any(h in house_set for h in ds.houses)]
            if relevant:
                pf = sum(1 for ds in relevant if ds.direction == "favorable")
                pu = sum(1 for ds in relevant if ds.direction == "unfavorable")
                pc = max(ds.convergence for ds in relevant)
                total_fav += pf
                total_unfav += pu
                if pc > best_conv:
                    best_conv = pc
                    best_peak = max(relevant, key=lambda d: d.convergence).peak_window
                phase_entries.append({
                    "dasha_lord": phase.lord,
                    "period": (phase.start_year, phase.end_year),
                    "direction": "favorable" if pf > pu else ("unfavorable" if pu > pf else "mixed"),
                    "convergence": pc,
                })

        overall = "favorable" if total_fav > total_unfav else (
            "unfavorable" if total_unfav > total_fav else "mixed")

        narratives[domain_name] = DomainNarrative(
            domain=domain_name, phases=phase_entries,
            peak_period=best_peak, overall_direction=overall,
        )

    return narratives


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def narrate(
    timed_predictions: list[TimedPrediction],
    ctx: ChartContext,
    eval_results: list | None = None,
) -> NarrativeReport:
    """Synthesize timed predictions into a narrative report.

    Parameters
    ----------
    timed_predictions : list[TimedPrediction]
        From time_project().
    ctx : ChartContext
        Pre-computed chart context (needs dashas for life phases).
    eval_results : list[EvalResult], optional
        From evaluate_all_rules(). Used to extract claim texts for
        natural language templates.

    Returns
    -------
    NarrativeReport
        Life phases, interactions, absences, arc, domain narratives.
    """
    dashas = ctx.dashas or []

    # Extract claims from corpus rules for NL templates
    house_claims = _extract_house_claims(eval_results) if eval_results else {}

    life_phases = _build_life_phases(timed_predictions, dashas, house_claims)
    interactions = _detect_interactions(life_phases)
    absences = _analyze_absences(timed_predictions, ctx)
    arc = _compute_arc(life_phases)
    domain_narratives = _build_domain_narratives(life_phases)

    return NarrativeReport(
        life_phases=life_phases,
        interaction_effects=interactions,
        absence_analysis=absences,
        overall_arc=arc,
        per_domain_narratives=domain_narratives,
        lagna_sign=ctx.chart.lagna_sign,
        total_predictions=len(timed_predictions),
    )
