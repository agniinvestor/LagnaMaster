"""
src/corpus/uttara_kalamrita_rules.py — Uttara Kalamrita Rule Encoding (S207)

Kalidasa's Uttara Kalamrita — famous for special lagnas, argala, and
detailed timing rules. Complements BPHS with distinctive house lord analysis.

All rules: implemented=False (Phase 1 targets)
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

UTTARA_KALAMRITA_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord("UK001", "Uttara Kalamrita", "Ch.4 v.1", "parashari", "special",
               "Arudha Lagna (AL): the sign as far from lagna lord as it is from lagna. "
               "AL shows the external image and how the world perceives the native.",
               0.9, tags=["arudha", "arudha_lagna", "external_image"], implemented=False),
    RuleRecord("UK002", "Uttara Kalamrita", "Ch.4 v.3", "parashari", "special",
               "Upapada Lagna (UL): Arudha of the 12th house — shows spouse's image "
               "and the marriage partner as experienced externally.",
               0.85, tags=["upapada", "ul", "spouse", "marriage"], implemented=False),
    RuleRecord("UK003", "Uttara Kalamrita", "Ch.4 v.5", "parashari", "house_quality",
               "Bhavat Bhavam: the house that is as far from a house as that house is "
               "from lagna acts as the secondary indicator for the same themes.",
               0.85, tags=["bhavat_bhavam", "secondary_house"], implemented=False),
    RuleRecord("UK004", "Uttara Kalamrita", "Ch.5 v.1", "parashari", "timing",
               "Antardasha (sub-period) results depend on the relationship between "
               "MD lord and AD lord — friends give better results than enemies.",
               0.85, tags=["antardasha", "sub_period", "vimshottari"], implemented=False),
    RuleRecord("UK005", "Uttara Kalamrita", "Ch.5 v.8", "parashari", "timing",
               "Transit of dasha lord over natal Moon, lagna, or 10th house sign "
               "activates the dasha period's primary themes.",
               0.8, tags=["dasha_transit", "timing", "activation"], implemented=False),
    RuleRecord("UK006", "Uttara Kalamrita", "Ch.2 v.1", "parashari", "special",
               "Hora Lagna: lagna that progresses at twice the solar rate. "
               "Used for wealth analysis — planets strong from Hora Lagna give wealth.",
               0.8, tags=["hora_lagna", "wealth", "special_lagna"], implemented=False),
    RuleRecord("UK007", "Uttara Kalamrita", "Ch.2 v.4", "parashari", "special",
               "Ghati Lagna (GL): rises at 5x the solar rate. Shows power and authority. "
               "Strong planets from GL indicate leadership and rajayoga potential.",
               0.8, tags=["ghati_lagna", "power", "authority", "special_lagna"], implemented=False),
    RuleRecord("UK008", "Uttara Kalamrita", "Ch.3 v.1", "parashari", "house_quality",
               "The 11th house from any planet shows the gains that planet brings. "
               "Strong 11th from each planet = that planet gives results easily.",
               0.8, tags=["11th", "gains", "11th_from_planet"], implemented=False),
    RuleRecord("UK009", "Uttara Kalamrita", "Ch.6 v.2", "parashari", "dasha",
               "Planets in mutual trine in D9 (Navamsha) activate each other during "
               "their respective Vimshottari periods — Navamsha trine relationship "
               "gives persistent mutual support.",
               0.8, tags=["navamsha", "d9", "trine", "vimshottari"], implemented=False),
    RuleRecord("UK010", "Uttara Kalamrita", "Ch.7 v.1", "parashari", "yoga",
               "Mahapurusha Yoga: a planet in its own sign or exaltation in a kendra "
               "produces one of five Mahapurusha yogas depending on the planet. "
               "Mars=Ruchaka, Mercury=Bhadra, Jupiter=Hamsa, Venus=Malavya, Saturn=Shasha.",
               0.95, verse="Ruchakadi panchamahapurusha yoga",
               tags=["mahapurusha", "kendra", "exaltation", "own_sign"], implemented=False),
    RuleRecord("UK011", "Uttara Kalamrita", "Ch.7 v.3", "parashari", "yoga",
               "Ruchaka Yoga: Mars in own sign or exaltation in kendra — gives "
               "military ability, courage, physical strength, leadership.",
               0.9, tags=["ruchaka", "mars", "kendra"], implemented=False),
    RuleRecord("UK012", "Uttara Kalamrita", "Ch.7 v.4", "parashari", "yoga",
               "Hamsa Yoga: Jupiter in own sign or exaltation in kendra — gives "
               "spiritual wisdom, righteousness, good fortune, teaching ability.",
               0.9, tags=["hamsa", "jupiter", "kendra"], implemented=False),
    RuleRecord("UK013", "Uttara Kalamrita", "Ch.7 v.5", "parashari", "yoga",
               "Malavya Yoga: Venus in own sign or exaltation in kendra — gives "
               "beauty, artistic talent, luxury, marital happiness.",
               0.9, tags=["malavya", "venus", "kendra"], implemented=False),
    RuleRecord("UK014", "Uttara Kalamrita", "Ch.7 v.6", "parashari", "yoga",
               "Shasha Yoga: Saturn in own sign or exaltation in kendra — gives "
               "discipline, authority over servants and the masses, longevity.",
               0.9, tags=["shasha", "saturn", "kendra"], implemented=False),
    RuleRecord("UK015", "Uttara Kalamrita", "Ch.7 v.2", "parashari", "yoga",
               "Bhadra Yoga: Mercury in own sign or exaltation in kendra — gives "
               "intelligence, eloquence, skill in commerce and communication.",
               0.9, tags=["bhadra", "mercury", "kendra"], implemented=False),
    RuleRecord("UK016", "Uttara Kalamrita", "Ch.8 v.1", "parashari", "timing",
               "Dasha sequence activation: the strongest house-promise fructifies "
               "during the Mahadasha of the planet most strongly connected to it "
               "(either as bhavesh, occupant, or strong aspector).",
               0.85, tags=["dasha_fructification", "timing", "bhavesh"], implemented=False),
    RuleRecord("UK017", "Uttara Kalamrita", "Ch.9 v.2", "parashari", "house_quality",
               "Bhava Madhya (house midpoint): the exact degree midpoint of a house "
               "is stronger than the cusp. Planet near bhava madhya has maximum "
               "influence on house themes.",
               0.8, tags=["bhava_madhya", "house_midpoint", "strength"], implemented=False),
]

for _r in _RULES:
    UTTARA_KALAMRITA_REGISTRY.add(_r)
