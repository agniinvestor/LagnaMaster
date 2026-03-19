# LagnaMaster — Build Plan
> Sessions 1–14 complete | 312/312 tests passing

## Sessions
| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | ephemeris.py | ✅ | 14 |
| 2 | 7 calc modules | ✅ | 36 |
| 3 | scoring + API + db | ✅ | 20 |
| 4 | Streamlit UI | ✅ | 6 |
| 5 | Docker + integration | ✅ | 17 |
| 6 | Vimshottari + SVG | ✅ | 20 |
| 7 | Yogas | ✅ | 14 |
| 8 | Ashtakavarga | ✅ | 26 |
| 9 | Gochara + Sade Sati | ✅ | 29 |
| 10 | Panchanga + D9 | ✅ | 40 |
| 11 | Pushkara Navamsha (R21) + Monte Carlo | ✅ | 30 |
| 12 | Kundali Milan — Ashtakoot 36-pt | ✅ | 25 |
| 13 | PDF Chart Report (reportlab) | ✅ | 15 |
| 14 | Jaimini Chara Dasha | ✅ | 20 |
| 15 | AV Kakshya bindus + Gochara AV-weighted | 🔲 Next | — |
| 16 | Performance benchmark | 🔲 | — |
| 17 | Pre-production cleanup | 🔲 | — |

## Architecture
- src/ephemeris.py
- src/calculations/: dignity, nakshatra, friendship, house_lord, chara_karak,
    narayana_dasa, shadbala, vimshottari_dasa, yogas, ashtakavarga, gochara,
    panchanga, pushkara_navamsha, kundali_milan, chara_dasha
- src/scoring.py — 22 BPHS rules (R21 live: PN → +0.5)
- src/montecarlo.py — ProcessPoolExecutor sensitivity
- src/reports/chart_pdf.py — reportlab A4 PDF export
- src/api/main.py + src/api/models.py — FastAPI
- src/db.py — SQLite immutable inserts
- src/ui/app.py — Streamlit 9-tab UI
- src/ui/chart_visual.py — South Indian SVG
- src/ui/kundali_page.py — Kundali Milan page

## Open manual patches
- src/scoring.py R21: docs/session11_scoring_r21_patch.py
- src/ui/app.py tab 8 (Sensitivity): docs/session11_ui_sensitivity.py
- src/ui/app.py tab 9 (Kundali Milan): docs/session12_app_patch.py
- src/ui/app.py tab 10 (Chara Dasha): docs/session14_app_patch.py
