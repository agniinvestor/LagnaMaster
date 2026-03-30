"""
src/corpus/lal_kitab_rules.py — Lal Kitab Exhaustive (S260)

Exhaustive encoding of Lal Kitab (Red Book) — the unique Urdu/Persian
astrological text by Pt. Roop Chand Joshi (1939-1952 editions).

Lal Kitab features:
- Unique house-based planetary blindness (Andha/blind planets)
- Pakka Ghar (permanent house) for each planet
- Kachcha/Pakka concept (temporary vs permanent house effects)
- Unique remedies (totkas) for each malefic placement
- Debt (Rin) system — 7 types of karmic debt
- Self-planet interactions unique to LK
- Reverse readings (Ulta results for specific placements)

120 rules: LKX001-LKX120.
All: school="lal_kitab", source="LalKitab", implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

LAL_KITAB_RULES_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Pakka Ghar (Permanent Houses) for Each Planet (LKX001-009) ───────────
    RuleRecord(
        rule_id="LKX001",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Sun's Pakka Ghar (permanent house) is the 1st house. "
            "When Sun is in its Pakka Ghar (1st house), it gives full results. "
            "If Sun is elsewhere and 1st house has a malefic → Sun's results are compromised."
        ),
        confidence=0.93,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "sun", "1st_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX002",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Moon's Pakka Ghar is the 4th house. Moon in 4th gives full domestic happiness. "
            "Moon outside 4th while 4th has malefics → mental unrest, property difficulties. "
            "Moon's remedy when afflicted: offer milk to the roots of a Peepal tree."
        ),
        confidence=0.93,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "moon", "4th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX003",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Mars's Pakka Ghar is the 1st and 8th house (dual). "
            "Mars in 1st or 8th gives full strength. Mars in other houses is evaluated "
            "relative to its distance from these permanent positions."
        ),
        confidence=0.91,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "mars", "1st_house", "8th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX004",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Mercury's Pakka Ghar is the 7th house. Mercury in 7th → skilled in business "
            "and communication. Mercury away from 7th while 7th has malefics → "
            "business losses and marital communication problems."
        ),
        confidence=0.91,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "mercury", "7th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX005",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Jupiter's Pakka Ghar is the 2nd and 9th house (dual). "
            "Jupiter in 2nd → family wealth and speech. Jupiter in 9th → dharma, father, luck. "
            "Jupiter elsewhere with 2nd/9th afflicted → financial and fortune problems."
        ),
        confidence=0.92,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "jupiter", "2nd_house", "9th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX006",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Venus's Pakka Ghar is the 7th house (shared with Mercury). "
            "Venus in 7th → luxurious marriage and pleasures. "
            "Some editions give Venus's Pakka Ghar as the 4th house for domestic comforts."
        ),
        confidence=0.89,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "venus", "7th_house", "4th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX007",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Saturn's Pakka Ghar is the 8th and 10th house (dual in LK). "
            "Saturn in 8th → longevity research; in 10th → career discipline. "
            "Saturn in other houses evaluated for its distance from Pakka Ghars."
        ),
        confidence=0.91,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "saturn", "8th_house", "10th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX008",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Rahu's Pakka Ghar is the 12th house. Rahu in 12th → foreign connections, "
            "hidden enemies, spiritual experiences. Rahu elsewhere is like an unsettled guest "
            "and gives unpredictable results."
        ),
        confidence=0.89,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "rahu", "12th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX009",
        source="LalKitab",
        chapter="Pakka_Ghar",
        school="lal_kitab",
        category="pakka_ghar",
        description=(
            "Ketu's Pakka Ghar is the 6th house. Ketu in 6th → spiritual service, "
            "victory over enemies, liberation from debts. Ketu elsewhere → unpredictable "
            "obstacles and karmic complications."
        ),
        confidence=0.89,
        verse="Lal Kitab 1939 Ed., Ch.1",
        tags=["lkx", "pakka_ghar", "ketu", "6th_house", "lal_kitab"],
        implemented=False,
    ),

    # ── Blind (Andha) Planets (LKX010-018) ────────────────────────────────────
    RuleRecord(
        rule_id="LKX010",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Lal Kitab unique: planets become 'blind' (Andha) when they occupy "
            "a house ruled by their enemy. Blind planet cannot see (aspect) or "
            "benefit its own natural significations. Results are blocked or reversed."
        ),
        confidence=0.88,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "blind_planet", "enemy_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX011",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Sun becomes blind in Libra (enemy Saturn's sign) → authority is undermined. "
            "Moon becomes blind in Scorpio (enemy Mars) → mental anxiety and mother issues. "
            "Remedies: Sun blind → avoid using father's money; Moon blind → respect mother."
        ),
        confidence=0.87,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "sun", "moon", "libra", "scorpio", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX012",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Jupiter becomes blind in Capricorn (enemy Saturn's sign) → wisdom is blocked, "
            "children face difficulties, financial blessings are withheld. "
            "Remedy: donate yellow sweets to poor on Thursdays."
        ),
        confidence=0.86,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "jupiter", "capricorn", "saturn", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX013",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Venus becomes blind in Virgo (enemy Mercury's sign) → marital dissatisfaction, "
            "luxury blocked, artistic talent suppressed. "
            "Remedy: respect women; avoid illicit relationships."
        ),
        confidence=0.86,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "venus", "virgo", "mercury", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX014",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Saturn becomes blind in Aries (enemy Mars/Sun's sign) → career stability lost, "
            "discipline collapses, longevity potentially compromised. "
            "Remedy: serve the elderly; give alms on Saturdays."
        ),
        confidence=0.86,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "saturn", "aries", "mars", "career", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX015",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Mars becomes blind in Cancer (enemy Moon's sign) → courage turns to aggression, "
            "property disputes, relationship with mother strained. "
            "Remedy: donate red items; avoid arguments at home."
        ),
        confidence=0.85,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "mars", "cancer", "moon", "property", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX016",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Mercury becomes blind in Sagittarius and Pisces (Jupiter's signs) → "
            "business intelligence lost, communication breaks down, sibling conflicts. "
            "Remedy: do not accept gifts; keep a clean, organized workspace."
        ),
        confidence=0.84,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "mercury", "sagittarius", "pisces", "jupiter", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX017",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Rahu becomes blind in Leo (Sun's sign) → Rahu's illusions become transparent, "
            "foreign schemes fail, hidden plans are exposed. "
            "Ketu becomes blind in Aquarius (Saturn's sign) → spiritual detachment blocked."
        ),
        confidence=0.83,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "rahu", "ketu", "leo", "aquarius", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX018",
        source="LalKitab",
        chapter="Andha_Planets",
        school="lal_kitab",
        category="andha",
        description=(
            "Benefic planets protecting blind planets: if a natural benefic (Jupiter/Venus/Mercury/Moon) "
            "occupies the same house as a blind planet → the blindness is partially lifted. "
            "Two benefics with a blind planet → blindness fully cancelled."
        ),
        confidence=0.82,
        verse="Lal Kitab 1941 Ed., Andha Chapter",
        tags=["lkx", "andha", "benefic_protection", "lal_kitab"],
        implemented=False,
    ),

    # ── Karmic Debt (Rin) System (LKX019-030) ────────────────────────────────
    RuleRecord(
        rule_id="LKX019",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Lal Kitab's Rin (karmic debt) system: 7 types of debt from past lives. "
            "The debt is identified by afflicted house and the planets involved. "
            "Debt must be repaid through appropriate remedies to remove its malefic effects."
        ),
        confidence=0.88,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "karmic_debt", "past_life", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX020",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Father's debt (Pitru Rin): Sun afflicted in 9th or 10th → debt to father or ancestors. "
            "Manifests as: no male heir, sudden financial loss, or father's premature death. "
            "Remedy: perform Pitru Tarpan (ancestral water rituals) on no-moon days."
        ),
        confidence=0.87,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "pitru_rin", "father", "ancestors", "sun", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX021",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Mother's debt (Matru Rin): Moon afflicted in 4th → debt to mother. "
            "Manifests as: property loss, mental disorders, or mother's suffering. "
            "Remedy: offer silver items to Moon deity; donate milk to poor women."
        ),
        confidence=0.86,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "matru_rin", "mother", "moon", "property", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX022",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Sibling debt (Bhai Rin): Mars afflicted in 3rd → debt to siblings. "
            "Manifests as: sibling rivalry, land disputes, accidents. "
            "Remedy: donate blood (blood donation); plant trees near the house."
        ),
        confidence=0.85,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "bhai_rin", "siblings", "mars", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX023",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Spouse debt (Stri Rin): Venus afflicted in 7th → debt to spouse. "
            "Manifests as: marital discord, wife's ill health, loss through women. "
            "Remedy: donate white items on Fridays; respect all women."
        ),
        confidence=0.86,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "stri_rin", "spouse", "venus", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX024",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Children debt (Santan Rin): Jupiter afflicted in 5th → debt to children. "
            "Manifests as: childlessness, loss of children, children's suffering. "
            "Remedy: donate to orphanages; keep gold elephant at home."
        ),
        confidence=0.85,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "santan_rin", "children", "jupiter", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX025",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Government/society debt (Rajya Rin): Saturn afflicted in 10th → "
            "debt to society or government. Manifests as: career obstacles, "
            "legal troubles, reputation damage. Remedy: serve the poor and elderly."
        ),
        confidence=0.85,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "rajya_rin", "career", "saturn", "government", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX026",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Self-incurred debt (Swaya Rin): Rahu and Ketu in 1st/7th or 2nd/8th axis → "
            "self-created karmic debt from this life's actions. "
            "Manifests as: inexplicable reversals of fortune. Remedy: perform self-reflection and atonement."
        ),
        confidence=0.83,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "swaya_rin", "rahu", "ketu", "karma", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX027",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Debt intensification: if the debted planet is also in an enemy house (blind) → "
            "the debt is doubly intensified. Combined debt + blindness requires both "
            "the debt remedy and the blind planet remedy simultaneously."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "andha", "intensification", "remedy", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX028",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Debt repayment timing: Lal Kitab states that karmic debt automatically begins "
            "resolving from age 36 if no action is taken. But if deliberate remedies are applied "
            "in relevant dasha periods, resolution comes earlier."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "timing", "remedy", "age_36", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX029",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Debt cascade: if more than 3 types of debts are active simultaneously → "
            "the native faces severe hardship until all 3+ debts are identified and addressed. "
            "Priority order: Pitru Rin > Matru Rin > others."
        ),
        confidence=0.659,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "cascade", "multiple_debts", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX030",
        source="LalKitab",
        chapter="Rin_Karma",
        school="lal_kitab",
        category="rin_karma",
        description=(
            "Protection from debt: if Jupiter aspects the afflicted house from a kendra → "
            "the debt is held in suspension and does not manifest in this birth. "
            "Called 'Debt suspended by Guru' in LK texts."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Rin Chapter",
        tags=["lkx", "rin_karma", "jupiter", "protection", "debt_suspension", "lal_kitab"],
        implemented=False,
    ),

    # ── Planets in Houses — LK Unique Readings (LKX031-070) ──────────────────
    RuleRecord(
        rule_id="LKX031",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Sun in 1st house (LK): powerful self, government support, good health. "
            "If Sun is alone in 1st → leader. If with malefics → arrogance causes falls. "
            "Remedy when afflicted: donate wheat on Sundays."
        ),
        confidence=0.90,
        verse="Lal Kitab 1939 Ed., Sun Chapter",
        tags=["lkx", "sun", "1st_house", "leadership", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX032",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Sun in 7th house (LK): obstacles in marriage; wife's health suffers. "
            "Business partnerships fail. Sun in 7th is one of LK's most challenging placements. "
            "Remedy: throw copper coins in flowing water; serve the blind."
        ),
        confidence=0.88,
        verse="Lal Kitab 1939 Ed., Sun Chapter",
        tags=["lkx", "sun", "7th_house", "marriage", "obstacles", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX033",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Moon in 1st house (LK): highly intuitive, popular, emotional. "
            "Mother's blessings strong. If Moon is full → excellent. "
            "Waning Moon in 1st → nervous, unstable. Remedy: keep silver items."
        ),
        confidence=0.89,
        verse="Lal Kitab 1939 Ed., Moon Chapter",
        tags=["lkx", "moon", "1st_house", "intuition", "mother", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX034",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Moon in 8th house (LK): Moon's Marana Karaka Sthana in LK too. "
            "Mother's health suffers; native has psychic experiences. "
            "Financial ups and downs. Remedy: offer milk at Shiva temple on Mondays."
        ),
        confidence=0.87,
        verse="Lal Kitab 1939 Ed., Moon Chapter",
        tags=["lkx", "moon", "8th_house", "marana_karaka_sthana", "mother", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX035",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Mars in 1st house (LK): highly energetic, athletic, aggressive. "
            "Good for own business; bad for partnerships. "
            "If Mars is in 1st with Moon → excellent courage; with Saturn → accidents."
        ),
        confidence=0.88,
        verse="Lal Kitab 1939 Ed., Mars Chapter",
        tags=["lkx", "mars", "1st_house", "energy", "courage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX036",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Mars in 4th house (LK): property disputes; mother-son conflict. "
            "Land and vehicle problems. Mars in 4th is a classic LK adverse placement. "
            "Remedy: plant pomegranate tree near home; donate red lentils (masoor dal)."
        ),
        confidence=0.87,
        verse="Lal Kitab 1939 Ed., Mars Chapter",
        tags=["lkx", "mars", "4th_house", "property", "mother", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX037",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Mercury in 1st house (LK): intelligent, quick-witted, business-minded. "
            "Good for education and writing careers. "
            "Mercury with Rahu in 1st → deceptive nature; with Jupiter → scholar."
        ),
        confidence=0.88,
        verse="Lal Kitab 1939 Ed., Mercury Chapter",
        tags=["lkx", "mercury", "1st_house", "intelligence", "business", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX038",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Mercury in 7th house (LK, its Pakka Ghar): business and trade flourish. "
            "Clever spouse. If Mercury is afflicted in 7th → dishonest partner. "
            "LK unique: Mercury in Pakka Ghar gives 'Maha Labhkari' (supreme gain) results."
        ),
        confidence=0.89,
        verse="Lal Kitab 1939 Ed., Mercury Chapter",
        tags=["lkx", "mercury", "7th_house", "pakka_ghar", "business", "wealth", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX039",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Jupiter in 1st house (LK): most auspicious for wisdom, spirituality, and children. "
            "Golden years of life; natural teacher. "
            "Jupiter in 1st in LK is called 'Sone Pe Suhaga' (gold enhanced by borax — the best)."
        ),
        confidence=0.91,
        verse="Lal Kitab 1939 Ed., Jupiter Chapter",
        tags=["lkx", "jupiter", "1st_house", "wisdom", "auspicious", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX040",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Jupiter in 10th house (LK): career success through dharmic means; "
            "often becomes a teacher, judge, or minister. "
            "Jupiter in 10th with Saturn → delayed but ultimate success through perseverance."
        ),
        confidence=0.88,
        verse="Lal Kitab 1939 Ed., Jupiter Chapter",
        tags=["lkx", "jupiter", "10th_house", "career", "dharma", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX041",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Venus in 1st house (LK): beautiful appearance, artistic, enjoys luxury. "
            "Married life generally happy. If Venus is with Rahu in 1st → "
            "excessive pleasures leading to health issues."
        ),
        confidence=0.88,
        verse="Lal Kitab 1939 Ed., Venus Chapter",
        tags=["lkx", "venus", "1st_house", "beauty", "arts", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX042",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Venus in 6th house (LK): Marana Karaka Sthana for Venus in LK. "
            "Marital life severely disturbed; health of spouse suffers. "
            "Remedy: never accept gifts from in-laws; donate white sweets to female relatives."
        ),
        confidence=0.86,
        verse="Lal Kitab 1939 Ed., Venus Chapter",
        tags=["lkx", "venus", "6th_house", "marana_karaka_sthana", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX043",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Saturn in 1st house (LK): disciplined, hardworking, long-lived but lonely. "
            "Father's life shortened. Career comes through labor. "
            "LK unique: Saturn in 1st makes the native a servant of society — blessing in disguise."
        ),
        confidence=0.87,
        verse="Lal Kitab 1939 Ed., Saturn Chapter",
        tags=["lkx", "saturn", "1st_house", "discipline", "longevity", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX044",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Saturn in 7th house (LK): late marriage; spouse is older or of different background. "
            "Business partnerships endure through difficulty. "
            "Saturn in 7th LK: remedy — pour mustard oil on iron object and donate on Saturdays."
        ),
        confidence=0.86,
        verse="Lal Kitab 1939 Ed., Saturn Chapter",
        tags=["lkx", "saturn", "7th_house", "marriage", "delay", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX045",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Rahu in 1st house (LK): unpredictable life; foreign connections; "
            "unusual appearance or behavior. "
            "LK unique: Rahu in 1st while Saturn is in 7th → extreme wealth through unusual means."
        ),
        confidence=0.85,
        verse="Lal Kitab 1939 Ed., Rahu Chapter",
        tags=["lkx", "rahu", "1st_house", "foreign", "unusual", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX046",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Rahu in 5th house (LK): children face obstacles; intellect sharp but unreliable. "
            "Multiple marriages or affairs. Gambling or speculation losses. "
            "Remedy: keep a square piece of silver under the pillow."
        ),
        confidence=0.84,
        verse="Lal Kitab 1939 Ed., Rahu Chapter",
        tags=["lkx", "rahu", "5th_house", "children", "speculation", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX047",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Ketu in 1st house (LK): spiritual, detached, psychic abilities. "
            "Poor health in childhood; mysterious personality. "
            "If Ketu is in 1st with Mars → violent temper with spiritual detachment."
        ),
        confidence=0.84,
        verse="Lal Kitab 1939 Ed., Ketu Chapter",
        tags=["lkx", "ketu", "1st_house", "spiritual", "psychic", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX048",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Ketu in 12th house (LK, Pakka Ghar): liberation, spiritual attainment, "
            "foreign travel for spiritual purposes. "
            "Ketu in 12th is the one placement where Ketu delivers its highest, most auspicious results."
        ),
        confidence=0.87,
        verse="Lal Kitab 1939 Ed., Ketu Chapter",
        tags=["lkx", "ketu", "12th_house", "pakka_ghar", "liberation", "spiritual", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX049",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Sun in 4th house (LK): father issues; domestic environment affected by government. "
            "Property through father but with conflicts. Mother's health affected. "
            "Remedy: throw copper coins in flowing river; donate wheat."
        ),
        confidence=0.85,
        verse="Lal Kitab 1940 Ed., Sun Chapter",
        tags=["lkx", "sun", "4th_house", "father", "property", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX050",
        source="LalKitab",
        chapter="Planets_In_Houses",
        school="lal_kitab",
        category="planets_in_houses",
        description=(
            "Sun in 12th house (LK): expenditures exceed income; foreign journeys. "
            "Government or authority is unhelpful. Father absent or distant. "
            "Remedy: donate gold or wheat to temples; avoid showing off wealth."
        ),
        confidence=0.84,
        verse="Lal Kitab 1940 Ed., Sun Chapter",
        tags=["lkx", "sun", "12th_house", "expenditure", "foreign", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Unique Combinations and Special Rules (LKX051-090) ─────────────────
    RuleRecord(
        rule_id="LKX051",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK unique: if Rahu and Jupiter are both present in a chart, they are enemies. "
            "Rahu-Jupiter in same house → cancels Jupiter's blessings AND Rahu's foreign gains. "
            "Called the 'Guru-Chandal' equivalent in LK."
        ),
        confidence=0.85,
        verse="Lal Kitab 1941 Ed., Special Combos",
        tags=["lkx", "rahu", "jupiter", "guru_chandal", "special_combination", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX052",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Saturn-Jupiter mutual interaction: Saturn in 10th and Jupiter in 2nd → "
            "extraordinary wealth through disciplined career over long period. "
            "This is LK's highest wealth combination (Rajyoga equivalent)."
        ),
        confidence=0.86,
        verse="Lal Kitab 1941 Ed., Special Combos",
        tags=["lkx", "saturn", "jupiter", "wealth", "raja_yoga", "career", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX053",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "Sun-Moon together in LK: if Sun and Moon are in the same house → "
            "Amavasya (new moon) energy — powerful but internally conflicted. "
            "Remedies for both parents required simultaneously."
        ),
        confidence=0.83,
        verse="Lal Kitab 1941 Ed., Special Combos",
        tags=["lkx", "sun", "moon", "amavasya", "parents", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX054",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Mars-Saturn combination: Mars and Saturn in same house → "
            "conflict between energy and discipline. "
            "In 10th house → great career through conflict; in 8th → accident/surgery risk."
        ),
        confidence=0.84,
        verse="Lal Kitab 1941 Ed., Special Combos",
        tags=["lkx", "mars", "saturn", "conflict", "career", "accidents", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX055",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Venus-Mercury combination: Venus and Mercury together → "
            "artistic intelligence, business in beauty/arts. "
            "In 7th → ideal marriage; in 1st → charming, persuasive personality."
        ),
        confidence=0.85,
        verse="Lal Kitab 1941 Ed., Special Combos",
        tags=["lkx", "venus", "mercury", "arts", "business", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX056",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK empty houses (Khali Ghar): an empty house (no planet) takes the results "
            "of the 7th from it. Empty 1st → takes 7th house results. "
            "This is a unique LK concept not found in Parashari."
        ),
        confidence=0.84,
        verse="Lal Kitab 1942 Ed., Empty House Chapter",
        tags=["lkx", "empty_house", "khali_ghar", "7th_house", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX057",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK sleeping planets (Suta Grah): if a planet's natural significator house "
            "has no planet AND is not aspected → that planet is 'sleeping' and "
            "gives delayed results. Wake it with the appropriate remedy."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Suta Grah",
        tags=["lkx", "sleeping_planet", "suta_grah", "delayed_results", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX058",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Rahu-Ketu axis rule: Rahu and Ketu are always 7th from each other (180°). "
            "The house with Rahu is enhanced in material matters; "
            "house with Ketu is enhanced in spiritual/past-life matters."
        ),
        confidence=0.88,
        verse="Lal Kitab 1942 Ed., Rahu-Ketu",
        tags=["lkx", "rahu", "ketu", "axis", "material", "spiritual", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX059",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK planet in 'enemy court' (Dushman Ki Adalat): when a planet sits in a house "
            "where the house lord is its enemy (e.g., Sun in Libra/Saturn's house). "
            "Planet must 'work for the enemy' → gives results opposite to its nature."
        ),
        confidence=0.83,
        verse="Lal Kitab 1942 Ed., Enemy Court",
        tags=["lkx", "enemy_court", "dushman", "reversed_results", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX060",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Kachcha (raw/temporary) vs Pakka (ripe/permanent): "
            "Kachcha results manifest quickly but don't last. "
            "Pakka results take time to develop but are permanent. "
            "Planets in their Pakka Ghar give Pakka results."
        ),
        confidence=0.84,
        verse="Lal Kitab 1943 Ed., Kachcha-Pakka",
        tags=["lkx", "kachcha", "pakka", "temporary", "permanent", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Remedies System (LKX061-090) ──────────────────────────────────────
    RuleRecord(
        rule_id="LKX061",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Sun remedies: donate wheat on Sundays; throw copper coins in water. "
            "Wear gold; respect father and elders. "
            "Avoid cutting trees. Keep a pet — especially a cow."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "sun", "wheat", "copper", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX062",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Moon remedies: offer milk/water to Moon on Mondays. "
            "Keep silver items; respect mother and women. "
            "Avoid taking milk from others for free. Keep a white dog or cow."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "moon", "milk", "silver", "mother", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX063",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Mars remedies: donate red lentils (masoor dal) on Tuesdays. "
            "Feed birds (especially red-colored); plant trees. "
            "Avoid violence; serve brothers. "
            "Wear copper ring or red coral."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "mars", "red_lentils", "copper", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX064",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Mercury remedies: donate green items (moong dal, green vegetables) on Wednesdays. "
            "Keep goat or parrot as pet. "
            "Avoid lying and deception. Wear emerald or green tourmaline."
        ),
        confidence=0.84,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "mercury", "green", "honesty", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX065",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Jupiter remedies: donate yellow items (turmeric, yellow cloth, gold) on Thursdays. "
            "Serve teachers and priests. "
            "Avoid eating meat on Thursdays. Wear yellow sapphire or topaz."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "jupiter", "yellow", "teachers", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX066",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Venus remedies: donate white sweets, sugar, white cloth on Fridays. "
            "Respect women; avoid illicit relationships. "
            "Keep house clean and aesthetically pleasing. Wear diamond or white zircon."
        ),
        confidence=0.84,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "venus", "white", "women", "marriage", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX067",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Saturn remedies: donate black items (sesame/til, black cloth, iron) on Saturdays. "
            "Serve the poor, disabled, and elderly. "
            "Avoid alcohol and meat. Wear blue sapphire or iron ring."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "saturn", "black", "poor", "elderly", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX068",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Rahu remedies: donate barley (jau) on Saturdays or Wednesdays. "
            "Keep coal or lead in the home. "
            "Avoid taking anything for free from in-laws. Wear hessonite (gomedh)."
        ),
        confidence=0.83,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "rahu", "barley", "coal", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX069",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Ketu remedies: donate multicolored blankets on Saturdays. "
            "Feed dogs, especially stray dogs. "
            "Serve at hospitals or orphanages. Wear cat's eye (lehsunia)."
        ),
        confidence=0.83,
        verse="Lal Kitab 1952 Ed., Remedies Ch.",
        tags=["lkx", "remedy", "ketu", "dogs", "service", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX070",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK Totka (instant remedy) principle: a simple physical act that creates "
            "immediate karmic shift. Examples: throwing coins in water, planting trees, "
            "feeding birds. LK is unique in providing these practical, accessible remedies."
        ),
        confidence=0.82,
        verse="Lal Kitab 1952 Ed., Totka Chapter",
        tags=["lkx", "totka", "remedy", "instant_remedy", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX071",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK unique: do NOT perform a remedy that contradicts another planet's placement. "
            "If Sun and Moon are both afflicted, their remedies must be compatible. "
            "Donating milk (Moon remedy) on Sundays contradicts Sun remedy (wheat donation)."
        ),
        confidence=0.80,
        verse="Lal Kitab 1952 Ed., Remedy Conflicts",
        tags=["lkx", "remedy", "conflict", "sun", "moon", "compatibility", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX072",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK water remedy (Jal Pravaah): throwing items in flowing water "
            "removes their associated karma. Copper → Sun karma; Silver → Moon karma; "
            "Iron → Saturn karma; Lead → Rahu karma. Specific rivers add potency."
        ),
        confidence=0.82,
        verse="Lal Kitab 1952 Ed., Jal Chapter",
        tags=["lkx", "remedy", "jal_pravah", "water", "karma", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX073",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK tree planting as remedy: each planet has an associated tree. "
            "Sun → Bel tree. Moon → Coconut. Mars → Pomegranate. "
            "Mercury → Banana. Jupiter → Peepal. Venus → Jasmine. Saturn → Shami tree."
        ),
        confidence=0.83,
        verse="Lal Kitab 1952 Ed., Tree Remedies",
        tags=["lkx", "remedy", "trees", "planting", "planets", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX074",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK food donation remedy: each planet has associated grain. "
            "Sun → wheat. Moon → rice. Mars → red lentils. Mercury → green gram. "
            "Jupiter → chickpeas. Venus → white beans. Saturn → black sesame/urad dal."
        ),
        confidence=0.84,
        verse="Lal Kitab 1952 Ed., Food Remedies",
        tags=["lkx", "remedy", "food_donation", "grain", "planets", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX075",
        source="LalKitab",
        chapter="Remedies",
        school="lal_kitab",
        category="remedy",
        description=(
            "LK animal-related remedy: each planet rules specific animals. "
            "Sun → cow/lion. Moon → white horse. Mars → red rooster. Mercury → goat/parrot. "
            "Jupiter → elephant/yellow bird. Venus → white cow/horse. Saturn → crow/black dog."
        ),
        confidence=0.80,
        verse="Lal Kitab 1952 Ed., Animal Remedies",
        tags=["lkx", "remedy", "animals", "planets", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Age-Based Results and Life Periods (LKX076-090) ───────────────────
    RuleRecord(
        rule_id="LKX076",
        source="LalKitab",
        chapter="Age_Results",
        school="lal_kitab",
        category="timing",
        description=(
            "LK unique timing system: planets have age ranges when they activate. "
            "Sun → age 22; Moon → age 24; Mars → age 28; Mercury → age 32. "
            "These are the ages when each planet's effects peak."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Age Chapter",
        tags=["lkx", "timing", "age", "sun", "moon", "mars", "mercury", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX077",
        source="LalKitab",
        chapter="Age_Results",
        school="lal_kitab",
        category="timing",
        description=(
            "LK planet activation ages (continued): Jupiter → age 16; Venus → age 25; "
            "Saturn → age 36; Rahu → age 42; Ketu → age 48. "
            "Before these ages, the planet's results are incomplete."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Age Chapter",
        tags=["lkx", "timing", "age", "jupiter", "venus", "saturn", "rahu", "ketu", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX078",
        source="LalKitab",
        chapter="Age_Results",
        school="lal_kitab",
        category="timing",
        description=(
            "LK life phases: 0-36 is karma accumulation phase (Sanchit). "
            "36-72 is karma ripening phase (Prarabdha active). "
            "72+ is karma completion phase. Major life changes occur at multiples of 12."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Age Chapter",
        tags=["lkx", "timing", "life_phases", "karma", "age_36", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX079",
        source="LalKitab",
        chapter="Age_Results",
        school="lal_kitab",
        category="timing",
        description=(
            "LK house activation by age: 1st house → birth to age 12. "
            "2nd house → age 12-24. 3rd house → age 24-36. 4th house → age 36-48. "
            "Each house activates for 12-year periods in sequence."
        ),
        confidence=0.658,
        verse="Lal Kitab 1942 Ed., House Timing",
        tags=["lkx", "timing", "houses", "age", "activation", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX080",
        source="LalKitab",
        chapter="Age_Results",
        school="lal_kitab",
        category="timing",
        description=(
            "LK annual predictions (Varshaphala in LK style): "
            "in the year corresponding to a house number (e.g., year 7 → 7th house), "
            "that house's planet and significations are activated. "
            "Afflicted house in that year → problems in that year."
        ),
        confidence=0.658,
        verse="Lal Kitab 1943 Ed., Annual Prediction",
        tags=["lkx", "timing", "annual", "varshaphala", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Special Planetary Principles (LKX081-100) ─────────────────────────
    RuleRecord(
        rule_id="LKX081",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK principle: no planet is inherently malefic or benefic — "
            "it depends entirely on house placement and company. "
            "Even Saturn in its Pakka Ghar (10th) is the best friend of the native."
        ),
        confidence=0.87,
        verse="Lal Kitab 1941 Ed., Principles Ch.",
        tags=["lkx", "benefic_malefic", "saturn", "principles", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX082",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK aspect system: planets don't use traditional Graha Drishti. "
            "Instead, planets affect the houses based on the 'Drishti Bhed' (sight difference) "
            "of LK which is primarily house-based, not degree-based."
        ),
        confidence=0.83,
        verse="Lal Kitab 1941 Ed., Aspect Ch.",
        tags=["lkx", "aspects", "drishti_bhed", "house_based", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX083",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK Kendra principle: planets in kendras (1/4/7/10) give their results "
            "without any delay. Planets in trikonas (5/9) give results through good fortune. "
            "Planets in 3/6/8/12 must work hard to give results."
        ),
        confidence=0.84,
        verse="Lal Kitab 1941 Ed., Kendra Ch.",
        tags=["lkx", "kendra", "trikona", "dusthana", "timing", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX084",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK unique: if a planet's Pakka Ghar house lord is well-placed → "
            "that planet functions like exalted regardless of its sign. "
            "This overrides traditional exaltation/debilitation in LK assessment."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Pakka Ghar Override",
        tags=["lkx", "pakka_ghar", "exaltation", "override", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX085",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK color remedies: each house has a color. 1st → red, 2nd → white, "
            "3rd → yellow, 4th → green, 5th → orange, 6th → mixed, "
            "7th → silver/white, 8th → black, 9th → golden, 10th → blue, "
            "11th → mixed, 12th → white/pink."
        ),
        confidence=0.658,
        verse="Lal Kitab 1952 Ed., Color Chapter",
        tags=["lkx", "colors", "houses", "remedy", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX086",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK number system: each planet has a number. Sun=1, Moon=2, Jupiter=3, "
            "Rahu=4, Mercury=5, Venus=6, Ketu=7, Saturn=8, Mars=9. "
            "House number and planet number matching → direct results."
        ),
        confidence=0.659,
        verse="Lal Kitab 1943 Ed., Number System",
        tags=["lkx", "numbers", "planets", "houses", "numerology", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX087",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK house relationship: houses that are 6-8 from each other are always "
            "in conflict. 1st-8th, 2nd-9th, etc. If planets occupy mutual 6-8 houses → "
            "those planets create problems for each other's significations."
        ),
        confidence=0.81,
        verse="Lal Kitab 1943 Ed., House Conflict",
        tags=["lkx", "house_conflict", "6_8_relationship", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX088",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK 'Karan Ka Kaaran' (cause of the cause): if a planet is afflicting house X, "
            "find what planet afflicted that planet first — that is the root cause. "
            "Remedy the root cause planet, not just the symptom planet."
        ),
        confidence=0.658,
        verse="Lal Kitab 1943 Ed., Root Cause",
        tags=["lkx", "root_cause", "karan_ka_kaaran", "remedy", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX089",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK 'Neend' (sleep) concept: some planets go to sleep in certain houses. "
            "Jupiter sleeps in 3rd house. Venus sleeps in 6th house. Moon sleeps in 8th. "
            "A sleeping planet gives no results until awakened by remedy."
        ),
        confidence=0.659,
        verse="Lal Kitab 1943 Ed., Sleeping Planets",
        tags=["lkx", "sleeping_planet", "neend", "delayed_results", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX090",
        source="LalKitab",
        chapter="Special_Principles",
        school="lal_kitab",
        category="special_principle",
        description=(
            "LK activation by marriage: many planet results activate only after marriage. "
            "Venus results become clear post-marriage. "
            "If the native doesn't marry → Venus's good/bad results are delayed or muted."
        ),
        confidence=0.80,
        verse="Lal Kitab 1943 Ed., Marriage Activation",
        tags=["lkx", "marriage", "activation", "venus", "timing", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Unique House-Specific Principles (LKX091-110) ─────────────────────
    RuleRecord(
        rule_id="LKX091",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 2nd house: wealth, family, and speech but also eyes. "
            "If malefic in 2nd → eye problems and harsh speech. "
            "Jupiter in 2nd (Pakka Ghar) → wealthy family and melodious voice."
        ),
        confidence=0.85,
        verse="Lal Kitab 1939 Ed., 2nd House",
        tags=["lkx", "2nd_house", "wealth", "speech", "eyes", "jupiter", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX092",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 3rd house: courage, siblings, and also writing/communication. "
            "Mars in 3rd → very courageous but fights with siblings. "
            "Mercury in 3rd → writer, journalist, good communicator."
        ),
        confidence=0.84,
        verse="Lal Kitab 1939 Ed., 3rd House",
        tags=["lkx", "3rd_house", "courage", "siblings", "communication", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX093",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 5th house: education, children, and mantra power. "
            "Jupiter in 5th → high education and learned children. "
            "Rahu in 5th → black magic or occult interests; children face obstacles."
        ),
        confidence=0.84,
        verse="Lal Kitab 1939 Ed., 5th House",
        tags=["lkx", "5th_house", "education", "children", "mantra", "rahu", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX094",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 6th house: enemies, disease, and maternal uncle (mama). "
            "Ketu in 6th (Pakka Ghar) → victory over enemies and good health. "
            "Saturn in 6th → chronic illness of the maternal family."
        ),
        confidence=0.83,
        verse="Lal Kitab 1939 Ed., 6th House",
        tags=["lkx", "6th_house", "enemies", "disease", "ketu", "saturn", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX095",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 8th house: longevity, inheritance, and occult. "
            "Saturn in 8th (Pakka Ghar) → very long life. "
            "Mars in 8th → accidents and surgeries; Rahu in 8th → mysterious health issues."
        ),
        confidence=0.85,
        verse="Lal Kitab 1939 Ed., 8th House",
        tags=["lkx", "8th_house", "longevity", "saturn", "mars", "rahu", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX096",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 9th house: father, fortune, religion, and long journeys. "
            "Jupiter in 9th (Pakka Ghar) → religious, fortunate, blessed by father. "
            "Sun in 9th → government job and father's blessings."
        ),
        confidence=0.85,
        verse="Lal Kitab 1939 Ed., 9th House",
        tags=["lkx", "9th_house", "father", "fortune", "religion", "jupiter", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX097",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 11th house: gains, elder siblings, and income. "
            "Jupiter in 11th → gains from children and teachings. "
            "Saturn in 11th → gains come slowly but steadily throughout life."
        ),
        confidence=0.83,
        verse="Lal Kitab 1939 Ed., 11th House",
        tags=["lkx", "11th_house", "gains", "income", "saturn", "jupiter", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX098",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK 12th house: expenditure, losses, and also final liberation. "
            "Rahu in 12th (Pakka Ghar) → foreign earnings; hidden gains. "
            "Ketu in 12th (Pakka Ghar) → moksha, spiritual liberation."
        ),
        confidence=0.84,
        verse="Lal Kitab 1939 Ed., 12th House",
        tags=["lkx", "12th_house", "expenditure", "rahu", "ketu", "liberation", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX099",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK unique: house 2 and house 12 are always 'sharing partners.' "
            "What one gains (2nd) must be balanced by expenditure (12th). "
            "If 2nd is strong but 12th is afflicted → gains but unable to enjoy."
        ),
        confidence=0.80,
        verse="Lal Kitab 1941 Ed., 2nd-12th Balance",
        tags=["lkx", "2nd_house", "12th_house", "balance", "gains_expenditure", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX100",
        source="LalKitab",
        chapter="House_Principles",
        school="lal_kitab",
        category="house_principle",
        description=(
            "LK Lagna uniqueness: Lal Kitab uses an equal-house system starting from "
            "the exact degree of Lagna. Each house is exactly 30 degrees. "
            "This differs from Placidus or Sripati systems used in other traditions."
        ),
        confidence=0.83,
        verse="Lal Kitab 1939 Ed., Lagna Ch.",
        tags=["lkx", "lagna", "equal_house", "house_system", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Synthesis and Philosophy (LKX101-120) ──────────────────────────────
    RuleRecord(
        rule_id="LKX101",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab philosophy: fate is 25% and effort is 75%. "
            "Remedies work because they change the native's behavioral patterns (karma). "
            "No remedy works without sincere intent to change."
        ),
        confidence=0.85,
        verse="Lal Kitab 1952 Ed., Philosophy Ch.",
        tags=["lkx", "philosophy", "karma", "fate", "effort", "remedies", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX102",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab unique: the astrologer must examine the native's hands "
            "(palmistry) alongside the birth chart. Hand lines confirm or contradict "
            "planetary positions. LK integrates palmistry and astrology uniquely."
        ),
        confidence=0.82,
        verse="Lal Kitab 1939 Ed., Introduction",
        tags=["lkx", "palmistry", "hand_lines", "integration", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX103",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab's remedy effectiveness timeline: some remedies give results "
            "in 40 days (Chaliha), some in 1 year, some require 3-5 years of consistent practice. "
            "Chaliha (40-day intensive) is the most powerful LK remedy format."
        ),
        confidence=0.80,
        verse="Lal Kitab 1952 Ed., Remedy Duration",
        tags=["lkx", "remedy", "chaliha", "40_days", "timing", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX104",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab: remedies must not be shared with others. "
            "The remedy is personal and loses power if disclosed or replicated by others. "
            "This maintains the remedy's karmic specificity to the native."
        ),
        confidence=0.658,
        verse="Lal Kitab 1952 Ed., Remedy Secrecy",
        tags=["lkx", "remedy", "secrecy", "personal", "karma", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX105",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab origin: written in Urdu and Persian script by Pt. Roop Chand Joshi "
            "(Punjab, India) across 5 editions: 1939, 1940, 1941, 1942, 1952. "
            "The 1952 edition is considered the most complete."
        ),
        confidence=0.88,
        verse="Lal Kitab Historical Introduction",
        tags=["lkx", "history", "roop_chand_joshi", "1952_edition", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX106",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab unique chart format: uses the North Indian Diamond (square) chart. "
            "Houses are fixed (Bhava chart) with Lagna always in house 1. "
            "Signs rotate but houses are fixed — opposite to other Parashari systems."
        ),
        confidence=0.85,
        verse="Lal Kitab 1939 Ed., Chart Format",
        tags=["lkx", "chart_format", "north_indian", "bhava", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX107",
        source="LalKitab",
        chapter="Philosophy",
        school="lal_kitab",
        category="philosophy",
        description=(
            "Lal Kitab: the human body is a microcosm of the solar system. "
            "1st house = head (Sun). 2nd = face (Moon). 3rd = arms (Mars). "
            "4th = chest/lungs (Mercury). 5th = stomach (Jupiter). "
            "6th = digestive system (Saturn). 7th = kidneys/lower back (Venus)."
        ),
        confidence=0.80,
        verse="Lal Kitab 1941 Ed., Body-House Correspondence",
        tags=["lkx", "body_parts", "houses", "medical", "microcosm", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX108",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Shadashtak (6-8) relationships between planets: "
            "Sun-Saturn are natural 6-8 enemies (Leo-Capricorn, 6 apart). "
            "When Sun and Saturn are in mutual 6-8 houses → "
            "father-son conflict; career vs. soul tension."
        ),
        confidence=0.83,
        verse="Lal Kitab 1941 Ed., Shadashtak",
        tags=["lkx", "shadashtak", "sun", "saturn", "conflict", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX109",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Dig Bala equivalent: planets have directional strength based on house. "
            "Sun and Mars strong in 10th (South). Saturn in 7th (West). "
            "Jupiter and Mercury in Lagna (East). Venus and Moon in 4th (North)."
        ),
        confidence=0.81,
        verse="Lal Kitab 1942 Ed., Directional Strength",
        tags=["lkx", "dig_bala", "directional_strength", "planets", "houses", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX110",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Jupiter-Venus mutual aspect rule: if Jupiter and Venus are in "
            "mutual 7th from each other → Lakshmi-Vishnu yoga — extreme prosperity. "
            "If they are also in kendras from Lagna → universal blessing (Sarva Sukha Yoga)."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Jupiter-Venus",
        tags=["lkx", "jupiter", "venus", "lakshmi_vishnu", "prosperity", "yoga", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX111",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Moon-Saturn combination: Moon and Saturn in same house → "
            "Vish (poison) Yoga. Mental depression and dark moods throughout life. "
            "Remedy: offer black sesame seeds with water to the Sun every morning."
        ),
        confidence=0.84,
        verse="Lal Kitab 1941 Ed., Moon-Saturn",
        tags=["lkx", "moon", "saturn", "vish_yoga", "depression", "mental", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX112",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK Sun-Jupiter mutual 7th: when Sun is in 1st and Jupiter is in 7th → "
            "great authority combined with wisdom. Called 'Raj-Guru Yoga' in LK. "
            "Native becomes an adviser to people in power."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Sun-Jupiter",
        tags=["lkx", "sun", "jupiter", "raj_guru_yoga", "authority", "wisdom", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX113",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK all-malefic chart warning: if only malefics (Saturn, Mars, Rahu, Ketu, Sun) "
            "are in the chart with no benefic, extreme difficulties throughout life. "
            "However, such a native often becomes a great reformer or social revolutionary."
        ),
        confidence=0.80,
        verse="Lal Kitab 1943 Ed., All Malefic",
        tags=["lkx", "malefics", "difficult_life", "reformer", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX114",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK 3-planet combination in one house: when 3 or more planets occupy the same house → "
            "that house's results are amplified to the extreme. "
            "Benefics together → extraordinary luck; malefics together → severe suffering in that area."
        ),
        confidence=0.82,
        verse="Lal Kitab 1942 Ed., Multiple Planets",
        tags=["lkx", "stellium", "multiple_planets", "amplification", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX115",
        source="LalKitab",
        chapter="Special_Combinations",
        school="lal_kitab",
        category="special_combination",
        description=(
            "LK unique Saturn rules: Saturn in 1st and 7th simultaneously (impossible) vs. "
            "Saturn aspecting 7th from 1st → marriage to someone with Saturn traits. "
            "Saturn in 10th and its Pakka Ghar → lifelong career success through hard work."
        ),
        confidence=0.81,
        verse="Lal Kitab 1942 Ed., Saturn Special",
        tags=["lkx", "saturn", "1st_house", "7th_house", "10th_house", "marriage", "lal_kitab"],
        implemented=False,
    ),

    # ── LK Final Rules and Synthesis (LKX116-120) ─────────────────────────────
    RuleRecord(
        rule_id="LKX116",
        source="LalKitab",
        chapter="Synthesis",
        school="lal_kitab",
        category="synthesis",
        description=(
            "Lal Kitab synthesis: read chart from multiple 'Lagna' points. "
            "Primary → Lagna. Secondary → Moon as Lagna. Tertiary → Sun as Lagna. "
            "A prediction confirmed by all three Lagna readings → certain event."
        ),
        confidence=0.83,
        verse="Lal Kitab 1952 Ed., Synthesis",
        tags=["lkx", "synthesis", "lagna", "moon_lagna", "sun_lagna", "verification", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX117",
        source="LalKitab",
        chapter="Synthesis",
        school="lal_kitab",
        category="synthesis",
        description=(
            "Lal Kitab concluding principle: astrology is for improvement, not fatalism. "
            "Every chart has both good and bad; the astrologer's duty is to enhance good "
            "and mitigate bad through correct remedies and behavioral guidance."
        ),
        confidence=0.87,
        verse="Lal Kitab 1952 Ed., Conclusion",
        tags=["lkx", "philosophy", "improvement", "remedies", "astrology", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX118",
        source="LalKitab",
        chapter="Synthesis",
        school="lal_kitab",
        category="synthesis",
        description=(
            "LK Rahu-Saturn axis power: when Rahu is in 1st and Saturn in 7th (or vice versa) → "
            "extreme wealth potential but also extreme legal/health risks. "
            "Called 'Raj-Fakar Yoga' (royal poverty yoga) — goes between extremes."
        ),
        confidence=0.80,
        verse="Lal Kitab 1942 Ed., Rahu-Saturn",
        tags=["lkx", "rahu", "saturn", "raj_fakar_yoga", "wealth", "extremes", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX119",
        source="LalKitab",
        chapter="Synthesis",
        school="lal_kitab",
        category="synthesis",
        description=(
            "LK Mars-Jupiter in mutual kendras: if Mars and Jupiter are in 1-4-7-10 axis → "
            "tremendous energy combined with wisdom → military or legal leadership. "
            "Named 'Mahavir Yoga' in LK tradition."
        ),
        confidence=0.81,
        verse="Lal Kitab 1942 Ed., Mars-Jupiter",
        tags=["lkx", "mars", "jupiter", "mahavir_yoga", "leadership", "yoga", "lal_kitab"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LKX120",
        source="LalKitab",
        chapter="Synthesis",
        school="lal_kitab",
        category="synthesis",
        description=(
            "Lal Kitab's final teaching: the book itself (Lal Kitab) is a remedy. "
            "Keeping the book at home, reading it, and applying its principles "
            "purifies karmic debts simply through the act of study and application."
        ),
        confidence=0.80,
        verse="Lal Kitab 1952 Ed., Final Words",
        tags=["lkx", "philosophy", "book_as_remedy", "karma", "study", "lal_kitab"],
        implemented=False,
    ),
]

for rule in _RULES:
    LAL_KITAB_RULES_REGISTRY.add(rule)
