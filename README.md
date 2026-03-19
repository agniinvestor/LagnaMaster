# LagnaMaster

Vedic Jyotish birth chart scoring platform — full workbook parity (Phase 5).

**![CI](https://github.com/agniinvestor/LagnaMaster/actions/workflows/ci.yml/badge.svg) ~900 tests passing | Sessions 1–40 complete**

## The Life Pressure Index

Full 7-layer synthesis (D1×35% + CL×15% + SL×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%):

```python
from src.calculations.scoring_v3 import score_chart_v3

result = score_chart_v3(chart, dashas, on_date=date.today(), school="parashari")
print(result.summary())

# Per-house full index
for h, hl in result.lpi.houses.items():
    print(f"H{h}: {hl.full_index:+.2f} [{hl.rag}] {hl.confidence} confidence")

# Domain balance
print(result.lpi.domain_balance)  # {Dharma: -0.71, Artha: -0.63, ...}

# Scenario explorer
from src.calculations.scenario import compare_scenarios
scenarios = [("Sun to Leo", {"Sun": {"longitude": 120.0}})]
compare_scenarios(chart, scenarios, dashas)
```

## Coverage vs workbook

| Section | Status |
|---------|--------|
| D1 scoring (R01–R23) | ✅ Complete |
| Chandra/Surya/D9/D10/Karakamsha axes | ✅ Complete |
| 7-layer Life Pressure Index | ✅ Complete |
| Rule interaction engine (30 pairs) | ✅ Complete |
| All 12 Arudha Padas | ✅ Complete |
| Vimshopaka Bala (16 vargas) | ✅ Complete |
| D60 Shastiamsha (60 names) | ✅ Complete |
| Raja + Dhana Yogas | ✅ Complete |
| Viparita + Neecha Bhanga Yogas | ✅ Complete |
| Rasi Drishti (12×12) | ✅ Complete |
| Bhavat Bhavam | ✅ Complete |
| Baaladi avastha (corrected) | ✅ Fixed |
| Sayanadi avastha (12 states) | ✅ Complete |
| Narrative report generator | ✅ Complete |
| Scenario / counterfactual explorer | ✅ Complete |
| Scoring Engine v3 (all layers) | ✅ Complete |
