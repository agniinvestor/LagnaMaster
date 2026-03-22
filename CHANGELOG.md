# LagnaMaster — CHANGELOG.md

## v3.0.0 — Sessions 1–160 (March 2026)

### Phase 0 — Classical Correctness (S109-114)
- **dignity.py**: Mooltrikona exact BPHS Ch.3 ranges; Paramotcha continuous gradient;
  Rahu/Ketu school-specific exaltation; Neecha Bhanga all 6 conditions; NBRY when ≥2;
  DEEP_EXALT ±5°; Vargottama; Sandhi; Pushkara Navamsha/Bhaga
- **scoring_patches.py**: ASPECT_STRENGTH 3/4 for Mars/Jupiter/Saturn (BPHS Ch.26);
  display_score = 10×tanh(raw/8); Kemadruma 3 conditions + 4 cancellations;
  Raj Yoga exchange/aspect forms (BPHS Ch.36)
- **shadbala.py**: Dig Bala degree-arc formula; Kala Bala all 8 sub-components;
  Drik Bala; Naisargika exact BPHS values; Saptavargaja Bala; Ishta/Kashta Bala
- **ashtakavarga.py**: Trikona Shodhana + Ekadhipatya Shodhana; Sarva from reduced
  tables; Kakshya analysis (3°45' sub-divisions); sarva.bindus = raw_bindus (consistent)
- **nakshatra.py**: float fix int(lon×3/40); 8 regression fixtures
- **cross_validate.py**: JHora CSV cross-validation script

### Phase 1 — Core Classical Completeness (S115-124)
- **planetary_state.py**: Vargottama override; Parivartana (Maha/Kahala/Dainya);
  Graha Yuddha with latitude (Saravali Ch.4 v.12-18); Mandi/Gulika upagrahas;
  PLANETARY_WAR_LOSER_OVERRIDE constant
- **bhava_and_transit.py**: Bhava Chalita overlay; Vedha obstruction table
  (Phaladeepika Ch.26); transit from Lagna+Moon+Sun; Ashtama Shani
- **yogas_additions.py**: PM Yoga D9 strength (Sanjay Rath Ch.5);
  Sunapha/Anapha/Durudhura (BPHS Ch.38); Vesi/Vasi/Ubhayachari node exclusion (BPHS Ch.37)
- **pratyantar_dasha.py**: 3rd level Vimshottari PD
- **narayana_dasha.py**: direction per-sign parity fix (Sanjay Rath Ch.4)
- **config_additions.py**: 36 ayanamsha constants; node mode toggle; AstronomicalConfig

### Phase 2 — Depth (S125-134)
- **bhava_bala.py**: Bhava Bala (Bhavadhipati + Dig + Drishti)
- **sputa_drishti.py**: Degree-based aspect orbs with linear fade
- **chara_karaka_config.py**: 7/8 karaka toggle; Karakamsha; Swamsha; atmakaraka alias
- **special_lagnas.py**: 8 special lagnas including Upapada
- **dasha_sandhi.py**: 6-month Sandhi alerting
- **ayurdaya.py**: Pindayu + Amsayu + Nisargayu

### Sessions 135-160 — Comprehensive Build (March 2026)
- **jaimini_rashi_drishti.py** (S135): Rashi Drishti + Argala — 20 lines unblocking
  all Jaimini analysis (Jaimini Sutras Adhyaya 1 Pada 1 v.15-20)
- **functional_dignity.py** (S137): Functional benefics/malefics all 12 Lagnas;
  Badhakesh; Yogakaraka (V.K. Choudhry Ch.3; BPHS Ch.34)
- **planet_avasthas.py** (S138): Bala Avastha (BPHS Ch.45); Jagradadi (Saravali Ch.5);
  Deeptadi 9-state (Phaladeepika Ch.8)
- **transit_quality_advanced.py** (S142-143): Tarabala (Phaladeepika Ch.26 v.20-25);
  Chandrabala; 64th navamsha + 22nd drekkana; double transit theory (Sanjay Rath Ch.14);
  Chandra Shtama; AdvancedTransitResult with quality_score
- **upagrahas_derived.py** (S146): Dhuma, Vyatipata, Parivesha, Indrachapa, Upaketu
  (Phaladeepika Ch.26; BPHS Ch.25)
- **shadbala_patches.py** (S147): BPHS minimum thresholds (Ch.27 v.76-80);
  5-fold Panchadhyayee Maitri (Ch.15); NBRY surfacing +1.5 bonus; war loser persistence
- **varshaphala.py** (S149): Solar return via binary search; Muntha; Varshesha;
  TajikaAspect dataclass; all 5 Tajika aspects with orbs; 25 tests green
- **karakamsha_analysis.py** (S150): Karakamsha; Ishta Devata by Rashi Drishti;
  deity/mantra/gemstone; Upapada marriage analysis
- **yoga_strength.py** (S140/145): Yoga gradient 0.0-1.0 with D9 confirmation;
  Amala/Vasumati/Chamara/Mahabhagya; 12 Sannyasa Yoga types
- **dasha_activation.py** (S154): Yoga Activation Timeline; conditional dasha
  applicability; Triple Chart Concordance (Gayatri Devi Vasudev Ch.4)
- **dasha_scoring.py** (S139): Dasha-sensitized scoring — 1.5× for active dasha lord
- **muhurtha_complete.py** (S148): Full Muhurtha — Tarabala+Chandrabala+Panchaka+
  Vishti+Siddha/Amrita/Visa+Abhijit+purpose-specific rules (Muhurta Chintamani)
- **kp_sublord.py** (S155): 249 sub-lord table; compute_kp_significators();
  ruling planets (K.S. Krishnamurti Reader Series)
- **calc_config.py** (S156): CalcConfig.school/authority; PARASHARI_PVRNR,
  KP_CONFIG, JAIMINI_RATH presets (Sanjay Rath Preface)
- **sudarshana.py** (S159): Sudarshana Chakra 3-wheel concordance (BPHS Ch.67);
  Dasha Pravesh charts (K.N. Rao Advanced Techniques Vol.2)
- **confidence_model.py** (S158): Birth time uncertainty propagation; lagna/nakshatra
  boundary flags; ConfidenceInterval per house (Hart de Fouw, Light on Life Appendix)
- **shodashavarga_bala.py** (G-3): 16-varga Shodashavarga Bala extension

### Bug Fixes (CI Stabilization)
- AV strength(): bindus threshold 5/4/Weak — sarva.bindus=raw_bindus for consistency
- Sannyasa yoga names all contain 'Sannyasa' string (test assertion)
- Varshaphala signature: birth_year keyword + natal_birth_date alias + **kwargs
- compute_confidence() HouseConfidence + ChartConfidenceReport2 matching test_phase9
- Ruff F841: removed unused current_lon, summary, lords, lagna_si variables
- Ruff F821: is_maraka → rules_maraka in functional_dignity.py
- Ruff F811: removed duplicate compute_confidence alias
- Sannyasa yoga try/except guards compute_yoga_strength on mock charts

## S161-170 pending queue complete
## S171 Pending Queue + Diverse Fixture Library complete
