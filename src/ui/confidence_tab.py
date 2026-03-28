"""
src/ui/confidence_tab.py — Streamlit tab for Birth Time Sensitivity / Confidence Model

Surfaces the existing GET /charts/{id}/confidence endpoint (built S188).
Previously only accessible via API — no UI. This closes UI-1.

Layer 1 (Birth Time Sensitivity) of the prediction pipeline:
  D1: ±2hr accuracy → HIGH confidence for 99% of charts
  D9: ±5min required for character/marriage
  D10: ±6min required for career
  D60: ±1-2min required (rarely available)
  KP sublord: ±30sec required (rarely available)
"""
from __future__ import annotations

try:
    import streamlit as st
    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False


# ─────────────────────────────────────────────────────────────────────────────
# Accuracy requirements by divisional chart (from PREDICTION_PIPELINE.md L1)
# ─────────────────────────────────────────────────────────────────────────────

_VARGA_ACCURACY = [
    ("D1 (Natal Chart)", "±2 hours", "HIGH", "✅"),
    ("D9 (Character, Marriage)", "±5 minutes", "MEDIUM-HIGH", "⚠️"),
    ("D10 (Career)", "±6 minutes", "MEDIUM", "⚠️"),
    ("D60 (Karmic)", "±1–2 minutes", "LOW", "🔴"),
    ("KP Sub-lord", "±30 seconds", "LOW", "🔴"),
]

_GRADE_COLOUR = {
    "HIGH": "#2d7a2d",
    "MEDIUM-HIGH": "#7a7a2d",
    "MEDIUM": "#c17a00",
    "LOW": "#b02020",
    "VERY_LOW": "#7a1010",
}


def _grade_html(grade: str, value: float | None = None) -> str:
    colour = _GRADE_COLOUR.get(grade, "#555")
    label = f"{grade}" + (f" ({value:.1f}%)" if value is not None else "")
    return f'<span style="color:{colour};font-weight:bold">{label}</span>'


def _sensitivity_bar(value: float, max_val: float = 30.0) -> str:
    """Return a visual bar string for a sensitivity value."""
    pct = min(1.0, value / max_val) if max_val > 0 else 0
    filled = int(pct * 20)
    bar = "█" * filled + "░" * (20 - filled)
    colour = "#b02020" if pct > 0.7 else "#c17a00" if pct > 0.3 else "#2d7a2d"
    return f'<span style="font-family:monospace;color:{colour}">[{bar}]</span>'


# ─────────────────────────────────────────────────────────────────────────────
# API call helper (uses Streamlit's session state to track chart_id)
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_confidence(chart_id: str, api_base: str = "http://localhost:8000") -> dict:
    """Call GET /charts/{id}/confidence and return parsed JSON."""
    try:
        import requests  # noqa: PLC0415
        resp = requests.get(f"{api_base}/charts/{chart_id}/confidence", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


# ─────────────────────────────────────────────────────────────────────────────
# Main tab renderer
# ─────────────────────────────────────────────────────────────────────────────

def render_confidence_tab(chart_id: str | None = None, api_base: str = "http://localhost:8000") -> None:
    """
    Render the Confidence / Birth Time Sensitivity tab in Streamlit.

    Args:
        chart_id: Chart UUID to fetch confidence for. If None, prompts user.
        api_base: FastAPI base URL.
    """
    if not _HAS_STREAMLIT:
        raise RuntimeError("Streamlit is not installed")

    st.subheader("🎯 Birth Time Sensitivity — Layer 1 Confidence")
    st.caption(
        "How accurate does the birth time need to be for each level of analysis? "
        "This is Layer 1 of the prediction pipeline — the foundation for all assessments."
    )

    # ── Chart ID input ────────────────────────────────────────────────────────
    if chart_id is None:
        chart_id = st.text_input(
            "Chart ID", placeholder="Enter chart UUID from the Scores tab", key="confidence_chart_id"
        )

    if not chart_id:
        st.info("Enter a chart ID above to see birth time sensitivity analysis.")
        _render_accuracy_table()
        return

    # ── Fetch from API ────────────────────────────────────────────────────────
    with st.spinner("Fetching confidence data..."):
        data = _fetch_confidence(chart_id, api_base)

    if "error" in data:
        st.error(f"API error: {data['error']}")
        st.caption("Is the FastAPI server running? Start with: `uvicorn src.api.main:app --reload`")
        _render_accuracy_table()
        return

    # ── Render confidence summary ─────────────────────────────────────────────
    _render_confidence_summary(data)
    st.divider()
    _render_accuracy_table()
    st.divider()
    _render_sensitivity_detail(data)


def _render_confidence_summary(data: dict) -> None:
    """Overall confidence grade and key flags."""
    if not _HAS_STREAMLIT:
        return

    grade = data.get("grade", "UNKNOWN")
    lagna_stable = data.get("lagna_stable", True)
    nakshatra_stable = data.get("nakshatra_stable", True)
    birth_time_window = data.get("birth_time_window_minutes", 30)

    col1, col2, col3 = st.columns(3)

    with col1:
        colour = _GRADE_COLOUR.get(grade, "#555")
        st.markdown(
            f'<div style="font-size:2rem;text-align:center;color:{colour}">'
            f'{"🟢" if grade == "HIGH" else "🟡" if "MEDIUM" in grade else "🔴"}'
            f"</div>"
            f'<div style="text-align:center;font-weight:bold;color:{colour}">{grade}</div>'
            f'<div style="text-align:center;font-size:0.8rem">Overall confidence</div>',
            unsafe_allow_html=True,
        )

    with col2:
        icon = "✅" if lagna_stable else "⚠️"
        st.metric("Lagna Stable", icon, help="Does the rising sign remain constant across the sensitivity window?")

    with col3:
        icon = "✅" if nakshatra_stable else "⚠️"
        st.metric("Nakshatra Stable", icon, help="Does the birth nakshatra (and dasha timing) remain constant?")

    # Warnings
    if not lagna_stable:
        st.warning(
            "⚠️ **Lagna boundary sensitivity detected.** "
            "The rising sign may change within the birth time window. "
            "House-based predictions carry higher uncertainty. "
            "Verify birth time from hospital records if possible."
        )
    if not nakshatra_stable:
        st.warning(
            "⚠️ **Nakshatra boundary sensitivity detected.** "
            "Dasha timing may shift within the birth time window. "
            "Temporal predictions (dasha/antardasha) carry higher uncertainty."
        )
    if lagna_stable and nakshatra_stable:
        st.success(
            f"✅ Chart is stable across a ±{birth_time_window}-minute window. "
            "D1 assessments can be issued with standard confidence."
        )


def _render_accuracy_table() -> None:
    """Display the varga accuracy requirements table."""
    if not _HAS_STREAMLIT:
        return

    st.markdown("#### Birth Time Accuracy Requirements by Analysis Level")
    st.caption("Different analysis depths require different birth time precision.")

    cols = st.columns([3, 2, 2, 1])
    headers = ["Divisional Chart", "Required Accuracy", "Confidence Grade", ""]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    for varga, accuracy, grade, icon in _VARGA_ACCURACY:
        cols = st.columns([3, 2, 2, 1])
        cols[0].markdown(varga)
        cols[1].markdown(f"`{accuracy}`")
        colour = _GRADE_COLOUR.get(grade, "#555")
        cols[2].markdown(
            f'<span style="color:{colour};font-weight:bold">{grade}</span>',
            unsafe_allow_html=True,
        )
        cols[3].markdown(icon)


def _render_sensitivity_detail(data: dict) -> None:
    """Per-house sensitivity details if available."""
    if not _HAS_STREAMLIT:
        return

    houses = data.get("houses", {})
    if not houses:
        st.caption("No per-house sensitivity data available for this chart.")
        return

    st.markdown("#### Per-House Sensitivity")
    st.caption(
        "Houses where the score changes significantly across the birth time window "
        "should be treated with additional caution."
    )

    sensitive_houses = []
    for house_num, house_data in houses.items():
        std = house_data.get("std_score", 0)
        if std > 0.5:  # sensitive
            sensitive_houses.append((int(house_num), std, house_data))

    if not sensitive_houses:
        st.success("No houses show high sensitivity to birth time uncertainty.")
        return

    sensitive_houses.sort(key=lambda x: x[1], reverse=True)
    for house_num, std, house_data in sensitive_houses[:6]:
        mean = house_data.get("mean_score", 0)
        stable = house_data.get("stable", False)
        icon = "🟡" if not stable else "✅"
        st.markdown(
            f"{icon} **House {house_num}** — "
            f"mean score: `{mean:.2f}`, sensitivity: `±{std:.2f}` "
            f"{'(stable)' if stable else '(sensitive to birth time)'}",
        )
