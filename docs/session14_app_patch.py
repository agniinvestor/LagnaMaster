"""
Chara Dasha tab patch for src/ui/app.py — Session 14

STEP 1 — Add import:
    from src.calculations.chara_dasha import compute_chara_dasha, current_chara_dasha, atmakaraka_sign

STEP 2 — Add "Chara Dasha" to st.tabs() as tab10

STEP 3 — Add tab body:
    with tab10:
        st.header("Jaimini Chara Dasha")
        if st.session_state.get("chart") and st.session_state.get("birth_date"):
            chart = st.session_state["chart"]
            bd = st.session_state["birth_date"]
            ak, ak_sign = atmakaraka_sign(chart)
            st.info(f"Atmakaraka: **{ak}** in **{ak_sign}**")
            dashas = compute_chara_dasha(chart, bd)
            current = current_chara_dasha(dashas)
            st.metric("Current Chara Dasha", current.sign,
                      delta=f"until {current.end.strftime('%b %Y')}")
            import pandas as pd
            rows = [{"Sign": d.sign, "Start": d.start.strftime("%d %b %Y"),
                     "End": d.end.strftime("%d %b %Y"),
                     "Years": f"{d.years:.1f}",
                     "Planets": ", ".join(d.planets_in_sign) or "—",
                     "Active": "✅" if d.is_current else ""} for d in dashas]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
"""
