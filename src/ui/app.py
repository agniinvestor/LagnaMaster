"""
src/ui/app.py
=============
LagnaMaster Streamlit UI.

Tabs:
  1. Chart         — South Indian visual + planet position table + house map
  2. Domain Scores — 12 house score cards + summary table
  3. Dashas        — Vimshottari Dasha timeline + antardasha breakdown
  4. Rule Detail   — per-house 22-rule breakdown
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
import streamlit.components.v1 as components

from src.ephemeris import compute_chart, BirthChart, SIGNS
from src.scoring import score_chart, ChartScores
from src.db import init_db, save_chart, list_charts, get_chart
from src.ui.chart_visual import south_indian_svg
from src.calculations.nakshatra import nakshatra_position
from src.calculations.dignity import compute_all_dignities, DignityLevel
from src.calculations.yogas import detect_yogas, Yoga
from src.calculations.ashtakavarga import compute_ashtakavarga, _PLANETS as _AV_PLANETS
from src.calculations.shadbala import compute_shadbala
from src.calculations.gochara import compute_gochara

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LagnaMaster",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ── Helpers ───────────────────────────────────────────────────────────────────
_RATING_COLOR = {
    "Excellent": "#1a7a1a", "Strong":   "#4caf50",
    "Moderate":  "#f0a500", "Weak":     "#e05c00",
    "Very Weak": "#b71c1c",
}
_RATING_BG = {
    "Excellent": "#e8f5e9", "Strong":   "#f1f8f2",
    "Moderate":  "#fff8e1", "Weak":     "#fff3e0",
    "Very Weak": "#fdecea",
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
_DASHA_COLOR = {
    "Sun": "#FF6B35", "Moon": "#4A90D9", "Mars": "#D9534F",
    "Mercury": "#5CB85C", "Jupiter": "#F0AD4E", "Venus": "#9B59B6",
    "Saturn": "#34495E", "Rahu": "#7D3C98", "Ketu": "#BDC3C7",
}

def _sign_fmt(sign: str) -> str:
    return f"{_SIGN_SYMBOL.get(sign, '')} {sign}"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🪐 LagnaMaster")
    st.caption("Vedic Jyotish Birth Chart")
    st.divider()

    st.subheader("Birth Data")
    name_input = st.text_input("Name / Label", placeholder="e.g. India Independence")

    col1, col2 = st.columns(2)
    with col1:
        birth_date_input = st.date_input("Birth Date", value=None,
                                          min_value=date(1915, 1, 1),
                                          max_value=date.today())
    with col2:
        birth_time_input = st.time_input("Birth Time (local)", value=None, step=60)

    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude (°N)", min_value=-90.0, max_value=90.0,
                              value=28.6139, format="%.4f", step=0.0001)
    with col4:
        lon = st.number_input("Longitude (°E)", min_value=-180.0, max_value=180.0,
                              value=77.2090, format="%.4f", step=0.0001)

    tz_offset = st.number_input("UTC Offset (hours)", min_value=-12.0, max_value=14.0,
                                value=5.5, step=0.5, format="%.1f", help="IST = +5.5")
    ayanamsha = st.selectbox("Ayanamsha", ["lahiri", "raman", "krishnamurti"], index=0)

    compute_btn = st.button("Compute Chart", type="primary", use_container_width=True)
    st.divider()
    demo_btn = st.button("Load India 1947", use_container_width=True,
                         help="1947-08-15 00:00 IST, New Delhi — Taurus Lagna")
    history_btn = st.button("Show History", use_container_width=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("chart", None), ("scores", None), ("chart_id", None),
    ("birth_date", None), ("show_history", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


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
            st.session_state.chart      = chart
            st.session_state.scores     = scores
            st.session_state.chart_id   = chart_id
            st.session_state.birth_date = date(year, month, day)
            st.session_state.show_history = False
        except ValueError as e:
            st.error(str(e))


# ── Button handlers ───────────────────────────────────────────────────────────
if demo_btn:
    _run_compute(1947, 8, 15, 0.0, 28.6139, 77.2090, 5.5, "lahiri", "India Independence")

if compute_btn:
    if birth_date_input is None or birth_time_input is None:
        st.sidebar.error("Please enter both birth date and time.")
    else:
        hour = birth_time_input.hour + birth_time_input.minute / 60.0
        _run_compute(
            birth_date_input.year, birth_date_input.month, birth_date_input.day,
            hour, lat, lon, tz_offset, ayanamsha, name_input,
        )

if history_btn:
    st.session_state.show_history = True


# ── History view ──────────────────────────────────────────────────────────────
if st.session_state.show_history:
    st.title("Chart History")
    rows = list_charts(limit=30)
    if not rows:
        st.info("No charts saved yet. Compute a chart first.")
    else:
        for row in rows:
            label  = row.get("name") or f"#{row['id']}"
            dt_str = f"{row['year']}-{row['month']:02d}-{row['day']:02d} {row['hour']:.2f}h"
            btn_label = f"{label}  —  {dt_str}  ({row['lat']:.2f}°N, {row['lon']:.2f}°E)"
            if st.button(btn_label, key=f"hist_{row['id']}"):
                with st.spinner("Loading..."):
                    stored = get_chart(row["id"])
                    if stored:
                        chart = compute_chart(
                            year=stored["year"], month=stored["month"], day=stored["day"],
                            hour=stored["hour"], lat=stored["lat"], lon=stored["lon"],
                            tz_offset=stored["tz_offset"], ayanamsha=stored["ayanamsha"],
                        )
                        st.session_state.chart      = chart
                        st.session_state.scores     = score_chart(chart)
                        st.session_state.chart_id   = row["id"]
                        st.session_state.birth_date = date(row["year"], row["month"], row["day"])
                        st.session_state.show_history = False
                        st.rerun()
    st.stop()


# ── No chart yet ──────────────────────────────────────────────────────────────
if st.session_state.chart is None:
    st.title("🪐 LagnaMaster")
    st.markdown("""
    **Vedic Jyotish birth chart calculation and house scoring.**

    Enter birth data in the sidebar and click **Compute Chart**, or try the **India 1947** demo.

    ---
    **What you get:**
    - South Indian visual chart with planet placements
    - Sidereal planet positions (Lahiri / Raman / Krishnamurti ayanamsha)
    - 12-house domain scoring using 22 BPHS rules
    - Classical yoga detection (13 yoga types)
    - Ashtakavarga bindu tables (8-source strength system)
    - Shadbala planetary strength (6 components in Virupas)
    - Vimshottari Dasha timeline with antardasha breakdown
    - Gochara (transit) analysis with Sade Sati detection
    - Per-rule scoring detail for each house
    """)
    st.stop()


# ── Main display ──────────────────────────────────────────────────────────────
chart: BirthChart    = st.session_state.chart
scores: ChartScores  = st.session_state.scores
chart_id: int        = st.session_state.chart_id
birth_date_ss: date  = st.session_state.birth_date

lagna_sym = _SIGN_SYMBOL.get(chart.lagna_sign, "")
st.title(f"{lagna_sym} {chart.lagna_sign} Lagna — Chart #{chart_id}")
st.caption(
    f"Ayanamsha: {chart.ayanamsha_name.title()} = {chart.ayanamsha_value:.4f}°  |  "
    f"JD (UT): {chart.jd_ut:.4f}"
)

tab_chart, tab_scores, tab_yogas, tab_av, tab_dashas, tab_gochara, tab_rules = st.tabs([
    "Chart", "Domain Scores", "Yogas", "Ashtakavarga",
    "Vimshottari Dasha", "Transits", "Rule Detail",
])


# ══════════════════════════════════════════════════════════════════════════════
# Tab 1: Chart (visual + tables)
# ══════════════════════════════════════════════════════════════════════════════
with tab_chart:
    col_svg, col_table = st.columns([1, 1], gap="large")

    with col_svg:
        st.subheader("South Indian Chart")
        stored_name = ""
        if chart_id:
            row = get_chart(chart_id)
            if row:
                stored_name = row.get("name") or ""
        svg = south_indian_svg(chart, name=stored_name)
        components.html(
            f'<div style="display:flex;justify-content:center;">{svg}</div>',
            height=545,
        )

    with col_table:
        st.subheader(f"Lagna: {chart.lagna_degree_in_sign:.4f}° {_sign_fmt(chart.lagna_sign)}")

        dignities = compute_all_dignities(chart)
        rows_data = []
        for pname, p in chart.planets.items():
            sym   = _PLANET_SYMBOL.get(pname, "")
            retro = "℞" if p.is_retrograde else ""
            nak   = nakshatra_position(p.longitude)
            dig   = dignities.get(pname)
            dig_label = ""
            if dig:
                lvl = dig.dignity
                if lvl == DignityLevel.DEEP_EXALT:    dig_label = "⬆⬆ Deep Exalt"
                elif lvl == DignityLevel.EXALT:        dig_label = "⬆ Exalted"
                elif lvl == DignityLevel.MOOLTRIKONA:  dig_label = "◎ Moolatrikona"
                elif lvl == DignityLevel.OWN_SIGN:     dig_label = "✦ Own Sign"
                elif lvl == DignityLevel.FRIEND_SIGN:  dig_label = "＋ Friendly"
                elif lvl == DignityLevel.ENEMY_SIGN:   dig_label = "－ Enemy"
                elif lvl == DignityLevel.DEBIL:        dig_label = "⬇ Debilitated"
                elif lvl == DignityLevel.DEEP_DEBIL:   dig_label = "⬇⬇ Deep Debil"
                if dig.is_cazimi:    dig_label += " ☀cazimi"
                elif dig.is_combust: dig_label += " 🔥combust"
            rows_data.append({
                "": sym,
                "Planet":      pname,
                "Sign":        _sign_fmt(p.sign),
                "Degree":      f"{p.degree_in_sign:.2f}°",
                "Nakshatra":   f"{nak.nakshatra} P{nak.pada}",
                "Dignity":     dig_label,
                "Speed":       f"{p.speed:+.3f}",
                "Rx":          retro,
            })
        st.dataframe(rows_data, use_container_width=True, hide_index=True,
                     column_config={
                         "": st.column_config.TextColumn(width="small"),
                         "Rx": st.column_config.TextColumn(width="small"),
                     })

        st.subheader("Whole-Sign House Map")
        from src.calculations.house_lord import compute_house_map
        hmap = compute_house_map(chart)
        house_rows = []
        for h in range(1, 13):
            si   = hmap.house_sign[h - 1]
            lord = hmap.house_lord[h - 1]
            lh   = hmap.planet_house[lord]
            planets_in = ", ".join(
                f"{_PLANET_SYMBOL.get(p, '')}{p}"
                for p, pos in chart.planets.items()
                if pos.sign_index == si
            ) or "—"
            house_rows.append({
                "House": f"H{h}", "Sign": _sign_fmt(SIGNS[si]),
                "Lord": lord, "Lord in": f"H{lh}", "Occupants": planets_in,
            })
        st.dataframe(house_rows, use_container_width=True, hide_index=True)

        with st.expander("Shadbala — Planetary Strength (Virupas)"):
            sb = compute_shadbala(chart)
            sb_rows = []
            for pname, sp in sb.planets.items():
                sb_rows.append({
                    "Planet":    pname,
                    "Uchcha":    f"{sp.uchcha:.1f}",
                    "Kendradi":  f"{sp.kendradi:.1f}",
                    "Ojha-Yugma":f"{sp.ojha_yugma:.1f}",
                    "Dig Bala":  f"{sp.dig_bala:.1f}",
                    "Paksha":    f"{sp.paksha:.1f}",
                    "Chesta":    f"{sp.chesta:.1f}",
                    "Total":     f"{sp.total:.1f}",
                    "Min Req":   f"{sp.minimum:.0f}",
                    "Ishta%":    f"{sp.ishta_pct:.0f}%",
                    "✓":         "✓" if sp.meets_minimum else "",
                })
            st.dataframe(sb_rows, use_container_width=True, hide_index=True,
                         column_config={
                             "✓": st.column_config.TextColumn(width="small"),
                         })
            st.caption("Minimum required Virupas: Sun 390, Moon 360, Mars 300, "
                       "Mercury 420, Jupiter 390, Venus 330, Saturn 300")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 2: Domain Scores
# ══════════════════════════════════════════════════════════════════════════════
with tab_scores:
    st.subheader("12-House Domain Scores")
    st.caption("Score range: −10 (Very Weak) to +10 (Excellent) | WC rules at 0.5×")

    all_scores = [hs.final_score for hs in scores.houses.values()]
    avg_score  = sum(all_scores) / 12
    best_h     = max(scores.houses, key=lambda h: scores.houses[h].final_score)
    worst_h    = min(scores.houses, key=lambda h: scores.houses[h].final_score)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Lagna Sign", chart.lagna_sign)
    m2.metric("Average Score", f"{avg_score:+.2f}")
    m3.metric("Strongest", f"H{best_h} ({scores.houses[best_h].rating})",
              delta=f"{scores.houses[best_h].final_score:+.2f}")
    m4.metric("Weakest", f"H{worst_h} ({scores.houses[worst_h].rating})",
              delta=f"{scores.houses[worst_h].final_score:+.2f}", delta_color="inverse")

    st.divider()

    cols = st.columns(3)
    for i, h in enumerate(range(1, 13)):
        hs     = scores.houses[h]
        rating = hs.rating
        bg     = _RATING_BG[rating]
        fg     = _RATING_COLOR[rating]
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:{bg};border-left:4px solid {fg};'
                f'padding:10px 14px;border-radius:6px;margin-bottom:10px;">'
                f'<div style="font-size:11px;color:#666;font-weight:600;">'
                f'H{h} · {hs.domain}</div>'
                f'<div style="font-size:22px;font-weight:700;color:{fg};">'
                f'{hs.final_score:+.2f}</div>'
                f'<div style="font-size:11px;color:{fg};font-weight:600;">{rating}</div>'
                f'<div style="font-size:11px;color:#555;margin-top:4px;">'
                f'Lord: {hs.bhavesh} in H{hs.bhavesh_house}</div></div>',
                unsafe_allow_html=True,
            )

    st.divider()
    st.subheader("Score Table")
    table_rows = [{
        "H": h, "Domain": hs.domain,
        "Lord": hs.bhavesh, "Lord in": f"H{hs.bhavesh_house}",
        "Raw": f"{hs.raw_score:+.3f}", "Score": f"{hs.final_score:+.2f}",
        "Rating": hs.rating,
    } for h, hs in scores.houses.items()]
    st.dataframe(table_rows, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 3: Yogas
# ══════════════════════════════════════════════════════════════════════════════
with tab_yogas:
    yogas = detect_yogas(chart)

    benefic = [y for y in yogas if y.nature == "benefic"]
    mixed   = [y for y in yogas if y.nature == "mixed"]
    malefic = [y for y in yogas if y.nature == "malefic"]

    st.subheader(f"Detected Yogas — {len(yogas)} total")
    st.caption(
        f"✅ {len(benefic)} benefic  &nbsp;·&nbsp;  "
        f"⚖ {len(mixed)} mixed  &nbsp;·&nbsp;  "
        f"⚠ {len(malefic)} challenging"
    )

    if not yogas:
        st.info("No major yogas detected in this chart.")
    else:
        _YOGA_NATURE_STYLE = {
            "benefic": ("#1a7a1a", "#e8f5e9"),
            "mixed":   ("#7c5700", "#fff8e1"),
            "malefic": ("#b71c1c", "#fdecea"),
        }
        _YOGA_NATURE_ICON = {"benefic": "✅", "mixed": "⚖", "malefic": "⚠"}

        # Group by category
        from itertools import groupby
        for category, group in groupby(yogas, key=lambda y: y.category):
            group_list = list(group)
            st.markdown(f"**{category} Yogas** ({len(group_list)})")
            for y in group_list:
                fg, bg = _YOGA_NATURE_STYLE[y.nature]
                icon   = _YOGA_NATURE_ICON[y.nature]
                planets_str = " · ".join(
                    f"{_PLANET_SYMBOL.get(p,'')}{p}" for p in y.planets
                )
                st.markdown(
                    f'<div style="background:{bg};border-left:4px solid {fg};'
                    f'padding:10px 14px;border-radius:6px;margin-bottom:8px;">'
                    f'<span style="font-weight:700;color:{fg};">{icon} {y.name}</span>'
                    f'<span style="font-size:11px;color:#888;margin-left:10px;">'
                    f'{planets_str}</span><br>'
                    f'<span style="font-size:12px;color:#444;">{y.description}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.write("")  # spacing between categories


# ══════════════════════════════════════════════════════════════════════════════
# Tab 4: Ashtakavarga
# ══════════════════════════════════════════════════════════════════════════════
with tab_av:
    av = compute_ashtakavarga(chart)
    st.subheader("Ashtakavarga — 8-Source Bindu System")
    st.caption(
        "Each planet's table shows how many of the 8 contributors "
        "(Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Lagna) "
        "donate a bindu to each sign. "
        "**Strong ≥ 5, Average = 4, Weak ≤ 3** &nbsp;|&nbsp; "
        "Sarva (total): **Strong ≥ 30, Average ≥ 25, Weak < 25**"
    )

    # ── Sarvashtakavarga summary bar ──────────────────────────────────────────
    st.markdown("#### Sarvashtakavarga (All-Planet Total)")
    sarva_cols = st.columns(12)
    for si, sign in enumerate(SIGNS):
        b = av.sarva.bindus[si]
        strength = av.sarva.strength(si)
        color = {"Strong": "#1a7a1a", "Average": "#f0a500", "Weak": "#b71c1c"}[strength]
        bg    = {"Strong": "#e8f5e9", "Average": "#fff8e1", "Weak": "#fdecea"}[strength]
        is_lagna = (si == chart.lagna_sign_index)
        border = "3px solid #4B0082" if is_lagna else f"1px solid {color}"
        with sarva_cols[si]:
            st.markdown(
                f'<div style="background:{bg};border:{border};border-radius:6px;'
                f'padding:6px 4px;text-align:center;margin-bottom:4px;">'
                f'<div style="font-size:10px;color:#555;">{_SIGN_SYMBOL.get(sign,"")}</div>'
                f'<div style="font-size:14px;font-weight:700;color:{color};">{b}</div>'
                f'<div style="font-size:9px;color:{color};">{strength[:3]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Per-planet tables ─────────────────────────────────────────────────────
    st.markdown("#### Planet Bindu Tables")
    st.caption("Lagna sign highlighted with indigo border. "
               "Planet's own sign (where it sits in this chart) marked with ◉.")

    for planet in _AV_PLANETS:
        table = av.planet_av[planet]
        planet_si = chart.planets[planet].sign_index
        sym = _PLANET_SYMBOL.get(planet, "")

        p_cols = st.columns([1] + [1] * 12)
        with p_cols[0]:
            total_str = str(table.total)
            st.markdown(
                f'<div style="padding:6px 0;font-weight:700;color:{_DASHA_COLOR.get(planet,"#333")};">'
                f'{sym} {planet}<br>'
                f'<span style="font-size:10px;color:#888;">Σ={total_str}</span></div>',
                unsafe_allow_html=True,
            )
        for si, sign in enumerate(SIGNS):
            b = table.bindus[si]
            strength = table.strength(si)
            color = {"Strong": "#1a7a1a", "Average": "#f0a500", "Weak": "#b71c1c"}[strength]
            bg    = {"Strong": "#e8f5e9", "Average": "#fff8e1", "Weak": "#fdecea"}[strength]
            is_lagna_sign = (si == chart.lagna_sign_index)
            is_own_sign   = (si == planet_si)
            border = "2px solid #4B0082" if is_lagna_sign else f"1px solid {color}"
            marker = "◉" if is_own_sign else ""
            with p_cols[si + 1]:
                st.markdown(
                    f'<div style="background:{bg};border:{border};border-radius:4px;'
                    f'padding:4px 2px;text-align:center;">'
                    f'<div style="font-size:13px;font-weight:700;color:{color};">{b}{marker}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.divider()

    # ── Full data table ───────────────────────────────────────────────────────
    st.markdown("#### Full Bindu Table")
    full_rows = []
    for si, sign in enumerate(SIGNS):
        row: dict = {"Sign": _sign_fmt(sign)}
        for planet in _AV_PLANETS:
            row[planet[:3]] = av.planet_av[planet].bindus[si]
        row["Sarva"] = av.sarva.bindus[si]
        full_rows.append(row)
    st.dataframe(full_rows, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 5: Vimshottari Dasha
# ══════════════════════════════════════════════════════════════════════════════
with tab_dashas:
    from src.calculations.vimshottari_dasa import (
        compute_vimshottari_dasa, current_dasha, nakshatra_of_moon,
        VIMSHOTTARI_YEARS,
    )

    nak_name, dasha_lord = nakshatra_of_moon(chart)
    st.subheader("Vimshottari Dasha — 120-Year Cycle")
    st.caption(
        f"Moon nakshatra: **{nak_name}** (lord: **{dasha_lord}**) · "
        f"Birth dasha starts from {dasha_lord}"
    )

    if birth_date_ss is None:
        st.info("Birth date not available — load a chart via the sidebar to see dashas.")
        st.stop()

    dashas = compute_vimshottari_dasa(chart, birth_date_ss)
    today  = date.today()
    cur_md, cur_ad = current_dasha(dashas, today)

    # Current dasha banner
    clr = _DASHA_COLOR.get(cur_md.lord, "#555")
    st.markdown(
        f'<div style="background:#f0f0ff;border-left:5px solid {clr};'
        f'padding:12px 16px;border-radius:6px;margin-bottom:16px;">'
        f'<b style="font-size:15px;color:{clr};">Current Period (as of {today})</b><br>'
        f'<span style="font-size:18px;font-weight:700;color:{clr};">'
        f'{cur_md.lord} Mahadasha</span>'
        f'<span style="font-size:13px;color:#555;"> · ends {cur_md.end}</span><br>'
        f'<span style="font-size:14px;color:{_DASHA_COLOR.get(cur_ad.lord,"#555")};">'
        f'{cur_ad.lord} Antardasha</span>'
        f'<span style="font-size:12px;color:#888;"> · {cur_ad.start} → {cur_ad.end}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Full Mahadasha table
    st.subheader("Mahadasha Timeline")
    md_rows = []
    for md in dashas:
        is_cur = md.start <= today < md.end
        md_rows.append({
            "Lord":       md.lord,
            "Period (yr)": md.full_years,
            "Balance (yr)": f"{md.years:.2f}" if md.nakshatra else str(md.full_years),
            "Start":      str(md.start),
            "End":        str(md.end),
            "Active":     "◀ NOW" if is_cur else "",
        })
    st.dataframe(md_rows, use_container_width=True, hide_index=True)

    st.divider()

    # Antardasha detail for selected mahadasha
    st.subheader("Antardasha Breakdown")
    md_options = {
        f"{md.lord} ({md.start} → {md.end})": md
        for md in dashas
    }
    selected_label = st.selectbox(
        "Select Mahadasha",
        options=list(md_options.keys()),
        index=next(
            (i for i, md in enumerate(dashas) if md.start <= today < md.end),
            0,
        ),
    )
    selected_md = md_options[selected_label]

    ad_rows = []
    for ad in selected_md.antardashas:
        is_cur_ad = ad.start <= today < ad.end
        clr_ad = _DASHA_COLOR.get(ad.lord, "#555")
        ad_rows.append({
            "Lord":     ad.lord,
            "Years":    f"{ad.years:.3f}",
            "Start":    str(ad.start),
            "End":      str(ad.end),
            "Active":   "◀" if is_cur_ad else "",
        })
    st.dataframe(ad_rows, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 6: Gochara (Transits)
# ══════════════════════════════════════════════════════════════════════════════
with tab_gochara:
    st.subheader("Gochara — Planetary Transits")

    transit_date_input = st.date_input(
        "Transit Date",
        value=date.today(),
        min_value=date(1915, 1, 1),
        max_value=date(2100, 12, 31),
        key="transit_date_picker",
    )
    gochara = compute_gochara(chart, transit_date_input)

    # ── Summary banners ───────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("Transit Date", str(transit_date_input))
    m2.metric("Natal Lagna", gochara.natal_lagna_sign)
    m3.metric("Natal Moon", gochara.natal_moon_sign)

    # Sade Sati
    if gochara.sade_sati:
        phase_color = {"Rising": "#e05c00", "Peak": "#b71c1c", "Setting": "#e05c00"}
        pc = phase_color.get(gochara.sade_sati_phase, "#b71c1c")
        st.markdown(
            f'<div style="background:#fdecea;border-left:5px solid {pc};'
            f'padding:10px 14px;border-radius:6px;margin-bottom:12px;">'
            f'<b style="color:{pc};">⚠ Sade Sati — {gochara.sade_sati_phase} Phase</b><br>'
            f'<span style="font-size:12px;color:#555;">Saturn transiting '
            f'{gochara.planets["Saturn"].sign} — '
            f'natal Moon in {gochara.natal_moon_sign}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.success(f"No Sade Sati. Saturn in {gochara.planets['Saturn'].sign} "
                   f"(natal Moon: {gochara.natal_moon_sign})")

    if gochara.guru_chandal_transit:
        st.warning(
            f"Guru-Chandal Yoga in transit: Jupiter and Rahu both in "
            f"{gochara.planets['Jupiter'].sign}"
        )

    st.divider()

    # ── Transit table ─────────────────────────────────────────────────────────
    st.subheader("Current Transit Positions")
    t_rows = []
    for pname, tp in gochara.planets.items():
        sym  = _PLANET_SYMBOL.get(pname, "")
        retro = "℞" if tp.is_retrograde else ""
        av_str = str(tp.av_bindus) if tp.av_bindus >= 0 else "—"
        av_strength = ""
        if tp.av_bindus >= 5:
            av_strength = "Strong"
        elif tp.av_bindus == 4:
            av_strength = "Average"
        elif tp.av_bindus >= 0:
            av_strength = "Weak"
        t_rows.append({
            "": sym,
            "Planet":    pname,
            "Transit Sign": _sign_fmt(tp.sign),
            "Degree":    f"{tp.degree_in_sign:.2f}°",
            "Natal H":   f"H{tp.natal_house}",
            "Rx":        retro,
            "AV Bindus": av_str,
            "Strength":  av_strength,
        })
    st.dataframe(t_rows, use_container_width=True, hide_index=True,
                 column_config={
                     "": st.column_config.TextColumn(width="small"),
                     "Rx": st.column_config.TextColumn(width="small"),
                     "AV Bindus": st.column_config.TextColumn(width="small"),
                 })

    st.caption(
        "**AV Bindus** = Ashtakavarga bindus for transit sign from planet's own table. "
        "Strong ≥ 5 (beneficial transit), Average = 4, Weak ≤ 3 (challenging transit). "
        "Natal H = house in natal chart that the transit planet currently occupies (from lagna)."
    )


# ══════════════════════════════════════════════════════════════════════════════
# Tab 7: Rule Detail
# ══════════════════════════════════════════════════════════════════════════════
with tab_rules:
    st.subheader("Per-House Rule Breakdown")
    st.caption("22 BPHS rules per house. WC (Worth Considering) rules count at 0.5× weight.")

    house_select = st.selectbox(
        "Select House",
        options=list(range(1, 13)),
        format_func=lambda h: (
            f"H{h} — {scores.houses[h].domain} "
            f"({scores.houses[h].rating}: {scores.houses[h].final_score:+.2f})"
        ),
    )

    hs     = scores.houses[house_select]
    rating = hs.rating
    fg     = _RATING_COLOR[rating]
    bg     = _RATING_BG[rating]

    st.markdown(
        f'<div style="background:{bg};border-left:4px solid {fg};'
        f'padding:12px 16px;border-radius:6px;margin-bottom:16px;">'
        f'<b style="color:{fg};">H{house_select} — {hs.domain}</b><br>'
        f'<span style="font-size:13px;color:#555;">'
        f'Lord: <b>{hs.bhavesh}</b> in H{hs.bhavesh_house} &nbsp;|&nbsp; '
        f'Raw: {hs.raw_score:+.3f} &nbsp;|&nbsp; '
        f'Final: <b>{hs.final_score:+.2f}</b> &nbsp;|&nbsp; '
        f'<b style="color:{fg};">{rating}</b></span></div>',
        unsafe_allow_html=True,
    )

    rule_rows = []
    for r in hs.rules:
        effective = r.score * (0.5 if r.is_wc else 1.0)
        rule_rows.append({
            "Rule":        r.rule,
            "Description": r.description,
            "Raw Score":   f"{r.score:+.3f}",
            "WC":          "½×" if r.is_wc else "",
            "Effective":   f"{effective:+.3f}",
            "Active":      "✓" if r.triggered else "",
        })
    st.dataframe(rule_rows, use_container_width=True, hide_index=True,
                 column_config={
                     "Rule": st.column_config.TextColumn(width="small"),
                     "WC":   st.column_config.TextColumn(width="small"),
                     "Active": st.column_config.TextColumn(width="small"),
                 })

    positive = sum(r.score * (0.5 if r.is_wc else 1.0) for r in hs.rules if r.score > 0)
    negative = sum(r.score * (0.5 if r.is_wc else 1.0) for r in hs.rules if r.score < 0)
    active   = sum(1 for r in hs.rules if r.triggered)

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Active Rules",          f"{active}/22")
    t2.metric("Positive Contribution", f"{positive:+.3f}")
    t3.metric("Negative Contribution", f"{negative:+.3f}")
    t4.metric("Net (= Raw Score)",     f"{hs.raw_score:+.3f}")
