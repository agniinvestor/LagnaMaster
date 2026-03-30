"""src/corpus/bphs_1b_houses_2.py — S307: BPHS Ch.16-19 Phase 1B Re-encode.

BPHS0400–BPHS_NNN (rule count determined by source text).
Phase: 1B_matrix + 1B_conditional + 1B_compound | Source: BPHS | School: parashari

Chapters:
  Ch.16 — Putra Bhava (5th House): children, intelligence, purva punya
  Ch.17 — Ari Bhava (6th House): enemies, disease, debts, service
  Ch.18 — Yuvati Bhava (7th House): marriage, spouse, partnerships
  Ch.19 — Randhra Bhava (8th House): longevity, death, occult, inheritance

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
# CHAPTER 16 — Effects of the 5th House (Putra Bhava Phala)
# Santhanam Vol 1, 28 slokas, 26 predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH16_DATA = [
    # ── Slokas 1-3: 5th lord placement → children and intelligence ───────────
    ("h5_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     ["bphs", "parashari", "h5_lord", "kendra", "trikona", "children"],
     "Ch.16 v.1",
     "5th lord strong in kendra/trikona: many children, particularly sons, "
     "who are obedient and bring happiness. The native is highly intelligent, "
     "has strong discriminative faculty, and excels in learning",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["progeny"],
     ["bphs", "parashari", "h5_lord", "dusthana", "childlessness"],
     "Ch.16 v.2",
     "5th lord in dusthana (6/8/12): few or no children, or children who "
     "cause suffering. The native may face difficulty conceiving. If children "
     "are born, they may be sickly or estranged",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [5],
     [],
     "favorable", "strong",
     ["progeny", "intelligence_education", "spirituality"],
     ["bphs", "parashari", "h5_lord", "own_house", "purva_punya"],
     "Ch.16 v.3",
     "5th lord in own house (5th): strong purva punya (merit from past lives), "
     "intelligent and virtuous children, natural creative talent, spiritual "
     "inclination, and success in mantras and sacred practices",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 4-8: Specific planets in 5th ─────────────────────────────────
    ("jupiter", "house_placement", [5],
     [],
     "favorable", "strong",
     ["progeny", "intelligence_education", "spirituality"],
     ["bphs", "parashari", "jupiter", "h5", "children", "wisdom"],
     "Ch.16 v.4",
     "Jupiter in 5th (karaka for children in the house of children): many "
     "children, especially sons, who are learned and virtuous. The native is "
     "deeply intelligent, devoted to mantras and spiritual practices, and "
     "blessed with strong intuition. Excellent for advisors and teachers",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    ("venus", "house_placement", [5],
     [],
     "favorable", "moderate",
     ["progeny", "intelligence_education", "wealth"],
     ["bphs", "parashari", "venus", "h5", "daughters", "arts"],
     "Ch.16 v.5",
     "Venus in 5th: children (often daughters) who are beautiful and "
     "artistic. The native has creative intelligence, artistic talents, "
     "wealth through speculation or creative ventures, and romantic "
     "inclinations. Love affairs before marriage",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("sun", "house_placement", [5],
     [],
     "mixed", "moderate",
     ["progeny", "career_status"],
     ["bphs", "parashari", "sun", "h5", "few_sons", "authority"],
     "Ch.16 v.6",
     "Sun in 5th: few children, especially few sons, as Sun's heat is "
     "said to dry the house of progeny. However, the native gains authority, "
     "has strong willpower and intelligence, and may work in government "
     "or positions of creative leadership",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("saturn", "house_placement", [5],
     [],
     "unfavorable", "moderate",
     ["progeny", "intelligence_education"],
     ["bphs", "parashari", "saturn", "h5", "delayed_children", "slow_mind"],
     "Ch.16 v.7",
     "Saturn in 5th: delayed children, possible adoption, or children who "
     "cause worry. The native's intelligence is deep but slow — methodical "
     "rather than quick. Education may be interrupted or non-traditional. "
     "Past-life karma is heavy (purva punya deficiency)",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     ["if_saturn_in_own_or_exaltation"],
    ),
    ("mars", "house_placement", [5],
     [],
     "unfavorable", "moderate",
     ["progeny", "enemies_litigation"],
     ["bphs", "parashari", "mars", "h5", "child_loss", "disputes"],
     "Ch.16 v.8",
     "Mars in 5th: danger to children through accidents or surgery, "
     "miscarriages, quarrels related to children. The native is sharp-minded "
     "but argumentative, prone to speculation losses, and impulsive in "
     "romantic matters",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 9-12: More planets in 5th ────────────────────────────────────
    ("moon", "house_placement", [5],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["bphs", "parashari", "moon", "h5", "daughters", "imaginative"],
     "Ch.16 v.9",
     "Moon in 5th: children especially daughters, imaginative and creative "
     "intelligence, emotional attachment to children, success in public-facing "
     "creative work. Waxing Moon greatly improves children's wellbeing. "
     "The native has good memory and poetic sensibility",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("mercury", "house_placement", [5],
     [],
     "favorable", "moderate",
     ["intelligence_education", "progeny"],
     ["bphs", "parashari", "mercury", "h5", "intelligent_children"],
     "Ch.16 v.10",
     "Mercury in 5th: highly intelligent children, native excels in "
     "mathematics, logic, commerce, and astrology. Quick-witted with "
     "multiple skills. Success in speculation through calculation. "
     "Good at mantras involving speech and communication",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("rahu", "house_placement", [5],
     [],
     "unfavorable", "moderate",
     ["progeny", "mental_health"],
     ["bphs", "parashari", "rahu", "h5", "child_trouble", "anxiety"],
     "Ch.16 v.11",
     "Rahu in 5th: trouble with children — delayed, adopted, or from "
     "unconventional circumstances. Mental anxiety, obsessive thinking, "
     "unconventional intelligence. The native may pursue taboo or foreign "
     "forms of knowledge. Speculation is risky",
     [],
     "",
     [], [],
     [],
    ),
    ("ketu", "house_placement", [5],
     [],
     "mixed", "moderate",
     ["progeny", "spirituality"],
     ["bphs", "parashari", "ketu", "h5", "spiritual_child", "moksha"],
     "Ch.16 v.12",
     "Ketu in 5th: few children or spiritual/detached children. Strong "
     "past-life spiritual merit (purva punya). The native is drawn to "
     "moksha, meditation, and mystical knowledge. Intelligence is intuitive "
     "rather than academic. May have psychic abilities",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 13-18: 5th lord in various houses ────────────────────────────
    ("h5_lord", "lordship_placement", [1],
     [],
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["bphs", "parashari", "h5_lord", "h1", "intelligent_self"],
     "Ch.16 v.13",
     "5th lord in 1st: intelligence and creativity define the personality. "
     "The native is known for their brilliance. First child brings good "
     "fortune to the native's life direction",
     [],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [4],
     [],
     "favorable", "moderate",
     ["intelligence_education", "property_vehicles"],
     ["bphs", "parashari", "h5_lord", "h4", "educated_comfort"],
     "Ch.16 v.14",
     "5th lord in 4th: happiness through children and education. Property "
     "connected to educational institutions. Mother is intelligent. "
     "Academic success leads to material comfort",
     [],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [9],
     [],
     "favorable", "strong",
     ["spirituality", "wealth"],
     ["bphs", "parashari", "h5_lord", "h9", "purva_punya_dharma"],
     "Ch.16 v.15",
     "5th lord in 9th: powerful trikona-trikona link. Past-life merit "
     "manifests as present-life fortune. Children are dharmic. Native is "
     "both intelligent and fortunate. Excellent for spiritual teachers",
     [],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [8],
     [],
     "unfavorable", "moderate",
     ["progeny", "mental_health"],
     ["bphs", "parashari", "h5_lord", "h8", "child_health", "anxiety"],
     "Ch.16 v.16",
     "5th lord in 8th: children's health problems, mental anxiety about "
     "progeny, disrupted education, secret knowledge. The native may study "
     "occult subjects but faces emotional turbulence in creative matters",
     [],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [10],
     [],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["bphs", "parashari", "h5_lord", "h10", "career_intelligence"],
     "Ch.16 v.17",
     "5th lord in 10th: career driven by intelligence and creativity. "
     "The native rises through intellectual merit. Children support "
     "professional reputation. Excellent kendra-trikona exchange",
     [],
     "",
     [], [],
     [],
    ),
    ("h5_lord", "lordship_placement", [12],
     [],
     "mixed", "moderate",
     ["progeny", "spirituality"],
     ["bphs", "parashari", "h5_lord", "h12", "children_abroad"],
     "Ch.16 v.18",
     "5th lord in 12th: children may live in foreign lands or be lost. "
     "Expenses through children. But spiritual intelligence is strong — "
     "the native's purva punya manifests as liberation-oriented wisdom",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 19-24: Compound conditions ────────────────────────────────────
    # Jupiter (karaka) afflicted + 5th lord weak → child suffering.
    ("jupiter", "karaka_condition", "jupiter_as_h5_karaka",
     [{"condition": "afflicted_by_natural_malefics", "effect": "negates", "strength": "strong"},
      {"condition": "h5_lord_simultaneously_weak", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["progeny"],
     ["bphs", "parashari", "jupiter", "karaka", "h5", "child_suffering"],
     "Ch.16 v.19",
     "Jupiter (5th house karaka) afflicted by malefics AND 5th lord weak: "
     "severe problems with children — loss, serious illness, or complete "
     "denial of progeny. The double affliction of karaka and lord leaves "
     "no protective factor for the 5th house",
     ["Saravali"],
     "",
     [], [],
     ["if_benefic_aspects_jupiter_or_h5"],
    ),
    # 5th lord with benefics → intelligent, blessed children.
    ("h5_lord", "lordship_aspect_condition", "h5_lord_any_placement",
     [{"condition": "conjunct_or_aspected_by_natural_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["bphs", "parashari", "h5_lord", "benefic", "blessed_children"],
     "Ch.16 v.20",
     "5th lord conjunct/aspected by benefics: intelligent and blessed "
     "children, success in education and creative pursuits, strong mantra "
     "siddhi (power of sacred utterances)",
     [],
     "",
     [], [],
     [],
    ),
    # 5th lord exalted → exceptional progeny.
    ("h5_lord", "lordship_dignity_condition", "h5_lord_any_house",
     [{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     ["bphs", "parashari", "h5_lord", "exalted", "exceptional_children"],
     "Ch.16 v.21",
     "5th lord exalted: exceptional children who achieve great distinction. "
     "The native's intelligence is of the highest order. Purva punya is "
     "abundant — life carries the blessings of past-life merit",
     [],
     "",
     [], [],
     [],
    ),
    # 5th lord debilitated → children suffering.
    ("h5_lord", "lordship_dignity_condition", "h5_lord_any_house",
     [{"condition": "debilitated", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["progeny"],
     ["bphs", "parashari", "h5_lord", "debilitated", "child_suffering"],
     "Ch.16 v.22",
     "5th lord debilitated: children suffer or are denied entirely. "
     "Intelligence is present but misdirected. Education faces serious "
     "obstacles. Purva punya deficit — native must generate merit in "
     "this lifetime through dharmic action",
     [],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),
    # Sun + Jupiter in 5th → powerful raj yoga for progeny.
    ("sun_jupiter", "conjunction_in_house", [5],
     [],
     "favorable", "strong",
     ["progeny", "fame_reputation"],
     ["bphs", "parashari", "sun", "jupiter", "h5", "raj_yoga"],
     "Ch.16 v.23",
     "Sun and Jupiter together in 5th: powerful combination for sons who "
     "achieve fame and authority. The native is brilliant, authoritative "
     "in knowledge, and known for their wisdom. A raja yoga for progeny",
     [],
     "",
     [], [],
     [],
    ),
    # Saturn + Rahu in 5th → putradosha (curse on progeny).
    ("saturn_rahu", "conjunction_in_house", [5],
     [],
     "unfavorable", "strong",
     ["progeny"],
     ["bphs", "parashari", "saturn", "rahu", "h5", "putradosha"],
     "Ch.16 v.24",
     "Saturn and Rahu together in 5th: putradosha — a karmic curse on "
     "progeny. Children are denied, lost, or cause extreme suffering. "
     "The native's past-life karma blocks the 5th house completely. "
     "Remedial measures are specifically prescribed for this combination",
     [],
     "",
     [], [],
     ["if_jupiter_aspects_5th_house"],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 17 — Effects of the 6th House (Ari Bhava Phala)
# Santhanam Vol 1, 14 slokas. All predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH17_DATA = [
    # ── Slokas 1-2: 6th lord placement ──────────────────────────────────────
    ("h6_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [],
     "unfavorable", "moderate",
     ["enemies_litigation", "physical_health"],
     ["bphs", "parashari", "h6_lord", "kendra_trikona", "enemies"],
     "Ch.17 v.1",
     "6th lord in kendra/trikona is unfavorable — it brings the significations "
     "of the 6th house (enemies, disease, debt) into the most important "
     "houses. The native faces opposition in career, health issues affecting "
     "success, and persistent adversaries in positions of influence",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h6_lord", "lordship_placement", [6],
     [],
     "favorable", "moderate",
     ["enemies_litigation"],
     ["bphs", "parashari", "h6_lord", "own_house", "victory_enemies"],
     "Ch.17 v.2",
     "6th lord in own house (6th): the native conquers enemies, overcomes "
     "disease, and repays debts. Viparita Raja Yoga potential. Maternal "
     "uncle prospers. The native excels in competitive or service-oriented "
     "fields and develops strong immunity",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 3-8: Specific planets in 6th ─────────────────────────────────
    # Malefics in 6th (upachaya) — generally favorable per BPHS.
    ("mars", "house_placement", [6],
     [],
     "favorable", "strong",
     ["enemies_litigation", "career_status"],
     ["bphs", "parashari", "mars", "h6", "enemy_destroyer"],
     "Ch.17 v.3",
     "Mars in 6th (karaka for enemies in upachaya): destroys enemies "
     "completely, gives victory in litigation and competition, military "
     "or surgical career, strong immunity to disease. One of Mars's best "
     "placements. The native never backs down from a fight",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    ("saturn", "house_placement", [6],
     [],
     "favorable", "moderate",
     ["enemies_litigation", "career_status"],
     ["bphs", "parashari", "saturn", "h6", "service", "endurance"],
     "Ch.17 v.4",
     "Saturn in 6th (upachaya): gives victory over enemies through patience "
     "and persistence. Success in service-oriented career, legal matters, "
     "and labor management. The native outlasts all opponents. Good for "
     "doctors, lawyers, and administrators dealing with conflict",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("sun", "house_placement", [6],
     [],
     "favorable", "moderate",
     ["enemies_litigation", "career_status"],
     ["bphs", "parashari", "sun", "h6", "authority_over_enemies"],
     "Ch.17 v.5",
     "Sun in 6th: authority over enemies, government support in disputes, "
     "victory through royal/governmental backing. Father may have health "
     "issues but native personally defeats all opposition",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # Benefics in 6th — generally unfavorable per BPHS.
    ("jupiter", "house_placement", [6],
     [],
     "unfavorable", "moderate",
     ["enemies_litigation", "wealth"],
     ["bphs", "parashari", "jupiter", "h6", "enemies_thrive"],
     "Ch.17 v.6",
     "Jupiter in 6th: enemies are powerful and well-resourced. The native "
     "faces opposition from learned or religious people. Debts from "
     "overspending on dharmic activities. Maternal uncle may have "
     "disputes with the native. Digestive health issues",
     ["Saravali"],
     "Diverges from general principle that Jupiter is always benefic — "
     "in 6th house, Jupiter empowers enemies rather than the native",
     [], [],
     [],
    ),
    ("venus", "house_placement", [6],
     [],
     "unfavorable", "moderate",
     ["enemies_litigation", "marriage"],
     ["bphs", "parashari", "venus", "h6", "romantic_enemies"],
     "Ch.17 v.7",
     "Venus in 6th: enemies arise through romantic or marital matters. "
     "Disputes with spouse or partners. Health issues related to "
     "reproductive system or kidneys. The native spends on litigation "
     "or service. May serve in healthcare or beauty industry",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("moon", "house_placement", [6],
     [{"condition": "waning_or_afflicted", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "moderate",
     ["mental_health", "physical_health"],
     ["bphs", "parashari", "moon", "h6", "mental_enemies", "disease"],
     "Ch.17 v.8",
     "Moon in 6th: mental enemies — worry, anxiety, and psychosomatic "
     "illness. Waning Moon amplifies health problems. Stomach and "
     "digestive complaints. The native's enemies attack through emotional "
     "manipulation. Mother may have health issues",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 9-14: 6th lord positions and compound rules ──────────────────
    ("h6_lord", "lordship_placement", [12],
     [],
     "favorable", "moderate",
     ["enemies_litigation"],
     ["bphs", "parashari", "h6_lord", "h12", "viparita_raja_yoga"],
     "Ch.17 v.9",
     "6th lord in 12th: Viparita Raja Yoga — dusthana lord in dusthana. "
     "Enemies destroy themselves, diseases resolve on their own, debts "
     "are cleared. The native benefits from others' misfortune. An "
     "unexpectedly favorable placement",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("h6_lord", "lordship_placement", [8],
     [],
     "mixed", "moderate",
     ["enemies_litigation", "longevity"],
     ["bphs", "parashari", "h6_lord", "h8", "chronic_disease"],
     "Ch.17 v.10",
     "6th lord in 8th: chronic or lingering diseases, enemies who persist "
     "across long periods, hidden debts. But also Viparita Raja Yoga "
     "potential — dusthana lord in dusthana can give unexpected gains",
     [],
     "",
     [], [],
     [],
    ),
    ("rahu", "house_placement", [6],
     [],
     "favorable", "moderate",
     ["enemies_litigation"],
     ["bphs", "parashari", "rahu", "h6", "unconventional_victory"],
     "Ch.17 v.11",
     "Rahu in 6th: victory over enemies through unconventional or foreign "
     "means. The native outsmarts opponents. Success in dealing with foreign "
     "elements, technology, or taboo subjects. Strong immunity to poison "
     "and environmental toxins",
     [],
     "",
     [], [],
     [],
    ),
    ("ketu", "house_placement", [6],
     [],
     "favorable", "moderate",
     ["enemies_litigation", "spirituality"],
     ["bphs", "parashari", "ketu", "h6", "spiritual_victory"],
     "Ch.17 v.12",
     "Ketu in 6th: spiritual victory over enemies — the native transcends "
     "conflict rather than fighting it. Enemies become irrelevant. Strong "
     "healing abilities, resistance to disease, and capacity to overcome "
     "obstacles through detachment and inner strength",
     [],
     "",
     [], [],
     [],
    ),
    ("mercury", "house_placement", [6],
     [],
     "mixed", "moderate",
     ["enemies_litigation", "intelligence_education"],
     ["bphs", "parashari", "mercury", "h6", "intellectual_enemies"],
     "Ch.17 v.13",
     "Mercury in 6th: enemies through intellectual disputes, legal or "
     "commercial competition. The native is skilled in debate and legal "
     "matters, but faces constant intellectual opposition. Good for lawyers, "
     "accountants, or analysts. Health: nervous system complaints",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    # 6th lord with malefics in dusthana → complete enemy destruction.
    ("h6_lord", "lordship_placement", [6, 8, 12],
     [{"condition": "conjunct_natural_malefic", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["enemies_litigation"],
     ["bphs", "parashari", "h6_lord", "dusthana", "malefic", "destruction"],
     "Ch.17 v.14",
     "6th lord in any dusthana conjunct a natural malefic: complete "
     "destruction of enemies and obstacles. The malefic energy is directed "
     "at the native's adversaries. Debts are repaid, diseases overcome, "
     "and competitors vanquished. Viparita principle at full strength",
     [],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 18 — Effects of the 7th House (Yuvati Bhava Phala)
# Santhanam Vol 1, 18 slokas. All predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH18_DATA = [
    # ── Slokas 1-3: 7th lord placement → marriage and partnerships ───────────
    ("h7_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [{"condition": "planet_with_strength", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "strong",
     ["marriage"],
     ["bphs", "parashari", "h7_lord", "kendra_trikona", "marriage"],
     "Ch.18 v.1",
     "7th lord strong in kendra/trikona: timely marriage to a virtuous and "
     "compatible spouse. The marriage is happy and enduring. The native "
     "benefits from partnerships in business and personal life",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_placement", [6, 8, 12],
     [],
     "unfavorable", "moderate",
     ["marriage"],
     ["bphs", "parashari", "h7_lord", "dusthana", "marriage_trouble"],
     "Ch.18 v.2",
     "7th lord in dusthana (6/8/12): troubled marriage — disputes, "
     "separation, or spouse's health issues. The native may marry late "
     "or face multiple relationship failures. Business partnerships bring "
     "loss rather than gain",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_placement", [7],
     [],
     "favorable", "strong",
     ["marriage", "wealth"],
     ["bphs", "parashari", "h7_lord", "own_house", "good_marriage"],
     "Ch.18 v.3",
     "7th lord in own house (7th): excellent marriage to a loyal, wealthy, "
     "and compatible spouse. Strong business partnerships. The native "
     "gains through marriage. Sexual happiness and domestic harmony",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 4-10: Specific planets in 7th ────────────────────────────────
    ("venus", "house_placement", [7],
     [],
     "favorable", "strong",
     ["marriage", "physical_appearance"],
     ["bphs", "parashari", "venus", "h7", "beautiful_spouse"],
     "Ch.18 v.4",
     "Venus in 7th: beautiful, charming, and sensual spouse. Happy marriage "
     "with strong physical attraction. The native is skilled in romance "
     "and social interactions. Malavya Yoga potential in kendra. Wealth "
     "through spouse or partnerships",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    ("jupiter", "house_placement", [7],
     [],
     "favorable", "strong",
     ["marriage", "intelligence_education"],
     ["bphs", "parashari", "jupiter", "h7", "learned_spouse"],
     "Ch.18 v.5",
     "Jupiter in 7th: noble, learned, and virtuous spouse. Marriage brings "
     "wisdom, prosperity, and dharmic growth. The spouse is from a good "
     "family. Hamsa Yoga in kendra. Excellent for counselors and advisors",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     [],
    ),
    ("moon", "house_placement", [7],
     [{"condition": "waxing_or_bright", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["marriage", "physical_appearance"],
     ["bphs", "parashari", "moon", "h7", "attractive_spouse"],
     "Ch.18 v.6",
     "Moon in 7th: attractive and emotionally nurturing spouse. The "
     "marriage is emotionally rich but fluctuating. Multiple relationships "
     "possible if Moon is afflicted. Waxing Moon gives a beautiful and "
     "wealthy spouse",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("sun", "house_placement", [7],
     [],
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["bphs", "parashari", "sun", "h7", "dominating_spouse"],
     "Ch.18 v.7",
     "Sun in 7th: the spouse is proud, authoritative, and possibly "
     "dominating. The native's independence is challenged in marriage. "
     "Late marriage possible. But partnerships with government or "
     "authority figures bring career advancement",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("mars", "house_placement", [7],
     [],
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["bphs", "parashari", "mars", "h7", "mangal_dosha", "quarrels"],
     "Ch.18 v.8",
     "Mars in 7th: Mangal Dosha (Kuja Dosha) — quarrels in marriage, "
     "aggressive or domineering spouse, possible separation or loss of "
     "spouse. Physical injuries through partnerships. The native is "
     "passionate but creates conflict in intimate relationships",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     ["if_mars_in_own_or_exaltation_in_h7"],
    ),
    ("saturn", "house_placement", [7],
     [],
     "unfavorable", "moderate",
     ["marriage"],
     ["bphs", "parashari", "saturn", "h7", "delayed_marriage"],
     "Ch.18 v.9",
     "Saturn in 7th: significantly delayed marriage, older or mature spouse, "
     "cold or emotionally distant marital relationship. The spouse may be "
     "of lower status or from a different background. Marriage improves "
     "with age. Sasa Yoga potential in kendra",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     ["if_saturn_in_own_or_exaltation"],
    ),
    ("rahu", "house_placement", [7],
     [],
     "unfavorable", "moderate",
     ["marriage"],
     ["bphs", "parashari", "rahu", "h7", "unconventional_marriage"],
     "Ch.18 v.10",
     "Rahu in 7th: unconventional marriage — spouse may be from foreign "
     "or different cultural background. Deception or illusion in "
     "partnerships. Multiple marriages possible. The native is attracted "
     "to unusual or taboo relationships",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 11-14: 7th lord positions ────────────────────────────────────
    ("h7_lord", "lordship_placement", [1],
     [],
     "favorable", "moderate",
     ["marriage", "physical_appearance"],
     ["bphs", "parashari", "h7_lord", "h1", "spouse_influence"],
     "Ch.18 v.11",
     "7th lord in 1st: spouse strongly influences native's personality "
     "and life direction. The native is attractive, socially oriented, "
     "and gains through marriage. Early or predestined marriage",
     [],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_placement", [2],
     [],
     "favorable", "moderate",
     ["wealth", "marriage"],
     ["bphs", "parashari", "h7_lord", "h2", "wealth_through_spouse"],
     "Ch.18 v.12",
     "7th lord in 2nd: wealth through spouse and marriage. The native's "
     "family grows wealthier after marriage. Spouse contributes to family "
     "finances. Good food habits and family harmony through partnership",
     [],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_placement", [10],
     [],
     "favorable", "strong",
     ["career_status", "marriage"],
     ["bphs", "parashari", "h7_lord", "h10", "career_through_partner"],
     "Ch.18 v.13",
     "7th lord in 10th: career advancement through spouse or business "
     "partner. The native's professional rise is connected to marriage. "
     "Excellent kendra-kendra exchange",
     [],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_placement", [12],
     [],
     "mixed", "moderate",
     ["marriage", "foreign_travel"],
     ["bphs", "parashari", "h7_lord", "h12", "spouse_abroad"],
     "Ch.18 v.14",
     "7th lord in 12th: spouse from foreign land, or spouse lives abroad. "
     "Bed pleasures are emphasized. Marriage involves expenditure or loss. "
     "Separation from spouse due to foreign residence is likely",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 15-18: Compound conditions ────────────────────────────────────
    ("venus", "karaka_condition", "venus_as_h7_karaka",
     [{"condition": "afflicted_by_natural_malefics", "effect": "negates", "strength": "strong"},
      {"condition": "h7_lord_simultaneously_weak", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["marriage"],
     ["bphs", "parashari", "venus", "karaka", "h7", "marriage_denial"],
     "Ch.18 v.15",
     "Venus (7th house karaka) afflicted AND 7th lord weak: serious marriage "
     "problems — denial, multiple failures, or spouse's death. Double "
     "affliction leaves no protective factor for marriage",
     ["Saravali"],
     "",
     [], [],
     ["if_jupiter_aspects_venus_or_h7"],
    ),
    ("h7_lord", "lordship_dignity_condition", "h7_lord_any_house",
     [{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["marriage", "wealth"],
     ["bphs", "parashari", "h7_lord", "exalted", "ideal_marriage"],
     "Ch.18 v.16",
     "7th lord exalted: ideal marriage to a wealthy, virtuous, and "
     "supportive spouse. Partnerships bring great fortune. The spouse's "
     "status elevates the native",
     [],
     "",
     [], [],
     [],
    ),
    ("h7_lord", "lordship_dignity_condition", "h7_lord_any_house",
     [{"condition": "debilitated", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["marriage"],
     ["bphs", "parashari", "h7_lord", "debilitated", "bad_marriage"],
     "Ch.18 v.17",
     "7th lord debilitated: unhappy marriage to a spouse of questionable "
     "character or poor health. The native may face humiliation through "
     "partnerships. Marriage brings loss rather than gain",
     [],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),
    ("ketu", "house_placement", [7],
     [],
     "mixed", "moderate",
     ["marriage", "spirituality"],
     ["bphs", "parashari", "ketu", "h7", "detached_marriage"],
     "Ch.18 v.18",
     "Ketu in 7th: detachment from marriage, spiritual orientation in "
     "partnerships, or unconventional spouse. The native may prefer "
     "solitude over partnership. If married, the relationship has a "
     "karmic or past-life quality. Spouse may be spiritually inclined",
     [],
     "",
     [], [],
     [],
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 19 — Effects of the 8th House (Randhra Bhava Phala)
# Santhanam Vol 1, 19 slokas. All predictive.
# ═══════════════════════════════════════════════════════════════════════════════

_CH19_DATA = [
    # ── Slokas 1-3: 8th lord placement → longevity ──────────────────────────
    ("h8_lord", "lordship_placement", [1, 4, 5, 7, 9, 10],
     [],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "h8_lord", "kendra_trikona", "health_damage"],
     "Ch.19 v.1",
     "8th lord in kendra/trikona: brings death-like experiences, chronic "
     "health issues, and transformative crises into the most important "
     "life areas. Unlike 6th lord, 8th lord in good houses damages those "
     "houses rather than benefiting the native",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("h8_lord", "lordship_placement", [8],
     [],
     "favorable", "moderate",
     ["longevity"],
     ["bphs", "parashari", "h8_lord", "own_house", "long_life"],
     "Ch.19 v.2",
     "8th lord in own house (8th): long life — the lord protects its own "
     "house. Viparita Raja Yoga potential. The native has strong recuperative "
     "powers and overcomes life-threatening situations. Interest in occult "
     "and mystical subjects is rewarded",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("h8_lord", "lordship_placement", [6, 12],
     [],
     "mixed", "moderate",
     ["longevity"],
     ["bphs", "parashari", "h8_lord", "dusthana", "viparita_potential"],
     "Ch.19 v.3",
     "8th lord in 6th or 12th: Viparita Raja Yoga — dusthana lord in "
     "dusthana. Diseases resolve, death is averted, and the native may "
     "unexpectedly benefit from crises. Enemies' schemes backfire. "
     "However, chronic low-grade health issues persist",
     ["Phaladeepika"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 4-9: Specific planets in 8th ─────────────────────────────────
    ("saturn", "house_placement", [8],
     [],
     "mixed", "moderate",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "saturn", "h8", "long_life", "chronic"],
     "Ch.19 v.4",
     "Saturn in 8th: long life but with chronic health issues — joint pain, "
     "slow-developing diseases, and periodic crises. The native has strong "
     "endurance and survives what others cannot. Interest in death, mysticism, "
     "and hidden matters. Inheritance may be delayed or disputed",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("mars", "house_placement", [8],
     [],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "mars", "h8", "accidents", "surgery"],
     "Ch.19 v.5",
     "Mars in 8th: danger from accidents, surgery, fire, or violence. "
     "Short life if unmitigated by benefic aspects. Blood-related diseases, "
     "piles, or injuries to genitals. However, the native may excel in "
     "surgery, research, or investigation",
     ["Saravali", "Phaladeepika", "Brihat Jataka"],
     "",
     [], [],
     ["if_mars_in_own_sign_scorpio_in_h8"],
    ),
    ("sun", "house_placement", [8],
     [],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "sun", "h8", "eye_disease", "few_children"],
     "Ch.19 v.6",
     "Sun in 8th: eye diseases, few children, reduced longevity. "
     "Strained relationship with father. Government or authority may "
     "cause trouble. But also: inheritance from father, interest in "
     "psychology and hidden knowledge",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("moon", "house_placement", [8],
     [{"condition": "waning_or_afflicted", "effect": "amplifies", "strength": "strong"}],
     "unfavorable", "moderate",
     ["longevity", "mental_health"],
     ["bphs", "parashari", "moon", "h8", "short_life", "anxiety"],
     "Ch.19 v.7",
     "Moon in 8th: short life if waning and afflicted. Mental anxiety, "
     "fear of death, emotional crises. The native is drawn to the occult "
     "but suffers psychologically. Phlegmatic and waterborne diseases. "
     "Mother's health is poor",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("jupiter", "house_placement", [8],
     [],
     "favorable", "moderate",
     ["longevity", "intelligence_education"],
     ["bphs", "parashari", "jupiter", "h8", "long_life", "occult_wisdom"],
     "Ch.19 v.8",
     "Jupiter in 8th: long life — Jupiter as the greatest benefic protects "
     "the house of longevity. Deep wisdom about death, transformation, and "
     "hidden matters. Interest in astrology, occult sciences, and research. "
     "Inheritance through righteous means",
     ["Saravali", "Phaladeepika"],
     "",
     [], [],
     [],
    ),
    ("venus", "house_placement", [8],
     [],
     "mixed", "moderate",
     ["longevity", "wealth"],
     ["bphs", "parashari", "venus", "h8", "comfortable_death", "inheritance"],
     "Ch.19 v.9",
     "Venus in 8th: long life, comfortable death (not violent). Wealth "
     "through inheritance, insurance, or spouse's resources. Sexual "
     "intensity and interest in tantric practices. The native may face "
     "hidden romantic relationships",
     ["Saravali"],
     "",
     [], [],
     [],
    ),

    # ── Slokas 10-13: More planets and lord positions ────────────────────────
    ("mercury", "house_placement", [8],
     [],
     "mixed", "moderate",
     ["longevity", "intelligence_education"],
     ["bphs", "parashari", "mercury", "h8", "research", "nervous_disease"],
     "Ch.19 v.10",
     "Mercury in 8th: interest in research, investigation, and forensic "
     "sciences. Nervous system diseases. The native's intelligence is "
     "directed toward hidden matters. May excel in insurance, taxation, "
     "or detective work. Moderate longevity",
     ["Saravali"],
     "",
     [], [],
     [],
    ),
    ("rahu", "house_placement", [8],
     [],
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["bphs", "parashari", "rahu", "h8", "sudden_death", "poison"],
     "Ch.19 v.11",
     "Rahu in 8th: danger of sudden or unnatural death — accidents, "
     "poisoning, snake bite, or mysterious causes. Chronic hard-to-diagnose "
     "diseases. Fear and anxiety about death. However, strong interest "
     "in occult, tantra, and paranormal phenomena",
     [],
     "",
     [], [],
     ["if_rahu_aspected_by_jupiter"],
    ),
    ("ketu", "house_placement", [8],
     [],
     "mixed", "moderate",
     ["longevity", "spirituality"],
     ["bphs", "parashari", "ketu", "h8", "moksha", "mystical_death"],
     "Ch.19 v.12",
     "Ketu in 8th: strong moksha karaka placement. The native is drawn "
     "to liberation, past-life regression, and mystical experiences. "
     "Death may be peaceful or spiritually significant. Chronic skin "
     "or mysterious ailments. Detachment from material inheritance",
     [],
     "",
     [], [],
     [],
    ),
    ("h8_lord", "lordship_placement", [1],
     [],
     "unfavorable", "moderate",
     ["physical_health", "longevity"],
     ["bphs", "parashari", "h8_lord", "h1", "sickly_body"],
     "Ch.19 v.13",
     "8th lord in 1st: sickly body, chronic health problems that define "
     "the native's personality. Life is marked by transformative crises. "
     "However, the native develops strong survival instincts and may "
     "become a healer or researcher",
     [],
     "",
     [], [],
     [],
    ),

    # ── Slokas 14-19: Compound conditions and dignity ────────────────────────
    ("h8_lord", "lordship_placement", [10],
     [],
     "unfavorable", "moderate",
     ["career_status"],
     ["bphs", "parashari", "h8_lord", "h10", "career_disruption"],
     "Ch.19 v.14",
     "8th lord in 10th: career disruptions, scandals, or sudden falls "
     "from position. The native's career involves death, insurance, "
     "taxation, or research. Professional life is marked by upheavals "
     "but also deep transformation",
     [],
     "",
     [], [],
     [],
    ),
    ("h8_lord", "lordship_dignity_condition", "h8_lord_any_house",
     [{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
     "favorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "h8_lord", "exalted", "very_long_life"],
     "Ch.19 v.15",
     "8th lord exalted: very long life, strong regenerative powers, and "
     "the native survives all crises. Inheritance is substantial. Hidden "
     "wealth and resources. The native may have healing or occult powers",
     [],
     "",
     [], [],
     [],
    ),
    ("h8_lord", "lordship_dignity_condition", "h8_lord_any_house",
     [{"condition": "debilitated", "effect": "negates", "strength": "strong"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "h8_lord", "debilitated", "short_life"],
     "Ch.19 v.16",
     "8th lord debilitated: shortened lifespan, vulnerability to chronic "
     "disease, and difficulty recovering from crises. Inheritance is "
     "lost or never received. The native faces repeated near-death "
     "experiences without the strength to fully recover",
     [],
     "",
     [], [],
     ["if_neecha_bhanga_raja_yoga"],
    ),
    # Saturn (karaka for longevity) afflicted + 8th lord weak → short life.
    ("saturn", "karaka_condition", "saturn_as_longevity_karaka",
     [{"condition": "afflicted_by_natural_malefics", "effect": "negates", "strength": "strong"},
      {"condition": "h8_lord_simultaneously_weak", "effect": "amplifies", "strength": "moderate"}],
     "unfavorable", "strong",
     ["longevity"],
     ["bphs", "parashari", "saturn", "karaka", "h8", "short_life"],
     "Ch.19 v.17",
     "Saturn (longevity karaka) afflicted AND 8th lord weak: severely "
     "shortened life. The double affliction removes both the karaka and "
     "lord protection for the house of longevity. The native is vulnerable "
     "to fatal illness or accidents",
     [],
     "",
     [], [],
     ["if_jupiter_aspects_saturn_or_h8"],
    ),
    # 8th lord with benefics → protected longevity.
    ("h8_lord", "lordship_aspect_condition", "h8_lord_any_placement",
     [{"condition": "conjunct_or_aspected_by_natural_benefics", "effect": "amplifies", "strength": "moderate"}],
     "favorable", "moderate",
     ["longevity"],
     ["bphs", "parashari", "h8_lord", "benefic", "protected_longevity"],
     "Ch.19 v.18",
     "8th lord conjunct/aspected by benefics: protected longevity — crises "
     "are survived, diseases are cured, and death is delayed. The native "
     "has guardian angels or timely interventions that save their life",
     [],
     "",
     [], [],
     [],
    ),
    # Lagna lord + 8th lord exchange → major life transformation.
    ("lagna_lord", "lordship_aspect_condition", "lagna_lord_h8_lord_exchange",
     [{"condition": "mutual_exchange_with_h8_lord", "effect": "conditionalizes", "strength": "strong"}],
     "mixed", "strong",
     ["longevity", "career_status"],
     ["bphs", "parashari", "lagna_lord", "h8_lord", "parivartana"],
     "Ch.19 v.19",
     "Lagna lord and 8th lord in mutual exchange (parivartana): the native's "
     "identity is inseparable from transformation, death/rebirth experiences, "
     "and hidden matters. Life is marked by dramatic upheavals that ultimately "
     "strengthen the native. Career in occult, medicine, or investigation",
     [],
     "",
     [], [],
     [],
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder — same structure as bphs_1b_houses_1.py
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
            last_modified_session="S307",
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    """Build all BPHS Ch.16-19 rules."""
    result: list[RuleRecord] = []
    result.extend(_make_house_rules(
        _CH16_DATA, 400, "Ch.16", "5th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH17_DATA, 500, "Ch.17", "6th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH18_DATA, 600, "Ch.18", "7th_house_effects",
    ))
    result.extend(_make_house_rules(
        _CH19_DATA, 700, "Ch.19", "8th_house_effects",
    ))
    return result


BPHS_1B_HOUSES_2_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    BPHS_1B_HOUSES_2_REGISTRY.add(_rule)
