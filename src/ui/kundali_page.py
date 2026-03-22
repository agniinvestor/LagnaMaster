"""
src/ui/kundali_page.py — Kundali Milan (compatibility) Streamlit page (Session 12).

Run standalone:
    PYTHONPATH=. streamlit run src/ui/kundali_page.py

Or import into app.py as a new 9th tab:
    from src.ui.kundali_page import render_kundali_tab
    with tab9:
        render_kundali_tab()
"""

from __future__ import annotations

import streamlit as st
from datetime import date

from src.ephemeris import compute_chart
from src.calculations.kundali_milan import (
    compute_kundali_milan,
    KundaliMilanResult,
)
from src.ui.chart_visual import south_indian_svg


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------


def _score_color(score: float, max_score: float) -> str:
    pct = score / max_score if max_score else 0
    if pct >= 0.75:
        return "#1a7a1a"  # green
    if pct >= 0.4:
        return "#b8860b"  # amber
    return "#8b0000"  # red


def _grade_badge(grade: str) -> str:
    colours = {"Excellent": "#1a7a1a", "Good": "#b8860b", "Weak": "#8b0000"}
    c = colours.get(grade, "#333")
    return f'<span style="background:{c};color:#fff;padding:3px 10px;border-radius:4px;font-weight:bold">{grade}</span>'


# ---------------------------------------------------------------------------
# SVG gauge (0–36 arc)
# ---------------------------------------------------------------------------


def _gauge_svg(score: float) -> str:
    import math

    pct = score / 36.0
    colour = "#1a7a1a" if pct >= 0.78 else "#d4a017" if pct >= 0.5 else "#c0392b"
    # Arc: 180° sweep, radius 70
    cx, cy, r = 90, 90, 70
    angle = pct * 180
    rad = math.radians(180 - angle)
    x2 = cx + r * math.cos(rad)
    y2 = cy - r * math.sin(rad)
    large = 1 if angle > 180 else 0
    return f"""
<svg width="180" height="110" xmlns="http://www.w3.org/2000/svg">
  <path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}"
        fill="none" stroke="#ddd" stroke-width="14" stroke-linecap="round"/>
  <path d="M {cx - r} {cy} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}"
        fill="none" stroke="{colour}" stroke-width="14" stroke-linecap="round"/>
  <text x="{cx}" y="{cy + 10}" text-anchor="middle"
        font-size="26" font-weight="bold" fill="{colour}">{score:.1f}</text>
  <text x="{cx}" y="{cy + 28}" text-anchor="middle"
        font-size="11" fill="#666">out of 36</text>
</svg>"""


# ---------------------------------------------------------------------------
# Birth data input widget
# ---------------------------------------------------------------------------


def _birth_inputs(prefix: str, label: str, demo_defaults: dict) -> dict | None:
    """Render a compact birth data form; return dict of params or None."""
    st.subheader(label)
    col1, col2 = st.columns(2)
    with col1:
        bd = st.date_input(
            f"Birth date ({prefix})",
            value=demo_defaults["date"],
            min_value=date(1915, 1, 1),
            key=f"{prefix}_date",
        )
        hour = st.slider("Hour", 0, 23, demo_defaults["hour"], key=f"{prefix}_hour")
        minute = st.slider(
            "Minute", 0, 59, demo_defaults["minute"], key=f"{prefix}_minute"
        )
    with col2:
        lat = st.number_input(
            "Latitude (°N)",
            -90.0,
            90.0,
            demo_defaults["lat"],
            0.001,
            key=f"{prefix}_lat",
        )
        lon = st.number_input(
            "Longitude (°E)",
            -180.0,
            180.0,
            demo_defaults["lon"],
            0.001,
            key=f"{prefix}_lon",
        )
        tz = st.number_input(
            "UTC offset", -12.0, 14.0, demo_defaults["tz"], 0.5, key=f"{prefix}_tz"
        )
        ayanamsha = st.selectbox(
            "Ayanamsha", ["lahiri", "raman", "krishnamurti"], key=f"{prefix}_ayan"
        )
    return {
        "year": bd.year,
        "month": bd.month,
        "day": bd.day,
        "hour": hour + minute / 60,
        "lat": lat,
        "lon": lon,
        "tz_offset": tz,
        "ayanamsha": ayanamsha,
    }


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------


def render_kundali_tab() -> None:
    """Render the full Kundali Milan compatibility page."""
    st.header("Kundali Milan — Ashtakoot Compatibility")
    st.caption(
        "Ashtakoot matching: 8 qualities × 36 total Gunas. "
        "Minimum recommended score: **18/36**."
    )

    # Demo defaults — Nehru × Edwina Mountbatten (fun illustrative pair)
    demo_m = dict(
        date=date(1889, 11, 14), hour=23, minute=36, lat=27.1767, lon=79.9464, tz=5.5
    )  # Allahabad
    demo_f = dict(
        date=date(1901, 11, 28), hour=22, minute=0, lat=51.5074, lon=-0.1278, tz=0.0
    )  # London

    use_demo = st.button("📋 Load Demo Charts")

    if use_demo:
        st.session_state["km_demo"] = True

    demo = st.session_state.get("km_demo", False)

    col_m, col_f = st.columns(2)
    with col_m:
        params_m = _birth_inputs(
            "male",
            "Chart A (Male / Person 1)",
            demo_m
            if demo
            else dict(
                date=date(1990, 1, 1), hour=6, minute=0, lat=28.6139, lon=77.209, tz=5.5
            ),
        )
    with col_f:
        params_f = _birth_inputs(
            "female",
            "Chart B (Female / Person 2)",
            demo_f
            if demo
            else dict(
                date=date(1992, 6, 15),
                hour=10,
                minute=0,
                lat=19.076,
                lon=72.878,
                tz=5.5,
            ),
        )

    if st.button("▶  Compute Compatibility", use_container_width=True, type="primary"):
        with st.spinner("Computing charts…"):
            try:
                chart_m = compute_chart(**params_m)
                chart_f = compute_chart(**params_f)
                result = compute_kundali_milan(chart_m, chart_f)
            except Exception as exc:
                st.error(f"Error: {exc}")
                return

        _render_result(result, chart_m, chart_f)


def _render_result(
    result: KundaliMilanResult,
    chart_m,
    chart_f,
) -> None:
    """Render the full compatibility result."""

    # --- Score gauge + grade ---
    st.divider()
    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        st.markdown(_gauge_svg(result.total_score), unsafe_allow_html=True)
    with c2:
        st.metric(
            "Total Gunas",
            f"{result.total_score} / 36",
            delta=f"{result.percentage:.0f}%",
        )
        st.markdown(_grade_badge(result.grade), unsafe_allow_html=True)
    with c3:
        st.metric("Mangal Dosha (A)", "Yes ⚠️" if result.mangal_dosha_male else "No ✅")
        st.metric(
            "Mangal Dosha (B)", "Yes ⚠️" if result.mangal_dosha_female else "No ✅"
        )
        if result.dosha_cancelled:
            st.success("✅ Mutual Mangal Dosha — cancels each other")

    # --- Critical doshas banner ---
    if result.critical_doshas:
        st.error("⚠️ Critical doshas present: " + " | ".join(result.critical_doshas))
    else:
        st.success("✅ No critical doshas")

    st.divider()

    # --- Ashtakoot table ---
    st.subheader("Ashtakoot Detail")

    import pandas as pd

    rows = []
    for name, k in result.kootas.items():
        bar = "█" * int(k.score) + "░" * int(k.max_score - k.score)
        rows.append(
            {
                "Koota": name,
                "Score": f"{k.score:.1f} / {k.max_score:.0f}",
                "Visual": bar,
                "Chart A": k.male_value,
                "Chart B": k.female_value,
                "Note": k.note,
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Koota score bar chart ---
    st.subheader("Score Breakdown")
    chart_data = {k.name: k.score for k in result.kootas.values()}
    st.bar_chart(chart_data)

    # --- Side-by-side South Indian charts (collapsed) ---
    with st.expander("🗺️ View Birth Charts Side-by-Side"):
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Chart A")
            st.markdown(
                south_indian_svg(chart_m, name="Chart A"), unsafe_allow_html=True
            )
        with c2:
            st.caption("Chart B")
            st.markdown(
                south_indian_svg(chart_f, name="Chart B"), unsafe_allow_html=True
            )

    # --- Interpretation ---
    with st.expander("ℹ️ Interpretation Guide"):
        st.markdown("""
| Score | Grade | Meaning |
|-------|-------|---------|
| 28–36 | **Excellent** | Highly compatible — recommended match |
| 18–27 | **Good** | Acceptable match; minor adjustments advised |
| < 18  | **Weak** | Needs careful consideration; seek expert guidance |

**Critical Doshas**:
- **Nadi Dosha** (Nadi = 0/8): Same constitutional type — can cause health/progeny issues. Hardest to cancel.
- **Bhakut Dosha** (Bhakut = 0/7): Adverse sign relationship — can cause financial or family stress.
- **Mangal Dosha**: Mars in 1/2/4/7/8/12 from Lagna, Moon, or Venus. Cancels when both charts have it.
        """)


# ---------------------------------------------------------------------------
# Standalone entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    st.set_page_config(
        page_title="LagnaMaster — Kundali Milan",
        page_icon="💑",
        layout="wide",
    )
    render_kundali_tab()
