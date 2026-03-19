"""
src/ui/app.py — Session 19
===========================
Streamlit 12-tab UI covering all Sessions 1–18 modules.

Tabs
----
 1  📊 Chart           South Indian SVG, Panchanga, Shadbala, D9, Pushkara, PDF download
 2  🏠 Domain Scores   12-house scores bar chart + rating badges
 3  🧘 Yogas           Classical yoga cards grouped by category
 4  🔢 Ashtakavarga    Sarva bar + per-planet grids
 5  ⏱  Dashas          Vimshottari + Chara Dasha (S14)
 6  🌍 Transits        Sade Sati, Guru-Chandal, per-planet transit table
 7  📐 Varga Charts    D2/D3/D4/D7/D9/D10/D12/D60 South Indian SVG grids (S15)
 8  ⚖️  Vimshopak       Sapta Varga 20-pt dignity table (S16)
 9  🔑 KP Analysis     Sub-lord table + house significators (S17)
10  🌟 Annual Chart    Varshaphala solar return + Tajika aspects (S18)
11  💑 Kundali Milan   Ashtakoot 36-pt compatibility (S12)
12  📋 Rule Detail     Per-house 22-rule breakdown

New in Session 19
-----------------
- Monte Carlo birth-time sensitivity expander in Tab 1 (S11)
- Pushkara Navamsha indicators in planet table (S11)
- PDF download button in Tab 1 (S13)
- Chara Dasha section added to Tab 5 (S14)
- Tabs 7-11 (S12, S15-S18) all new
"""

import streamlit as st
from datetime import date, datetime

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LagnaMaster",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── core imports ──────────────────────────────────────────────────────────────
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.db import init_db, save_chart, list_charts, get_chart
from src.calculations.nakshatra import nakshatra_position
from src.calculations.dignity import compute_all_dignities, DignityLevel
from src.calculations.yogas import detect_yogas
from src.calculations.vimshottari_dasa import (
    compute_vimshottari_dasa, current_dasha, nakshatra_of_moon,
)
from src.calculations.ashtakavarga import compute_ashtakavarga, _PLANETS as _AV_PLANETS
from src.calculations.shadbala import compute_shadbala
from src.calculations.gochara import compute_gochara
from src.calculations.panchanga import compute_panchanga, compute_navamsha_chart
from src.ui.chart_visual import south_indian_svg, navamsha_svg

# ── S11-S18 imports (graceful degradation if module unavailable) ──────────────
try:
    from src.calculations.pushkara_navamsha import compute_pushkara
    _HAS_PUSHKARA = True
except ImportError:
    _HAS_PUSHKARA = False

try:
    from src.montecarlo import monte_carlo_sensitivity
    _HAS_MC = True
except ImportError:
    _HAS_MC = False

try:
    from src.reports.pdf_report import generate_pdf_report
    _HAS_PDF = True
except ImportError:
    _HAS_PDF = False

try:
    from src.calculations.chara_dasha import compute_chara_dasha, current_chara_dasha
    _HAS_CHARA = True
except ImportError:
    _HAS_CHARA = False

try:
    from src.calculations.kundali_milan import compute_kundali_milan
    _HAS_KUNDALI = True
except ImportError:
    _HAS_KUNDALI = False

try:
    from src.calculations.varga import compute_varga
    _HAS_VARGA = True
except ImportError:
    _HAS_VARGA = False

try:
    from src.calculations.sapta_varga import compute_vimshopak, vimshopak_grade
    _HAS_VIMSHOPAK = True
except ImportError:
    _HAS_VIMSHOPAK = False

try:
    from src.calculations.kp import compute_kp
    _HAS_KP = True
except ImportError:
    _HAS_KP = False

try:
    from src.calculations.varshaphala import compute_varshaphala
    _HAS_VARSHA = True
except ImportError:
    _HAS_VARSHA = False

# ── constants ──────────────────────────────────────────────────────────────────
_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_HOUSE_DOMAINS = {
    1: "Self & Vitality", 2: "Wealth & Family", 3: "Courage & Skills",
    4: "Home & Happiness", 5: "Intellect & Children", 6: "Challenges",
    7: "Relationships", 8: "Transformation", 9: "Fortune & Dharma",
    10: "Career & Status", 11: "Gains & Income", 12: "Liberation & Loss",
}
_RATING_COLOUR = {
    "Excellent": "🟢", "Strong": "🟢", "Moderate": "🟡",
    "Weak": "🟠", "Very Weak": "🔴",
}
_VARGA_DIVS = ["D2", "D3", "D4", "D7", "D9", "D10", "D12", "D60"]

init_db()

# ── session state defaults ─────────────────────────────────────────────────────
for _k, _v in [
    ("chart", None), ("scores", None), ("chart_id", None),
    ("birth_date", None), ("show_history", False),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🪐 LagnaMaster")
    st.markdown("---")

    # Demo button
    if st.button("🇮🇳 Demo: India 1947", use_container_width=True):
        st.session_state["_demo"] = True

    demo = st.session_state.pop("_demo", False)

    st.markdown("#### Birth Data")
    default_date = date(1947, 8, 15) if demo else date(1990, 1, 1)
    birth_date_input = st.date_input(
        "Birth Date", value=default_date, min_value=date(1815, 1, 1)
    )

    col1, col2 = st.columns(2)
    with col1:
        hour_val = st.slider("Hour", 0, 23, 0 if demo else 12)
    with col2:
        minute_val = st.slider("Minute", 0, 59, 0)

    hour_decimal = hour_val + minute_val / 60.0

    lat_val = st.number_input("Latitude (N+)", value=28.6139 if demo else 19.0760,
                               min_value=-90.0, max_value=90.0, format="%.4f")
    lon_val = st.number_input("Longitude (E+)", value=77.2090 if demo else 72.8777,
                               min_value=-180.0, max_value=180.0, format="%.4f")
    tz_val = st.number_input("UTC Offset (hrs)", value=5.5, min_value=-12.0,
                              max_value=14.0, step=0.5)
    ayan_val = st.selectbox("Ayanamsha", ["lahiri", "raman", "krishnamurti"])

    chart_name = st.text_input("Name / Label (optional)", value="India 1947" if demo else "")

    st.markdown("---")
    if st.button("⚡ Compute Chart", type="primary", use_container_width=True):
        with st.spinner("Computing chart…"):
            try:
                c = compute_chart(
                    year=birth_date_input.year,
                    month=birth_date_input.month,
                    day=birth_date_input.day,
                    hour=hour_decimal,
                    lat=lat_val,
                    lon=lon_val,
                    tz_offset=tz_val,
                    ayanamsha=ayan_val,
                )
                s = score_chart(c)
                import json
                chart_json = json.dumps({
                    "lagna": c.lagna,
                    "lagna_sign": c.lagna_sign,
                    "lagna_sign_index": c.lagna_sign_index,
                    "planets": {
                        p: {
                            "longitude": v.longitude,
                            "sign": v.sign,
                            "sign_index": v.sign_index,
                            "degree_in_sign": v.degree_in_sign,
                            "is_retrograde": v.is_retrograde,
                            "speed": v.speed,
                        }
                        for p, v in c.planets.items()
                    },
                })
                cid = save_chart(
                    birth_date_input.year, birth_date_input.month, birth_date_input.day,
                    hour_decimal, lat_val, lon_val, tz_val, ayan_val,
                    chart_json, name=chart_name or None,
                )
                st.session_state["chart"] = c
                st.session_state["scores"] = s
                st.session_state["chart_id"] = cid
                st.session_state["birth_date"] = birth_date_input
                st.session_state["_lat"] = lat_val
                st.session_state["_lon"] = lon_val
                st.session_state["_tz"] = tz_val
                st.session_state["_ayan"] = ayan_val
                st.success(f"Chart #{cid} computed ✓")
            except Exception as e:
                st.error(f"Error: {e}")

    st.session_state["show_history"] = st.checkbox(
        "Show Chart History", value=st.session_state["show_history"]
    )

    if st.session_state["show_history"]:
        st.markdown("#### Recent Charts")
        for row in list_charts(limit=10):
            lbl = row.get("name") or f"#{row['id']}"
            if st.button(f"{lbl} — {row['lagna_sign']}", key=f"hist_{row['id']}"):
                stored = get_chart(row["id"])
                if stored:
                    import json
                    d = json.loads(stored["chart_json"])
                    c = compute_chart(
                        year=stored["year"], month=stored["month"],
                        day=stored["day"], hour=stored["hour"],
                        lat=stored["lat"], lon=stored["lon"],
                        tz_offset=stored["tz_offset"],
                        ayanamsha=stored["ayanamsha"],
                    )
                    st.session_state["chart"] = c
                    st.session_state["scores"] = score_chart(c)
                    st.session_state["chart_id"] = row["id"]
                    st.session_state["birth_date"] = date(
                        stored["year"], stored["month"], stored["day"]
                    )

# ═════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═════════════════════════════════════════════════════════════════════════════
chart = st.session_state["chart"]
scores = st.session_state["scores"]
birth_date = st.session_state["birth_date"]

if chart is None:
    st.info("👈 Enter birth data in the sidebar and click **Compute Chart** to begin.")
    st.stop()

# ── tab layout ────────────────────────────────────────────────────────────────
(tab_chart, tab_scores, tab_yogas, tab_av,
 tab_dasha, tab_transits, tab_varga, tab_vimshopak,
 tab_kp, tab_annual, tab_kundali, tab_rules) = st.tabs([
    "📊 Chart", "🏠 Domain Scores", "🧘 Yogas", "🔢 Ashtakavarga",
    "⏱ Dashas", "🌍 Transits", "📐 Varga Charts", "⚖️ Vimshopak",
    "🔑 KP Analysis", "🌟 Annual Chart", "💑 Kundali Milan", "📋 Rule Detail",
])

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — CHART                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_chart:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Birth Chart (D1)")
        name_label = st.session_state.get("_name", "")
        svg_html = south_indian_svg(chart, name=chart_name or "")
        st.components.v1.html(f"<div style='text-align:center'>{svg_html}</div>",
                               height=540)

    with c2:
        # Panchanga
        st.markdown("### Panchanga")
        try:
            panch = compute_panchanga(chart, birth_date)
            pc1, pc2 = st.columns(2)
            with pc1:
                st.metric("Tithi", f"{panch.tithi} ({panch.paksha})")
                st.metric("Vara", panch.vara)
                st.metric("Nakshatra", f"{panch.nakshatra} P{panch.nakshatra_pada}")
            with pc2:
                st.metric("Yoga", panch.yoga)
                st.metric("Karana", panch.karana)
                st.metric("Lagna", f"{chart.lagna_sign} {chart.lagna_degree_in_sign:.2f}°")
        except Exception as e:
            st.warning(f"Panchanga: {e}")

        st.markdown("---")

        # Planet table
        st.markdown("### Planets")
        dignities = compute_all_dignities(chart)

        # Pushkara flags
        pushkara_flags = {}
        if _HAS_PUSHKARA:
            try:
                pushkara_flags = compute_pushkara(chart)
            except Exception:
                pass

        rows = []
        for p in _PLANETS:
            pp = chart.planets.get(p)
            if not pp:
                continue
            dig = dignities.get(p)
            dig_label = dig.dignity.name if dig else "—"
            combust = "💥" if (dig and dig.combust) else ""
            retro = "℞" if pp.is_retrograde else ""
            pk = "✨" if pushkara_flags.get(p) else ""
            colour = "🟢" if p in _BENEFICS else "🔴"
            rows.append({
                "": colour, "Planet": f"{p}{retro}{combust}{pk}",
                "Sign": pp.sign, "Deg": f"{pp.degree_in_sign:.2f}°",
                "Dignity": dig_label,
            })
        st.dataframe(rows, hide_index=True, use_container_width=True)
        if pushkara_flags:
            st.caption("✨ = Pushkara Navamsha")

    # Navamsha D9
    with st.expander("🔯 Navamsha (D9)"):
        try:
            nav = compute_navamsha_chart(chart)
            lagna_d9 = nav.pop("lagna", chart.lagna_sign_index)
            d9_svg = navamsha_svg(nav, lagna_d9, "D9 Navamsha")
            st.components.v1.html(
                f"<div style='text-align:center'>{d9_svg}</div>", height=540
            )
            nav["lagna"] = lagna_d9
        except Exception as e:
            st.warning(f"D9: {e}")

    # Shadbala
    with st.expander("💪 Shadbala"):
        try:
            sb_rows = []
            for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                sb = compute_shadbala(p, chart)
                sb_rows.append({
                    "Planet": p, "Uchcha": round(sb.uchcha, 1),
                    "Kendradi": round(sb.kendradi, 1), "Dig": round(sb.dig, 1),
                    "Paksha": round(sb.paksha, 1), "Chesta": round(sb.chesta, 1),
                    "Total": round(sb.total, 1),
                })
            st.dataframe(sb_rows, hide_index=True, use_container_width=True)
        except Exception as e:
            st.warning(f"Shadbala: {e}")

    # Monte Carlo
    if _HAS_MC:
        with st.expander("🎲 Monte Carlo — Birth Time Sensitivity (±30 min)"):
            if st.button("Run Monte Carlo (100 samples)", key="mc_run"):
                with st.spinner("Sampling birth times…"):
                    try:
                        mc = monte_carlo_sensitivity(
                            birth_date.year, birth_date.month, birth_date.day,
                            hour_decimal,
                            st.session_state.get("_lat", lat_val),
                            st.session_state.get("_lon", lon_val),
                            tz_offset=st.session_state.get("_tz", tz_val),
                            ayanamsha=st.session_state.get("_ayan", ayan_val),
                        )
                        mc_rows = []
                        for h in range(1, 13):
                            hs = mc.houses[h]
                            mc_rows.append({
                                "House": h, "Domain": _HOUSE_DOMAINS[h],
                                "Mean": round(hs.score_mean, 2),
                                "Std": round(hs.score_std, 2),
                                "Range": round(hs.score_range, 2),
                                "Stable": "✅" if hs.stable else "⚠️",
                            })
                        st.dataframe(mc_rows, hide_index=True, use_container_width=True)
                        st.caption(f"{mc.n_samples} samples over ±{mc.window_minutes} min")
                    except Exception as e:
                        st.error(f"Monte Carlo failed: {e}")

    # PDF download
    if _HAS_PDF:
        st.markdown("---")
        if st.button("📄 Download PDF Report"):
            try:
                yogas_for_pdf = detect_yogas(chart)
                dashas_for_pdf = compute_vimshottari_dasa(chart, birth_date)
                pdf_bytes = generate_pdf_report(
                    chart, scores, yogas_for_pdf, dashas_for_pdf,
                    birth_date, name=chart_name or ""
                )
                st.download_button(
                    "💾 Save PDF", data=pdf_bytes,
                    file_name=f"lagnamaster_{birth_date}.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — DOMAIN SCORES                                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_scores:
    st.markdown("### Domain Scores — 22 BPHS Rules × 12 Houses")
    cols = st.columns(3)
    for i, (house, hs) in enumerate(sorted(scores.houses.items())):
        with cols[i % 3]:
            icon = _RATING_COLOUR.get(hs.rating, "⚪")
            st.metric(
                label=f"H{house} {_HOUSE_DOMAINS.get(house, '')}",
                value=f"{hs.final_score:+.2f}",
                delta=hs.rating,
            )

    st.markdown("---")
    # Bar chart data
    import pandas as pd
    bar_data = pd.DataFrame([
        {"House": f"H{h}", "Score": s.final_score, "Rating": s.rating}
        for h, s in sorted(scores.houses.items())
    ])
    st.bar_chart(bar_data.set_index("House")["Score"])

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 3 — YOGAS                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_yogas:
    st.markdown("### Classical Yoga Formations")
    try:
        yogas = detect_yogas(chart)
        if not yogas:
            st.info("No classical yogas detected in this chart.")
        else:
            by_cat = {}
            for y in yogas:
                by_cat.setdefault(y.category, []).append(y)
            for cat, ylist in by_cat.items():
                st.markdown(f"#### {cat}")
                for y in ylist:
                    nature_icon = "🟢" if y.nature == "benefic" else ("🔴" if y.nature == "malefic" else "🟡")
                    with st.container():
                        st.markdown(
                            f"**{nature_icon} {y.name}** — planets: {', '.join(y.planets)}"
                        )
                        st.caption(y.description)
    except Exception as e:
        st.error(f"Yoga detection failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 4 — ASHTAKAVARGA                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_av:
    st.markdown("### Ashtakavarga — Bindu Tables")
    try:
        av = compute_ashtakavarga(chart)
        # Sarva bar
        sarva_data = pd.DataFrame({
            "Sign": _SIGNS,
            "Bindus": av.sarva.bindus,
        })
        st.markdown("#### Sarvashtakavarga (Total Bindus per Sign)")
        st.bar_chart(sarva_data.set_index("Sign")["Bindus"])

        # Per-planet grids
        selected_planet = st.selectbox("Planet", _AV_PLANETS, key="av_planet")
        pt = av.for_planet(selected_planet)
        av_rows = []
        for si, sign in enumerate(_SIGNS):
            av_rows.append({
                "Sign": sign, "Bindus": pt.bindus[si],
                "Strength": pt.strength(si),
            })
        st.dataframe(av_rows, hide_index=True, use_container_width=True)
        st.caption(f"Total: {pt.total} bindus")

        # Full table
        with st.expander("📊 Full Ashtakavarga Table"):
            full_rows = [{"Sign": s} for s in _SIGNS]
            for p in _AV_PLANETS:
                pt2 = av.for_planet(p)
                for i, row in enumerate(full_rows):
                    row[p] = pt2.bindus[i]
            st.dataframe(full_rows, hide_index=True, use_container_width=True)
    except Exception as e:
        st.error(f"Ashtakavarga failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 5 — DASHAS                                                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_dasha:
    today = date.today()

    # ── Vimshottari Dasha ─────────────────────────────────────────────────────
    st.markdown("### Vimshottari Dasha (120-year Nakshatra Cycle)")
    try:
        dashas = compute_vimshottari_dasa(chart, birth_date)
        nak_name, dasha_lord = nakshatra_of_moon(chart)
        cur_md, cur_ad = current_dasha(dashas, today)

        st.markdown(
            f"**Moon Nakshatra**: {nak_name} | "
            f"**Birth Lord**: {dasha_lord} | "
            f"**Current**: {cur_md.lord} MD / {cur_ad.lord} AD"
        )
        st.caption(f"AD period: {cur_ad.start} → {cur_ad.end}")

        md_rows = []
        for md in dashas:
            md_rows.append({
                "MahaDasha": md.lord,
                "Start": str(md.start), "End": str(md.end),
                "Years": round(md.years, 2),
                "Current": "▶" if md.lord == cur_md.lord else "",
            })
        st.dataframe(md_rows, hide_index=True, use_container_width=True)

        with st.expander(f"AntarDashas — {cur_md.lord} MahaDasha"):
            ad_rows = [
                {"AntarDasha": ad.lord, "Start": str(ad.start), "End": str(ad.end),
                 "Years": round(ad.years, 3),
                 "Current": "▶" if ad.lord == cur_ad.lord else ""}
                for ad in cur_md.antardashas
            ]
            st.dataframe(ad_rows, hide_index=True, use_container_width=True)
    except Exception as e:
        st.error(f"Vimshottari Dasha failed: {e}")

    # ── Chara Dasha ───────────────────────────────────────────────────────────
    if _HAS_CHARA:
        st.markdown("---")
        st.markdown("### Jaimini Chara Dasha (Sign-based Cycle)")
        try:
            chara_dashas = compute_chara_dasha(chart, birth_date)
            cur_cmd, cur_cad = current_chara_dasha(chara_dashas, today)
            st.markdown(
                f"**Current**: {cur_cmd.sign} MD / {cur_cad.sign} AD  "
                f"({cur_cad.start} → {cur_cad.end})"
            )
            cd_rows = [
                {"Sign": md.sign, "Start": str(md.start), "End": str(md.end),
                 "Years": round(md.years, 2),
                 "Current": "▶" if md.sign == cur_cmd.sign else ""}
                for md in chara_dashas
            ]
            st.dataframe(cd_rows, hide_index=True, use_container_width=True)
        except Exception as e:
            st.error(f"Chara Dasha failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 6 — TRANSITS                                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_transits:
    st.markdown("### Current Transits (Gochara)")
    transit_date = st.date_input("Transit Date", value=today, key="transit_date")
    try:
        gochara = compute_gochara(chart, transit_date)

        if gochara.sade_sati:
            phase = gochara.sade_sati_phase
            st.warning(f"⚠️ Sade Sati — **{phase}** phase (Saturn over natal Moon area)")
        if gochara.guru_chandal_transit:
            st.error("🔴 Guru-Chandal Yoga active in transit sky (Jupiter + Rahu conjunct)")

        tr_rows = []
        for p in _PLANETS:
            tp = gochara.planets.get(p)
            if not tp:
                continue
            tr_rows.append({
                "Planet": p,
                "Transit Sign": tp.sign,
                "Natal House": tp.natal_house,
                "AV Bindus": tp.av_bindus if tp.av_bindus >= 0 else "—",
                "Rx": "℞" if tp.is_retrograde else "",
            })
        st.dataframe(tr_rows, hide_index=True, use_container_width=True)
        st.caption(
            f"Natal Moon: {gochara.natal_moon_sign} | "
            f"Natal Lagna: {gochara.natal_lagna_sign}"
        )
    except Exception as e:
        st.error(f"Transit calculation failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 7 — VARGA CHARTS  (S15)                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_varga:
    st.markdown("### Varga Divisional Charts")
    if not _HAS_VARGA:
        st.info("varga.py not available.")
    else:
        try:
            vc = compute_varga(chart)
            selected_div = st.selectbox(
                "Division", _VARGA_DIVS,
                format_func=lambda d: f"{d} — {vc.for_division(d).label}",
                key="varga_div",
            )
            vt = vc.for_division(selected_div)

            col_svg, col_tbl = st.columns([1, 1])
            with col_svg:
                # Reuse navamsha_svg: takes {planet: sign_index} + lagna sign index
                d_data = {p: vt.planet_sign_index(p) for p in _PLANETS if p in vt.planets}
                varga_svg_str = navamsha_svg(
                    d_data, vt.varga_lagna_sign_index,
                    f"{selected_div} {vt.label}"
                )
                st.components.v1.html(
                    f"<div style='text-align:center'>{varga_svg_str}</div>",
                    height=540,
                )

            with col_tbl:
                st.markdown(f"**{selected_div} Lagna**: {vt.varga_lagna_sign}")
                st.markdown(f"**D1 Lagna**: {vt.lagna_sign}")
                v_rows = [
                    {
                        "Planet": p,
                        "D1 Sign": vt.planets[p].d1_sign,
                        f"{selected_div} Sign": vt.planets[p].varga_sign,
                        "Rx": "℞" if vt.planets[p].is_retrograde else "",
                    }
                    for p in _PLANETS if p in vt.planets
                ]
                st.dataframe(v_rows, hide_index=True, use_container_width=True)

            # Summary table — all divisions
            with st.expander("📊 All Divisions Summary"):
                all_rows = [{"Planet": p} for p in _PLANETS]
                for div in _VARGA_DIVS:
                    vt2 = vc.for_division(div)
                    for row in all_rows:
                        p = row["Planet"]
                        row[div] = vt2.planets[p].varga_sign if p in vt2.planets else "—"
                st.dataframe(all_rows, hide_index=True, use_container_width=True)

        except Exception as e:
            st.error(f"Varga Charts failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 8 — VIMSHOPAK BALA  (S16)                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_vimshopak:
    st.markdown("### Sapta Varga Vimshopak Bala (20-point Dignity Score)")
    if not _HAS_VIMSHOPAK:
        st.info("sapta_varga.py not available.")
    else:
        try:
            vim = compute_vimshopak(chart)

            # Ranking bar
            ranking = vim.ranking()
            rank_df = pd.DataFrame(ranking, columns=["Planet", "Score"])
            st.bar_chart(rank_df.set_index("Planet")["Score"])

            # Per-planet breakdown
            selected_planet_v = st.selectbox(
                "Planet Detail", [p for p, _ in ranking], key="vim_planet"
            )
            pv = vim.for_planet(selected_planet_v)
            st.markdown(
                f"**{selected_planet_v}** — Total: **{pv.total:.2f} / 20** "
                f"({pv.grade})"
            )
            vd_rows = [
                {
                    "Division": div,
                    "Weight": vd.weight,
                    "Sign": vd.sign_name,
                    "Dignity": vd.dignity,
                    "Points": round(vd.points, 3),
                }
                for div, vd in pv.varga_dignities.items()
            ]
            st.dataframe(vd_rows, hide_index=True, use_container_width=True)

            # Full table
            st.markdown("---")
            st.markdown("#### Full Table (all planets)")
            full_vim = []
            for p_name in _PLANETS + ["Lagna"]:
                if p_name not in vim.planets:
                    continue
                pv2 = vim.planets[p_name]
                row = {"Planet": p_name, "Total": round(pv2.total, 2), "Grade": pv2.grade}
                for div in ["D1", "D2", "D3", "D7", "D9", "D10", "D12"]:
                    if div in pv2.varga_dignities:
                        row[div] = pv2.varga_dignities[div].dignity[:4]
                full_vim.append(row)
            st.dataframe(full_vim, hide_index=True, use_container_width=True)
            st.caption(
                "Grade: Excellent ≥15 | Good ≥10 | Average ≥6 | Weak ≥3 | Very Weak <3"
            )
        except Exception as e:
            st.error(f"Vimshopak Bala failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 9 — KP ANALYSIS  (S17)                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_kp:
    st.markdown("### KP (Krishnamurti Paddhati) Sub-lord Analysis")
    if not _HAS_KP:
        st.info("kp.py not available.")
    else:
        try:
            kp = compute_kp(chart)

            # Lagna KP
            lk = kp.lagna_kp
            st.markdown(
                f"**Lagna KP** — Nakshatra: {lk.nakshatra} | "
                f"Star Lord: {lk.star_lord} | Sub Lord: **{lk.sub_lord}** | "
                f"Sub-Sub: {lk.sub_sub_lord}"
            )
            st.markdown("---")

            # Planet sub-lord table
            st.markdown("#### Planet Sub-lords")
            kp_rows = []
            for p in _PLANETS:
                kpp = kp.planets.get(p)
                if not kpp:
                    continue
                kp_rows.append({
                    "Planet": p + ("℞" if kpp.is_retrograde else ""),
                    "Sign": kpp.sign,
                    "Nakshatra": kpp.nakshatra,
                    "Star Lord (SL)": kpp.star_lord,
                    "Sub Lord": kpp.sub_lord,
                    "Sub-Sub": kpp.sub_sub_lord,
                })
            st.dataframe(kp_rows, hide_index=True, use_container_width=True)

            # House significators
            st.markdown("---")
            st.markdown("#### House Cusp Sub-lords & Significators")
            sig_rows = []
            for h in range(1, 13):
                hs = kp.houses[h]
                sig_rows.append({
                    "House": h,
                    "Domain": _HOUSE_DOMAINS.get(h, ""),
                    "Cusp Sub Lord": hs.cusp_sub_lord,
                    "Occupants": ", ".join(hs.occupants) or "—",
                    "House Lord": hs.house_lord,
                    "Significators": ", ".join(hs.significators[:5]),
                })
            st.dataframe(sig_rows, hide_index=True, use_container_width=True)
            st.caption("Pilot: whole-sign house cusps (0° of each sign)")
        except Exception as e:
            st.error(f"KP Analysis failed: {e}")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 10 — ANNUAL CHART (VARSHAPHALA)  (S18)                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_annual:
    st.markdown("### Varshaphala — Annual Solar Return Chart")
    if not _HAS_VARSHA:
        st.info("varshaphala.py not available.")
    else:
        target_year = st.number_input(
            "Target Year", min_value=1900, max_value=2100,
            value=today.year, key="varsha_year"
        )
        lat_v = st.session_state.get("_lat", lat_val)
        lon_v = st.session_state.get("_lon", lon_val)
        tz_v = st.session_state.get("_tz", tz_val)
        ayan_v = st.session_state.get("_ayan", ayan_val)

        if st.button("⚡ Compute Annual Chart", key="varsha_btn"):
            with st.spinner("Finding solar return moment…"):
                try:
                    vr = compute_varshaphala(
                        natal_chart=chart,
                        natal_birth_date=birth_date,
                        target_year=int(target_year),
                        lat=lat_v, lon=lon_v,
                        tz_offset=tz_v, ayanamsha=ayan_v,
                    )
                    st.session_state["_varsha_report"] = vr
                except Exception as e:
                    st.error(f"Varshaphala failed: {e}")

        vr = st.session_state.get("_varsha_report")
        if vr:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown("#### Annual Chart")
                ann_svg = south_indian_svg(
                    vr.varsha_chart, name=f"Annual {target_year}"
                )
                st.components.v1.html(
                    f"<div style='text-align:center'>{ann_svg}</div>", height=540
                )

            with col_b:
                st.markdown("#### Annual Indicators")
                st.metric("Solar Return Date", str(vr.solar_return_date))
                st.metric("Varsha Lagna", vr.varsha_lagna_sign)
                st.metric("Muntha Sign", vr.muntha_sign)
                st.metric("Varsha Pati (Year Lord)", vr.varsha_pati)
                st.metric("Years Elapsed", vr.years_elapsed)

                st.markdown("#### Tajika Aspects")
                if vr.tajika_aspects:
                    taj_rows = [
                        {
                            "Type": a.aspect_type,
                            "Planets": f"{a.planet_a} – {a.planet_b}",
                            "Angle": f"{a.angle}°",
                            "Orb": f"{a.orb:.2f}°",
                            "Mode": "Applying" if a.applying else "Separating",
                        }
                        for a in vr.tajika_aspects
                    ]
                    st.dataframe(taj_rows, hide_index=True, use_container_width=True)
                else:
                    st.info("No Tajika aspects within orb.")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 11 — KUNDALI MILAN  (S12)                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_kundali:
    st.markdown("### Kundali Milan — Ashtakoot Compatibility (36 points)")
    if not _HAS_KUNDALI:
        st.info("kundali_milan.py not available.")
    else:
        st.info(
            "Enter the **second person's** birth data below. "
            "The first chart uses the data already computed in the sidebar."
        )
        with st.form("kundali_form"):
            km_c1, km_c2 = st.columns(2)
            with km_c1:
                km_date = st.date_input("Birth Date (Person B)", value=date(1990, 1, 1))
                km_hour = st.slider("Hour (Person B)", 0, 23, 6)
                km_min = st.slider("Minute (Person B)", 0, 59, 0)
            with km_c2:
                km_lat = st.number_input("Lat (Person B)", value=28.6139, format="%.4f")
                km_lon = st.number_input("Lon (Person B)", value=77.2090, format="%.4f")
                km_tz = st.number_input("UTC Offset (Person B)", value=5.5, step=0.5)
            km_submit = st.form_submit_button("💑 Compute Compatibility")

        if km_submit:
            with st.spinner("Computing compatibility…"):
                try:
                    chart_b = compute_chart(
                        year=km_date.year, month=km_date.month, day=km_date.day,
                        hour=km_hour + km_min / 60.0,
                        lat=km_lat, lon=km_lon, tz_offset=km_tz, ayanamsha=ayan_val,
                    )
                    result = compute_kundali_milan(chart, chart_b)
                    st.session_state["_kundali_result"] = result
                    st.session_state["_chart_b"] = chart_b
                except Exception as e:
                    st.error(f"Kundali Milan failed: {e}")

        kr = st.session_state.get("_kundali_result")
        if kr:
            grade_icon = {"Excellent": "🟢", "Good": "🟡", "Average": "🟠", "Poor": "🔴"}.get(
                kr.grade, "⚪"
            )
            st.markdown(
                f"## {grade_icon} Total: **{kr.total:.1f} / 36** — {kr.grade}"
            )

            if kr.mangal_dosha_a:
                st.warning("⚠️ Person A has Mangal Dosha")
            if kr.mangal_dosha_b:
                st.warning("⚠️ Person B has Mangal Dosha")

            kuta_rows = []
            for kuta_name, ks in kr.kutas.items():
                kuta_rows.append({
                    "Kuta": kuta_name,
                    "Score": round(ks.score, 1),
                    "Max": ks.max_score,
                    "Detail": getattr(ks, "detail", ""),
                })
            st.dataframe(kuta_rows, hide_index=True, use_container_width=True)

            cb = st.session_state.get("_chart_b")
            if cb:
                k_c1, k_c2 = st.columns(2)
                with k_c1:
                    st.markdown("**Person A**")
                    st.components.v1.html(
                        f"<div style='text-align:center'>{south_indian_svg(chart, 'Person A')}</div>",
                        height=540,
                    )
                with k_c2:
                    st.markdown("**Person B**")
                    st.components.v1.html(
                        f"<div style='text-align:center'>{south_indian_svg(cb, 'Person B')}</div>",
                        height=540,
                    )

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 12 — RULE DETAIL                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab_rules:
    st.markdown("### Rule Detail — 22 BPHS Rules per House")
    house_sel = st.selectbox(
        "House", list(range(1, 13)),
        format_func=lambda h: f"H{h} — {_HOUSE_DOMAINS.get(h, '')}",
        key="rule_house",
    )
    hs = scores.houses.get(house_sel)
    if hs:
        st.markdown(
            f"**Bhavesh**: {hs.bhavesh} (in H{hs.bhavesh_house}) | "
            f"**Score**: {hs.final_score:+.2f} | **Rating**: {hs.rating}"
        )
        rule_rows = [
            {
                "Rule": r.rule,
                "Description": r.description,
                "Triggered": "✅" if r.triggered else "—",
                "Score": f"{r.score:+.3f}" if r.triggered else "0",
                "WC": "½×" if r.is_wc else "",
            }
            for r in hs.rules
        ]
        st.dataframe(rule_rows, hide_index=True, use_container_width=True)
        st.caption("WC = Worth Considering rules count at 0.5× weight")
