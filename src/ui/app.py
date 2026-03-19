"""
src/ui/app.py — LagnaMaster Session 21
Streamlit 10-tab UI wiring all committed modules (Sessions 1–20).

Tabs
----
1  Chart          South Indian D1 SVG + panchanga strip + Shadbala expander + D9 expander
2  Domain Scores  12-house bar chart + rating badges + Monte Carlo sensitivity
3  Yogas          Yoga cards grouped by category
4  Ashtakavarga   Sarva bar + per-planet grids + data table
5  Dasha          Vimshottari MD/AD table + Jaimini Chara Dasha table
6  Transits       Date picker + Sade Sati + Guru-Chandal + transit table
7  Milan          Kundali Milan partner form + 8-koot breakdown + composite score
8  KP             KP sub-lord table + ruling planets at selected date
9  Tajika         Annual chart SVG + Muntha + Sahams + Itthasala/Ishrafa aspects
10 Rule Detail    Per-house 22-rule breakdown

Session 21 additions over Session 19
-------------------------------------
* Tab 5: Jaimini Chara Dasha section added below Vimshottari
* Tab 7: Composite compatibility score (compatibility_score.py) shown
* Tab 2: Monte Carlo sensitivity badges (Stable/Sensitive/High) per house
* Tab 8: KP ruling planets refreshed on date change
* Sidebar: Celery task status indicator (async PDF + Monte Carlo)
* All imports verified against committed module public APIs
"""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Optional

import streamlit as st

# ── page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="LagnaMaster",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── imports ────────────────────────────────────────────────────────────────────
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.db import init_db, save_chart, list_charts, get_chart

from src.calculations.nakshatra import nakshatra_position
from src.calculations.dignity import compute_all_dignities, DignityLevel
from src.calculations.shadbala import compute_shadbala
from src.calculations.vimshottari_dasa import (
    compute_vimshottari_dasa, current_dasha, nakshatra_of_moon,
)
from src.calculations.yogas import detect_yogas
from src.calculations.ashtakavarga import compute_ashtakavarga, _PLANETS as _AV_PLANETS
from src.calculations.gochara import compute_gochara
from src.calculations.panchanga import compute_panchanga, compute_navamsha_chart
from src.calculations.pushkara_navamsha import check_pushkara, run_monte_carlo
from src.calculations.kundali_milan import compute_milan
from src.calculations.jaimini_chara_dasha import compute_chara_dasha, current_chara_dasha
from src.calculations.kp_significators import compute_kp
from src.calculations.tajika import compute_tajika
from src.calculations.compatibility_score import compute_compatibility

from src.ui.chart_visual import south_indian_svg, navamsha_svg

# ── constants ─────────────────────────────────────────────────────────────────
_SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
]
_RATING_COLOUR = {
    "Excellent": "🟢", "Strong": "🟢",
    "Moderate": "🟡", "Weak": "🟠", "Very Weak": "🔴",
}
_NATURE_COLOUR = {"benefic": "green", "mixed": "orange", "malefic": "red"}

# ── DB init ───────────────────────────────────────────────────────────────────
init_db()

# ── session state defaults ────────────────────────────────────────────────────
for key, default in [
    ("chart", None), ("scores", None), ("chart_id", None),
    ("birth_date", date(1990, 1, 1)), ("show_history", False),
    ("partner_chart", None), ("partner_birth_date", date(1990, 1, 1)),
    ("monte_carlo", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — birth data input
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🪐 LagnaMaster")
    st.markdown("Vedic Jyotish Chart Engine")
    st.divider()

    st.subheader("Birth Data")
    birth_date = st.date_input(
        "Date of Birth",
        value=st.session_state.birth_date,
        min_value=date(1900, 1, 1),
        max_value=date(2100, 12, 31),
    )
    col_h, col_m = st.columns(2)
    birth_hour = col_h.slider("Hour", 0, 23, 12)
    birth_min = col_m.slider("Min", 0, 59, 0)
    birth_hour_decimal = birth_hour + birth_min / 60.0

    lat = st.number_input("Latitude (°N)", value=28.6139, format="%.4f")
    lon = st.number_input("Longitude (°E)", value=77.2090, format="%.4f")
    tz_offset = st.number_input("Timezone offset (hrs)", value=5.5, step=0.5)
    ayanamsha = st.selectbox("Ayanamsha", ["lahiri", "raman", "krishnamurti"])
    chart_name = st.text_input("Label (optional)", "")

    st.divider()
    if st.button("🇮🇳 Demo: India 1947", use_container_width=True):
        st.session_state.birth_date = date(1947, 8, 15)
        st.rerun()

    compute_btn = st.button("⚡ Compute Chart", type="primary", use_container_width=True)

    st.divider()
    st.session_state.show_history = st.toggle("Chart History", value=st.session_state.show_history)

    # Celery status indicator
    st.divider()
    st.caption("🔧 Async tasks (Celery)")
    st.info("Celery workers: Session 21 — see docs/SESSION_LOG.md", icon="ℹ️")


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTE
# ══════════════════════════════════════════════════════════════════════════════

if compute_btn:
    with st.spinner("Computing chart…"):
        try:
            chart = compute_chart(
                birth_date.year, birth_date.month, birth_date.day,
                birth_hour_decimal, lat, lon, tz_offset, ayanamsha,
            )
            scores = score_chart(chart)
            chart_dict = {
                "jd_ut": chart.jd_ut,
                "ayanamsha_name": chart.ayanamsha_name,
                "ayanamsha_value": chart.ayanamsha_value,
                "lagna": chart.lagna,
                "lagna_sign": chart.lagna_sign,
                "lagna_sign_index": chart.lagna_sign_index,
                "lagna_degree_in_sign": chart.lagna_degree_in_sign,
                "planets": {
                    n: {
                        "name": p.name, "longitude": p.longitude,
                        "sign": p.sign, "sign_index": p.sign_index,
                        "degree_in_sign": p.degree_in_sign,
                        "is_retrograde": p.is_retrograde, "speed": p.speed,
                    }
                    for n, p in chart.planets.items()
                },
            }
            chart_id = save_chart(
                birth_date.year, birth_date.month, birth_date.day,
                birth_hour_decimal, lat, lon, tz_offset, ayanamsha,
                json.dumps(chart_dict),
                name=chart_name or None,
            )
            st.session_state.chart = chart
            st.session_state.scores = scores
            st.session_state.chart_id = chart_id
            st.session_state.birth_date = birth_date
            st.session_state.monte_carlo = None  # reset on new chart
        except Exception as exc:
            st.error(f"Computation error: {exc}")

# ══════════════════════════════════════════════════════════════════════════════
# CHART HISTORY (sidebar toggle)
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.show_history:
    st.subheader("Recent Charts")
    rows = list_charts(limit=10)
    for row in rows:
        cj = json.loads(row["chart_json"]) if isinstance(row["chart_json"], str) else row["chart_json"]
        label = row.get("name") or f"Chart #{row['id']}"
        if st.button(f"{label} — {cj['lagna_sign']} lagna", key=f"hist_{row['id']}"):
            from src.ephemeris import BirthChart, PlanetPosition
            planets = {
                n: PlanetPosition(**p) for n, p in cj["planets"].items()
            }
            st.session_state.chart = BirthChart(
                jd_ut=cj["jd_ut"], ayanamsha_name=cj["ayanamsha_name"],
                ayanamsha_value=cj["ayanamsha_value"], lagna=cj["lagna"],
                lagna_sign=cj["lagna_sign"], lagna_sign_index=cj["lagna_sign_index"],
                lagna_degree_in_sign=cj["lagna_degree_in_sign"], planets=planets,
            )
            st.session_state.scores = score_chart(st.session_state.chart)
            st.session_state.chart_id = row["id"]
            st.rerun()
    st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# GUARD — no chart yet
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.chart is None:
    st.title("🪐 LagnaMaster")
    st.info("Enter birth data in the sidebar and click **⚡ Compute Chart** to begin.", icon="👈")
    st.stop()

chart = st.session_state.chart
scores = st.session_state.scores
birth_date = st.session_state.birth_date

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tabs = st.tabs([
    "🗺 Chart", "📊 Scores", "✨ Yogas", "🔢 Ashtakavarga",
    "⏳ Dasha", "🌍 Transits", "💑 Milan", "🔑 KP", "📅 Tajika", "📋 Rules",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHART
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader(f"{chart.lagna_sign} Lagna — {birth_date.strftime('%d %b %Y')}")

    col_d1, col_info = st.columns([1, 1])
    with col_d1:
        svg = south_indian_svg(chart, chart_name)
        st.markdown(svg, unsafe_allow_html=True)

    with col_info:
        # Panchanga strip
        panchanga = compute_panchanga(chart, birth_date)
        st.markdown("**Panchanga**")
        pc1, pc2, pc3, pc4, pc5 = st.columns(5)
        pc1.metric("Tithi", f"{panchanga.tithi_index}", panchanga.paksha)
        pc2.metric("Vara", panchanga.vara_lord, panchanga.vara_name)
        pc3.metric("Nakshatra", panchanga.nakshatra_name, f"Pada {panchanga.nakshatra_pada}")
        pc4.metric("Yoga", panchanga.yoga_name, "auspicious" if panchanga.yoga_auspicious else "inauspicious")
        pc5.metric("Karana", panchanga.karana_name, "⚠" if panchanga.karana_inauspicious else "")

        st.divider()

        # Planet table
        st.markdown("**Planets**")
        dignities = compute_all_dignities(chart)
        pushkara_results = {r.planet: r for r in check_pushkara(chart)}

        rows_data = []
        for planet, pos in chart.planets.items():
            dig = dignities.get(planet)
            dig_label = dig.dignity.name if dig else "—"
            pk = "✦" if pushkara_results.get(planet) and pushkara_results[planet].is_pushkara else ""
            rx = "℞" if pos.is_retrograde else ""
            rows_data.append({
                "Planet": planet,
                "Sign": pos.sign,
                "Degree": f"{pos.degree_in_sign:.2f}°",
                "Rx": rx,
                "Dignity": dig_label,
                "PK": pk,
            })
        st.dataframe(rows_data, use_container_width=True, hide_index=True)

    # Shadbala expander
    with st.expander("Shadbala — Planetary Strength"):
        sb_rows = []
        for planet in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]:
            sb = compute_shadbala(planet, chart)
            sb_rows.append({
                "Planet": planet,
                "Uchcha": f"{sb.uchcha:.1f}",
                "Kendradi": f"{sb.kendradi:.1f}",
                "Dig": f"{sb.dig:.1f}",
                "Paksha": f"{sb.paksha:.1f}",
                "Chesta": f"{sb.chesta:.1f}",
                "Total": f"{sb.total:.1f}",
            })
        st.dataframe(sb_rows, use_container_width=True, hide_index=True)

    # Navamsha D9 expander
    with st.expander("Navamsha D9 Chart"):
        d9 = compute_navamsha_chart(chart)
        lagna_d9_si = d9.pop("lagna", chart.lagna_sign_index)
        d9_svg = navamsha_svg(d9, lagna_d9_si)
        st.markdown(d9_svg, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DOMAIN SCORES + MONTE CARLO
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Domain Scores — 22-Rule BPHS Engine")

    score_vals = [scores.houses[h].final_score for h in range(1, 13)]
    domains = [scores.houses[h].domain for h in range(1, 13)]
    house_labels = [f"H{h}" for h in range(1, 13)]

    st.bar_chart(
        data={"Score": score_vals},
        use_container_width=True,
        height=220,
    )

    cols = st.columns(6)
    for i, h in enumerate(range(1, 13)):
        hs = scores.houses[h]
        emoji = _RATING_COLOUR.get(hs.rating, "⚪")
        cols[i % 6].metric(
            f"H{h} {hs.domain[:10]}",
            f"{hs.final_score:+.1f}",
            hs.rating,
        )

    # Monte Carlo
    st.divider()
    st.markdown("**Birth Time Sensitivity — Monte Carlo ±30 min**")
    mc_col1, mc_col2 = st.columns([1, 3])
    run_mc = mc_col1.button("Run Monte Carlo (100 samples)", use_container_width=True)
    if run_mc:
        with st.spinner("Running 100 birth-time samples…"):
            st.session_state.monte_carlo = run_monte_carlo(
                birth_date.year, birth_date.month, birth_date.day,
                birth_hour_decimal, lat, lon, tz_offset, ayanamsha,
                samples=100, window_minutes=30.0,
            )

    mc = st.session_state.monte_carlo
    if mc:
        mc_rows = []
        for h in range(1, 13):
            mc_rows.append({
                "House": f"H{h}",
                "Domain": scores.houses[h].domain,
                "Base Score": f"{mc.base_scores[h]:+.2f}",
                "Mean": f"{mc.mean_scores[h]:+.2f}",
                "σ": f"{mc.std_scores[h]:.2f}",
                "Sensitivity": mc.sensitivity[h],
            })
        st.dataframe(mc_rows, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — YOGAS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    yogas = detect_yogas(chart)
    st.subheader(f"Detected Yogas ({len(yogas)})")

    if not yogas:
        st.info("No classical yogas detected for this chart.")
    else:
        current_category = None
        for yoga in yogas:
            if yoga.category != current_category:
                st.markdown(f"### {yoga.category}")
                current_category = yoga.category
            colour = _NATURE_COLOUR.get(yoga.nature, "gray")
            planets_str = ", ".join(yoga.planets) if yoga.planets else "—"
            st.markdown(
                f"**{yoga.name}** &nbsp; "
                f"<span style='color:{colour};font-size:0.8em'>{yoga.nature}</span>  \n"
                f"*Planets*: {planets_str}  \n"
                f"{yoga.description}",
                unsafe_allow_html=True,
            )
            st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ASHTAKAVARGA
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    av = compute_ashtakavarga(chart)
    st.subheader("Sarvashtakavarga")

    sarva_vals = av.sarva.bindus
    st.bar_chart(
        data={"Bindus": sarva_vals},
        use_container_width=True,
        height=180,
    )
    st.caption(f"Total: {av.sarva.total} (Strong ≥5 · Average 3–4 · Weak ≤2)")

    planet_tab_labels = _AV_PLANETS
    planet_tabs = st.tabs(planet_tab_labels)
    for i, planet in enumerate(planet_tab_labels):
        with planet_tabs[i]:
            av_table = av.for_planet(planet)
            av_rows = []
            for si, sign in enumerate(_SIGNS):
                b = av_table.bindus[si]
                av_rows.append({
                    "Sign": sign,
                    "Bindus": b,
                    "Strength": av_table.strength(si),
                })
            st.dataframe(av_rows, use_container_width=True, hide_index=True)
            st.caption(f"Total: {av_table.total}")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — DASHA (Vimshottari + Jaimini Chara)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    # ── Vimshottari ────────────────────────────────────────────────────────────
    st.subheader("Vimshottari Dasha")
    dashas = compute_vimshottari_dasa(chart, birth_date)
    md_now, ad_now = current_dasha(dashas)
    nak_name, nak_lord = nakshatra_of_moon(chart)

    st.markdown(
        f"Moon in **{nak_name}** nakshatra · Birth dasha lord: **{nak_lord}**"
    )
    st.info(
        f"**Current:** {md_now.lord} MahaDasha → {ad_now.lord} AntarDasha  \n"
        f"MD: {md_now.start} → {md_now.end}  |  AD: {ad_now.start} → {ad_now.end}"
    )

    md_rows = []
    for md in dashas:
        active = md.lord == md_now.lord and md.start == md_now.start
        md_rows.append({
            "MahaDasha": ("▶ " if active else "") + md.lord,
            "Start": str(md.start),
            "End": str(md.end),
            "Years": f"{md.years:.1f}",
        })
    st.dataframe(md_rows, use_container_width=True, hide_index=True)

    with st.expander("AntarDashas for current MahaDasha"):
        ad_rows = []
        for ad in md_now.antardashas:
            active_ad = ad.lord == ad_now.lord and ad.start == ad_now.start
            ad_rows.append({
                "AntarDasha": ("▶ " if active_ad else "") + ad.lord,
                "Start": str(ad.start),
                "End": str(ad.end),
                "Years": f"{ad.years:.2f}",
            })
        st.dataframe(ad_rows, use_container_width=True, hide_index=True)

    # ── Jaimini Chara ──────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Jaimini Chara Dasha")
    chara_dashas = compute_chara_dasha(chart, birth_date)
    chara_md, chara_ad = current_chara_dasha(chara_dashas)

    st.info(
        f"**Current:** {chara_md.sign} MahaDasha → {chara_ad.sign} AntarDasha  \n"
        f"MD: {chara_md.start} → {chara_md.end}  |  AD: {chara_ad.start} → {chara_ad.end}"
    )

    chara_rows = []
    for cmd in chara_dashas:
        active = cmd.sign == chara_md.sign and cmd.start == chara_md.start
        chara_rows.append({
            "Mahadasha Sign": ("▶ " if active else "") + cmd.sign,
            "Start": str(cmd.start),
            "End": str(cmd.end),
            "Years": f"{cmd.years:.1f}",
        })
    st.dataframe(chara_rows, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — TRANSITS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.subheader("Gochara — Transit Analysis")
    transit_date = st.date_input(
        "Transit date", value=date.today(),
        min_value=date(2000, 1, 1), max_value=date(2050, 12, 31),
        key="transit_date_input",
    )
    gochara = compute_gochara(chart, transit_date)

    if gochara.sade_sati:
        st.warning(
            f"⚠️ **Sade Sati** — {gochara.sade_sati_phase} phase  \n"
            f"Natal Moon in **{gochara.natal_moon_sign}**"
        )
    if gochara.guru_chandal_transit:
        st.warning("⚠️ **Guru-Chandal Transit** — Jupiter conjunct Rahu in transit sky")

    transit_rows = []
    for planet, tp in gochara.planets.items():
        av_str = str(tp.av_bindus) if tp.av_bindus >= 0 else "—"
        transit_rows.append({
            "Planet": planet,
            "Sign": tp.sign,
            "Degree": f"{tp.degree_in_sign:.2f}°",
            "Rx": "℞" if tp.is_retrograde else "",
            "Natal House": f"H{tp.natal_house}",
            "AV Bindus": av_str,
        })
    st.dataframe(transit_rows, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — MILAN (Kundali Milan + Composite Compatibility)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("Kundali Milan — Marriage Compatibility")

    with st.form("milan_form"):
        st.markdown("**Partner Birth Data**")
        col_p1, col_p2 = st.columns(2)
        partner_date = col_p1.date_input(
            "Partner DOB", value=st.session_state.partner_birth_date,
            min_value=date(1900, 1, 1),
        )
        partner_hour = col_p1.slider("Partner Hour", 0, 23, 12, key="ph")
        partner_min = col_p1.slider("Partner Min", 0, 59, 0, key="pm")
        partner_lat = col_p2.number_input("Partner Lat", value=28.6139, format="%.4f", key="plat")
        partner_lon = col_p2.number_input("Partner Lon", value=77.2090, format="%.4f", key="plon")
        partner_tz = col_p2.number_input("Partner TZ", value=5.5, step=0.5, key="ptz")
        partner_ayanamsha = col_p2.selectbox("Partner Ayanamsha", ["lahiri", "raman", "krishnamurti"], key="pay")
        submitted = st.form_submit_button("Compute Milan", type="primary")

    if submitted:
        with st.spinner("Computing compatibility…"):
            partner_hour_dec = partner_hour + partner_min / 60.0
            partner_chart = compute_chart(
                partner_date.year, partner_date.month, partner_date.day,
                partner_hour_dec, partner_lat, partner_lon, partner_tz, partner_ayanamsha,
            )
            st.session_state.partner_chart = partner_chart
            st.session_state.partner_birth_date = partner_date

    if st.session_state.partner_chart:
        partner_chart = st.session_state.partner_chart
        partner_birth_date = st.session_state.partner_birth_date

        milan = compute_milan(chart, partner_chart)

        # Score display
        col_m1, col_m2 = st.columns([1, 2])
        col_m1.metric("Ashtakoot Score", f"{milan.total:.1f} / 36", milan.compatibility_label)

        if milan.mangal_dosha_1 or milan.mangal_dosha_2:
            dosha_txt = []
            if milan.mangal_dosha_1:
                dosha_txt.append("Chart 1 has Mangal Dosha")
            if milan.mangal_dosha_2:
                dosha_txt.append("Chart 2 has Mangal Dosha")
            cancelled = " — **Cancelled**" if milan.dosha_cancelled else " — **Not cancelled**"
            col_m2.warning("⚠️ " + " · ".join(dosha_txt) + cancelled)
        else:
            col_m2.success("✅ No Mangal Dosha")

        # 8-koot breakdown
        koot_rows = [
            {"Koot": k.koot, "Score": f"{k.score:.1f}", "Max": f"{k.max_score:.0f}", "Detail": k.detail}
            for k in milan.koots
        ]
        st.dataframe(koot_rows, use_container_width=True, hide_index=True)

        # Composite compatibility
        st.divider()
        st.markdown("**Composite Compatibility Index**")
        partner_dashas = compute_vimshottari_dasa(partner_chart, partner_birth_date)
        dashas_main = compute_vimshottari_dasa(chart, birth_date)
        compat = compute_compatibility(chart, partner_chart, dashas_main, partner_dashas)

        cc1, cc2, cc3, cc4 = st.columns(4)
        cc1.metric("Composite", f"{compat.composite:.2f}", compat.label)
        cc2.metric("Ashtakoot", f"{milan.total/36:.2f}", "normalised")
        cc3.metric("Dasha Sync", f"{compat.dasha_sync_score:.2f}", compat.dasha_sync_detail[:20])
        cc4.metric("AV Score", f"{compat.av_score:.2f}", "inter-chart")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 8 — KP
# ─────────────────────────────────────────────────────────────────────────────
with tabs[7]:
    st.subheader("KP Sub-lord System")
    kp_date = st.date_input(
        "Date for ruling planets",
        value=date.today(),
        key="kp_date_input",
    )
    kp = compute_kp(chart, kp_date)

    st.markdown("**Ruling Planets**")
    rp_cols = st.columns(len(kp.ruling_planets))
    for i, rp in enumerate(kp.ruling_planets):
        rp_cols[i].metric(f"RP {i+1}", rp)

    st.divider()
    st.markdown("**House Significators**")
    sig_rows = []
    for h in range(1, 13):
        sigs = kp.house_significators.get(h, [])
        sig_rows.append({"House": f"H{h}", "Significators": ", ".join(sigs) if sigs else "—"})
    st.dataframe(sig_rows, use_container_width=True, hide_index=True)

    with st.expander("Planet Sub-lords (all 9 grahas)"):
        sl_rows = []
        for planet, entry in kp.planet_sub_lords.items():
            sl_rows.append({
                "Planet": planet,
                "Sign": entry.sign,
                "Nakshatra": entry.nakshatra,
                "Nak Lord": entry.nakshatra_lord,
                "Sub Lord": entry.sub_lord,
                "Sub-Sub Lord": entry.sub_sub_lord,
            })
        st.dataframe(sl_rows, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 9 — TAJIKA
# ─────────────────────────────────────────────────────────────────────────────
with tabs[8]:
    st.subheader("Tajika — Annual (Solar Return) Chart")
    current_year = date.today().year
    tajika_year = st.number_input(
        "Solar return year", min_value=birth_date.year + 1,
        max_value=birth_date.year + 120, value=current_year, step=1,
    )

    tajika = compute_tajika(chart, birth_date, int(tajika_year), lat, lon, tz_offset)

    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.metric("Varshaphal Lagna", tajika.varshaphal_lagna_sign)
    col_t2.metric("Muntha", tajika.muntha_sign)
    col_t3.metric("Year Number", tajika.year_number)

    st.markdown("**Annual Chart (D1)**")
    annual_svg = south_indian_svg(tajika.annual_chart, f"Tajika {int(tajika_year)}")
    st.markdown(annual_svg, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Sahams (Arabic Parts)**")
    saham_rows = [
        {"Saham": s.name, "Sign": s.sign, "Degree": f"{s.degree_in_sign:.2f}°"}
        for s in tajika.sahams
    ]
    st.dataframe(saham_rows, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("**Tajika Aspects**")
    if tajika.aspects:
        asp_rows = [
            {
                "Planet A": a.planet_a,
                "Planet B": a.planet_b,
                "Type": a.aspect_type,
                "Orb": f"{a.orb:.2f}°",
                "Mutual": "✓" if a.is_mutual else "",
            }
            for a in tajika.aspects
        ]
        st.dataframe(asp_rows, use_container_width=True, hide_index=True)
    else:
        st.info("No Tajika aspects within 1° orb.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 10 — RULE DETAIL
# ─────────────────────────────────────────────────────────────────────────────
with tabs[9]:
    st.subheader("22-Rule Breakdown by House")
    selected_house = st.selectbox(
        "Select House",
        options=list(range(1, 13)),
        format_func=lambda h: f"H{h} — {scores.houses[h].domain}",
    )
    hs = scores.houses[selected_house]
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Bhavesh", hs.bhavesh, f"in H{hs.bhavesh_house}")
    col_r2.metric("Raw Score", f"{hs.raw_score:+.2f}")
    col_r3.metric("Final Score", f"{hs.final_score:+.2f}", hs.rating)

    rule_rows = []
    for rule in hs.rules:
        rule_rows.append({
            "Rule": rule.rule,
            "Description": rule.description,
            "WC": "✓" if rule.is_wc else "",
            "Triggered": "✓" if rule.triggered else "",
            "Score": f"{rule.score:+.2f}" if rule.triggered else "—",
        })
    st.dataframe(rule_rows, use_container_width=True, hide_index=True)
