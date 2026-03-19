"""
Kundali Milan 9th tab patch for src/ui/app.py — Session 12

STEP 1 — Add import:
    from src.ui.kundali_page import render_kundali_tab

STEP 2 — Extend st.tabs() to 9 tabs:
    tab1,...,tab9 = st.tabs([
        "Chart","Domain Scores","Yogas","Ashtakavarga",
        "Vimshottari Dasha","Transits","Rule Detail",
        "Sensitivity","Kundali Milan 💑",
    ])

STEP 3 — Add at end:
    with tab9:
        render_kundali_tab()
"""
