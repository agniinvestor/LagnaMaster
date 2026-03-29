"""
src/corpus/jataka_parijata_rules.py — Jataka Parijata Rule Encoding (S207)

Vaidyanatha Dikshita's Jataka Parijata (14th century) — extensive work
famous for Raja Yoga combinations, planetary results, and special lagnas.
Often cited alongside BPHS for authority.

All rules: implemented=False (Phase 1 targets)
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

JATAKA_PARIJATA_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord("JP001", "Jataka Parijata", "Ch.6 v.1", "parashari", "yoga",
               "Raja Yoga: kendra lord and trikona lord in conjunction, mutual "
               "aspect, or exchange — one of the strongest combinations for "
               "success, achievement, and status elevation.",
               0.95, verse="Kendrathrikonadhipathyam rajayogakarakam",
               tags=["raja_yoga", "kendra_lord", "trikona_lord"], implemented=False),
    RuleRecord("JP002", "Jataka Parijata", "Ch.6 v.5", "parashari", "yoga",
               "Dhana Yoga: 2nd and 11th lords conjunct or in exchange — "
               "primary combination for wealth accumulation.",
               0.9, tags=["dhana_yoga", "2nd_lord", "11th_lord", "wealth"], implemented=False),
    RuleRecord("JP003", "Jataka Parijata", "Ch.6 v.8", "parashari", "yoga",
               "Viparita Raja Yoga: 6th, 8th, or 12th lord in another dusthana — "
               "malefic results cancel each other; native gains despite obstacles. "
               "Particularly powerful when all three dusthana lords exchange.",
               0.85, tags=["viparita_raja_yoga", "dusthana", "cancellation"], implemented=False),
    RuleRecord("JP004", "Jataka Parijata", "Ch.7 v.1", "parashari", "dignity",
               "Exaltation cancellation (Neecha Bhanga): "
               "(1) lord of debilitation sign in kendra from lagna or Moon, OR "
               "(2) lord of exaltation sign in kendra from lagna or Moon, OR "
               "(3) debilitated planet aspected by its own sign lord.",
               0.9, tags=["neecha_bhanga", "debilitation_cancellation"], implemented=False),
    RuleRecord("JP005", "Jataka Parijata", "Ch.7 v.6", "parashari", "dignity",
               "Vargottama exaltation: planet exalted in D1 AND in exaltation navamsha "
               "in D9 — maximum strength, gives life-defining results in its dasha.",
               0.9, tags=["vargottama", "exaltation", "d9", "navamsha"], implemented=False),
    RuleRecord("JP006", "Jataka Parijata", "Ch.8 v.2", "parashari", "house_quality",
               "Sun in 10th: Dig Bala + career prominence. Career involves government, "
               "authority, or public visibility. Father and career themes aligned.",
               0.85, tags=["sun", "10th_house", "dig_bala", "career"], implemented=False),
    RuleRecord("JP007", "Jataka Parijata", "Ch.8 v.5", "parashari", "house_quality",
               "Jupiter in lagna or trikona — 'Guru in kendra' provides protection and "
               "positive disposition. Native is dharmic, fortunate, and well-regarded.",
               0.9, tags=["jupiter", "lagna", "trikona", "protection"], implemented=False),
    RuleRecord("JP008", "Jataka Parijata", "Ch.9 v.1", "parashari", "yoga",
               "Panchamahapurusha exception: the Mahapurusha yoga planet must be "
               "in its own sign or exaltation AND in a kendra from LAGNA (not just Moon). "
               "Jataka Parijata specifies lagna-only for full yoga strength.",
               0.85, tags=["mahapurusha", "kendra_from_lagna", "clarification"], implemented=False),
    RuleRecord("JP009", "Jataka Parijata", "Ch.9 v.8", "parashari", "house_quality",
               "Venus in 7th — Kalatra Karaka (natural significator of 7th) in its "
               "natural house. Gives beautiful spouse, artistic marriage, sensual pleasure.",
               0.85, tags=["venus", "7th_house", "kalatra_karaka", "spouse"], implemented=False),
    RuleRecord("JP010", "Jataka Parijata", "Ch.10 v.1", "parashari", "yoga",
               "Gajakesari Yoga: Jupiter in kendra from Moon — gives elephant-like "
               "strength, wisdom, and public recognition. One of the most common "
               "and widely cited yogas in classical texts.",
               0.9, tags=["gajakesari", "jupiter", "moon", "kendra"], implemented=False),
    RuleRecord("JP011", "Jataka Parijata", "Ch.10 v.4", "parashari", "yoga",
               "Sakata Yoga: Jupiter in 6th, 8th, or 12th from Moon — "
               "gives alternating periods of rise and fall, instability in life themes. "
               "Cancelled if Jupiter is in kendra from lagna.",
               0.85, tags=["sakata_yoga", "jupiter", "moon", "dusthana"], implemented=False),
    RuleRecord("JP012", "Jataka Parijata", "Ch.11 v.2", "parashari", "timing",
               "Active dasha period intensifies themes of the house occupied by the "
               "dasha lord AND the house it rules. Both must be evaluated.",
               0.85, tags=["dasha_timing", "dasha_lord", "house_occupied"], implemented=False),
    RuleRecord("JP013", "Jataka Parijata", "Ch.12 v.1", "parashari", "special",
               "Hora chart (D2) for wealth: planets in Sun's hora give wealth through "
               "government, authority, and career. Planets in Moon's hora give wealth "
               "through mother, agriculture, liquids, and public.",
               0.8, tags=["hora", "d2", "wealth", "sun_hora", "moon_hora"], implemented=False),
    RuleRecord("JP014", "Jataka Parijata", "Ch.13 v.1", "jaimini", "karak",
               "Chara Karakas: planet at highest degree in chart is Atmakaraka (AK), "
               "second = Amatyakaraka (AmK), third = Bhratrukaraka (BK), "
               "fourth = Matrukaraka (MK), fifth = Putrakaraka (PK), "
               "sixth = Gnatikaraka (GK), seventh = Darakaraka (DK).",
               0.9, tags=["chara_karak", "atmakaraka", "jaimini", "karakas"], implemented=False),
    RuleRecord("JP015", "Jataka Parijata", "Ch.14 v.3", "parashari", "house_quality",
               "8th lord in 8th (Sarpa Yoga): if well-dignified with benefic aspects, "
               "gives longevity, occult knowledge, and inheritance. If afflicted, "
               "serious transformation through loss.",
               0.8, tags=["8th_lord", "8th_house", "sarpa_yoga", "longevity"], implemented=False),
    RuleRecord("JP016", "Jataka Parijata", "Ch.15 v.1", "parashari", "house_quality",
               "Bhagya (9th house) activated when: 9th lord strong, Jupiter strong, "
               "and no malefic in 9th without benefic protection. "
               "All three conditions together = maximum fortune.",
               0.85, tags=["9th_house", "fortune", "bhagya", "jupiter"], implemented=False),
    RuleRecord("JP017", "Jataka Parijata", "Ch.16 v.2", "parashari", "yoga",
               "Chandra-Mangala Yoga: Moon and Mars in conjunction or mutual aspect — "
               "gives strong earning capacity, real estate, and financial drive. "
               "Native earns through initiative and property.",
               0.85, tags=["chandra_mangala", "moon", "mars", "wealth"], implemented=False),
]

for _r in _RULES:
    JATAKA_PARIJATA_REGISTRY.add(_r)
