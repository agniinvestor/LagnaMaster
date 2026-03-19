"""
src/ui/app.py
=============
LagnaMaster Streamlit UI.

Screens:
  1. Birth Data Input  — sidebar form
  2. Chart View        — lagna + planet positions table
  3. Domain Scores     — 12 houses with scores, ratings, bhavesh, color coding
  4. Rule Breakdown    — expandable per-house rule detail
  5. Chart History     — recent charts from SQLite
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make sure src/ is importable regardless of how streamlit is launched
_ROOT = Path(__file__).parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from src.ephemeris import compute_chart, BirthChart
from src.scoring import score_chart, ChartScores, _rating
from src.db import init_db, save_chart, list_charts, get_chart

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LagnaMaster",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ── Color helpers ────────────────────────────────────────────────────────────
_RATING_COLOR = {
    "Excellent":  "#1a7a1a",   # dark green
    "Strong":     "#4caf50",   # green
    "Moderate":   "#f0a500",   # amber
    "Weak":       "#e05c00",   # orange-red
    "Very Weak":  "#b71c1c",   # dark red
}

_RATING_BG = {
    "Excellent":  "#e8f5e9",
    "Strong":     "#f1f8f2",
    "Moderate":   "#fff8e1",
    "Weak":       "#fff3e0",
    "Very Weak":  "#fdecea",
}

_PLANET_SYMBOL = {
    "Sun": "☉", "Moon": "☽", "Mars": "♂", "Mercury": "☿",
    "Jupiter": "♃", "Venus": "♀", "Saturn": "♄",
    "Rahu": "☊", "Ketu": "☋",
}

_SIGN_SYMBOL = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓",
}


def _sign_fmt(sign: str) -> str:
    return f"{_SIGN_SYMBOL.get(sign, '')} {sign}"


def _score_bar(score: float) -> str:
    """Simple ASCII bar: -10 to +10."""
    filled = int((score + 10) / 20 * 20)
    bar = "█" * filled + "░" * (20 - filled)
    return bar


# ── Sidebar: Birth Data Form ─────────────────────────────────────────────────
with st.sidebar:
    st.title("🪐 LagnaMaster")
    st.caption("Vedic Jyotish Birth Chart")
    st.divider()

    st.subheader("Birth Data")

    name = st.text_input("Name / Label", placeholder="e.g. India Independence")

    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("Birth Date", value=None)
    with col2:
        birth_time = st.time_input("Birth Time (local)", value=None, step=60)

    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude (°N)", min_value=-90.0, max_value=90.0,
                              value=28.6139, format="%.4f", step=0.0001)
    with col4:
        lon = st.number_input("Longitude (°E)", min_value=-180.0, max_value=180.0,
                              value=77.2090, format="%.4f", step=0.0001)

    tz_offset = st.number_input("UTC Offset (hours)", min_value=-12.0, max_value=14.0,
                                value=5.5, step=0.5, format="%.1f",
                                help="IST = +5.5")
    ayanamsha = st.selectbox("Ayanamsha", ["lahiri", "raman", "krishnamurti"], index=0)

    compute_btn = st.button("Compute Chart", type="primary", use_container_width=True)

    st.divider()
    st.subheader("1947 Demo")
    demo_btn = st.button("Load India 1947", use_container_width=True,
                         help="1947-08-15 00:00 IST, New Delhi — Taurus Lagna")

    st.divider()
    history_btn = st.button("Show History", use_container_width=True)


# ── Session State ─────────────────────────────────────────────────────────────
if "chart" not in st.session_state:
    st.session_state.chart = None
if "scores" not in st.session_state:
    st.session_state.scores = None
if "chart_id" not in st.session_state:
    st.session_state.chart_id = None
if "show_history" not in st.session_state:
    st.session_state.show_history = False


def _run_compute(year, month, day, hour, lat, lon, tz_offset, ayanamsha, name=None):
    with st.spinner("Computing chart..."):
        try:
            chart = compute_chart(
                year=year, month=month, day=day, hour=hour,
                lat=lat, lon=lon, tz_offset=tz_offset, ayanamsha=ayanamsha,
            )
            scores = score_chart(chart)

            chart_json = {
                "lagna_sign": chart.lagna_sign,
                "lagna_sign_index": chart.lagna_sign_index,
                "lagna_degree": chart.lagna_degree_in_sign,
                "ayanamsha_name": chart.ayanamsha_name,
                "ayanamsha_value": chart.ayanamsha_value,
                "jd_ut": chart.jd_ut,
                "planets": {
                    n: {
                        "sign": p.sign, "sign_index": p.sign_index,
                        "degree_in_sign": p.degree_in_sign,
                        "longitude": p.longitude,
                        "is_retrograde": p.is_retrograde, "speed": p.speed,
                    }
                    for n, p in chart.planets.items()
                },
            }
            scores_json = {
                str(h): {
                    "domain": hs.domain, "final_score": hs.final_score,
                    "raw_score": hs.raw_score, "rating": hs.rating,
                    "bhavesh": hs.bhavesh, "bhavesh_house": hs.bhavesh_house,
                }
                for h, hs in scores.houses.items()
            }

            chart_id = save_chart(
                year=year, month=month, day=day, hour=hour,
                lat=lat, lon=lon, tz_offset=tz_offset, ayanamsha=ayanamsha,
                chart_json=chart_json, scores_json=scores_json, name=name or None,
            )
            st.session_state.chart = chart
            st.session_state.scores = scores
            st.session_state.chart_id = chart_id
            st.session_state.show_history = False
        except ValueError as e:
            st.error(str(e))


# ── Button handlers ────────────────────────────────────────────────────────────
if demo_btn:
    _run_compute(1947, 8, 15, 0.0, 28.6139, 77.2090, 5.5, "lahiri", "India Independence")

if compute_btn:
    if birth_date is None or birth_time is None:
        st.sidebar.error("Please enter both birth date and time.")
    else:
        hour = birth_time.hour + birth_time.minute / 60.0
        _run_compute(
            birth_date.year, birth_date.month, birth_date.day,
            hour, lat, lon, tz_offset, ayanamsha, name,
        )

if history_btn:
    st.session_state.show_history = True


# ── History View ──────────────────────────────────────────────────────────────
if st.session_state.show_history:
    st.title("Chart History")
    rows = list_charts(limit=30)
    if not rows:
        st.info("No charts saved yet. Compute a chart first.")
    else:
        for row in rows:
            label = row.get("name") or f"#{row['id']}"
            dt_str = f"{row['year']}-{row['month']:02d}-{row['day']:02d} {row['hour']:.2f}h"
            if st.button(f"{label}  —  {dt_str}  ({row['lat']:.2f}°N, {row['lon']:.2f}°E)",
                         key=f"hist_{row['id']}"):
                with st.spinner("Loading..."):
                    stored = get_chart(row["id"])
                    if stored:
                        cj = stored["chart_json"]
                        chart = compute_chart(
                            year=stored["year"], month=stored["month"], day=stored["day"],
                            hour=stored["hour"], lat=stored["lat"], lon=stored["lon"],
                            tz_offset=stored["tz_offset"], ayanamsha=stored["ayanamsha"],
                        )
                        st.session_state.chart = chart
                        st.session_state.scores = score_chart(chart)
                        st.session_state.chart_id = row["id"]
                        st.session_state.show_history = False
                        st.rerun()
    st.stop()


# ── No chart yet ──────────────────────────────────────────────────────────────
if st.session_state.chart is None:
    st.title("LagnaMaster")
    st.markdown("""
    **Vedic Jyotish birth chart calculation and house scoring.**

    Enter birth data in the sidebar and click **Compute Chart**, or try the **India 1947** demo.

    ---
    **What you get:**
    - Sidereal planet positions (Lahiri ayanamsha by default)
    - 12-house domain scoring using 22 BPHS rules
    - Per-rule breakdown for each house
    - Chart history from local SQLite database
    """)
    st.stop()


# ── Main display ──────────────────────────────────────────────────────────────
chart: BirthChart = st.session_state.chart
scores: ChartScores = st.session_state.scores
chart_id: int = st.session_state.chart_id

# Header
lagna_sym = _SIGN_SYMBOL.get(chart.lagna_sign, "")
st.title(f"{lagna_sym} {chart.lagna_sign} Lagna — Chart #{chart_id}")
st.caption(
    f"Ayanamsha: {chart.ayanamsha_name.title()} = {chart.ayanamsha_value:.4f}°  |  "
    f"JD (UT): {chart.jd_ut:.4f}"
)

# ── Tab layout ────────────────────────────────────────────────────────────────
tab_chart, tab_scores, tab_rules = st.tabs(["Planetary Positions", "Domain Scores", "Rule Breakdown"])


# ── Tab 1: Planetary Positions ────────────────────────────────────────────────
with tab_chart:
    st.subheader(f"Lagna: {chart.lagna_degree_in_sign:.4f}° {_sign_fmt(chart.lagna_sign)}")

    # Build planet table
    rows_data = []
    for name_p, p in chart.planets.items():
        sym = _PLANET_SYMBOL.get(name_p, "")
        retro = "℞" if p.is_retrograde else ""
        rows_data.append({
            "": sym,
            "Planet": name_p,
            "Sign": _sign_fmt(p.sign),
            "Degree": f"{p.degree_in_sign:.4f}°",
            "Longitude": f"{p.longitude:.4f}°",
            "Speed °/day": f"{p.speed:+.4f}",
            "Rx": retro,
        })

    st.dataframe(
        rows_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "": st.column_config.TextColumn(width="small"),
            "Degree": st.column_config.TextColumn(width="medium"),
            "Longitude": st.column_config.TextColumn(width="medium"),
            "Speed °/day": st.column_config.TextColumn(width="medium"),
            "Rx": st.column_config.TextColumn(width="small"),
        },
    )

    # Whole-sign house map
    st.subheader("Whole-Sign House Map")
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)

    house_rows = []
    for h in range(1, 13):
        sign_idx = hmap.house_sign[h - 1]
        sign = chart.planets["Sun"].__class__  # just need SIGNS list
        from src.ephemeris import SIGNS
        sign_name = SIGNS[sign_idx]
        lord = hmap.house_lord[h - 1]
        lord_house = hmap.planet_house[lord]
        planets_in = [
            f"{_PLANET_SYMBOL.get(p, '')}{p}"
            for p, pos in chart.planets.items()
            if pos.sign_index == sign_idx
        ]
        house_rows.append({
            "House": f"H{h}",
            "Sign": _sign_fmt(sign_name),
            "Lord": lord,
            "Lord in": f"H{lord_house}",
            "Planets": ", ".join(planets_in) if planets_in else "—",
        })

    st.dataframe(house_rows, use_container_width=True, hide_index=True)


# ── Tab 2: Domain Scores ───────────────────────────────────────────────────────
with tab_scores:
    st.subheader("12-House Domain Scores")
    st.caption("Score range: −10 (Very Weak) to +10 (Excellent) | WC rules counted at 0.5×")

    # Summary metric row: avg, best, worst
    all_scores = [hs.final_score for hs in scores.houses.values()]
    avg_score = sum(all_scores) / 12
    best_h = max(scores.houses, key=lambda h: scores.houses[h].final_score)
    worst_h = min(scores.houses, key=lambda h: scores.houses[h].final_score)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Lagna Sign", chart.lagna_sign)
    m2.metric("Average Score", f"{avg_score:+.2f}")
    m3.metric("Strongest House", f"H{best_h} ({scores.houses[best_h].rating})",
              delta=f"{scores.houses[best_h].final_score:+.2f}")
    m4.metric("Weakest House", f"H{worst_h} ({scores.houses[worst_h].rating})",
              delta=f"{scores.houses[worst_h].final_score:+.2f}", delta_color="inverse")

    st.divider()

    # Score cards in 3-column grid
    cols = st.columns(3)
    for i, h in enumerate(range(1, 13)):
        hs = scores.houses[h]
        col = cols[i % 3]
        rating = hs.rating
        bg = _RATING_BG[rating]
        fg = _RATING_COLOR[rating]

        with col:
            st.markdown(
                f"""
                <div style="background:{bg}; border-left:4px solid {fg};
                            padding:10px 14px; border-radius:6px; margin-bottom:10px;">
                  <div style="font-size:11px; color:#666; font-weight:600;">
                    H{h} · {hs.domain}
                  </div>
                  <div style="font-size:22px; font-weight:700; color:{fg};">
                    {hs.final_score:+.2f}
                  </div>
                  <div style="font-size:11px; color:{fg}; font-weight:600;">
                    {rating}
                  </div>
                  <div style="font-size:11px; color:#555; margin-top:4px;">
                    Lord: {hs.bhavesh} in H{hs.bhavesh_house}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Full table view
    st.divider()
    st.subheader("Score Table")
    table_rows = []
    for h in range(1, 13):
        hs = scores.houses[h]
        table_rows.append({
            "H": h,
            "Domain": hs.domain,
            "Lord": hs.bhavesh,
            "Lord in": f"H{hs.bhavesh_house}",
            "Raw": f"{hs.raw_score:+.3f}",
            "Score": f"{hs.final_score:+.2f}",
            "Rating": hs.rating,
        })
    st.dataframe(table_rows, use_container_width=True, hide_index=True)


# ── Tab 3: Rule Breakdown ──────────────────────────────────────────────────────
with tab_rules:
    st.subheader("Per-House Rule Breakdown")
    st.caption("Expand a house to see all 22 BPHS rules and their scores. WC = Worth Considering (0.5× weight).")

    house_select = st.selectbox(
        "Select House",
        options=list(range(1, 13)),
        format_func=lambda h: f"H{h} — {scores.houses[h].domain} ({scores.houses[h].rating}: {scores.houses[h].final_score:+.2f})",
    )

    hs = scores.houses[house_select]
    rating = hs.rating
    fg = _RATING_COLOR[rating]
    bg = _RATING_BG[rating]

    st.markdown(
        f"""
        <div style="background:{bg}; border-left:4px solid {fg};
                    padding:12px 16px; border-radius:6px; margin-bottom:16px;">
          <b style="color:{fg};">H{house_select} — {hs.domain}</b><br>
          <span style="font-size:13px; color:#555;">
            Lord (Bhavesh): <b>{hs.bhavesh}</b> in H{hs.bhavesh_house} &nbsp;|&nbsp;
            Raw: {hs.raw_score:+.3f} &nbsp;|&nbsp;
            Final: <b>{hs.final_score:+.2f}</b> &nbsp;|&nbsp;
            Rating: <b style="color:{fg};">{rating}</b>
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rules table
    rule_rows = []
    for r in hs.rules:
        effective = r.score * (0.5 if r.is_wc else 1.0)
        rule_rows.append({
            "Rule": r.rule,
            "Description": r.description,
            "Raw Score": f"{r.score:+.3f}",
            "WC": "½×" if r.is_wc else "",
            "Effective": f"{effective:+.3f}",
            "Active": "✓" if r.triggered else "",
        })

    st.dataframe(
        rule_rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rule": st.column_config.TextColumn(width="small"),
            "WC": st.column_config.TextColumn(width="small"),
            "Active": st.column_config.TextColumn(width="small"),
        },
    )

    # Totals
    total_effective = sum(
        r.score * (0.5 if r.is_wc else 1.0) for r in hs.rules
    )
    positive = sum(
        r.score * (0.5 if r.is_wc else 1.0)
        for r in hs.rules if r.score > 0
    )
    negative = sum(
        r.score * (0.5 if r.is_wc else 1.0)
        for r in hs.rules if r.score < 0
    )
    active_count = sum(1 for r in hs.rules if r.triggered)

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Active Rules", f"{active_count}/22")
    t2.metric("Positive Contribution", f"{positive:+.3f}")
    t3.metric("Negative Contribution", f"{negative:+.3f}")
    t4.metric("Net (= Raw Score)", f"{total_effective:+.3f}")
