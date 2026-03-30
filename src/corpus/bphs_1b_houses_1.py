"""src/corpus/bphs_1b_houses_1.py — S306: BPHS Ch.12-15 Phase 1B Re-encode.

BPHS0001–BPHS_NNN (rule count determined by source text).
Phase: 1B_matrix + 1B_conditional | Source: BPHS | School: parashari

BPHS (Brihat Parasara Hora Shastra) — R. Santhanam translation, Vol 1.
This file encodes Ch.12 (Tanu Bhava / 1st House), Ch.13 (Dhana Bhava / 2nd House),
Ch.14 (Sahaj Bhava / 3rd House), and Ch.15 (Sukha Bhava / 4th House) at sutra-level
depth with full Phase 1B contract compliance.

BPHS is the concordance anchor for all Parashari texts. Every rule here is
cross-referenced against existing Saravali, Bhavartha Ratnakara, and Laghu
Parashari rules at encoding time per PHASE1B_CONCORDANCE_WORKFLOW.md.

MODIFIER PROTOCOL (Option B — structural correctness):
  primary_condition = simplest atomic placement (planet in house, lord in house)
  modifiers = conditions stated in the verse that CHANGE the base prediction
    (dignity, aspects, strength, combustion, retrograde, dispositor)
  NO redundancy between primary_condition and modifiers.
  If the verse states a condition, it MUST appear as a structured modifier,
  not buried in the description prose.

Confidence formula (Phase 1B mechanical):
  base = 0.60 + 0.05 (verse_ref) = 0.65 minimum
  + 0.08 per concordance text
  - 0.05 per divergence text
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 12 — Effects of the 1st House (Tanu Bhava Phala)
# Santhanam Vol 1, 16 slokas. All predictive.
#
# Modifier principle: primary_condition = the PLACEMENT that triggers the rule.
# Modifiers = conditions the verse explicitly states that shift the outcome.
# ═══════════════════════════════════════════════════════════════════════════════

_CH12_DATA = [
    # ── Slokas 1-2: Longevity assessment from lagna ──────────────────────────
    # Sloka 1: "If lagna lord is strong and in kendra/trikona → long life."
    # Primary = lagna lord in kendra/trikona (the placement).
    # Modifier = "strong" (dignity/shadbala — the verse explicitly conditions on this).
    ("lagna_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "lagna_lord", "kendra", "trikona", "longevity"],
     "Ch.12 v.1",
     "If the lagna lord is endowed with strength and is placed in a kendra "
     "(1/4/7/10) or trikona (1/5/9), the native enjoys a full span of life "
     "with good health and vitality throughout",
     ["Saravali"],  # concordance
     "",  # no divergence
     [], [],  # universal lagna and dasha scope
     ["if_lagna_lord_in_dusthana"],  # exception
    ),
    # Sloka 1 continued: "If weak and in dusthana → short life."
    # Primary = lagna lord in dusthana. Modifier = "weak".
    ("lagna_lord", "lordship_placement", [6, 8, 12],
     [{"condition": "planet_without_strength", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "lagna_lord", "dusthana", "longevity", "short_life"],
     "Ch.12 v.1",
     "If the lagna lord is devoid of strength and is placed in a dusthana "
     "(6th/8th/12th house), the native has a shortened lifespan and suffers "
     "from persistent health afflictions",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # Sloka 2: "Benefics in lagna or aspecting lagna → long life."
    # Primary = benefic in house 1. No modifier — the verse states no condition.
    ("any_benefic", "house_placement", [1],
     [],
     "favorable", "strong",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "benefic", "lagna", "longevity"],
     "Ch.12 v.2",
     "Natural benefics (Jupiter, Venus, strong Moon, unafflicted Mercury) "
     "placed in the lagna or aspecting it confer long life, good health, "
     "and a strong constitution upon the native",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    # Sloka 2 continued: "Malefics in lagna without benefic aspect → reduced longevity."
    # Primary = malefic in house 1. Modifier = "no benefic aspect" (verse says this).
    ("any_malefic", "house_placement", [1],
     [{"condition": "no_benefic_aspect_received", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "malefic", "lagna", "longevity", "reduced"],
     "Ch.12 v.2",
     "Natural malefics (Saturn, Mars, Rahu, Ketu, Sun) placed in the lagna "
     "without the aspect of any benefic planet reduce the native's longevity "
     "and cause health afflictions from early life",
     ["Saravali"],
     "",
     [], [],
     ["if_malefic_in_own_sign_or_exalted"],
    ),

    # ── Slokas 3-5: Lagna lord dignity → appearance and character ────────────
    # Sloka 3: "Lagna lord in own sign or exalted in lagna → handsome, famous."
    # Primary = lagna lord in house 1.
    # Modifier = "in own sign or exalted" (dignity condition stated in verse).
    ("lagna_lord", "lordship_placement", [1],
     [{"condition": "in_own_sign_or_exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["physical_appearance", "fame_reputation", "character_temperament"],
     ["bphs", "parashari", "lagna_lord", "own_sign", "appearance", "fame"],
     "Ch.12 v.3",
     "When the lagna lord occupies its own sign or exaltation sign in the "
     "lagna itself, the native possesses a handsome and well-proportioned body, "
     "attractive features, natural self-confidence, and earns fame through "
     "personal qualities and bearing",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 4: "Lagna lord debilitated or in enemy sign → sickly, unattractive."
    # Primary = lagna lord in house 1.
    # Modifier = "debilitated or enemy sign" (dignity condition stated in verse).
    ("lagna_lord", "lordship_placement", [1],
     [{"condition": "debilitated_or_in_enemy_sign", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["physical_appearance", "physical_health", "character_temperament"],
     ["bphs", "parashari", "lagna_lord", "debilitated", "sickly", "weakness"],
     "Ch.12 v.4",
     "When the lagna lord is debilitated or placed in an enemy sign, the native "
     "has an unattractive or unhealthy body, suffers from chronic ailments, lacks "
     "self-confidence, and faces difficulty establishing themselves in life",
     ["Saravali"],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),

    # Sloka 5: "Lagna lord aspected by benefics → virtuous character."
    # Primary = lagna lord (any placement).
    # Modifier = "aspected by benefics" (stated in verse).
    ("lagna_lord", "lordship_aspect_condition", "lagna_lord_any_placement",
     [{"condition": "aspected_by_natural_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["bphs", "parashari", "lagna_lord", "benefic_aspect", "virtue"],
     "Ch.12 v.5",
     "The lagna lord receiving aspects from natural benefic planets bestows "
     "a virtuous and righteous character upon the native, who becomes known "
     "for their good conduct, generosity, and honorable disposition",
     [],
     "",
     [], [],
     [],
    ),
    # Sloka 5 continued: "Lagna lord aspected by malefics → mean character."
    ("lagna_lord", "lordship_aspect_condition", "lagna_lord_any_placement",
     [{"condition": "aspected_by_natural_malefics", "effect": "negates", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "lagna_lord", "malefic_aspect", "mean_nature"],
     "Ch.12 v.5",
     "The lagna lord receiving aspects from natural malefic planets without "
     "benefic mitigation produces a native of questionable character, prone to "
     "cruelty, dishonesty, or antisocial tendencies",
     [],
     "",
     [], [],
     ["if_malefic_is_yogakaraka"],
    ),

    # ── Slokas 6-8: Specific planets in lagna — base placements ─────────────
    # Sloka 6: "Jupiter in lagna → learned, long-lived, respected."
    # Primary = Jupiter in house 1. No modifier — base placement rule.
    # Verse also states "if in own sign Sagittarius/Pisces → Hamsa Yoga" — that
    # is a separate dignity modifier.
    ("jupiter", "house_placement", [1],
     [],
     "favorable", "strong",
     ["longevity", "intelligence_education", "fame_reputation"],
     ["bphs", "parashari", "jupiter", "lagna", "learned", "longevity"],
     "Ch.12 v.6",
     "Jupiter placed in the lagna bestows long life, deep learning, eloquent "
     "speech, knowledge of scriptures, and wide respect. The native is wise, "
     "generous, dignified in bearing, and favored by superiors and teachers",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    # Sloka 6 dignity modifier: Jupiter in lagna in own/exaltation → Hamsa Yoga.
    ("jupiter", "house_placement", [1],
     [{"condition": "in_own_sign_or_exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["fame_reputation", "career_status", "spirituality"],
     ["bphs", "parashari", "jupiter", "lagna", "hamsa_yoga", "dignity"],
     "Ch.12 v.6",
     "Jupiter in the lagna in its own sign (Sagittarius/Pisces) or exaltation "
     "(Cancer) forms Hamsa Yoga — one of the Pancha Mahapurusha Yogas. The "
     "native attains the highest respect, becomes a teacher or spiritual guide, "
     "and is honored like a king among scholars",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),

    # Sloka 7: "Venus in lagna → beautiful, happy, wealthy."
    ("venus", "house_placement", [1],
     [],
     "favorable", "moderate",
     ["physical_appearance", "marriage", "wealth"],
     ["bphs", "parashari", "venus", "lagna", "beauty", "happiness"],
     "Ch.12 v.7",
     "Venus placed in the lagna gives a beautiful and attractive body, "
     "a pleasing disposition, love of comforts and fine things, happiness "
     "through marriage, and acquisition of wealth through charm and social "
     "grace. The native is artistically inclined and enjoys sensual pleasures",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 7 continued: "Mercury in lagna → witty, learned in many subjects."
    ("mercury", "house_placement", [1],
     [],
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["bphs", "parashari", "mercury", "lagna", "wit", "learning"],
     "Ch.12 v.7",
     "Mercury placed in the lagna makes the native quick-witted, versatile "
     "in learning, skilled in speech and communication, knowledgeable in many "
     "subjects, adaptable in nature, and youthful in appearance. The native "
     "excels in trade, writing, and intellectual pursuits",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 8: "Strong (waxing) Moon in lagna → attractive, popular, healthy."
    # Primary = Moon in house 1. Modifier = "waxing/strong" (verse conditions on this).
    ("moon", "house_placement", [1],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "strong"}],
     "favorable", "moderate",
     ["physical_appearance", "fame_reputation", "physical_health"],
     ["bphs", "parashari", "moon", "lagna", "attractive", "popular"],
     "Ch.12 v.8",
     "A strong (waxing or bright) Moon placed in the lagna gives an attractive "
     "face and body, good complexion, popularity among people, sound physical "
     "health, and a pleasant, emotionally sensitive disposition. The native is "
     "well-liked and succeeds in public-facing roles",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # Sloka 8 continued: "Weak (waning) Moon in lagna → sickly, unstable."
    # Same primary. Modifier = "waning/afflicted".
    ("moon", "house_placement", [1],
     [{"condition": "waning_or_afflicted", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["bphs", "parashari", "moon", "lagna", "waning", "sickly"],
     "Ch.12 v.8",
     "A weak (waning, dark) Moon placed in the lagna produces a sickly body, "
     "fluctuating health, emotional instability, mental worry, and difficulty "
     "establishing oneself. The native is prone to cold-related ailments, "
     "phlegmatic disorders, and depression",
     ["Saravali"],
     "Saravali emphasizes mental fluctuation more than physical sickness; "
     "BPHS treats both equally as outcomes of weak Moon in lagna",
     [], [],
     [],
    ),

    # ── Slokas 9-10: Sun and Mars in lagna ──────────────────────────────────
    # Sloka 9: "Sun in lagna → bold, valorous, but lazy and hot-tempered."
    # Base placement rule — the mixed outcome is inherent, not modifier-dependent.
    ("sun", "house_placement", [1],
     [],
     "mixed", "moderate",
     ["character_temperament", "physical_health", "career_status"],
     ["bphs", "parashari", "sun", "lagna", "bold", "pitta"],
     "Ch.12 v.9",
     "Sun placed in the lagna makes the native bold and courageous, with "
     "a commanding presence and leadership capacity. However, the native is "
     "also hot-tempered, proud, given to laziness, and suffers from bilious "
     "(pitta) health complaints including fevers and eye disorders. The native "
     "gains through government and authority figures",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 10: "Mars in lagna → brave, short-tempered, wounded body."
    ("mars", "house_placement", [1],
     [],
     "mixed", "moderate",
     ["character_temperament", "physical_health", "enemies_litigation"],
     ["bphs", "parashari", "mars", "lagna", "brave", "wounds"],
     "Ch.12 v.10",
     "Mars placed in the lagna makes the native brave, adventurous, and "
     "physically active. But Mars also causes a wounded or scarred body "
     "(injuries from accidents, weapons, or fire), short temper, quarrels "
     "with others, and enmity. The native is impulsive in action and may "
     "face legal troubles or physical confrontations",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 11-12: Saturn, Rahu, Ketu in lagna ───────────────────────────
    # Sloka 11: "Saturn in lagna → lean, unhappy, lazy, poor in early life."
    # Base placement. Verse also states Sasa Yoga exception for own/exaltation.
    ("saturn", "house_placement", [1],
     [],
     "unfavorable", "moderate",
     ["physical_appearance", "character_temperament", "wealth"],
     ["bphs", "parashari", "saturn", "lagna", "lean", "hardship"],
     "Ch.12 v.11",
     "Saturn placed in the lagna gives a lean and bony body, dark complexion, "
     "melancholic and serious disposition, laziness, and poverty or hardship "
     "in early life. The native faces delays in all undertakings, is slow to "
     "act, and may suffer from vata-related ailments (joint pains, cold)",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     ["if_saturn_in_own_or_exaltation_sign"],
    ),
    # Sloka 11 dignity modifier: Saturn in lagna in own/exaltation → Sasa Yoga.
    ("saturn", "house_placement", [1],
     [{"condition": "in_own_sign_or_exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["bphs", "parashari", "saturn", "lagna", "sasa_yoga", "dignity"],
     "Ch.12 v.11",
     "Saturn in the lagna in Capricorn, Aquarius, or Libra forms Sasa Yoga "
     "— one of the Pancha Mahapurusha Yogas. The native rises to authority "
     "through discipline, commands large organizations, and earns lasting "
     "respect through hard work and perseverance",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 12: "Rahu in lagna → fearful, unhealthy, short-lived."
    # Verse conditions: "without benefic aspects" — this is a modifier.
    ("rahu", "house_placement", [1],
     [{"condition": "no_benefic_aspect_received", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["physical_health", "longevity", "character_temperament"],
     ["bphs", "parashari", "rahu", "lagna", "fearful", "unhealthy"],
     "Ch.12 v.12",
     "Rahu placed in the lagna without benefic aspects causes fear and "
     "anxiety, an unhealthy body prone to mysterious or hard-to-diagnose "
     "ailments, a deceptive or unconventional nature, and reduced longevity. "
     "The native may be misunderstood by society, faces sudden upheavals, "
     "and is prone to poisoning or toxic exposure",
     [],
     "",
     [], [],
     ["if_rahu_in_trikona_with_benefic_aspect"],
    ),

    # Sloka 12 continued: "Ketu in lagna → lean, ungrateful, unhappy."
    # Verse also states "if aspected by Jupiter → spiritual" — separate modifier rule.
    ("ketu", "house_placement", [1],
     [],
     "unfavorable", "moderate",
     ["physical_appearance", "character_temperament", "physical_health"],
     ["bphs", "parashari", "ketu", "lagna", "lean", "ungrateful"],
     "Ch.12 v.12",
     "Ketu placed in the lagna gives a lean and dry body, an ungrateful and "
     "dissatisfied disposition, tendency toward detachment or disinterest in "
     "worldly matters. The native may suffer from mysterious ailments, skin "
     "diseases, or wounds from sharp objects",
     [],
     "",
     [], [],
     [],
    ),
    # Ketu in lagna with Jupiter aspect → spiritual (verse-stated modifier).
    ("ketu", "house_placement", [1],
     [{"condition": "aspected_by_jupiter", "effect": "conditionalizes", "strength": "strong"}],
     "favorable", "moderate",
     ["spirituality", "character_temperament"],
     ["bphs", "parashari", "ketu", "lagna", "jupiter_aspect", "moksha"],
     "Ch.12 v.12",
     "Ketu in the lagna aspected by Jupiter transforms the detachment into "
     "spiritual inclination. The native becomes moksha-oriented, interested "
     "in liberation and higher knowledge, and the lean body becomes an "
     "ascetic's frame rather than a sickly one",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 13-14: Combined conditions ────────────────────────────────────
    # Sloka 13: "Lagna lord in kendra with benefic aspect → prosperity."
    # Primary = lagna lord in kendra. Modifier = benefic aspect (verse states both).
    ("lagna_lord", "lordship_placement", [1, 4, 7, 10],
     [{"condition": "aspected_by_natural_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth", "fame_reputation", "physical_health"],
     ["bphs", "parashari", "lagna_lord", "kendra", "benefic_aspect", "prosperity"],
     "Ch.12 v.13",
     "When the lagna lord is placed in a kendra (1/4/7/10) and simultaneously "
     "receives the aspect of natural benefic planets, the native enjoys "
     "prosperity, wealth, good health, fame, and a comfortable life. All "
     "undertakings meet with success",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # Sloka 14: "Lagna lord in trikona aspected by its dispositor → raja yoga."
    # Primary = lagna lord in trikona. Modifier = aspected by dispositor.
    ("lagna_lord", "lordship_placement", [1, 5, 9],
     [{"condition": "aspected_by_sign_dispositor", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["career_status", "fame_reputation", "wealth"],
     ["bphs", "parashari", "lagna_lord", "trikona", "dispositor", "raja_yoga"],
     "Ch.12 v.14",
     "When the lagna lord is placed in a trikona (1/5/9) and receives the "
     "aspect of its sign dispositor, a powerful Raja Yoga is formed. The native "
     "attains kingly status, high position, authority over others, and lasting "
     "fame. Wealth flows abundantly",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 15-16: Dignity-based overall life quality ─────────────────────
    # Sloka 15: "Lagna lord exalted → leader, wealthy, virtuous."
    # Primary = lagna lord (any placement). Modifier = exalted (dignity).
    ("lagna_lord", "lordship_dignity_condition", "lagna_lord_any_house",
     [{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["career_status", "wealth", "character_temperament"],
     ["bphs", "parashari", "lagna_lord", "exalted", "leader", "wealthy"],
     "Ch.12 v.15",
     "When the lagna lord attains exaltation, the native becomes a leader "
     "among their community, acquires great wealth, is of virtuous character, "
     "enjoys excellent health, and is honored by rulers and learned assemblies. "
     "The native's endeavors are crowned with success",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 16: "Lagna lord in moolatrikona → steady prosperity."
    ("lagna_lord", "lordship_dignity_condition", "lagna_lord_any_house",
     [{"condition": "in_moolatrikona", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["wealth", "physical_health", "career_status"],
     ["bphs", "parashari", "lagna_lord", "moolatrikona", "prosperity"],
     "Ch.12 v.16",
     "When the lagna lord occupies its moolatrikona sign, the native enjoys "
     "steady prosperity, reliable health, a stable career, and consistent "
     "progress in life. The effects are slightly less dramatic than exaltation "
     "but more enduring and dependable",
     [],
     "",
     [], [],
     [],
    ),

    # Sloka 16 continued: "Lagna lord combust → health suffers, identity crisis."
    ("lagna_lord", "lordship_dignity_condition", "lagna_lord_any_house",
     [{"condition": "combust", "effect": "negates", "strength": "strong"}],
     "unfavorable", "moderate",
     ["physical_health", "character_temperament"],
     ["bphs", "parashari", "lagna_lord", "combust", "health", "identity"],
     "Ch.12 v.16",
     "When the lagna lord is combust (too close to the Sun), the native's "
     "health suffers, personal identity is overshadowed, and the native "
     "struggles to establish themselves independently. Self-confidence is "
     "diminished and vitality is low. The native lives in the shadow of "
     "more dominant figures",
     [],
     "",
     [], [],
     ["if_sun_is_lagna_lord"],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 13 — Effects of the 2nd House (Dhana Bhava Phala)
# Santhanam Vol 1, 12 slokas. All predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH13_DATA = [
    # ── Slokas 1-2: 2nd lord placement → wealth and speech ──────────────────
    # Sloka 1: "2nd lord strong in kendra/trikona → wealth, eloquent speech."
    # Primary = 2nd lord in kendra/trikona. Modifier = "strong" (verse states).
    ("h2_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h2_lord", "kendra", "trikona", "wealth"],
     "Ch.13 v.1",
     "When the lord of the 2nd house is endowed with strength and placed in "
     "a kendra or trikona, the native comes from a wealthy family, accumulates "
     "significant personal wealth, and maintains prosperity throughout life",
     ["Saravali"],
     "",
     [], [],
     ["if_h2_lord_in_dusthana"],
    ),
    # Same verse, second outcome domain: speech/education.
    ("h2_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["bphs", "parashari", "h2_lord", "speech", "eloquence"],
     "Ch.13 v.1",
     "The 2nd lord strong in kendra or trikona also bestows eloquent and "
     "persuasive speech, good education, a refined manner of expression, "
     "and a truthful disposition. The native speaks sweetly and convincingly",
     [],
     "",
     [], [],
     [],
    ),

    # Sloka 2: "2nd lord in dusthana → poverty, harsh speech."
    ("h2_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "h2_lord", "dusthana", "poverty"],
     "Ch.13 v.2",
     "When the 2nd lord occupies a dusthana (6th, 8th, or 12th house), the "
     "native faces poverty or financial instability, loss of family wealth, "
     "and difficulty accumulating resources. Debts may plague the native",
     ["Saravali"],
     "",
     [], [],
     ["if_h2_lord_in_own_sign_in_dusthana"],
    ),
    ("h2_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "h2_lord", "dusthana", "harsh_speech"],
     "Ch.13 v.2",
     "The 2nd lord in a dusthana also produces harsh, unpleasant, or "
     "dishonest speech. The native speaks abruptly, may use vulgar language, "
     "or lies for personal gain. Family relationships suffer",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 3-4: Benefics/malefics in 2nd house ──────────────────────────
    # Sloka 3: "Benefics in 2nd → sweet speech, education, wealth."
    ("any_benefic", "house_placement", [2],
     [],
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["bphs", "parashari", "benefic", "h2", "wealth", "education"],
     "Ch.13 v.3",
     "Natural benefic planets occupying the 2nd house give wealth through "
     "legitimate means, good education, sweet and truthful speech, a happy "
     "family life, and enjoyment of fine food. The native may be talented "
     "in music or have a pleasant voice",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 4: "Malefics in 2nd without benefic aspect → loss of wealth."
    ("any_malefic", "house_placement", [2],
     [{"condition": "no_benefic_aspect_received", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["wealth"],
     ["bphs", "parashari", "malefic", "h2", "loss_wealth"],
     "Ch.13 v.4",
     "Natural malefic planets in the 2nd house without benefic aspect cause "
     "loss of family wealth, financial setbacks, and difficulty in saving. "
     "Speech becomes harsh and unreliable",
     ["Saravali"],
     "",
     [], [],
     ["if_malefic_in_own_sign"],
    ),

    # ── Slokas 5-12: Specific planets in 2nd house ──────────────────────────
    # Sloka 5: "Jupiter in 2nd → great wealth, learned family, truthful."
    ("jupiter", "house_placement", [2],
     [],
     "favorable", "strong",
     ["wealth", "intelligence_education", "character_temperament"],
     ["bphs", "parashari", "jupiter", "h2", "wealth", "truthful"],
     "Ch.13 v.5",
     "Jupiter in the 2nd house bestows great wealth, a learned and "
     "respectable family, truthful and measured speech, knowledge of "
     "scriptures, and the native becomes a repository of family tradition",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),

    # Sloka 6: "Saturn in 2nd → poverty, harsh speech, dental issues."
    ("saturn", "house_placement", [2],
     [],
     "unfavorable", "moderate",
     ["wealth", "physical_health", "character_temperament"],
     ["bphs", "parashari", "saturn", "h2", "poverty", "dental"],
     "Ch.13 v.6",
     "Saturn in the 2nd house indicates limited wealth, harsh or stammering "
     "speech, dental or throat ailments, and a frugal family background. "
     "The native eats poorly or irregularly",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     ["if_saturn_in_own_or_exaltation"],
    ),

    # Sloka 7: "Mars in 2nd → harsh speech, face/eye injuries."
    ("mars", "house_placement", [2],
     [],
     "unfavorable", "moderate",
     ["character_temperament", "physical_health", "enemies_litigation"],
     ["bphs", "parashari", "mars", "h2", "harsh_speech", "face_injury"],
     "Ch.13 v.7",
     "Mars in the 2nd house produces harsh, aggressive speech, injuries or "
     "marks on the face, eye problems, dental issues, quarrels within the "
     "family, and expenditure exceeding income. Disputes over inheritance",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 8: "Venus in 2nd → wealth, poetic speech, beautiful face."
    ("venus", "house_placement", [2],
     [],
     "favorable", "moderate",
     ["wealth", "physical_appearance", "intelligence_education"],
     ["bphs", "parashari", "venus", "h2", "wealth", "poetic", "beauty"],
     "Ch.13 v.8",
     "Venus in the 2nd house grants considerable wealth, a beautiful face, "
     "poetic and charming speech, enjoyment of fine foods and luxuries, "
     "and a well-off family. The native earns through artistic pursuits",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # Sloka 9: "Sun in 2nd → wealth through government, eye issues."
    ("sun", "house_placement", [2],
     [],
     "mixed", "moderate",
     ["wealth", "physical_health", "career_status"],
     ["bphs", "parashari", "sun", "h2", "government_wealth", "eyes"],
     "Ch.13 v.9",
     "Sun in the 2nd house gives wealth through government connections, "
     "but also causes eye ailments, defective speech or stammering, and "
     "an authoritarian manner. The native may face family estrangement",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # Sloka 10: "Moon in 2nd → beautiful face, fluctuating wealth."
    # Verse conditions on waxing/waning — modifier.
    ("moon", "house_placement", [2],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "moderate"}],
     "mixed", "moderate",
     ["physical_appearance", "wealth"],
     ["bphs", "parashari", "moon", "h2", "beautiful_face", "fluctuating_wealth"],
     "Ch.13 v.10",
     "Moon in the 2nd house gives a beautiful round face and sweet voice, "
     "but fluctuating wealth that comes and goes in cycles. A waxing Moon "
     "here is significantly better. The native is fond of dairy and sweets",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # Sloka 11: "Rahu in 2nd → deception in speech, foreign food habits."
    ("rahu", "house_placement", [2],
     [],
     "unfavorable", "moderate",
     ["character_temperament", "wealth"],
     ["bphs", "parashari", "rahu", "h2", "deceptive_speech", "foreign_food"],
     "Ch.13 v.11",
     "Rahu in the 2nd house causes deceptive or misleading speech, "
     "unconventional eating habits, loss of family wealth, and an unsettled "
     "family life. The native may earn through irregular or foreign sources. "
     "Face or teeth may have unusual features",
     [],
     "",
     [], [],
     [],
    ),

    # Sloka 12: "Mercury in 2nd → witty speech, commercial wealth."
    ("mercury", "house_placement", [2],
     [],
     "favorable", "moderate",
     ["wealth", "intelligence_education", "character_temperament"],
     ["bphs", "parashari", "mercury", "h2", "witty", "commercial_wealth"],
     "Ch.13 v.12",
     "Mercury in the 2nd house bestows witty and humorous speech, wealth "
     "through trade or intellectual work, versatile skills, and a quick "
     "mind for financial calculations. The native earns through writing, "
     "teaching, or accounting",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 14 — Effects of the 3rd House (Sahaj Bhava Phala)
# Santhanam Vol 1, 22 slokas, 20 predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH14_DATA = [
    # ── Slokas 1-2: 3rd lord placement ──────────────────────────────────────
    ("h3_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["character_temperament"],
     ["bphs", "parashari", "h3_lord", "kendra", "trikona", "courage"],
     "Ch.14 v.1",
     "When the 3rd lord is strong and placed in a kendra or trikona, the "
     "native is endowed with great courage, valor, and self-initiative. "
     "Many younger siblings with good relations among them",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h3_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["character_temperament", "progeny"],
     ["bphs", "parashari", "h3_lord", "dusthana", "cowardice", "sibling_loss"],
     "Ch.14 v.2",
     "When the 3rd lord occupies a dusthana (6/8/12), the native lacks courage, "
     "is timid in undertakings, and may lose younger siblings or have strained "
     "relations with them. Short journeys bring problems",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 3-4: Benefics/malefics in 3rd ────────────────────────────────
    ("any_benefic", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["bphs", "parashari", "benefic", "h3", "siblings", "arts"],
     "Ch.14 v.3",
     "Natural benefics in the 3rd house give helpful siblings, artistic "
     "talents, good communication skills, and success in media pursuits",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # Malefics in 3rd — upachaya: verse states BOTH positive (courage) and negative
    # (rash). This is genuinely mixed per the verse, not modifier-dependent.
    ("any_malefic", "house_placement", [3],
     [],
     "mixed", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["bphs", "parashari", "malefic", "h3", "brave", "rash", "upachaya"],
     "Ch.14 v.4",
     "Natural malefics in the 3rd house (an upachaya) give courage and "
     "boldness — malefics do well in upachaya houses. However, the native "
     "is rash, aggressive in communication, and may conflict with siblings",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 5-8: Mars, Saturn, Jupiter in 3rd ────────────────────────────
    ("mars", "house_placement", [3],
     [],
     "favorable", "strong",
     ["character_temperament", "career_status"],
     ["bphs", "parashari", "mars", "h3", "bravery", "military"],
     "Ch.14 v.5",
     "Mars in the 3rd house (karaka for courage in the house of courage) "
     "gives extraordinary bravery, physical prowess, success in military "
     "or competitive fields. Excellent for athletes, soldiers, surgeons",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("mars", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["bphs", "parashari", "mars", "h3", "travel_gains", "technical"],
     "Ch.14 v.6",
     "Mars in 3rd also makes short journeys profitable, gives command over "
     "workers, mechanical/technical skills, and ability to execute plans "
     "with precision. The native earns through effort and enterprise",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("saturn", "house_placement", [3],
     [],
     "mixed", "moderate",
     ["character_temperament", "progeny"],
     ["bphs", "parashari", "saturn", "h3", "sibling_loss", "patience"],
     "Ch.14 v.7",
     "Saturn in the 3rd house (upachaya) gives patient enduring courage, "
     "not impulsive bravery. The native perseveres. However, younger siblings "
     "may be lost or relations with them are cold. Communication is slow",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("jupiter", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["bphs", "parashari", "jupiter", "h3", "brothers", "noble_courage"],
     "Ch.14 v.8",
     "Jupiter in the 3rd house gives prosperity to younger siblings, noble "
     "dharmic courage, success in pilgrimages, and a philosophical approach "
     "to self-initiative. Bravery through wisdom, not force",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 9-12: Sun, Mercury, Venus, Moon in 3rd ───────────────────────
    ("sun", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["bphs", "parashari", "sun", "h3", "brave", "defeats_enemies"],
     "Ch.14 v.9",
     "Sun in the 3rd house makes the native valorous, able to defeat enemies. "
     "Gains through government on short journeys, authority over siblings",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("mercury", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["bphs", "parashari", "mercury", "h3", "communication", "versatile"],
     "Ch.14 v.10",
     "Mercury in 3rd gives excellent communication skills, versatility, "
     "talent for writing/journalism, good sibling rapport, and success "
     "in trade-related travels",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("venus", "house_placement", [3],
     [],
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["bphs", "parashari", "venus", "h3", "artistic", "social_charm"],
     "Ch.14 v.11",
     "Venus in 3rd gives artistic talents, charming communication, happy "
     "younger siblings (especially sisters), social grace, and success "
     "in entertainment fields",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # Moon in 3rd — verse explicitly conditions on waxing phase.
    ("moon", "house_placement", [3],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "moderate"}],
     "mixed", "moderate",
     ["character_temperament"],
     ["bphs", "parashari", "moon", "h3", "timid", "changeable"],
     "Ch.14 v.12",
     "Moon in 3rd gives fluctuating courage — bold at times, timid at others. "
     "More female siblings. Initiative depends on emotional state. Waxing "
     "Moon significantly improves results",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 13-16: 3rd lord in various houses ────────────────────────────
    ("h3_lord", "lordship_placement", [1],
     [],
     "favorable", "moderate",
     ["character_temperament", "physical_health"],
     ["bphs", "parashari", "h3_lord", "h1", "self_reliant"],
     "Ch.14 v.13",
     "3rd lord in 1st makes the native self-reliant and courageous. "
     "Personal initiative defines their identity. Good health through "
     "physical activity. Siblings helpful to native's growth",
     [],
     "",
     [], [],
     [],
    ),
    ("h3_lord", "lordship_placement", [6],
     [],
     "unfavorable", "moderate",
     ["enemies_litigation"],
     ["bphs", "parashari", "h3_lord", "h6", "sibling_enmity"],
     "Ch.14 v.14",
     "3rd lord in 6th creates enmity with younger siblings, disputes over "
     "shared resources, and litigation from relatives",
     [],
     "",
     [], [],
     [],
    ),
    ("h3_lord", "lordship_placement", [11],
     [],
     "favorable", "strong",
     ["wealth"],
     ["bphs", "parashari", "h3_lord", "h11", "gains"],
     "Ch.14 v.15",
     "3rd lord in 11th brings gains through siblings, courage, and enterprise. "
     "Initiative directly translates to financial gains. Excellent for "
     "entrepreneurs",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 17-20: Rahu/Ketu, compound conditions ────────────────────────
    ("rahu", "house_placement", [3],
     [],
     "mixed", "moderate",
     ["character_temperament", "foreign_travel"],
     ["bphs", "parashari", "rahu", "h3", "bold", "unconventional"],
     "Ch.14 v.17",
     "Rahu in 3rd (upachaya) gives unconventional bravery, success through "
     "unusual or foreign means, foreign connections. The native may work "
     "in technology, media, or foreign trade. Siblings may live abroad",
     [],
     "",
     [], [],
     [],
    ),
    ("ketu", "house_placement", [3],
     [],
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["bphs", "parashari", "ketu", "h3", "spiritual_courage"],
     "Ch.14 v.18",
     "Ketu in 3rd gives courage of spiritual or non-material nature. Brave "
     "in spiritual pursuits but detached from worldly ambition. Distant "
     "sibling relations. May have unusual talents or occult interests",
     [],
     "",
     [], [],
     [],
    ),
    # Compound: 3rd lord with malefic in 8th — verse states conjunction as condition.
    ("h3_lord", "lordship_placement", [8],
     [{"condition": "conjunct_natural_malefic", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "h3_lord", "h8", "malefic", "sibling_danger"],
     "Ch.14 v.19",
     "3rd lord in 8th conjunct natural malefics endangers younger siblings' "
     "life and health. The native may lose a sibling early or face severe "
     "estrangement. Own courage undermined by hidden fears",
     [],
     "",
     [], [],
     ["if_benefic_aspects_h3_lord"],
    ),
    ("h3_lord", "lordship_placement", [9],
     [],
     "favorable", "moderate",
     ["spirituality", "foreign_travel"],
     ["bphs", "parashari", "h3_lord", "h9", "dharma", "fortunate_travel"],
     "Ch.14 v.20",
     "3rd lord in 9th channels courage toward dharmic pursuits. Fortunate "
     "long-distance journeys, especially pilgrimages. Father and younger "
     "siblings have good relations. Self-effort blessed by fortune",
     [],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 15 — Effects of the 4th House (Sukha Bhava Phala)
# Santhanam Vol 1, 31 slokas, 28 predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH15_DATA = [
    # ── Slokas 1-3: 4th lord placement ──────────────────────────────────────
    ("h4_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["property_vehicles", "wealth"],
     ["bphs", "parashari", "h4_lord", "kendra", "trikona", "property"],
     "Ch.15 v.1",
     "When the 4th lord is strong and in kendra/trikona, the native acquires "
     "property, vehicles, a comfortable home, and domestic happiness. Mother "
     "is long-lived. Education completed successfully",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "h4_lord", "dusthana", "no_property"],
     "Ch.15 v.2",
     "4th lord in dusthana: no domestic happiness, difficulty acquiring "
     "property, mother faces health issues. Mental peace disturbed. "
     "Education may be interrupted",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [4],
     [],
     "favorable", "strong",
     ["property_vehicles", "wealth", "intelligence_education"],
     ["bphs", "parashari", "h4_lord", "own_house", "great_happiness"],
     "Ch.15 v.3",
     "4th lord in own house (4th) gives exceptional domestic happiness, many "
     "properties and vehicles, devoted mother, excellent education, mental peace",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 4-12: Specific planets in 4th ────────────────────────────────
    ("jupiter", "house_placement", [4],
     [],
     "favorable", "strong",
     ["property_vehicles", "intelligence_education", "wealth"],
     ["bphs", "parashari", "jupiter", "h4", "happy", "learned"],
     "Ch.15 v.4",
     "Jupiter in 4th gives abundant happiness, many properties, deep learning, "
     "mother's blessings and long life, a spacious home. Respected in "
     "residential area. Hamsa Yoga potential in kendra",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    ("venus", "house_placement", [4],
     [],
     "favorable", "strong",
     ["property_vehicles", "wealth"],
     ["bphs", "parashari", "venus", "h4", "luxury", "vehicles"],
     "Ch.15 v.5",
     "Venus in 4th gives luxurious beautifully decorated home, many fine "
     "vehicles, artistic domestic sensibilities, loving mother. Malavya "
     "Yoga potential in kendra",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    # Moon in 4th — verse conditions on waxing/strong (dig bala here).
    ("moon", "house_placement", [4],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "strong"},
      {"condition": "dig_bala_in_fourth", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["mental_health", "property_vehicles"],
     ["bphs", "parashari", "moon", "h4", "happy_mind", "dig_bala"],
     "Ch.15 v.6",
     "Moon in 4th (directional strength / dig bala position) gives happy "
     "peaceful mind, emotional security, strong mother attachment, comforts "
     "of home and land, popularity. Waxing Moon amplifies all effects",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     ["if_moon_waning_and_afflicted"],
    ),
    ("saturn", "house_placement", [4],
     [],
     "unfavorable", "moderate",
     ["mental_health", "property_vehicles"],
     ["bphs", "parashari", "saturn", "h4", "unhappy", "property_struggles"],
     "Ch.15 v.7",
     "Saturn in 4th creates unhappy domestic environment, delays in property "
     "acquisition, old or dilapidated home, mother's suffering, mental "
     "depression. May live in rented accommodation long. Education interrupted",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     ["if_saturn_in_own_or_exaltation"],
    ),
    ("sun", "house_placement", [4],
     [],
     "unfavorable", "moderate",
     ["mental_health", "property_vehicles"],
     ["bphs", "parashari", "sun", "h4", "unhappy", "dig_bala_loss"],
     "Ch.15 v.8",
     "Sun in 4th (loses directional strength here) creates unhappiness in "
     "domestic affairs, property disputes with government, strained relation "
     "with mother, mental restlessness. May have to leave birthplace. "
     "Heart-related health issues possible",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("mars", "house_placement", [4],
     [],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "mars", "h4", "no_property", "quarrels"],
     "Ch.15 v.9",
     "Mars in 4th denies or delays property acquisition, creates domestic "
     "quarrels, may cause fire damage to home, disturbs mental peace. "
     "Conflicted relation with mother. Frequent residence changes",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("mercury", "house_placement", [4],
     [],
     "favorable", "moderate",
     ["intelligence_education", "property_vehicles"],
     ["bphs", "parashari", "mercury", "h4", "educated", "comfortable"],
     "Ch.15 v.10",
     "Mercury in 4th gives a well-educated native with learned friends, "
     "comfortable home filled with books, witty mother, success in academia, "
     "property through commercial/intellectual activities",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("rahu", "house_placement", [4],
     [],
     "unfavorable", "moderate",
     ["mental_health", "property_vehicles", "foreign_travel"],
     ["bphs", "parashari", "rahu", "h4", "disturbed", "foreign"],
     "Ch.15 v.11",
     "Rahu in 4th disturbs domestic peace, causes sudden disruptions in "
     "living arrangements, may lead to foreign residence, creates anxiety "
     "about home. Mother may face health issues. Property deception risk",
     [],
     "",
     [], [],
     [],
    ),
    ("ketu", "house_placement", [4],
     [],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "ketu", "h4", "property_loss", "detachment"],
     "Ch.15 v.12",
     "Ketu in 4th indicates property loss or difficulty retaining it, "
     "feeling of homelessness, spiritual detachment from comfort. May "
     "renounce comforts voluntarily. Mother's influence absent or karmic",
     [],
     "",
     [], [],
     ["if_ketu_aspected_by_jupiter"],
    ),

    # ── Slokas 13-17: 4th lord in various houses ────────────────────────────
    ("h4_lord", "lordship_placement", [1],
     [],
     "favorable", "moderate",
     ["character_temperament", "property_vehicles"],
     ["bphs", "parashari", "h4_lord", "h1", "happy_disposition"],
     "Ch.15 v.13",
     "4th lord in 1st gives a naturally happy and contented disposition. "
     "Property through personal effort. Mother shapes native's personality",
     [],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [7],
     [],
     "favorable", "moderate",
     ["marriage", "property_vehicles"],
     ["bphs", "parashari", "h4_lord", "h7", "spouse_happiness"],
     "Ch.15 v.14",
     "4th lord in 7th brings domestic happiness through spouse. Property "
     "acquired after marriage. Spouse from good family contributes to comfort",
     [],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [10],
     [],
     "favorable", "strong",
     ["career_status", "property_vehicles"],
     ["bphs", "parashari", "h4_lord", "h10", "career_property"],
     "Ch.15 v.15",
     "4th lord in 10th gives career in property/real estate/agriculture. "
     "High professional status. Excellent kendra-kendra exchange",
     [],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [8],
     [],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "h4_lord", "h8", "property_dispute"],
     "Ch.15 v.16",
     "4th lord in 8th creates chronic anxiety, disputes over inherited "
     "property, loss of family land, mother's health problems. Hidden "
     "property may be involved",
     [],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [12],
     [],
     "mixed", "moderate",
     ["foreign_travel", "property_vehicles"],
     ["bphs", "parashari", "h4_lord", "h12", "foreign_residence"],
     "Ch.15 v.17",
     "4th lord in 12th: residence in foreign lands, loss of ancestral "
     "property, reduced comforts at home, but potential property abroad. "
     "May find happiness away from birthplace. Mother lives separately",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 19-24: Modifier-dependent compound conditions ────────────────
    # Verse 19 explicitly conditions on benefic conjunction/aspect.
    ("h4_lord", "lordship_aspect_condition", "h4_lord_any_placement",
     [{"condition": "conjunct_or_aspected_by_natural_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["property_vehicles"],
     ["bphs", "parashari", "h4_lord", "benefic", "vehicles"],
     "Ch.15 v.19",
     "4th lord conjunct/aspected by benefics: many vehicles, comfortable "
     "well-furnished home, abundant comforts, pleasant domestic environment. "
     "Mother healthy and happy",
     [],
     "",
     [], [],
     [],
    ),
    # Verse 20 explicitly conditions on malefic conjunction/aspect.
    ("h4_lord", "lordship_aspect_condition", "h4_lord_any_placement",
     [{"condition": "conjunct_or_aspected_by_natural_malefics", "effect": "negates", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "h4_lord", "malefic", "loss_vehicles"],
     "Ch.15 v.20",
     "4th lord conjunct/aspected by malefics without benefic influence: "
     "vehicles lost to accidents/theft, domestic strife, mental peace "
     "constantly disturbed",
     [],
     "",
     [], [],
     [],
    ),
    # Verse 21: Moon AND Venus in 4th — compound placement.
    ("moon_venus", "conjunction_in_house", [4],
     [],
     "favorable", "strong",
     ["property_vehicles", "wealth", "mental_health"],
     ["bphs", "parashari", "moon", "venus", "h4", "luxury"],
     "Ch.15 v.21",
     "Moon and Venus together in 4th: exceptional domestic luxury, beautiful "
     "home, many vehicles, devoted beautiful mother, deep emotional happiness. "
     "Home becomes center of beauty, comfort, hospitality",
     [],
     "",
     [], [],
     [],
    ),
    # Verse 22: 4th lord exalted — dignity modifier.
    ("h4_lord", "lordship_dignity_condition", "h4_lord_any_house",
     [{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "h4_lord", "exalted", "many_properties"],
     "Ch.15 v.22",
     "4th lord exalted: owns multiple properties, several vehicles, great "
     "domestic happiness. Mother prosperous and long-lived. Education of "
     "highest caliber. Mental peace assured",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # Verse 23: 4th lord debilitated — dignity modifier.
    ("h4_lord", "lordship_dignity_condition", "h4_lord_any_house",
     [{"condition": "debilitated", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["property_vehicles", "mental_health"],
     ["bphs", "parashari", "h4_lord", "debilitated", "no_property"],
     "Ch.15 v.23",
     "4th lord debilitated: denied property, uncomfortable living conditions, "
     "mother's health suffers, education incomplete, chronic mental "
     "unhappiness",
     [],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),

    # ── Slokas 25-28: Additional conditions ──────────────────────────────────
    # Verse 25: compound — karaka afflicted AND lord weak.
    ("moon", "karaka_condition", "moon_as_h4_karaka",
     [{"condition": "afflicted_by_natural_malefics", "effect": "negates", "strength": "strong"},
      {"condition": "h4_lord_simultaneously_weak", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["physical_health"],
     ["bphs", "parashari", "moon", "karaka", "h4_lord", "mother_trouble"],
     "Ch.15 v.25",
     "Moon (4th house karaka) afflicted by malefics AND 4th lord weak: "
     "serious health problems or early death for mother. Native deprived "
     "of maternal care from childhood",
     ["Saravali"],
     "",
     [], [],
     ["if_jupiter_aspects_moon_or_h4"],
    ),
    ("h4_lord", "lordship_placement", [5],
     [],
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["bphs", "parashari", "h4_lord", "h5", "children_happiness"],
     "Ch.15 v.26",
     "4th lord in 5th: happiness through children, property connected to "
     "education. Comfort from creative/intellectual pursuits. Trikona "
     "placement strengthens both houses",
     [],
     "",
     [], [],
     [],
    ),
    ("h4_lord", "lordship_placement", [9],
     [],
     "favorable", "strong",
     ["property_vehicles", "wealth", "spirituality"],
     ["bphs", "parashari", "h4_lord", "h9", "fortune_property"],
     "Ch.15 v.27",
     "4th lord in 9th: powerful kendra-trikona link bringing fortune through "
     "property, ancestral wealth, religiously inclined mother. Happiness "
     "connected to dharmic living",
     [],
     "",
     [], [],
     [],
    ),
    # Verse 28: Mars in 10th aspecting 4th — verse states the aspect condition.
    ("mars", "house_placement", [10],
     [{"condition": "4th_aspect_falls_on_4th_house", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["property_vehicles", "career_status"],
     ["bphs", "parashari", "mars", "h10", "aspect_h4", "government_property"],
     "Ch.15 v.28",
     "Mars in 10th aspecting 4th house: property through career, especially "
     "government allotment, military housing. Professional standing translates "
     "to material comfort and property",
     [],
     "",
     [], [],
     [],
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder — converts data tuples to RuleRecord objects
# ═══════════════════════════════════════════════════════════════════════════════

def _make_house_rules(
    data: list,
    start_num: int,
    chapter: str,
    category: str,
) -> list[RuleRecord]:
    """Build RuleRecord objects for BPHS house-effect rules.

    Modifier protocol (Option B):
      primary_condition = atomic placement (planet in house, lord in house list)
      modifiers = verse-stated conditions that CHANGE the outcome
      No redundancy between primary_condition and modifiers.
    """
    rules: list[RuleRecord] = []
    num = start_num
    for entry in data:
        (planet, ptype, value_or_label, modifiers_raw,
         odir, oint, odoms, extra_tags, vref, desc,
         conc_texts, div_notes,
         lagna_sc, dasha_sc,
         exceptions_list) = entry

        rid = f"BPHS{num:04d}"

        # Build primary_condition — always the simplest atomic placement
        if ptype == "house_placement":
            primary = {
                "planet": planet,
                "placement_type": "house",
                "placement_value": value_or_label,  # already a list
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
            # value_or_label is a list of house numbers the lord is placed in
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

        # Modifiers: always a list
        modifiers = list(modifiers_raw) if modifiers_raw else []

        # Timing
        if any(d in odoms for d in ("character_temperament", "physical_appearance")):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        # Confidence: mechanical formula
        conc_count = len(conc_texts) if conc_texts else 0
        div_count = len([x for x in div_notes.split(",") if x.strip()]) if div_notes else 0
        confidence = min(1.0, 0.60 + 0.05 + (0.08 * conc_count) - (0.05 * div_count))

        # Phase classification
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
            tags=tags,
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
            last_modified_session="S306",
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    """Build all BPHS Ch.12-15 rules."""
    result: list[RuleRecord] = []
    result.extend(_make_house_rules(
        _CH12_DATA, 1, "Ch.12", "1st_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH13_DATA, 100, "Ch.13", "2nd_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH14_DATA, 200, "Ch.14", "3rd_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH15_DATA, 300, "Ch.15", "4th_house_effects",
    ))
    return result


BPHS_1B_HOUSES_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    BPHS_1B_HOUSES_1_REGISTRY.add(_rule)
