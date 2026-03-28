"""
src/corpus/bphs_yogas_basic.py — BPHS Basic Yogas (S222)

Encodes fundamental yoga combinations from BPHS Ch.36-38.
These are the foundational yogas that appear across all Parashari
analysis and several also have KP/Jaimini cross-school counterparts.

Sources:
  BPHS Ch.36 — Pancha Mahapurusha Yoga
  BPHS Ch.37 — Gajakesari and other benefic yogas
  BPHS Ch.38 — General yoga rules

25 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_YOGAS_BASIC_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Pancha Mahapurusha Yogas — BPHS Ch.36 ────────────────────────────────
    RuleRecord(
        rule_id="YB001",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Ruchaka Yoga: Mars in own sign (Aries/Scorpio) or exaltation "
            "(Capricorn) in a kendra (1/4/7/10). Native is courageous, "
            "commanding, long-lived, with reddish complexion. Leader "
            "among warriors."
        ),
        confidence=0.9,
        verse="Ch.36 v.1-4",
        tags=["yoga", "mahapurusha", "mars", "kendra", "ruchaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB002",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Bhadra Yoga: Mercury in own sign (Gemini/Virgo) or exaltation "
            "(Virgo) in a kendra (1/4/7/10). Native is intelligent, eloquent, "
            "long-lived, with well-formed body. Excels in learning."
        ),
        confidence=0.9,
        verse="Ch.36 v.5-8",
        tags=["yoga", "mahapurusha", "mercury", "kendra", "bhadra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB003",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Hamsa Yoga: Jupiter in own sign (Sagittarius/Pisces) or exaltation "
            "(Cancer) in a kendra (1/4/7/10). Native is righteous, devoted, "
            "respected by kings, long-lived. Exceptional wisdom."
        ),
        confidence=0.9,
        verse="Ch.36 v.9-12",
        tags=["yoga", "mahapurusha", "jupiter", "kendra", "hamsa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB004",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Malavya Yoga: Venus in own sign (Taurus/Libra) or exaltation "
            "(Pisces) in a kendra (1/4/7/10). Native is handsome, cultured, "
            "wealthy, long-lived. Expertise in arts and luxury."
        ),
        confidence=0.9,
        verse="Ch.36 v.13-16",
        tags=["yoga", "mahapurusha", "venus", "kendra", "malavya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB005",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Shasha Yoga: Saturn in own sign (Capricorn/Aquarius) or exaltation "
            "(Libra) in a kendra (1/4/7/10). Native is disciplined, authoritative, "
            "long-lived, leader of workers and servants."
        ),
        confidence=0.9,
        verse="Ch.36 v.17-20",
        tags=["yoga", "mahapurusha", "saturn", "kendra", "shasha"],
        implemented=False,
    ),

    # ── Gajakesari and Major Benefic Yogas — BPHS Ch.37 ──────────────────────
    RuleRecord(
        rule_id="YB006",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Gajakesari Yoga: Jupiter in kendra from Moon (or from lagna). "
            "Native is intelligent, virtuous, wealthy, long-lived. Famous "
            "and respected. One of the most powerful benefic yogas."
        ),
        confidence=0.9,
        verse="Ch.37 v.1-4",
        tags=["yoga", "benefic", "jupiter", "moon", "gajakesari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB007",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Adhi Yoga: benefics (Mercury, Jupiter, Venus) in H6, H7, and H8 "
            "from Moon. Native is compassionate, healthy, prosperous, "
            "long-lived. Becomes a king or equivalent."
        ),
        confidence=0.85,
        verse="Ch.37 v.5-8",
        tags=["yoga", "benefic", "moon", "adhi_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB008",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Anapha Yoga: planets in H12 from Moon (Moon not in H1). "
            "Native is well-built, virtuous, famous, enjoys life. "
            "Good health and material comfort."
        ),
        confidence=0.8,
        verse="Ch.37 v.9-12",
        tags=["yoga", "moon_based", "anapha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB009",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Sunapha Yoga: planets in H2 from Moon (not Sun). Native is "
            "self-earned wealth, intelligent, king-like, comfortable. "
            "Financial independence."
        ),
        confidence=0.8,
        verse="Ch.37 v.13-16",
        tags=["yoga", "moon_based", "sunapha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB010",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Durudhara Yoga: planets in both H2 and H12 from Moon (not Sun). "
            "Native is generous, charitable, military success, respected. "
            "Combination of Sunapha and Anapha."
        ),
        confidence=0.8,
        verse="Ch.37 v.17-20",
        tags=["yoga", "moon_based", "durudhara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB011",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Kemadruma Yoga: no planets in H2 or H12 from Moon (not Sun). "
            "Native may lack support, face poverty, mental instability. "
            "Isolated from society; antidote: strong benefic aspect on Moon."
        ),
        confidence=0.8,
        verse="Ch.37 v.21-24",
        tags=["yoga", "moon_based", "kemadruma", "affliction"],
        implemented=False,
    ),

    # ── General Yoga Rules — BPHS Ch.38 ──────────────────────────────────────
    RuleRecord(
        rule_id="YB012",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Neecha Bhanga Raja Yoga: debilitated planet's lord is in kendra "
            "from lagna or Moon, OR lord of the sign where it is exalted is "
            "in kendra. Debilitation is cancelled; exceptional rise results."
        ),
        confidence=0.9,
        verse="Ch.38 v.1-5",
        tags=["yoga", "neecha_bhanga", "debilitation", "cancellation", "raja_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB013",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Exchange yoga (Parivartana): two planets occupy each other's "
            "signs. They effectively strengthen each other and the houses "
            "they rule. Major enhancement of both house themes."
        ),
        confidence=0.9,
        verse="Ch.38 v.6-9",
        tags=["yoga", "parivartana", "exchange", "house_strengthening"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB014",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Viparita Raja Yoga: dusthana lord (6/8/12) in another dusthana "
            "(6/8/12). Obstacles neutralize each other; unexpected rise after "
            "crisis. Most powerful when H8 lord in H12 or H12 lord in H8."
        ),
        confidence=0.85,
        verse="Ch.38 v.10-14",
        tags=["yoga", "viparita_raja_yoga", "dusthana", "unexpected_rise"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB015",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Vesi Yoga: planets (not Moon) in H2 from Sun. Native is truthful, "
            "courageous, wealthy, comfortable in life. Enhances Sun's "
            "significations."
        ),
        confidence=0.8,
        verse="Ch.38 v.15-17",
        tags=["yoga", "sun_based", "vesi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB016",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Vosi Yoga: planets (not Moon) in H12 from Sun. Native is truthful, "
            "learned, lazy (but intellectually capable), moderate wealth. "
            "Complements Vesi."
        ),
        confidence=0.75,
        verse="Ch.38 v.18-20",
        tags=["yoga", "sun_based", "vosi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB017",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Ubhayachari Yoga: planets in both H2 and H12 from Sun. Native "
            "achieves high status, wealth, and fame. Combination of Vesi "
            "and Vosi yoga effects."
        ),
        confidence=0.8,
        verse="Ch.38 v.21-23",
        tags=["yoga", "sun_based", "ubhayachari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB018",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Budha-Aditya Yoga (Nipuna Yoga): Sun and Mercury conjunct. "
            "Native is skilled, learned, respected by scholars, capable "
            "in business or government."
        ),
        confidence=0.85,
        verse="Ch.38 v.24-26",
        tags=["yoga", "sun", "mercury", "conjunction", "budha_aditya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB019",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Chandra-Mangala Yoga: Moon and Mars conjunct or mutual aspect. "
            "Native earns through trade, mother's business, or food-related "
            "fields. Financial drive through emotional intensity."
        ),
        confidence=0.8,
        verse="Ch.38 v.27-29",
        tags=["yoga", "moon", "mars", "conjunction", "chandra_mangala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB020",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Guru-Mangala Yoga: Jupiter and Mars conjunct or mutual aspect. "
            "Native is courageous, learned in dharma, charitable, "
            "long-lived. Excellence in spiritual and physical disciplines."
        ),
        confidence=0.8,
        verse="Ch.38 v.30-32",
        tags=["yoga", "jupiter", "mars", "conjunction", "guru_mangala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB021",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Lakshmi Yoga: Venus in own sign or exaltation AND lord of H9 "
            "in own sign, exaltation, or kendra. Native has exceptional "
            "wealth, beauty, and prosperity."
        ),
        confidence=0.85,
        verse="Ch.38 v.33-35",
        tags=["yoga", "venus", "9th_lord", "lakshmi_yoga", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB022",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Saraswati Yoga: Venus, Mercury, and Jupiter in own signs, "
            "exaltation, or kendra/trikona simultaneously. Native is "
            "supremely learned, artistic, eloquent."
        ),
        confidence=0.85,
        verse="Ch.38 v.36-38",
        tags=["yoga", "venus", "mercury", "jupiter", "saraswati_yoga", "learning"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB023",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Dharma Karma Adhipati Yoga: lord of H9 and lord of H10 conjunct, "
            "in mutual aspect, or exchanged. Native's righteous karma brings "
            "professional success. Powerful raja yoga variant."
        ),
        confidence=0.9,
        verse="Ch.38 v.39-42",
        tags=["yoga", "9th_lord", "10th_lord", "dharma_karma_adhipati", "raja_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB024",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Kahal Yoga: lord of H4 and lord of H10 mutually exchange or "
            "conjunct, AND lord of lagna strong. Native becomes renowned, "
            "courageous, heads an army or large organization."
        ),
        confidence=0.8,
        verse="Ch.38 v.43-45",
        tags=["yoga", "4th_lord", "10th_lord", "kahal_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YB025",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Kahala Yoga (variant): lord of H4 in H10 or lord of H10 in H4 "
            "(bhavat bhavam connection). Strengthens both home and career "
            "simultaneously. Authority in domestic or real-estate fields."
        ),
        confidence=0.75,
        verse="Ch.38 v.46-48",
        tags=["yoga", "4th_lord", "10th_lord", "bhavat_bhavam"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_YOGAS_BASIC_REGISTRY.add(_r)
