# LagnaMaster Session Log
> 2026-03-19 | Sessions 1-14 complete | 312/312 tests

## Summary
| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1-10 | Pilot: ephemeris→panchanga | 222 |
| 11 | Pushkara Navamsha (R21) + Monte Carlo sensitivity | 30 |
| 12 | Kundali Milan — Ashtakoot 36-pt + Mangal Dosha | 25 |
| 13 | PDF Chart Report — reportlab A4 | 15 |
| 14 | Jaimini Chara Dasha — sign-based predictive cycle | 20 |

## Session 14 Details
- src/calculations/chara_dasha.py: compute_chara_dasha(), current_chara_dasha(), atmakaraka_sign()
- K.N.Rao/Iranganti method: years = planets_in_sign + sign_lord_distance, clamped [1,12]
- Odd lagna → forward; Even lagna → backward
- Birth balance from AK degree fraction (AK = highest-degree planet)
- 1947 India: Taurus lagna (even) → Taurus, Aries, Pisces... | AK = Sun (27.989° Cancer)
- tests/test_chara_dasha.py: 20 tests

## Open manual patches (apply to existing files)
- src/scoring.py R21: docs/session11_scoring_r21_patch.py
- src/ui/app.py tab 8 (Sensitivity): docs/session11_ui_sensitivity.py
- src/ui/app.py tab 9 (Kundali Milan): docs/session12_app_patch.py
- src/ui/app.py tab 10 (Chara Dasha): docs/session14_app_patch.py

## Session 15 — Next
- src/calculations/ashtakavarga.py: Kakshya (sub-sign) bindu calculation
- Gochara scoring weighted by AV bindus at transit sign
- tests/test_av_kakshya.py: 15 tests
