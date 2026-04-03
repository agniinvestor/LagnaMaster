"""src/corpus/bphs_1b_houses_3.py — S308: BPHS Ch.20-23 Phase 1B Re-encode.

BPHS0800–BPHS_NNN (rule count determined by source text).
Phase: 1B_matrix + 1B_conditional + 1B_compound | Source: BPHS | School: parashari

Chapters:
  Ch.20 — Dharma Bhava (9th House): fortune, father, dharma, luck
  Ch.21 — Karma Bhava (10th House): career, profession, fame, deeds
  Ch.22 — Labha Bhava (11th House): gains, income, fulfillment
  Ch.23 — Vyaya Bhava (12th House): expenses, loss, emancipation, foreign

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications.
Pages: 172-189.

Modifier protocol (Option B — locked in S306):
  primary_condition = simplest atomic placement
  modifiers = verse-stated conditions that CHANGE the outcome
  Zero redundancy. Dignity/aspect modifiers split into separate rules.

Confidence formula (Phase 1B mechanical):
  base = 0.60 + 0.05 (verse_ref) = 0.65 minimum
  + 0.08 per concordance text
  - 0.05 per divergence text
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 20 — Effects of the 9th House (Dharma Bhava Phala)
# Santhanam Vol 1, pp.172-178. 32 slokas, ~20 predictive groups.
# Topics: fortune, father's welfare, devotion, dharma, begging.
# ═══════════════════════════════════════════════════════════════════════════════

_CH20_DATA = [
    # ── Slokas 1-2: Combinations for fortune ────────────────────────────────
    # v.1: 9th lord strong in 9th = fortunate/affluent.
    ("h9_lord", "lordship_placement", [9],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["bphs", "parashari", "h9_lord", "own_house", "fortune", "dharma"],
     "Ch.20 v.1",
     "9th lord with strength in the 9th house: the native is fortunate and "
     "affluent. The Bhagya-sthana (house of fortune) is fully activated when "
     "its lord occupies it with strength. Wealth accumulation, dharmic "
     "inclination, and father's prosperity are all indicated",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    # v.2: Jupiter in 9th + 9th lord in angle + ascendant lord strong.
    ("jupiter", "house_placement", [9],
     [{"condition": "h9_lord_in_kendra", "effect": "amplifies", "strength": "strong"},
      {"condition": "ascendant_lord_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     ["bphs", "parashari", "jupiter", "h9", "fortune", "triple_condition"],
     "Ch.20 v.2",
     "Jupiter in the 9th while the 9th lord is in a kendra and the ascendant "
     "lord is endowed with strength: the native is extremely fortunate. This "
     "triple combination of karaka, lord, and lagna lord produces the highest "
     "grade of fortune — wealth, fame, and dharmic success",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 3: Fortunate (affluent) father ────────────────────────────────
    # v.3: 9th lord with strength + Venus in 9th + Jupiter in angle = father fortunate.
    ("h9_lord", "lordship_aspect_condition", "h9_lord_venus_jupiter_compound",
     [{"condition": "venus_in_9th", "effect": "amplifies", "strength": "moderate"},
      {"condition": "jupiter_in_kendra_from_ascendant", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h9_lord", "venus", "jupiter", "father_fortune"],
     "Ch.20 v.3",
     "9th lord with strength as Venus is in the 9th and Jupiter is in a "
     "kendra from the ascendant: the native's father is fortunate and affluent. "
     "Venus and Jupiter together supporting the 9th house ensure the father "
     "enjoys wealth and status throughout life",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 4: Indigent father ────────────────────────────────────────────
    # v.4: 9th lord debilitated + Mars in 2nd/4th from 9th = father poor.
    ("h9_lord", "lordship_dignity_condition", "h9_lord_any_house",
     [{"condition": "debilitated", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "h9_lord", "debilitated", "father_poverty"],
     "Ch.20 v.4a",
     "9th lord in debilitation: poverty of wealth for the father. The "
     "debilitated 9th lord cannot protect father's finances. Even if there "
     "is some wealth, Mars in the 10th or 12th from ascendant (not in own "
     "house or exaltation) will cause the native to disinherit patrimony "
     "or enter into litigations over property",
     ["Saravali"],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),
    # Mars in 10th/12th (2nd/4th from 9th) making patrimony inaccessible.
    ("mars", "house_placement", [10, 12],
     [{"condition": "not_in_own_or_exaltation", "effect": "conditionalizes", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["wealth", "enemies_litigation"],
     ["bphs", "parashari", "mars", "h10", "h12", "patrimony_loss"],
     "Ch.20 v.4b",
     "Mars in the 10th or 12th (i.e., 2nd or 4th from the 9th house) and "
     "not in own house or exaltation: patrimony will not come to the hands "
     "of the native easily. Litigations over father's property, or the "
     "father disinherits the native. Conflict between generations over wealth",
     [],
     "",
     [], [],
     ["if_mars_in_own_or_exaltation"],
    ),

    # ── Sloka 5: Long-living father ─────────────────────────────────────────
    # v.5: 9th lord in deep exaltation + Venus in angle + Jupiter in 9th from D9 asc.
    ("h9_lord", "lordship_dignity_condition", "h9_lord_any_house",
     [{"condition": "in_deep_exaltation", "effect": "amplifies", "strength": "strong"},
      {"condition": "venus_in_kendra", "effect": "amplifies", "strength": "moderate"},
      {"condition": "jupiter_9th_from_navamsa_ascendant", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "h9_lord", "exalted", "father_longevity"],
     "Ch.20 v.5",
     "9th lord in deep exaltation while Venus is in an angle from the "
     "ascendant and Jupiter is in the 9th from Navamsa ascendant: the "
     "father of the native will enjoy a long span of life. Three-factor "
     "protection — exalted lord, benefic kendra, and D9 confirmation",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 6: Royal status for father ────────────────────────────────────
    # v.6: 9th lord in angle + aspect to Jupiter = father like king.
    ("h9_lord", "lordship_placement", [1, 4, 7, 10],
     [{"condition": "aspecting_or_aspected_by_jupiter", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["career_status", "wealth"],
     ["bphs", "parashari", "h9_lord", "kendra", "jupiter", "father_royal"],
     "Ch.20 v.6",
     "9th lord in a kendra in aspect to Jupiter: the native's father will "
     "be a king or equal to a king, endowed with conveyances and authority. "
     "The kendra placement gives the lord directional strength while "
     "Jupiter's aspect confers dignity, status, and material prosperity",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 7: Wealthy and famous father ──────────────────────────────────
    # v.7: 9th lord in 10th + 10th lord aspected by benefic.
    ("h9_lord", "lordship_placement", [10],
     [{"condition": "h10_lord_aspected_by_benefic", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["bphs", "parashari", "h9_lord", "h10", "father_wealthy_famous"],
     "Ch.20 v.7",
     "9th lord in the 10th while the 10th lord is aspected by a benefic: "
     "the native's father will be very rich and famous. The 9th-10th "
     "connection (dharma-karma adhipati yoga) elevates the father's status "
     "and the benefic aspect ensures lasting prosperity",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 8-9: Virtuous and devoted to father ─────────────────────────
    # v.8-9a: Sun in deep exaltation as 9th lord in 11th.
    ("sun", "house_placement", [11],
     [{"condition": "sun_as_h9_lord_in_deep_exaltation", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["character_temperament", "spirituality"],
     ["bphs", "parashari", "sun", "h11", "h9_lord", "virtuous", "devoted"],
     "Ch.20 v.8-9a",
     "Sun in deep exaltation as the 9th lord placed in the 11th: the "
     "native will be virtuous, dear to king and devoted to father. The "
     "exalted Sun as 9th lord in the 11th (3rd from 9th) gives moral "
     "character and filial devotion alongside gains from authority figures",
     [],
     "",
     [], [],
     [],
    ),
    # v.9b: Sun in trine + 9th lord in 7th + conjunction/aspect to Jupiter.
    ("h9_lord", "lordship_placement", [7],
     [{"condition": "sun_in_trine_from_ascendant", "effect": "amplifies", "strength": "moderate"},
      {"condition": "conjunct_or_aspected_by_jupiter", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["bphs", "parashari", "h9_lord", "h7", "sun", "jupiter", "devoted"],
     "Ch.20 v.9b",
     "Sun in a trine from the ascendant while the 9th lord is in the "
     "7th in conjunction with or in aspect to Jupiter: the native will "
     "be devoted to his father. Jupiter's aspect on the 9th lord ensures "
     "a dharmic relationship with the father",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 10: Fortunes, conveyances, fame ──────────────────────────────
    # v.10: 9th lord in 2nd + 2nd lord in 9th = fortune at age 32.
    ("h9_lord", "lordship_placement", [2],
     [{"condition": "h2_lord_in_9th_exchange", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth", "property_vehicles", "fame_reputation"],
     ["bphs", "parashari", "h9_lord", "h2", "exchange", "fortune_timing"],
     "Ch.20 v.10",
     "9th lord in the 2nd while the 2nd lord is in the 9th: acquisition "
     "of fortunes, conveyances, and fame will follow in the 32nd year of "
     "age. This parivartana between houses of wealth (2nd) and fortune "
     "(9th) manifests at a specific timing point",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 11: Inimical to father ────────────────────────────────────────
    # v.11: Ascendant lord in 9th + lord of 6th in 9th.
    ("lagna_lord", "lordship_placement", [9],
     [{"condition": "h6_lord_also_in_9th", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "lagna_lord", "h9", "h6_lord", "father_enmity"],
     "Ch.20 v.11",
     "Ascendant lord in the 9th but with the lord of the 6th also in "
     "the 9th: mutual enmity between the father and the native. The "
     "father's disposition will be contemptible. The 6th lord pollutes "
     "the 9th house with hostility, turning the dharma-sthana into a "
     "battlefield between parent and child",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 12: Begged food ───────────────────────────────────────────────
    # v.12: 10th lord + 3rd lord bereft of strength + 9th lord in fall/combustion.
    ("h9_lord", "lordship_dignity_condition", "h9_lord_any_house",
     [{"condition": "in_fall_or_combustion", "effect": "negates", "strength": "strong"},
      {"condition": "h10_lord_and_h3_lord_bereft_of_strength", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h9_lord", "debilitated", "combust", "begging"],
     "Ch.20 v.12",
     "10th lord and 3rd lord both bereft of strength while the 9th lord "
     "is in fall or combustion: the native will go abegging for food. "
     "Triple weakness — no karma (10th), no initiative (3rd), and no "
     "fortune (9th) — produces total destitution",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 13-25: Combinations for father's death ──────────────────────
    # These are compound timing rules. Key predictive combinations encoded.
    # v.13: Sun in 6th/8th/12th as 8th lord in 9th → father passed before birth.
    ("sun", "karaka_condition", "sun_father_karaka_affliction",
     [{"condition": "sun_in_6_8_12", "effect": "negates", "strength": "strong"},
      {"condition": "h8_lord_in_9th", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "sun", "h8_lord", "h9", "father_death_birth"],
     "Ch.20 v.13",
     "Father will have passed away prior to native's birth if the Sun "
     "is in the 6th/8th/12th while the 8th lord is in the 9th. Also: "
     "12th lord in the ascendant and 6th lord in the 5th produces "
     "similar father's death at or before birth. The 8th lord (death) "
     "occupying the father's house (9th) directly threatens the father",
     [],
     "",
     [], [],
     ["if_jupiter_aspects_9th_house"],
    ),
    # v.14-16: Saturn from 8th to 9th → fatal timing for father.
    ("saturn", "karaka_condition", "saturn_position_relative_to_9th",
     [{"condition": "saturn_in_7th_from_h8", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "saturn", "father_death_timing"],
     "Ch.20 v.14-16",
     "Various Saturn positions relative to the 8th and 9th houses indicate "
     "timing of father's death. Saturn in the 7th from the 8th (i.e., 2nd "
     "from ascendant) while Sun is in the 7th from Saturn is fatal for "
     "father at ages 6, 25, or specific dasha periods. Complex timing rules "
     "requiring multiple chart factors",
     [],
     "",
     [], [],
     [],
    ),
    # v.17-18: 9th lord in debilitation Navamsa → father death at specific age.
    ("h9_lord", "lordship_dignity_condition", "h9_lord_debilitation_navamsa",
     [{"condition": "debilitation_navamsa", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "h9_lord", "debilitation_navamsa", "father_death"],
     "Ch.20 v.17-18",
     "9th lord in debilitation Navamsa: the native's father will face his "
     "end during the 3rd or 16th year of the native's life. If the lord "
     "of the 12th is in the 9th while the 9th lord is in the 12th, the "
     "native will lose his father. Navamsa debilitation of the 9th lord "
     "is a more precise indicator than rasi debilitation",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 26: Abundant fortunes ─────────────────────────────────────────
    # v.26: Venus in deep exaltation + company of 9th lord + Saturn in 3rd.
    ("venus", "house_placement", [9],
     [{"condition": "in_deep_exaltation", "effect": "amplifies", "strength": "strong"},
      {"condition": "conjunct_h9_lord", "effect": "amplifies", "strength": "moderate"},
      {"condition": "saturn_in_3rd", "effect": "amplifies", "strength": "weak"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "venus", "exalted", "h9", "fortune"],
     "Ch.20 v.26",
     "Venus in deep exaltation in the company of the 9th lord with Saturn "
     "in the 3rd: abundant fortunes. Venus exalted in Pisces (sign of "
     "Jupiter, natural 9th house significator) conjunct the 9th lord "
     "creates a powerful Lakshmi yoga. Saturn in 3rd gives initiative "
     "and endurance to accumulate wealth",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 27-28: Fortunate periods ─────────────────────────────────────
    # v.27: Jupiter in 9th + lord's lord in angle = fortunes after 20th year.
    ("jupiter", "house_placement", [9],
     [{"condition": "h9_lords_dispositor_in_kendra", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "jupiter", "h9", "fortune_timing_20"],
     "Ch.20 v.27",
     "Jupiter in the 9th while the 9th lord has its dispositor in a "
     "kendra from the ascendant: abundant fortunes will be acquired after "
     "the 20th year of age. Jupiter in the house of fortune with its "
     "lord's dispositor strongly placed creates a time-activated wealth "
     "combination",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.28: Mercury in deep exaltation as 9th lord in 9th = fortunes after 36th year.
    ("mercury", "house_placement", [9],
     [{"condition": "mercury_as_h9_lord_in_deep_exaltation", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "mercury", "h9", "h9_lord", "exalted", "fortune_36"],
     "Ch.20 v.28",
     "Mercury in deep exaltation as the 9th lord in the 9th itself: "
     "abundant fortunes will be earned after the 36th year. Mercury "
     "exalted in Virgo as the 9th lord (for Capricorn or Aquarius lagna) "
     "in its own house of fortune gives delayed but substantial wealth",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 29: 9th lord and ascendant lord exchange ──────────────────────
    # v.29: Ascendant lord in 9th + 9th lord in ascendant + Jupiter in 7th.
    ("lagna_lord", "lordship_placement", [9],
     [{"condition": "h9_lord_in_ascendant_exchange", "effect": "amplifies", "strength": "strong"},
      {"condition": "jupiter_in_7th", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth", "property_vehicles"],
     ["bphs", "parashari", "lagna_lord", "h9", "exchange", "jupiter"],
     "Ch.20 v.29",
     "Ascendant lord in the 9th while the 9th lord is in the ascendant "
     "and Jupiter is in the 7th: gains of wealth and conveyances. The "
     "lagna-9th parivartana creates a powerful dharma-lagna link, and "
     "Jupiter in the 7th (10th from 9th) amplifies fortune through "
     "partnerships or spouse",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 30: Lack of fortunes ──────────────────────────────────────────
    # v.30: Rahu in 9th + dispositor in 8th + 9th lord in fall.
    ("rahu", "house_placement", [9],
     [{"condition": "rahus_dispositor_in_8th", "effect": "negates", "strength": "strong"},
      {"condition": "h9_lord_in_fall", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "rahu", "h9", "no_fortune"],
     "Ch.20 v.30",
     "Rahu in the 9th (5th from ascendant) with its dispositor in the "
     "8th from the ascendant and the 9th lord in fall: the native will "
     "be devoid of fortunes. Triple affliction — Rahu polluting the 9th, "
     "dispositor in the house of obstacles, and lord fallen — destroys "
     "all fortune significations",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 31: Food by begging ───────────────────────────────────────────
    # v.31: Saturn in 9th + Moon + ascendant lord in fall.
    ("saturn", "house_placement", [9],
     [{"condition": "conjunct_moon", "effect": "negates", "strength": "moderate"},
      {"condition": "ascendant_lord_in_fall", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "saturn", "h9", "moon", "begging"],
     "Ch.20 v.31",
     "Saturn in the 9th along with the Moon while the ascendant lord is "
     "in fall: the native will acquire food by begging. Saturn and Moon "
     "together in the 9th destroy fortune through poverty-inducing "
     "combinations, and the fallen ascendant lord removes all personal "
     "agency to overcome the situation",
     [],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 21 — Effects of the 10th House (Karma Bhava Phala)
# Santhanam Vol 1, pp.178-183. 22 slokas, ~20 predictive.
# Topics: career, profession, fame, deeds, paternal happiness.
# ═══════════════════════════════════════════════════════════════════════════════

_CH21_DATA = [
    # ── Sloka 2: Paternal happiness, fame, good deeds ──────────────────────
    # v.2: 10th lord strong in exaltation or own Rasi/Navamsa.
    ("h10_lord", "lordship_dignity_condition", "h10_lord_any_house",
     [{"condition": "in_exaltation_or_own_rasi_navamsa", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["bphs", "parashari", "h10_lord", "exalted", "own_sign", "paternal"],
     "Ch.21 v.2",
     "10th lord strong and in exaltation or in own Rasi/Navamsa: the native "
     "will derive extreme paternal happiness, enjoy fame, and perform good "
     "deeds. The strong 10th lord confers a meaningful and respected "
     "profession that brings honor to the family lineage",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 3: Obstructions in work; Rahu in angle/trine ─────────────────
    # v.3a: 10th lord devoid of strength → obstructions.
    ("h10_lord", "lordship_dignity_condition", "h10_lord_any_house",
     [{"condition": "devoid_of_strength", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["career_status"],
     ["bphs", "parashari", "h10_lord", "weak", "career_obstruction"],
     "Ch.21 v.3a",
     "10th lord devoid of strength: the native will face obstructions in "
     "his work. Professional efforts meet resistance, career advancement "
     "is blocked, and the native struggles to establish a meaningful "
     "vocation. The weak 10th lord cannot sustain professional momentum",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.3b: Rahu in angle or trine → Jyotishtoma sacrifice (religious merit).
    ("rahu", "house_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "strongly_disposed", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["spirituality"],
     ["bphs", "parashari", "rahu", "kendra_trikona", "jyotishtoma"],
     "Ch.21 v.3b",
     "Rahu strongly disposed in a kendra or trikona: the native will "
     "perform religious sacrifices like Jyotishtoma — a Soma sacrifice "
     "consisting of sixteen Vedic rites. The native will be extremely "
     "religious and meritorious. Rahu in angles amplifies unconventional "
     "spiritual pursuits",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 4: Royal patronage and business ──────────────────────────────
    # v.4: 10th lord with benefic or in auspicious house → royal patronage.
    ("h10_lord", "lordship_aspect_condition", "h10_lord_any_placement",
     [{"condition": "conjunct_benefic_or_in_benefic_rasi", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["career_status", "wealth"],
     ["bphs", "parashari", "h10_lord", "benefic", "royal_patronage"],
     "Ch.21 v.4",
     "10th lord with a benefic or in an auspicious (benefic's) house: the "
     "native will always gain through royal patronage and in business. In "
     "a contrary situation — 10th lord with a malefic or in a malefic's "
     "Rasi — the native will be a loser in his calling and will not serve "
     "the king or a worthy person",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 5: Both 10th and 11th occupied by malefics ───────────────────
    # v.5: 10th + 11th both with malefics → bad deeds.
    ("any_malefic", "house_placement", [10, 11],
     [{"condition": "both_h10_and_h11_occupied_by_malefics", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["character_temperament", "career_status"],
     ["bphs", "parashari", "malefics", "h10", "h11", "bad_deeds"],
     "Ch.21 v.5",
     "Both the 10th and 11th houses occupied by malefics: the native will "
     "indulge only in bad deeds and will defile his own men. Malefic "
     "influence on both the house of karma (10th) and gains (11th) "
     "corrupts the native's actions and relationships",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 6: 10th lord in 8th with Rahu ─────────────────────────────────
    # v.6: 10th lord relegated to 8th with Rahu → fool, bad deeds.
    ("h10_lord", "lordship_placement", [8],
     [{"condition": "conjunct_rahu", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["bphs", "parashari", "h10_lord", "h8", "rahu", "foolish"],
     "Ch.21 v.6",
     "10th lord relegated to the 8th along with Rahu: the native will "
     "hate others, be a great fool, and perform bad deeds. Rahu in the "
     "company of the 10th lord in the 8th spoils professional happiness "
     "and leads to questionable and foolish actions, misconceptions, and "
     "social alienation",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 7: Saturn, Mars, 10th lord in 7th ─────────────────────────────
    # v.7: Saturn, Mars and 10th lord in 7th as malefic → carnal pleasures.
    ("saturn_mars", "conjunction_in_house", [7],
     [{"condition": "h10_lord_also_in_7th_as_malefic", "effect": "conditionalizes", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["character_temperament", "marriage"],
     ["bphs", "parashari", "saturn", "mars", "h10_lord", "h7", "carnal"],
     "Ch.21 v.7",
     "Saturn, Mars, and the 10th lord are in the 7th as malefic: the "
     "native will be fond of carnal pleasures and filling his belly. "
     "The combination described by 'Sisnodara Parayana' — devoted to "
     "sensual organs and stomach. Professional energy misdirected "
     "toward base pursuits",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 8-10: 10th lord exalted + Jupiter combinations ──────────────
    # v.8-10a: 10th lord exalted in angle + Jupiter as 9th lord in 10th.
    ("h10_lord", "lordship_dignity_condition", "h10_lord_any_house",
     [{"condition": "exalted_in_kendra_or_trikona", "effect": "amplifies", "strength": "strong"},
      {"condition": "jupiter_as_h9_lord_in_10th", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     ["bphs", "parashari", "h10_lord", "exalted", "jupiter", "honour"],
     "Ch.21 v.8-10a",
     "10th lord exalted in a kendra or trikona while Jupiter is the 9th "
     "lord in the 10th: the native will be endowed with honour, wealth, "
     "and valour. Happy life if the 11th lord is in the 10th and the 10th "
     "lord is conjunct Jupiter. This dharma-karma adhipati yoga produces "
     "the highest career success — robes, ornaments, and happiness",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 11: Rahu + Sun + Saturn + Mars in 11th ────────────────────────
    # v.11: 4 planets in 11th → cessation of duties.
    ("rahu", "house_placement", [11],
     [{"condition": "conjunct_sun_saturn_mars_in_11th", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["career_status"],
     ["bphs", "parashari", "rahu", "sun", "saturn", "mars", "h11", "cessation"],
     "Ch.21 v.11",
     "Rahu, Sun, Saturn, and Mars in the 11th house: the native will "
     "incur cessation of his duties. The four malefics joining in the "
     "11th house will ensure the native will not be successful in "
     "performance — no happy calling or profession worth the name, "
     "and nothing will be gained",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 12: Jupiter in Pisces + Venus + strong ascendant lord ─────────
    # v.12: Jupiter in Pisces + Venus + ascendant lord strong + Moon exalted.
    ("jupiter", "house_placement", [12],
     [{"condition": "jupiter_in_pisces", "effect": "amplifies", "strength": "strong"},
      {"condition": "conjunct_venus", "effect": "amplifies", "strength": "moderate"},
      {"condition": "ascendant_lord_strong_moon_exalted", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["intelligence_education", "wealth", "spirituality"],
     ["bphs", "parashari", "jupiter", "pisces", "venus", "gnana_yoga"],
     "Ch.21 v.12",
     "Jupiter in Pisces along with Venus while the ascendant lord is "
     "strong and the Moon is in exaltation: the native will be learned "
     "and wealthy. This is Gnana Yoga — supreme knowledge derived from "
     "meditation and philosophy. Jupiter and Venus in Pisces (terminal "
     "house) endow the native with knowledge of self and the Almighty. "
     "Material wealth comes as a by-product of spiritual attainment",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 13: Precious stones ───────────────────────────────────────────
    # v.13: 10th lord in 11th + 11th lord in ascendant + Venus in 10th.
    ("h10_lord", "lordship_placement", [11],
     [{"condition": "h11_lord_in_ascendant", "effect": "amplifies", "strength": "moderate"},
      {"condition": "venus_in_10th", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h10_lord", "h11", "venus", "precious_stones"],
     "Ch.21 v.13",
     "10th lord in the 11th while the 11th lord is in the ascendant and "
     "Venus is in the 10th: the native will be endowed with precious "
     "stones. A huge influx of material wealth — the planets described "
     "confer luxury possessions and gemstones through career success",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 14: Worthy deeds ──────────────────────────────────────────────
    # v.14: 10th lord exalted in angle/trine + company of Jupiter.
    ("h10_lord", "lordship_dignity_condition", "h10_lord_any_house",
     [{"condition": "exalted_in_kendra_or_trikona", "effect": "amplifies", "strength": "strong"},
      {"condition": "conjunct_or_aspected_by_jupiter", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["character_temperament", "spirituality"],
     ["bphs", "parashari", "h10_lord", "exalted", "jupiter", "worthy_deeds"],
     "Ch.21 v.14",
     "10th lord exalted in an angle or a trine and in the company of "
     "or in aspect to Jupiter: one will be endowed with worthy deeds. "
     "Jupiter's benefic influence on the exalted 10th lord ensures "
     "professional actions are dharmic and meritorious",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 15: Good deeds through ascendant lord connection ──────────────
    # v.15: 10th lord in ascendant + ascendant lord with Moon in angle/trine.
    ("h10_lord", "lordship_placement", [1],
     [{"condition": "ascendant_lord_with_moon_in_kendra_trikona", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "h10_lord", "h1", "lagna_lord", "moon", "good_deeds"],
     "Ch.21 v.15",
     "10th lord in the ascendant along with the ascendant lord and the "
     "Moon in an angle or a trine: the native will be interested in "
     "good deeds. The 10th lord coming to the lagna connects profession "
     "with personality, and Moon's well-placed support gives emotional "
     "investment in virtuous actions",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 16: Bereft of virtuous acts ───────────────────────────────────
    # v.16: Saturn in 10th + debilitated planet + Navamsa with malefic.
    ("saturn", "house_placement", [10],
     [{"condition": "conjunct_debilitated_planet", "effect": "negates", "strength": "moderate"},
      {"condition": "navamsa_ascendant_with_malefic", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "saturn", "h10", "debilitated", "no_virtue"],
     "Ch.21 v.16",
     "Saturn in the 10th along with a debilitated planet while the "
     "Navamsa ascendant is occupied by a malefic: the native will be "
     "bereft of virtuous acts. Saturn's restriction combined with "
     "debilitation and D9 malefic confirmation triply blocks dharmic "
     "professional conduct",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 17: Bad acts from 8th-10th connection ─────────────────────────
    # v.17: 10th lord in 8th + 8th lord in 10th with malefic.
    ("h10_lord", "lordship_placement", [8],
     [{"condition": "h8_lord_in_10th_with_malefic", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["character_temperament", "career_status"],
     ["bphs", "parashari", "h10_lord", "h8", "exchange", "bad_acts"],
     "Ch.21 v.17",
     "10th lord in the 8th while the 8th lord is in the 10th with a "
     "malefic: one will indulge in bad acts. The 8th-10th exchange "
     "brings hidden, destructive, or criminal tendencies into the "
     "professional sphere. Career involves scandals or unethical conduct",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 18: Obstructions in career ────────────────────────────────────
    # v.18: 10th lord in fall + 10th from ascendant and 10th both with malefics.
    ("h10_lord", "lordship_dignity_condition", "h10_lord_any_house",
     [{"condition": "in_fall", "effect": "negates", "strength": "strong"},
      {"condition": "h10_from_both_asc_and_10th_with_malefics", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["career_status"],
     ["bphs", "parashari", "h10_lord", "debilitated", "malefics", "obstruction"],
     "Ch.21 v.18",
     "Obstructions to the native's acts will crop up if the 10th lord "
     "is in fall, both the 10th from the ascendant and the 10th from "
     "the 10th (7th from ascendant) have malefic occupations. Career "
     "completely blocked from multiple directions",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 19-21: Combinations for fame ─────────────────────────────────
    # v.19: Moon in 10th + 10th lord in trine + ascendant lord in angle.
    ("moon", "house_placement", [10],
     [{"condition": "h10_lord_in_trikona", "effect": "amplifies", "strength": "moderate"},
      {"condition": "ascendant_lord_in_kendra", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["fame_reputation"],
     ["bphs", "parashari", "moon", "h10", "fame"],
     "Ch.21 v.19",
     "Moon in the 10th while the 10th lord is in a trine and the "
     "ascendant lord is in a kendra's angle: one will be endowed with "
     "fame. Public visibility (Moon in 10th) combined with strong "
     "support from the 10th lord and lagna lord creates lasting renown",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.20: 11th lord in 10th + 10th lord strong + aspect to Jupiter.
    ("h11_lord", "lordship_placement", [10],
     [{"condition": "h10_lord_strong_aspected_by_jupiter", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["fame_reputation", "career_status"],
     ["bphs", "parashari", "h11_lord", "h10", "jupiter", "fame"],
     "Ch.21 v.20",
     "11th lord in the 10th while the 10th lord is strong and in aspect "
     "to Jupiter: similar fame will come to pass. The 11th-10th "
     "connection with Jupiter's blessing brings recognition through "
     "professional achievement and gains",
     [],
     "",
     [], [],
     [],
    ),
    # v.21: 10th lord in 9th + ascendant lord in 10th + Moon in 5th.
    ("h10_lord", "lordship_placement", [9],
     [{"condition": "ascendant_lord_in_10th", "effect": "amplifies", "strength": "moderate"},
      {"condition": "moon_in_5th", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["fame_reputation"],
     ["bphs", "parashari", "h10_lord", "h9", "lagna_lord", "moon", "fame"],
     "Ch.21 v.21",
     "Fame will come to the native if the 10th lord is in the 9th and "
     "the ascendant lord is in the 10th and the Moon is in the 5th from "
     "the ascendant. The 9th-10th dharma-karma connection reinforced by "
     "Moon in the 5th (purva punya) produces lasting renown",
     [],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 22 — Effects of the 11th House (Labha Bhava Phala)
# Santhanam Vol 1, pp.183-186. 14 slokas total. Topics: gains, income.
# Note: Many slokas specify wealth in "Nishkas" — a gold coin measure.
# ═══════════════════════════════════════════════════════════════════════════════

_CH22_DATA = [
    # ── Sloka 2: 11th lord in 11th or angle/trine ──────────────────────────
    # v.2: 11th lord in 11th itself or angle/trine → many gains.
    ("h11_lord", "lordship_placement", [1, 4, 5, 7, 9, 10, 11],
     [],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "kendra_trikona", "gains"],
     "Ch.22 v.2a",
     "11th lord in the 11th itself or in an angle or trine from the "
     "ascendant: there will be many gains. The 11th lord well-placed "
     "in its own house or in a kendra/trikona activates the house of "
     "gains fully. Income flows from multiple sources",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.2b: Even if combust but exalted → abundant gains.
    ("h11_lord", "lordship_dignity_condition", "h11_lord_any_house",
     [{"condition": "exalted_though_combust", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "exalted", "combust", "gains"],
     "Ch.22 v.2b",
     "Even though the 11th lord is combust (having lost rays in the "
     "Sun), if it is in exaltation the native will gain abundantly. "
     "Exaltation strength overrides combustion weakness for the 11th "
     "lord — the power of dignity trumps proximity to the Sun",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 3: Great gains through 11th-2nd-Jupiter ──────────────────────
    # v.3: 11th lord in 2nd + 2nd lord in angle + Jupiter → great gains.
    ("h11_lord", "lordship_placement", [2],
     [{"condition": "h2_lord_in_kendra_with_jupiter", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "h2", "jupiter", "great_gains"],
     "Ch.22 v.3",
     "11th lord in the 2nd while the 2nd lord is in an angle from the "
     "ascendant along with Jupiter: the gains will be great. Two wealth "
     "houses (2nd and 11th) connected with Jupiter's amplification "
     "creates a powerful dhana yoga for accumulated riches",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 4: 2000 Nishkas at 36th year ─────────────────────────────────
    # v.4: 11th lord in 3rd + 11th occupied by benefic → wealth at 36.
    ("h11_lord", "lordship_placement", [3],
     [{"condition": "h11_occupied_by_benefic", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "h3", "benefic", "wealth_timing"],
     "Ch.22 v.4",
     "11th lord in the 3rd while the 11th is occupied by a benefic: "
     "the native will gain 2000 Nishkas (gold coins of significant "
     "value) in his 36th year. The 3rd house placement gives initiative, "
     "and the benefic in 11th ensures the gains manifest at this "
     "specific age",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 5: 500 Nishkas at 40th year ──────────────────────────────────
    # v.5: 11th lord conjunct benefic in angle/trine → 500 Nishkas at 40.
    ("h11_lord", "lordship_aspect_condition", "h11_lord_any_placement",
     [{"condition": "conjunct_benefic_in_kendra_trikona", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "benefic", "kendra", "wealth_40"],
     "Ch.22 v.5",
     "11th lord conjunct a benefic in an angle or a trine from the "
     "ascendant: the native will acquire 500 Nishkas in his 40th year. "
     "A benefic in kendra/trikona supporting the 11th lord gives "
     "moderate but reliable gains at a specific age",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 6: 6000 Nishkas through Jupiter in 11th ──────────────────────
    # v.6: Jupiter in 11th + 2nd by Moon + 9th by Venus → 6000 Nishkas.
    ("jupiter", "house_placement", [11],
     [{"condition": "moon_in_2nd", "effect": "amplifies", "strength": "moderate"},
      {"condition": "venus_in_9th", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "jupiter", "h11", "moon", "venus", "great_wealth"],
     "Ch.22 v.6",
     "Jupiter occupying the 11th while the 2nd and 9th are taken over "
     "by the Moon and Venus respectively: the native will own 6000 "
     "Nishkas. The three natural benefics in houses of wealth (2nd), "
     "fortune (9th), and gains (11th) create an extraordinary dhana "
     "yoga of the highest order",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 7: Jupiter, Mercury, Moon in 11th ─────────────────────────────
    # v.7: Jupiter + Mercury + Moon in 11th → wealth, diamonds, ornaments.
    ("jupiter_mercury_moon", "conjunction_in_house", [11],
     [],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "jupiter", "mercury", "moon", "h11", "diamonds"],
     "Ch.22 v.7",
     "Jupiter, Mercury, and the Moon in the 11th (9th from the "
     "ascendant): the native will be endowed with wealth, grains, "
     "fortunes, diamonds, and ornaments. Three benefics combining in "
     "the house of gains produces extraordinary material prosperity "
     "across multiple categories of wealth",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 8: Mutual exchange 11th-1st ───────────────────────────────────
    # v.8: 11th lord in ascendant + ascendant lord in 11th → 1000 Nishkas at 33.
    ("h11_lord", "lordship_placement", [1],
     [{"condition": "ascendant_lord_in_11th_exchange", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "h1", "parivartana", "wealth_33"],
     "Ch.22 v.8",
     "11th lord in the ascendant while the ascendant lord is in the "
     "11th: one will gain 1000 Nishkas in his 33rd year. This mutual "
     "exchange (parivartana) between the 1st and 11th houses directly "
     "links the native's personality with gains, manifesting at age 33",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 9: Fortunes after marriage ────────────────────────────────────
    # v.9: 11th lord in 2nd as 2nd lord in 11th → abundant after marriage.
    ("h11_lord", "lordship_placement", [2],
     [{"condition": "h2_lord_in_11th_exchange", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth", "marriage"],
     ["bphs", "parashari", "h11_lord", "h2", "exchange", "after_marriage"],
     "Ch.22 v.9",
     "11th lord in the 2nd as the 2nd lord is in the 11th: one will "
     "amass abundant fortunes after marriage. The 2nd-11th parivartana "
     "ties wealth accumulation to the marital partnership — finances "
     "improve significantly once married",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 10: Wealth through co-born ────────────────────────────────────
    # v.10: 11th lord in 3rd as 3rd lord in 11th → wealth through siblings.
    ("h11_lord", "lordship_placement", [3],
     [{"condition": "h3_lord_in_11th_exchange", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "h3", "exchange", "co_born_wealth"],
     "Ch.22 v.10",
     "11th lord in the 3rd as the 3rd lord is in the 11th: one will "
     "gain wealth through co-born (siblings) and be endowed with "
     "excellent ornaments. The 3rd-11th exchange connects initiative "
     "and siblings with the house of gains",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 11: No gains despite efforts ──────────────────────────────────
    # v.11: 11th lord in fall/combustion or 6th/8th/12th with malefic → no gains.
    ("h11_lord", "lordship_placement", [6, 8, 12],
     [{"condition": "in_fall_or_combustion", "effect": "negates", "strength": "strong"},
      {"condition": "conjunct_malefic", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h11_lord", "dusthana", "no_gains"],
     "Ch.22 v.11",
     "There will be no gains in spite of numerous efforts if the 11th "
     "lord is in fall or combustion, or is in the 6th/8th/12th with "
     "a malefic. The dusthana placement combined with affliction "
     "completely blocks the house of gains — effort produces no return",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 23 — Effects of the 12th House (Vyaya Bhava Phala)
# Santhanam Vol 1, pp.186-189. 17 slokas, ~16 predictive.
# Topics: expenses, loss, emancipation, foreign travel, bed pleasures.
# ═══════════════════════════════════════════════════════════════════════════════

_CH23_DATA = [
    # ── Slokas 1-4: 12th lord benefic conditions ───────────────────────────
    # v.1-2: 12th lord with benefic or in own house/exalted → good expenses.
    ("h12_lord", "lordship_aspect_condition", "h12_lord_any_placement",
     [{"condition": "with_benefic_or_in_own_house_or_exalted", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth", "property_vehicles"],
     ["bphs", "parashari", "h12_lord", "benefic", "good_expenses"],
     "Ch.23 v.1-2",
     "12th lord with a benefic, or in its own house, or exalted, or "
     "aspected by a benefic: expenses will be on good accounts. One "
     "will own beautiful houses and beds and be endowed with superior "
     "scented articles and pleasures. Well-placed 12th lord channels "
     "expenditure toward luxury and comfort rather than loss",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.3-4: Moon as 12th lord exalted/own sign in 11th/9th/5th → rich.
    ("moon", "lordship_aspect_condition", "moon_as_h12_lord",
     [{"condition": "in_exaltation_or_own_sign", "effect": "amplifies", "strength": "strong"},
      {"condition": "placed_in_11_9_or_5_rasi_navamsa", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["bphs", "parashari", "moon", "h12_lord", "exalted", "rich_clothes"],
     "Ch.23 v.3-4",
     "Moon as the 12th lord exalted or in own sign/Navamsa, placed in "
     "the 11th/9th/5th in Rasi/Navamsa: the native will live with rich "
     "clothes, ornaments, be learned and lordly. The dignified Moon as "
     "12th lord transforms expenditure into prosperity when well-placed "
     "in a trikona or 11th house",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 5-6: 12th lord in dusthana/debilitation ─────────────────────
    # v.5-6a: 12th lord in 6th/8th or debilitation Navamsa → devoid of happiness.
    ("h12_lord", "lordship_placement", [6, 8],
     [{"condition": "debilitation_navamsa", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["bphs", "parashari", "h12_lord", "dusthana", "devoid_happiness"],
     "Ch.23 v.5-6a",
     "12th lord in the 6th/8th or in debilitation Navamsa or in 8th "
     "Navamsa: one will be devoid of happiness from wife, be troubled "
     "by expenses, and deprived of general happiness. The 12th lord in "
     "another dusthana compounds loss — expenses become debts, and "
     "domestic peace is disrupted",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # v.6b: If 12th lord in angle/trine → will beget spouse.
    ("h12_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [],
     "favorable", "moderate",
     ["marriage"],
     ["bphs", "parashari", "h12_lord", "kendra_trikona", "spouse"],
     "Ch.23 v.6b",
     "If the 12th lord is in an angle or trine: one will beget a spouse. "
     "Despite the 12th house being a house of loss, its lord in a "
     "kendra/trikona redirects the energy positively — bed pleasures "
     "(12th house signification) manifest as a happy marital relationship",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 8: Visible vs invisible half ──────────────────────────────────
    # v.8: Planets in visible half → explicit results; invisible half → secret.
    ("any_planet", "house_placement", [7, 8, 9, 10, 11, 12],
     [],
     "neutral", "moderate",
     ["fame_reputation"],
     ["bphs", "parashari", "visible_half", "explicit_results"],
     "Ch.23 v.8",
     "Planets placed in the visible half of the zodiac (within 180 "
     "degrees from the ascendant's cusp seen backwards) will give "
     "explicit results, while those in the invisible half produce "
     "secret results. A planet in the visible half has more potential "
     "in effects — results are manifest and publicly recognized",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 9: Rahu + Mars + Saturn + Sun in 12th ─────────────────────────
    # v.9: Rahu in 12th + Mars + Saturn + Sun + 12th lord with Sun → hell.
    ("rahu", "house_placement", [12],
     [{"condition": "conjunct_mars_saturn_sun", "effect": "negates", "strength": "strong"},
      {"condition": "h12_lord_with_sun", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["spirituality", "character_temperament"],
     ["bphs", "parashari", "rahu", "mars", "saturn", "sun", "h12", "hell"],
     "Ch.23 v.9",
     "Rahu in the 12th along with Mars, Saturn, and the Sun, and the "
     "12th lord is with the Sun: the native will go to hell (face severe "
     "karmic consequences after death). The 12th house governs final "
     "emancipation — four malefics there with the afflicted 12th lord "
     "deny moksha and indicate severe post-mortem suffering",
     [],
     "",
     [], [],
     [],
    ),

    # ── Sloka 10: Final emancipation (moksha) ───────────────────────────────
    # v.10: Benefic in 12th + exalted/conjunct/aspected benefic → moksha.
    ("any_benefic", "house_placement", [12],
     [{"condition": "exalted_or_conjunct_aspected_by_benefic", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["spirituality"],
     ["bphs", "parashari", "benefic", "h12", "exalted", "moksha"],
     "Ch.23 v.10",
     "A benefic in the 12th house that is exalted or conjunct/aspected "
     "by another benefic: one will attain final emancipation (moksha). "
     "The 12th house of liberation supported by strong benefics channels "
     "the soul toward spiritual release rather than material loss",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 11: Wandering from country to country ─────────────────────────
    # v.11: 12th lord and 12th with malefics → wander abroad.
    ("h12_lord", "lordship_aspect_condition", "h12_lord_any_placement",
     [{"condition": "h12_lord_and_h12_with_malefics", "effect": "negates", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["foreign_travel"],
     ["bphs", "parashari", "h12_lord", "malefics", "wandering"],
     "Ch.23 v.11",
     "12th lord and 12th house both associated with malefics and "
     "aspected by malefics: one will wander from country to country. "
     "Malefic influence on the 12th house and its lord creates "
     "compulsive displacement — the native cannot settle in one place "
     "and is driven to foreign lands by misfortune",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 12: Stay in own country ───────────────────────────────────────
    # v.12: 12th lord and 12th with benefics → own country.
    ("h12_lord", "lordship_aspect_condition", "h12_lord_any_placement",
     [{"condition": "h12_lord_and_h12_with_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["property_vehicles"],
     ["bphs", "parashari", "h12_lord", "benefics", "own_country"],
     "Ch.23 v.12",
     "12th lord and 12th house both connected with benefics and "
     "aspected by benefics: one will move in his own country and "
     "progress in his own place. Benefic influence on the 12th house "
     "channels expenditure toward local establishment rather than "
     "displacement, enabling the native to stay rooted",
     ["Saravali"],
     "Saravali agrees on benefic influence keeping native in homeland "
     "but does not specify exact 12th lord position",
     [], [],
     [],
    ),

    # ── Sloka 13: Sinful earnings ───────────────────────────────────────────
    # v.13: Saturn/Mars in 12th + no benefic aspect → sinful earnings.
    ("saturn", "house_placement", [12],
     [{"condition": "conjunct_mars", "effect": "negates", "strength": "moderate"},
      {"condition": "not_aspected_by_benefic", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["bphs", "parashari", "saturn", "mars", "h12", "sinful_earnings"],
     "Ch.23 v.13",
     "12th house occupied by Saturn or Mars etc., and not aspected by "
     "a benefic: earnings will be through sinful measures. The malefic "
     "12th house without benefic correction leads to income through "
     "unethical means — the native resorts to dishonest methods to "
     "finance expenditures",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Sloka 14: Expenses on religious grounds ─────────────────────────────
    # v.14: Ascendant lord in 12th + Venus in 12th → religious expenses.
    ("lagna_lord", "lordship_placement", [12],
     [{"condition": "conjunct_venus_in_12th", "effect": "conditionalizes", "strength": "moderate"}],
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["bphs", "parashari", "lagna_lord", "h12", "venus", "religious_expense"],
     "Ch.23 v.14",
     "Ascendant lord in the 12th while the 12th is also occupied by "
     "Venus: expenses will be on religious grounds. Venus in the 12th "
     "is one of Venus's best placements (bed pleasures, luxury in "
     "isolation) — combined with lagna lord, the native spends "
     "generously on dharmic and spiritual causes",
     [],
     "",
     [], [],
     [],
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder — same structure as bphs_1b_houses_1.py / bphs_1b_houses_2.py
# ═══════════════════════════════════════════════════════════════════════════════

def _make_house_rules(
    data: list,
    start_num: int,
    chapter: str,
    category: str,
) -> list[RuleRecord]:
    """Build RuleRecord objects for BPHS house-effect rules."""
    rules: list[RuleRecord] = []
    num = start_num
    for entry in data:
        (planet, ptype, value_or_label, modifiers_raw,
         odir, oint, odoms, extra_tags, vref, desc,
         conc_texts, div_notes,
         lagna_sc, dasha_sc,
         exceptions_list) = entry

        rid = f"BPHS{num:04d}"

        # Build primary_condition — atomic placement
        if ptype == "house_placement":
            primary = {
                "planet": planet,
                "placement_type": "house",
                "placement_value": value_or_label,
                "house": value_or_label[0] if len(value_or_label) == 1 else value_or_label,
            }
        elif ptype == "conjunction_in_house":
            planets = planet.split("_")
            primary = {
                "planet": planet,
                "placement_type": "conjunction_in_house",
                "placement_value": value_or_label,
                "house": value_or_label[0] if len(value_or_label) == 1 else value_or_label,
                "planets": planets,
            }
        elif ptype == "lordship_placement":
            primary = {
                "planet": planet,
                "placement_type": "lordship_placement",
                "placement_value": value_or_label,
            }
        elif ptype in ("lordship_aspect_condition", "lordship_dignity_condition",
                        "karaka_condition"):
            primary = {
                "planet": planet,
                "placement_type": ptype,
                "yoga_label": value_or_label,
            }
        else:
            primary = {
                "planet": planet,
                "placement_type": ptype,
                "yoga_label": value_or_label,
            }

        modifiers = list(modifiers_raw) if modifiers_raw else []

        if any(d in odoms for d in ("character_temperament", "physical_appearance")):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        conc_count = len(conc_texts) if conc_texts else 0
        div_count = len([x for x in div_notes.split(",") if x.strip()]) if div_notes else 0
        confidence = min(1.0, 0.60 + 0.05 + (0.08 * conc_count) - (0.05 * div_count))

        if lagna_sc:
            phase = "1B_conditional"
        elif ptype in ("conjunction_in_house", "karaka_condition"):
            phase = "1B_compound"
        else:
            phase = "1B_matrix"

        tags = list(dict.fromkeys(
            ["bphs", "parashari", "house_effects"] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="BPHS",
            chapter=chapter,
            school="parashari",
            category=category,
            description=f"[BPHS — {category}] {desc}",
            confidence=confidence,
            keyword_tags=tags,
            implemented=False,
            primary_condition=primary,
            modifiers=modifiers,
            exceptions=exceptions_list,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing=timing,
            lagna_scope=lagna_sc,
            dasha_scope=dasha_sc,
            verse_ref=vref,
            concordance_texts=conc_texts,
            divergence_notes=div_notes,
            phase=phase,
            system="natal",
            prediction_type="event",
            gender_scope="universal",
            certainty_level="definite",
            strength_condition="any",
            house_system="sign_based",
            ayanamsha_sensitive=False,
            evaluation_method="placement_check" if ptype == "house_placement" else "lordship_check",
            last_modified_session="S308",
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    """Build all BPHS Ch.20-23 rules."""
    result: list[RuleRecord] = []
    result.extend(_make_house_rules(
        _CH20_DATA, 800, "Ch.20", "9th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH21_DATA, 900, "Ch.21", "10th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH22_DATA, 1000, "Ch.22", "11th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH23_DATA, 1100, "Ch.23", "12th_house_effects",
    ))
    return result


BPHS_1B_HOUSES_3_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    BPHS_1B_HOUSES_3_REGISTRY.add(_rule)
