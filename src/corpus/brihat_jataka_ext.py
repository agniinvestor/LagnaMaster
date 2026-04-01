"""
src/corpus/brihat_jataka_ext.py — Brihat Jataka Extended Rules (S238)

Encodes Varahamihira's Brihat Jataka (6th century CE) planetary nature rules,
unique interpretive principles distinct from BPHS.

Sources:
  Brihat Jataka (Varahamihira) — Chapters 2, 4, 14, 15, 19
  Subrahmanya Sastri translation
  Panditabhushana Sitaram Jha commentary

30 rules total: BJE001-BJE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BRIHAT_JATAKA_EXT_REGISTRY = CorpusRegistry()

_BRIHAT_JATAKA_EXT = [
    # --- Planetary Nature Classification (BJE001-009) ---
    RuleRecord(
        rule_id="BJE001",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira's planetary classification: "
            "Sun (male, Sattwic, Kshatriya, bones, fire element, eastern direction). "
            "Soul (Atma) significator. Governs vitality, ego, authority."
        ),
        confidence=0.92,
        verse="BJ Ch.2 v.1-3",
        tags=["planetary_nature", "sun", "atma", "sattwic", "kshatriya", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE002",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Moon: female, Sattwic/Rajasic, Vaishya, blood/mind, water element, NW direction. "
            "Manas (mind) significator. Governs emotions, mother, public, fluids."
        ),
        confidence=0.92,
        verse="BJ Ch.2 v.4-5",
        tags=["planetary_nature", "moon", "manas", "sattwic", "water", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE003",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Mars: male, Tamasic, Kshatriya, marrow/muscles, fire element, south direction. "
            "Bhratra (brother) significator. Governs courage, conflict, land, fire."
        ),
        confidence=0.92,
        verse="BJ Ch.2 v.6-7",
        tags=["planetary_nature", "mars", "tamasic", "kshatriya", "fire", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE004",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Mercury: neuter/eunuch, mixed (Rajasic/Sattwic), Vaishya/Shudra, skin/speech, "
            "earth element, north direction. Buddhi (intellect) significator."
        ),
        confidence=0.91,
        verse="BJ Ch.2 v.8-9",
        tags=["planetary_nature", "mercury", "buddhi", "rajasic", "earth", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE005",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Jupiter: male, Sattwic, Brahmin, fat/liver, ether/space element, NE direction. "
            "Putra (children) and Jnana (wisdom) significator. Most benefic among grahas."
        ),
        confidence=0.93,
        verse="BJ Ch.2 v.10-11",
        tags=["planetary_nature", "jupiter", "sattwic", "brahmin", "jnana", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE006",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Venus: female/hermaphrodite, Rajasic, Brahmin, semen/vitality, water element, SE direction. "
            "Kalatra (wife/partner) significator. Governs beauty, luxury, pleasure."
        ),
        confidence=0.92,
        verse="BJ Ch.2 v.12-13",
        tags=["planetary_nature", "venus", "rajasic", "brahmin", "kalatra", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE007",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Saturn: neuter/eunuch, Tamasic, Shudra, nerves/tendons, air element, west direction. "
            "Ayu (longevity) and suffering significator. Rules karma, delay, limitation."
        ),
        confidence=0.92,
        verse="BJ Ch.2 v.14-15",
        tags=["planetary_nature", "saturn", "tamasic", "shudra", "ayu", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE008",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Rahu: shadowy/Tamasic, Shudra/outcast, SW direction. "
            "Varahamihira treats Rahu as a malefic shadowy body similar to Saturn "
            "but more sudden and foreign in its effects."
        ),
        confidence=0.87,
        verse="BJ Ch.2 v.16-17",
        tags=["planetary_nature", "rahu", "tamasic", "shadow_planet", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE009",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Ketu: shadowy/Tamasic, Shudra/outcast, NW-SW direction. "
            "Varahamihira treats Ketu as malefic, focused on past karma, "
            "spiritual detachment, and moksha."
        ),
        confidence=0.87,
        verse="BJ Ch.2 v.18-19",
        tags=["planetary_nature", "ketu", "tamasic", "shadow_planet", "moksha", "varahamihira"],
        implemented=False,
    ),
    # --- Brihat Jataka Unique Rules (BJE010-020) ---
    RuleRecord(
        rule_id="BJE010",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira's Hora (half-sign) system: Each 15° half of a sign "
            "is ruled by Sun (first half) or Moon (second half). "
            "Hora of birth planet determines the sex and nature of results."
        ),
        confidence=0.86,
        verse="BJ Ch.4 v.1-3",
        tags=["hora", "half_sign", "sun_hora", "moon_hora", "sex_determination", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE011",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Drekkana (D3) lords: Each sign has 3 decans of 10°. "
            "In Brihat Jataka, decans are ruled by the sign lord in trines: "
            "1st decan = sign lord, 2nd = 5th sign lord, 3rd = 9th sign lord."
        ),
        confidence=0.87,
        verse="BJ Ch.4 v.4-6",
        tags=["drekkana", "d3", "decan_lords", "trine_lords", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE012",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Navamsha lords (Varahamihira system): 9 navamshas per sign, "
            "beginning from Aries for fire signs, Cancer for water signs, "
            "Libra for air signs, Capricorn for earth signs."
        ),
        confidence=0.90,
        verse="BJ Ch.4 v.7-9",
        tags=["navamsha", "d9_lords", "element_based_start", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE013",
        source="Brihat Jataka",
        chapter="Ch.14",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka Yoga: Two or more planets in mutual angular (kendra) "
            "relationship from each other create powerful yogas. "
            "The nature of the yoga depends on the planets involved."
        ),
        confidence=0.85,
        verse="BJ Ch.14 v.1-4",
        tags=["yoga", "mutual_kendra", "angular_relationship", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE014",
        source="Brihat Jataka",
        chapter="Ch.14",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira's Shadbala weightings differ from later sources. "
            "He emphasizes Sthana Bala (positional strength) most highly, "
            "especially for exaltation and own-sign positions."
        ),
        confidence=0.84,
        verse="BJ Ch.14 v.5-8",
        tags=["shadbala", "sthana_bala", "positional_strength", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE015",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka Raja Yoga: Sun and Moon together in a kendra or trikona "
            "from the lagna creates a basic raja yoga. "
            "The sign they occupy modifies the nature of leadership."
        ),
        confidence=0.85,
        verse="BJ Ch.15 v.1-3",
        tags=["raja_yoga", "sun_moon_kendra", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE016",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka Dhana Yoga: Jupiter and Venus in mutual kendra "
            "from lagna, with the 2nd lord strong, creates major wealth yoga. "
            "Both benefics must be well-placed and unafflicted."
        ),
        confidence=0.85,
        verse="BJ Ch.15 v.4-6",
        tags=["dhana_yoga", "jupiter_venus_kendra", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE017",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on Sun-Moon relationship: Full Moon (15th tithi) in a "
            "birth chart gives strong mind and emotional stability. "
            "New Moon (Amavasya) births show difficulty with mother and mental focus."
        ),
        confidence=0.86,
        verse="BJ Ch.15 v.7-9",
        tags=["sun_moon_angle", "full_moon", "new_moon", "paksha_bala", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE018",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka on benefic/malefic classification: "
            "Full Moon, Mercury without malefics, Jupiter, Venus = benefics. "
            "Sun, Saturn, Mars, Rahu, Ketu = malefics. "
            "Waning Moon (Krishna Paksha) = malefic."
        ),
        confidence=0.92,
        verse="BJ Ch.15 v.10-12",
        tags=["benefic_malefic", "classification", "waning_moon", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE019",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on planet gender for chart analysis: "
            "Sun, Mars, Jupiter = male planets. Moon, Venus = female planets. "
            "Saturn, Mercury, Rahu = neuter/eunuch planets. "
            "Gender of 1st/7th lord affects relationship themes."
        ),
        confidence=0.88,
        verse="BJ Ch.15 v.13-15",
        tags=["planet_gender", "male_female_neuter", "relationship", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE020",
        source="Brihat Jataka",
        chapter="Ch.19",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka on Dasha systems: Varahamihira acknowledges multiple "
            "dasha systems but considers planetary Udu Dasha (nakshatra dasha) "
            "most reliable for timing. The Vimshottari system is described in detail."
        ),
        confidence=0.86,
        verse="BJ Ch.19 v.1-4",
        tags=["dasha_system", "udu_dasha", "vimshottari", "timing", "varahamihira"],
        implemented=False,
    ),
    # --- Brihat Jataka Aspect Rules (BJE021-025) ---
    RuleRecord(
        rule_id="BJE021",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira's aspect system: All planets aspect the 7th house "
            "(180° opposition). Saturn additionally aspects 3rd and 10th. "
            "Jupiter additionally aspects 5th and 9th. Mars additionally aspects 4th and 8th."
        ),
        confidence=0.93,
        verse="BJ Ch.4 v.10-12",
        tags=["aspects", "special_aspects", "7th_aspect", "saturn_mars_jupiter", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE022",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka: Aspect strength proportional. "
            "Trine aspects (5th, 9th) are considered '3/4 aspect' by some traditions. "
            "Varahamihira counts the additional aspects as full in strength."
        ),
        confidence=0.84,
        verse="BJ Ch.4 v.13-14",
        tags=["aspects", "aspect_strength", "trine_aspect", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE023",
        source="Brihat Jataka",
        chapter="Ch.4",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Mutual aspects: Two planets in 7th from each other create "
            "a mutual aspect (opposition). This is significant in yogas and "
            "relationship analysis in Brihat Jataka methodology."
        ),
        confidence=0.86,
        verse="BJ Ch.4 v.15-16",
        tags=["aspects", "mutual_aspect", "opposition", "yoga", "varahamihira"],
        implemented=False,
    ),
    # --- Brihat Jataka on Specific Life Events (BJE024-030) ---
    RuleRecord(
        rule_id="BJE024",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Longevity by lagna lord strength (BJ method): "
            "Lagna lord in kendra with benefic aspect = long life (75+ years). "
            "Lagna lord in 6/8/12 with malefics = short life. "
            "Middle life (40-75) when mixed indicators."
        ),
        confidence=0.86,
        verse="BJ Ch.15 v.16-18",
        tags=["longevity", "lagna_lord_kendra", "bj_method", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE025",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on wealth: "
            "Venus and Jupiter in 2nd from lagna = abundant wealth. "
            "Mercury in 2nd = wealth through trade. "
            "Saturn in 2nd = delayed wealth through hard labor."
        ),
        confidence=0.85,
        verse="BJ Ch.15 v.19-21",
        tags=["wealth", "2nd_house", "venus_jupiter", "saturn", "bj_method", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE026",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on education: "
            "Mercury in kendra from lagna = excellent education. "
            "Jupiter in 5th from lagna = scholarly, wise. "
            "Both strong = native becomes teacher or advisor."
        ),
        confidence=0.85,
        verse="BJ Ch.15 v.22-24",
        tags=["education", "mercury_kendra", "jupiter_5th", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE027",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on foreign travel: "
            "Saturn in the 12th from Moon indicates travel to foreign lands. "
            "Rahu in 9th or 12th also indicates foreign connections. "
            "Moon in Sagittarius or 9th activates wanderlust."
        ),
        confidence=0.83,
        verse="BJ Ch.15 v.25-27",
        tags=["foreign_travel", "saturn_12th", "rahu_9th", "moon", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE028",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on imprisonment/confinement: "
            "Saturn in lagna with malefics = long-term confinement or isolation. "
            "Rahu in 1st aspected by Saturn = difficulties through enemies. "
            "12th lord in lagna with Saturn = self-imposed isolation."
        ),
        confidence=0.83,
        verse="BJ Ch.15 v.28-30",
        tags=["imprisonment", "confinement", "saturn_lagna", "rahu", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE029",
        source="Brihat Jataka",
        chapter="Ch.19",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Varahamihira on Antardashas: "
            "The bhukti (sub-period) lord modifies the maha dasha. "
            "Dasha-bhukti lords that are friendly and in kendra/trikona from "
            "each other give positive results; in 6/8/12 relationship give difficulties."
        ),
        confidence=0.87,
        verse="BJ Ch.19 v.5-8",
        tags=["antardasha", "bhukti", "dasha_bhukti_relationship", "timing", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJE030",
        source="Brihat Jataka",
        chapter="Ch.19",
        school="varahamihira",
        category="planetary_nature",
        description=(
            "Brihat Jataka on Pratyantardasha (sub-sub period): "
            "Results are most specific when all three periods (dasha/bhukti/antara) "
            "are significators of the relevant house. "
            "Transit of Moon over the dasha lord's natal position triggers events."
        ),
        confidence=0.85,
        verse="BJ Ch.19 v.9-12",
        tags=["pratyantardasha", "sub_sub_period", "triple_dasha", "timing", "varahamihira"],
        implemented=False,
    ),
]

for _r in _BRIHAT_JATAKA_EXT:
    BRIHAT_JATAKA_EXT_REGISTRY.add(_r)
