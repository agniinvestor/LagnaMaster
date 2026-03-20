# LagnaMaster — Programme Plan

## Status: COMPLETE — Sessions 1–48 ✅

~789 tests passing. ENGINE_VERSION = "3.0.0".

---

## Phase 6 — Classical Depth (Sessions 41–48)

### Session 41 — Ishta / Kashta Phala
**File:** `src/calculations/ishta_kashta.py`
- BPHS Ch.27: Ishta = √(Uchcha_Bala × Cheshta_Bala), Kashta = √((60−U)×(60−C))
- Net Sphuta = Ishta − Kashta (range −60 to +60 Virupas)
- All 7 planets. Addresses PVRNR gap: full strength doctrine beyond Shadbala

### Session 42 — Longevity Doctrine
**File:** `src/calculations/longevity.py`
- Three methods: Pindayu (exaltation ratios), Nisargayu (natural years × house weight), Amsayu (D9 dignity)
- Average → Short/Medium/Long span classification
- Balarishta: Moon in dusthana, Lagnesh in dusthana, malefics H1+H8

### Session 43 — Yogini Dasha
**File:** `src/calculations/yogini_dasha.py`
- 8-lord 36-year cycle: Mangala(Moon,1)→Pingala(Sun,2)→Dhanya(Jup,3)→Bhramari(Mars,4)→Bhadrika(Mer,5)→Ulka(Sat,6)→Siddha(Ven,7)→Sankata(Rahu,8)
- Starting Yogini from birth nakshatra mod 8
- Antardashas proportional. current_yogini() for any date.

### Session 44 — Full KP Engine
**File:** `src/calculations/kp_full.py`
- Sub-lord chain: sign lord → nakshatra lord → sub-lord → sub-sub-lord
- Matches REF_KPSubLordTable exactly. India 1947: Lagna Krittika → nak lord Sun ✓
- compute_kp_cusps() for all 12 houses
- kp_ruling_planets() method
- kp_event_promise(): sub-lord signification + ruling planet overlap

### Session 45 — Extended Yoga Library (200+)
**File:** `src/calculations/yogas_extended.py`
- Nabhasa: Rajju/Musala/Nala/Mala/Sarpa + Sankhya (Gola through Veena)
- Chandra: Sunapha/Anapha/Durudhura/Kemadruma/Adhi
- Surya: Vesi/Vasi/Ubhayachari
- Extended Dhana: Lakshmi/Duryoga/Daridra/Mahabhagya
- All with dasha weighting (dormant=0.5×, active=1.0×)

### Session 46 — Special Lagnas
**File:** `src/calculations/special_lagnas.py`
- Hora Lagna (Sun + hour×30°)
- Ghati Lagna (Lagna + hour×37.5°)
- Sree Lagna (Moon distance from Sun + Lagna)
- Indu Lagna (9th lord Indu values mod 12 from Moon)
- Pranapada (Sun + 2×degree_in_sign)

### Session 47 — Full Jaimini System
**File:** `src/calculations/jaimini_full.py`
- AK in Kendra yoga, AK+AmK conjunction yoga
- Karakamsha Gyana Yoga (benefics 5/9 from Karakamsha)
- Arudha 7th quality, Upapada lord strength
- Karakamsha house scoring via Jaimini school weights
- Jaimini longevity: Brahma/Maheshvara/Rudra method
- Pada relationship scoring (6/8 = −1.5×, trine = +1.5×, same sign = +2.0×)

### Session 48 — Empirical Validation Backend
**Files:** `src/calculations/empirica.py`, `src/api/empirica_router.py`
- REF_EmpiricaSchema live: 18-column SQLite event log
- record_event(), get_events(), compute_accuracy()
- Per-rule lift ratios (manifested/fired vs base rate)
- Accuracy by house, event type, Mahadasha
- Three 1947 India seed events (1971 war, 1991 liberalisation, 2001 Parliament attack)
- FastAPI: POST /empirica/events, GET /empirica/events/{id}, GET /empirica/accuracy

---

## Phases 1–5 — see previous PLAN.md entries

---

## Remaining Gaps (out of scope / not encodable)

| Item | Reason |
|------|--------|
| UX_StudentMode | Pedagogical UI — product decision needed |
| API_ProkeralaScript | External API integration |
| "Strong benefic cancels afflictions" rule | Threshold unspecified in classical texts |
| Holistic chart gestalt synthesis | Requires practitioner tacit knowledge |
| Kalachakra Dasha | Highly complex, textual disagreement |
| Full Placidus cusps (KP) | Requires swe.houses('P') — partial implementation |
