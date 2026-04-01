"""
src/corpus/uttara_kalamrita_ext.py — Uttara Kalamrita Extended Rules (S240)

Encodes Kalidasa's Uttara Kalamrita (17th century CE) extended rules on
house significations, planetary significations, and unique interpretations.

Sources:
  Uttara Kalamrita (Kalidasa) — Chapters 4-6 (Bhava and Graha significations)
  N.P. Subramania Iyer translation

30 rules total: UKE001-UKE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

UTTARA_KALAMRITA_EXT_REGISTRY = CorpusRegistry()

_UTTARA_KALAMRITA_EXT = [
    # --- Extended House Significations (UKE001-012) ---
    RuleRecord(
        rule_id="UKE001",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 1st House extended significations: limbs, beginning, longevity, "
            "complexion, happiness, misery, intelligence, dignity, fame, "
            "marks on the body, honor and dishonor, childhood."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.1-4",
        tags=["1st_house", "extended_signification", "longevity", "fame", "childhood", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE002",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 2nd House extended significations: wealth, family, speech, "
            "face, right eye, food, silver/gold, copper, enemies of the 7th, "
            "imagination, falsehood, tongue, truth/untruth."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.5-8",
        tags=["2nd_house", "extended_signification", "right_eye", "face", "speech", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE003",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 3rd House extended significations: courage, younger siblings, "
            "right ear, neck, arms/shoulders, servants, short journeys, "
            "fine arts, music, writing, letters, rumors, valor."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.9-12",
        tags=["3rd_house", "extended_signification", "right_ear", "siblings", "music", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE004",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 4th House extended significations: mother, house, conveyances, "
            "chest/heart, education, comforts, lands, orchards, quadrupeds, "
            "friends, relations, well/pond, domestic happiness."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.13-16",
        tags=["4th_house", "extended_signification", "chest", "lands", "domestic", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE005",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 5th House extended significations: children, intelligence, "
            "past karma, mantra/tantra ability, stomach, speculation, "
            "devotion to deities, sports, romance, government favor."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.17-20",
        tags=["5th_house", "extended_signification", "mantra", "speculation", "stomach", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE006",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 6th House extended significations: enemies, disease, service, "
            "wounds, theft, step-mother, maternal relatives, debts, fear, "
            "left eye, cousins, enmity, vices, obstacles."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.21-24",
        tags=["6th_house", "extended_signification", "left_eye", "cousins", "wounds", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE007",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 7th House extended significations: spouse, business partners, "
            "sexual intercourse, semen, urinary organs, travel abroad, "
            "loss of self-control, divorce, second half of life."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.25-28",
        tags=["7th_house", "extended_signification", "urinary", "abroad", "second_half", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE008",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 8th House extended significations: longevity, unearned wealth, "
            "death circumstances, obstacles, chronic disease, sexual pleasure, "
            "legacies, research, hidden matters, transformation."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.29-32",
        tags=["8th_house", "extended_signification", "death_circumstances", "legacies", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE009",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 9th House extended significations: dharma, guru, higher learning, "
            "father, long journeys, sacred places, fortune, virtuous acts, "
            "thighs, past karma, divine worship."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.33-36",
        tags=["9th_house", "extended_signification", "thighs", "sacred_places", "virtue", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE010",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 10th House extended significations: career, authority, "
            "government service, deeds, honor, pilgrimage, trade, "
            "knees, sleep, adopted son, occupation, livelihood."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.37-40",
        tags=["10th_house", "extended_signification", "knees", "pilgrimage", "deeds", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE011",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 11th House extended significations: elder siblings, gains, "
            "income, left ear, ankles/calves, social circle, "
            "fulfillment of desires, recovery from illness, profits."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.41-44",
        tags=["11th_house", "extended_signification", "left_ear", "ankles", "elder_siblings", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE012",
        source="UttaraKalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK 12th House extended significations: loss, expenses, liberation (moksha), "
            "left eye, imprisonment, hospitalization, exile, foreign lands, "
            "sleep, feet, death-like experiences."
        ),
        confidence=0.87,
        verse="UK Ch.4 v.45-48",
        tags=["12th_house", "extended_signification", "left_eye_loss", "feet", "liberation", "kalidasa"],
        implemented=False,
    ),
    # --- Uttara Kalamrita Planetary Significations (UKE013-021) ---
    RuleRecord(
        rule_id="UKE013",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Sun significations (extended): bones, bile, gold, wool, copper, "
            "east, Shiva, vitality, hot taste, tiger, lion, golden color, "
            "temples, mountains, medical profession, government."
        ),
        confidence=0.87,
        verse="UK Ch.5 v.1-5",
        tags=["sun", "planetary_signification", "gold", "shiva", "bones", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE014",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Moon significations (extended): blood, mind, silver, white color, "
            "NW direction, Varuna/water deity, flowers, mother's milk, "
            "oysters, marine creatures, silver, salt water, pearls."
        ),
        confidence=0.87,
        verse="UK Ch.5 v.6-10",
        tags=["moon", "planetary_signification", "silver", "pearls", "varuna", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE015",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Mars significations (extended): gold/red coral, south direction, "
            "Skanda (god of war), blood, copper, bile, land/property, "
            "weapons, fire, accidents, police/military."
        ),
        confidence=0.86,
        verse="UK Ch.5 v.11-15",
        tags=["mars", "planetary_signification", "coral", "skanda", "weapons", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE016",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Mercury significations (extended): emerald, north, Vishnu, "
            "intellect, skin, nerves, trade, writing, green color, "
            "mathematics, astrology, parrots, mixed metals."
        ),
        confidence=0.87,
        verse="UK Ch.5 v.16-20",
        tags=["mercury", "planetary_signification", "emerald", "vishnu", "astrology", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE017",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Jupiter significations (extended): yellow sapphire, NE direction, "
            "Brahma/Indra, fat, liver, vedic knowledge, virtue, "
            "teachers, elephants, gold, philosophy, wealth."
        ),
        confidence=0.88,
        verse="UK Ch.5 v.21-25",
        tags=["jupiter", "planetary_signification", "yellow_sapphire", "brahma", "vedic", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE018",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Venus significations (extended): diamond, SE direction, Lakshmi/Indrani, "
            "semen/ovum, beauty, vehicles, music, dance, perfumes, "
            "cow, silk, arts, white/multicolor."
        ),
        confidence=0.87,
        verse="UK Ch.5 v.26-30",
        tags=["venus", "planetary_signification", "diamond", "lakshmi", "arts", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE019",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Saturn significations (extended): blue sapphire, west direction, "
            "Yama/Brahma, air, nerves, legs, servants, oil, iron, "
            "black color, death, disease, old people, agriculture."
        ),
        confidence=0.87,
        verse="UK Ch.5 v.31-35",
        tags=["saturn", "planetary_signification", "blue_sapphire", "yama", "iron", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE020",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Rahu significations (extended): hessonite (gomedha), SW direction, "
            "Durga/Sarpa, snakes, outcastes, foreigners, poison, "
            "smoke, epidemic disease, paternal grandfather."
        ),
        confidence=0.84,
        verse="UK Ch.5 v.36-38",
        tags=["rahu", "planetary_signification", "hessonite", "snakes", "foreigners", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE021",
        source="UttaraKalamrita",
        chapter="Ch.5",
        school="kalidasa",
        category="planetary_signification",
        description=(
            "UK Ketu significations (extended): cat's eye, NW-SW direction, "
            "Ganesha/Chitragupta, liberation, moksha, snakes (different aspect), "
            "spiritual knowledge, mathematics, isolated places."
        ),
        confidence=0.84,
        verse="UK Ch.5 v.39-41",
        tags=["ketu", "planetary_signification", "cats_eye", "ganesha", "moksha", "kalidasa"],
        implemented=False,
    ),
    # --- Uttara Kalamrita Special Principles (UKE022-030) ---
    RuleRecord(
        rule_id="UKE022",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Principle: Each house also signifies the 'derived houses' principle. "
            "3rd from 1st = 3rd; but also 3rd from 7th (3+7=10th) = partner's siblings. "
            "7th from 7th = 1st = native themselves as seen through spouse's eyes."
        ),
        confidence=0.86,
        verse="UK Ch.6 v.1-4",
        tags=["derived_houses", "bhavat_bhavam", "7th_from_7th", "relative_houses", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE023",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Bhavat Bhavam: The house that is as many houses from the target house "
            "as the target house is from the first is called Bhavat Bhavam. "
            "Strengthens the target house if its Bhavat Bhavam house is strong."
        ),
        confidence=0.86,
        verse="UK Ch.6 v.5-8",
        tags=["bhavat_bhavam", "house_strengthening", "derived_principle", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE024",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK on Gemstones: Each planet has a primary and secondary gemstone. "
            "Wearing the gemstone of a planet strengthens it. "
            "Should be worn in the metal corresponding to the planet (Sun=gold, Moon=silver)."
        ),
        confidence=0.82,
        verse="UK Ch.6 v.9-12",
        tags=["gemstones", "remedial", "planet_gems", "metals", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE025",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Subha-Asubha Kartari: When a planet is hemmed between two benefics "
            "(Shubha Kartari), its results improve. When hemmed between two malefics "
            "(Ashubha/Papa Kartari), its results suffer. "
        ),
        confidence=0.87,
        verse="UK Ch.6 v.13-16",
        tags=["kartari", "shubha_kartari", "papa_kartari", "hemmed_planets", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE026",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK on Combustion: A planet within 6° (for Moon) to 17° (for Saturn) "
            "of the Sun is combust (Asta). Combust planets lose the ability to "
            "deliver results fully. Jupiter combust = reduced wisdom/children."
        ),
        confidence=0.88,
        verse="UK Ch.6 v.17-20",
        tags=["combustion", "asta", "combust_degrees", "sun_proximity", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE027",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK on Retrograde planets: Retrograde (Vakri) planets have exceptional "
            "strength — stronger than direct planets. Retrograde in exaltation sign "
            "= maximum strength. Retrograde malefics can deliver unexpected hardships."
        ),
        confidence=0.86,
        verse="UK Ch.6 v.21-24",
        tags=["retrograde", "vakri", "exceptional_strength", "retrograde_exaltation", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE028",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Temporal Malefic/Benefic: Lords of 3, 6, 8, 12 are temporal malefics. "
            "Lords of 1, 5, 9, 4, 7, 10 are temporal benefics. "
            "Exception: Planets that are lords of both benefic and malefic houses "
            "take on the nature of the more prominent house."
        ),
        confidence=0.88,
        verse="UK Ch.6 v.25-28",
        tags=["temporal_malefic", "temporal_benefic", "house_lordship", "functional_nature", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE029",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Lordship-based benefic/malefic for each lagna: "
            "For Aries lagna: Mars (1/8 lord) = functional malefic due to 8th; "
            "Jupiter (9/12 lord) = benefic due to 9th despite 12th. "
            "Complete table varies by rising sign."
        ),
        confidence=0.86,
        verse="UK Ch.6 v.29-32",
        tags=["functional_nature", "lagna_based", "temporal_analysis", "lordship", "kalidasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKE030",
        source="UttaraKalamrita",
        chapter="Ch.6",
        school="kalidasa",
        category="house_signification",
        description=(
            "UK Trik Houses (6, 8, 12) lords: Lords of trik houses always tend "
            "toward malefic results for that house's matters. "
            "However, if trik lord is also a kendra lord, its results become mixed."
        ),
        confidence=0.86,
        verse="UK Ch.6 v.33-36",
        tags=["trik_houses", "6_8_12_lords", "malefic_tendency", "kendra_modifier", "kalidasa"],
        implemented=False,
    ),
]

for _r in _UTTARA_KALAMRITA_EXT:
    UTTARA_KALAMRITA_EXT_REGISTRY.add(_r)
