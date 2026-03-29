"""
src/corpus/laghu_parashari_functional.py — Laghu Parashari Functional Nature Table (S264)

Section A of docs/coverage_maps/laghu_parashari.md.
108 rules (LPF001–LPF108): functional classification of 9 planets × 12 lagnas.

For each lagna, each of the 9 planets is classified as:
  yogakaraka        — owns one kendra (H4/H7/H10) AND one trikona (H5/H9) — strongly favorable
  lagna_lord        — owns H1 (first consideration; may also own dusthana)
  trikona_lord      — owns H5 or H9, conferring functional beneficence
  trikona_dusthana  — owns trikona AND dusthana (trikona dominates; benefic with reservation)
  kendra_lord       — natural malefic owning kendra only (temporal neutral/mildly positive)
  kendradhipati     — natural benefic owning kendra (4/7/10) but no trikona (loses beneficence)
  functional_malefic — owns dusthana (H6/H8/H12) with no balancing trikona
  maraka            — primarily owns H2 or H7 (death-inflicting in dasha)
  chameleon         — Rahu/Ketu: adopts nature of dispositor

Phase 1B schema:
  phase = "1B_conditional" (all rules are lagna-conditional)
  lagna_scope = [lagna] for each rule
  primary_condition = {planet, placement_type: "house_lordship", placement_value: [houses], for_lagna: lagna}
  verse_ref = "Ch.1 v.N" (best-effort; verse refs are navigation aids, see PHASE1B_RULE_CONTRACT.md)
  concordance_texts = [] (LP functional nature table is not encoded in Phase 1A)

Registry: LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
"""

from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ── Functional nature data table ─────────────────────────────────────────────
# Format per planet entry:
#   houses: list of house numbers owned (for this lagna)
#   func:   functional classification string
#   odirs:  outcome_direction
#   oint:   outcome_intensity
#   odoms:  outcome_domains (from taxonomy)
#   desc:   plain-language suffix for description
#
# Planets in order: sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu
# (rule IDs: +1, +2, +3, +4, +5, +6, +7, +8, +9 within each lagna block)

_TABLE: dict[str, list[dict]] = {
    "aries": [
        # Sun → H5 (trikona)
        {"planet": "sun",     "houses": [5],      "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "intelligence_education"],
         "desc": "Sun as 5th lord (trikona) is a functional benefic for Aries lagna; its dasha produces intelligence, purva punya, and spiritual inclinations."},
        # Moon → H4 (kendra, natural benefic)
        {"planet": "moon",    "houses": [4],      "func": "kendradhipati",
         "odir": "neutral",   "oint": "weak",
         "odoms": ["mental_health", "property_vehicles"],
         "desc": "Moon as 4th lord (kendra) suffers kendradhipati dosha for Aries lagna — a natural benefic owning a kendra loses its natural beneficence; results become mixed in its dasha."},
        # Mars → H1+H8 (lagna lord + dusthana)
        {"planet": "mars",    "houses": [1, 8],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Mars as lagna lord (H1) and 8th lord for Aries — lagna lordship dominates; Mars dasha is generally favorable for Aries natives, though the H8 co-ownership introduces some obstacles and longevity themes."},
        # Mercury → H3+H6 (upachaya + dusthana)
        {"planet": "mercury", "houses": [3, 6],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "physical_health"],
         "desc": "Mercury as 3rd and 6th lord for Aries lagna is a functional malefic — ownership of H6 (dusthana: enemies, disease) makes Mercury's dasha produce obstructions, conflicts, and health issues."},
        # Jupiter → H9+H12 (trikona + dusthana)
        {"planet": "jupiter", "houses": [9, 12],  "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Jupiter as 9th and 12th lord for Aries — H9 trikona lordship makes Jupiter a functional benefic despite H12 dusthana ownership; its dasha produces dharma, fortune, and spiritual growth, with some foreign or expenditure themes from H12."},
        # Venus → H2+H7 (maraka + kendra, natural benefic)
        {"planet": "venus",   "houses": [2, 7],   "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "marriage"],
         "desc": "Venus as 2nd and 7th lord for Aries is a maraka — it owns both maraka houses (H2 and H7) and is additionally a kendradhipati (natural benefic owning H7 kendra). Venus dasha can trigger health crises and is significant in longevity calculations."},
        # Saturn → H10+H11 (kendra + upachaya)
        {"planet": "saturn",  "houses": [10, 11], "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["career_status", "wealth"],
         "desc": "Saturn as 10th and 11th lord for Aries lagna is a functional malefic — it is the temporal enemy of Aries (Mars-ruled lagna) and owns neither a trikona; its dasha tends to produce delays, obstacles, and adversarial conditions despite kendra ownership."},
        # Rahu → chameleon
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu has no fixed house lordship in Laghu Parashari; for Aries lagna it acts as a chameleon, adopting the functional nature of its sign dispositor. Results in Rahu dasha depend entirely on the strength and nature of the dispositor planet."},
        # Ketu → chameleon
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu has no fixed house lordship in Laghu Parashari; for Aries lagna it acts as a chameleon, adopting the functional nature of its sign dispositor. Ketu's dasha results depend on its dispositor's strength and the houses it occupies."},
    ],

    "taurus": [
        # Sun → H4 (kendra, natural malefic)
        {"planet": "sun",     "houses": [4],      "func": "kendra_lord",
         "odir": "neutral",   "oint": "weak",
         "odoms": ["property_vehicles", "mental_health"],
         "desc": "Sun as 4th lord (kendra) for Taurus lagna — a natural malefic owning a kendra gains some temporal strength; Sun dasha produces mixed domestic and property results; not a trikona lord so not a functional benefic."},
        # Moon → H3 (upachaya)
        {"planet": "moon",    "houses": [3],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "weak",
         "odoms": ["character_temperament"],
         "desc": "Moon as 3rd lord for Taurus lagna — H3 ownership gives Moon a mildly malefic functional nature; its dasha produces courage-related themes but the 3rd house is considered inimical to natural benefics in LP tradition."},
        # Mars → H7+H12 (maraka + dusthana)
        {"planet": "mars",    "houses": [7, 12],  "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "foreign_travel"],
         "desc": "Mars as 7th and 12th lord for Taurus lagna is a maraka — H7 lordship confers maraka status, and H12 dusthana ownership makes Mars functionally malefic; its dasha can trigger losses, foreign separation, and health vulnerabilities."},
        # Mercury → H2+H5 (maraka + trikona)
        {"planet": "mercury", "houses": [2, 5],   "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["intelligence_education", "progeny", "wealth"],
         "desc": "Mercury as 2nd and 5th lord for Taurus — H5 trikona lordship makes Mercury a functional benefic; its dasha produces intelligence, children-related results, and wealth accumulation; H2 ownership adds a maraka dimension but trikona lordship dominates."},
        # Jupiter → H8+H11 (dusthana + upachaya)
        {"planet": "jupiter", "houses": [8, 11],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Jupiter as 8th and 11th lord for Taurus is a functional malefic — H8 dusthana ownership is particularly damaging; despite being a natural benefic, Jupiter's dasha for Taurus tends to produce obstacles, delays, and longevity concerns."},
        # Venus → H1+H6 (lagna lord + dusthana)
        {"planet": "venus",   "houses": [1, 6],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Venus as lagna lord (H1) for Taurus — lagna lordship is paramount; Venus dasha is generally favorable for Taurus natives in terms of personality, appearance, and overall wellbeing; H6 co-ownership introduces some health or conflict themes."},
        # Saturn → H9+H10 (trikona + kendra) = YOGAKARAKA
        {"planet": "saturn",  "houses": [9, 10],  "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "fame_reputation"],
         "desc": "Saturn as 9th and 10th lord is the yogakaraka for Taurus lagna — owning both a trikona (H9: dharma/fortune) and a kendra (H10: karma/career) simultaneously, Saturn's dasha produces exceptional career advancement, wealth, and lasting fame for Taurus natives."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Taurus lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Taurus lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "gemini": [
        # Sun → H3
        {"planet": "sun",     "houses": [3],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "weak",
         "odoms": ["character_temperament"],
         "desc": "Sun as 3rd lord for Gemini lagna has a mildly malefic functional nature — H3 upachaya ownership without trikona; its dasha produces themes of effort, siblings, and communication but is not strongly beneficial."},
        # Moon → H2 (maraka)
        {"planet": "moon",    "houses": [2],      "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Moon as 2nd lord for Gemini lagna is a maraka — H2 lordship confers death-inflicting potential; Moon dasha can bring wealth accumulation themes but also health vulnerabilities and longevity concerns."},
        # Mars → H6+H11 (dusthana + upachaya)
        {"planet": "mars",    "houses": [6, 11],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "wealth"],
         "desc": "Mars as 6th and 11th lord for Gemini is a functional malefic — H6 dusthana ownership makes Mars produce conflicts, enemies, and health issues in its dasha; the 11th house gains theme is overshadowed by the 6th house's malefic nature."},
        # Mercury → H1+H4 (lagna lord + kendra, natural benefic)
        {"planet": "mercury", "houses": [1, 4],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament", "property_vehicles"],
         "desc": "Mercury as lagna lord and 4th lord for Gemini — lagna lordship is paramount; Mercury dasha is generally favorable; H4 co-ownership as a natural benefic technically creates a minor kendradhipati situation but lagna lordship outweighs this."},
        # Jupiter → H7+H10 (two kendras, natural benefic) = strong kendradhipati
        {"planet": "jupiter", "houses": [7, 10],  "func": "kendradhipati",
         "odir": "neutral",   "oint": "moderate",
         "odoms": ["marriage", "career_status"],
         "desc": "Jupiter as 7th and 10th lord for Gemini lagna suffers strong kendradhipati dosha — owning two kendra houses (both H7 and H10) as a natural benefic causes significant loss of natural beneficence; Jupiter dasha produces mixed career and marriage results; H7 also makes Jupiter a maraka."},
        # Venus → H5+H12 (trikona + dusthana)
        {"planet": "venus",   "houses": [5, 12],  "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["progeny", "intelligence_education", "foreign_travel"],
         "desc": "Venus as 5th and 12th lord for Gemini — H5 trikona lordship makes Venus a functional benefic; its dasha produces intelligence, creative expression, and purva punya themes; H12 co-ownership introduces foreign travel or expenditure subthemes."},
        # Saturn → H8+H9 (dusthana + trikona)
        {"planet": "saturn",  "houses": [8, 9],   "func": "trikona_dusthana",
         "odir": "mixed",     "oint": "moderate",
         "odoms": ["spirituality", "wealth", "longevity"],
         "desc": "Saturn as 8th and 9th lord for Gemini presents a tension — H9 trikona confers some dharmic and fortune results, but H8 dusthana ownership is severely problematic; Saturn's dasha for Gemini is mixed, with spiritual and fortune themes but also longevity concerns and transformative events."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Gemini lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Gemini lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "cancer": [
        # Sun → H2 (maraka)
        {"planet": "sun",     "houses": [2],      "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Sun as 2nd lord for Cancer lagna is a maraka — H2 lordship confers death-inflicting potential; Sun dasha brings wealth and family themes but also longevity concerns and health vulnerabilities."},
        # Moon → H1 (lagna lord)
        {"planet": "moon",    "houses": [1],      "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Moon as lagna lord for Cancer — Moon dasha is highly significant for Cancer natives, activating self, health, and personality themes; the native's mind and emotional wellbeing are highlighted."},
        # Mars → H5+H10 (trikona + kendra) = YOGAKARAKA
        {"planet": "mars",    "houses": [5, 10],  "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "fame_reputation", "progeny"],
         "desc": "Mars as 5th and 10th lord is the yogakaraka for Cancer lagna — owning trikona (H5: intelligence/progeny) and kendra (H10: career/status), Mars dasha produces raja yoga results: exceptional career advancement, recognition, and lasting achievements for Cancer natives."},
        # Mercury → H3+H12 (upachaya + dusthana)
        {"planet": "mercury", "houses": [3, 12],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["foreign_travel", "enemies_litigation"],
         "desc": "Mercury as 3rd and 12th lord for Cancer is a functional malefic — H12 dusthana ownership makes Mercury's dasha produce losses, foreign separation, and expenditure themes; H3 upachaya ownership adds effort-related themes."},
        # Jupiter → H6+H9 (dusthana + trikona)
        {"planet": "jupiter", "houses": [6, 9],   "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Jupiter as 6th and 9th lord for Cancer — H9 trikona makes Jupiter a functional benefic despite H6 dusthana ownership; its dasha produces dharmic blessings and fortune, with some conflict or health subthemes from H6."},
        # Venus → H4+H11 (kendra + upachaya, natural benefic)
        {"planet": "venus",   "houses": [4, 11],  "func": "kendradhipati",
         "odir": "neutral",   "oint": "weak",
         "odoms": ["property_vehicles", "wealth", "mental_health"],
         "desc": "Venus as 4th and 11th lord for Cancer — H4 kendra ownership as a natural benefic creates kendradhipati dosha; Venus loses natural beneficence; its dasha produces mixed results with property and material gain themes overshadowed by reduced beneficence."},
        # Saturn → H7+H8 (maraka + dusthana)
        {"planet": "saturn",  "houses": [7, 8],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "strong",
         "odoms": ["longevity", "marriage"],
         "desc": "Saturn as 7th and 8th lord for Cancer lagna is among the most malefic planets — owning both a maraka house (H7) and a severe dusthana (H8); Saturn dasha for Cancer natives carries significant longevity concerns, partnership difficulties, and transformative hardships."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Cancer lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Cancer lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "leo": [
        # Sun → H1 (lagna lord)
        {"planet": "sun",     "houses": [1],      "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament", "fame_reputation"],
         "desc": "Sun as lagna lord for Leo — Sun dasha is highly significant; it activates self, personality, vitality, and authority themes; Leo natives experience identity consolidation and leadership expression during Sun dasha."},
        # Moon → H12 (dusthana)
        {"planet": "moon",    "houses": [12],     "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["foreign_travel", "mental_health"],
         "desc": "Moon as 12th lord for Leo is a functional malefic — H12 dusthana ownership makes Moon's dasha produce isolation, foreign separation, expenditure, and mental strain themes."},
        # Mars → H4+H9 (kendra + trikona) = YOGAKARAKA
        {"planet": "mars",    "houses": [4, 9],   "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "spirituality", "property_vehicles"],
         "desc": "Mars as 4th and 9th lord is the yogakaraka for Leo lagna — owning kendra (H4: domestic happiness/property) and trikona (H9: dharma/fortune), Mars dasha produces exceptional raja yoga results including property acquisition, fortune, and dharmic advancement for Leo natives."},
        # Mercury → H2+H11 (maraka + upachaya)
        {"planet": "mercury", "houses": [2, 11],  "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Mercury as 2nd and 11th lord for Leo lagna is a maraka — H2 maraka ownership makes Mercury's dasha significant for longevity; H11 gains ownership provides wealth themes but H2 maraka nature dominates the functional classification."},
        # Jupiter → H5+H8 (trikona + dusthana)
        {"planet": "jupiter", "houses": [5, 8],   "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["intelligence_education", "progeny", "spirituality"],
         "desc": "Jupiter as 5th and 8th lord for Leo — H5 trikona lordship makes Jupiter a functional benefic; its dasha produces intelligence, children, and spiritual inclination themes; H8 co-ownership introduces longevity and hidden knowledge subthemes."},
        # Venus → H3+H10 (upachaya + kendra, natural benefic)
        {"planet": "venus",   "houses": [3, 10],  "func": "kendradhipati",
         "odir": "neutral",   "oint": "moderate",
         "odoms": ["career_status", "character_temperament"],
         "desc": "Venus as 3rd and 10th lord for Leo — H10 kendra ownership as a natural benefic creates kendradhipati dosha; Venus loses natural beneficence; its dasha produces mixed career and creative themes."},
        # Saturn → H6+H7 (dusthana + maraka)
        {"planet": "saturn",  "houses": [6, 7],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "strong",
         "odoms": ["longevity", "enemies_litigation", "marriage"],
         "desc": "Saturn as 6th and 7th lord for Leo lagna is highly malefic — owning a dusthana (H6: enemies/disease) and a maraka house (H7); Saturn dasha for Leo natives carries strong longevity concerns, conflict with enemies, and partnership difficulties."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Leo lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Leo lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "virgo": [
        # Sun → H12 (dusthana)
        {"planet": "sun",     "houses": [12],     "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["foreign_travel", "mental_health"],
         "desc": "Sun as 12th lord for Virgo is a functional malefic — H12 dusthana ownership makes Sun's dasha produce expenditure, isolation, foreign themes, and spiritual seeking."},
        # Moon → H11 (upachaya)
        {"planet": "moon",    "houses": [11],     "func": "functional_malefic",
         "odir": "unfavorable", "oint": "weak",
         "odoms": ["wealth"],
         "desc": "Moon as 11th lord for Virgo has a mildly malefic functional nature in LP tradition — upachaya ownership without trikona; Moon dasha brings gains and fulfillment of desires but is not strongly beneficial as a trikona lord."},
        # Mars → H3+H8 (upachaya + dusthana)
        {"planet": "mars",    "houses": [3, 8],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "enemies_litigation"],
         "desc": "Mars as 3rd and 8th lord for Virgo is a functional malefic — H8 severe dusthana ownership makes Mars dasha produce longevity concerns, sudden events, and transformative hardships."},
        # Mercury → H1+H10 (lagna lord + kendra, natural benefic)
        {"planet": "mercury", "houses": [1, 10],  "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "career_status", "character_temperament"],
         "desc": "Mercury as lagna lord and 10th lord for Virgo — lagna lordship is paramount; Mercury dasha is favorable for Virgo natives, activating personality, career, and analytical prowess themes; H10 co-ownership as natural benefic creates minor kendradhipati but lagna lordship overrides."},
        # Jupiter → H4+H7 (two kendras, natural benefic) = strong kendradhipati
        {"planet": "jupiter", "houses": [4, 7],   "func": "kendradhipati",
         "odir": "neutral",   "oint": "moderate",
         "odoms": ["marriage", "property_vehicles", "mental_health"],
         "desc": "Jupiter as 4th and 7th lord for Virgo suffers strong kendradhipati dosha — owning two kendra houses as a natural benefic; Jupiter dasha produces mixed domestic, marriage, and property results; H7 lordship also makes Jupiter a maraka for Virgo."},
        # Venus → H2+H9 (maraka + trikona)
        {"planet": "venus",   "houses": [2, 9],   "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Venus as 2nd and 9th lord for Virgo — H9 trikona lordship makes Venus a functional benefic; its dasha produces dharma, fortune, and wealth themes; H2 ownership adds maraka potential but trikona lordship is the dominant functional characteristic."},
        # Saturn → H5+H6 (trikona + dusthana)
        {"planet": "saturn",  "houses": [5, 6],   "func": "trikona_dusthana",
         "odir": "mixed",     "oint": "moderate",
         "odoms": ["intelligence_education", "progeny", "enemies_litigation"],
         "desc": "Saturn as 5th and 6th lord for Virgo presents a tension — H5 trikona ownership gives some functional beneficence while H6 dusthana ownership introduces malefic themes; Saturn dasha for Virgo is mixed, with intelligence and progeny themes alongside conflict and health issues."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Virgo lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Virgo lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "libra": [
        # Sun → H11 (upachaya)
        {"planet": "sun",     "houses": [11],     "func": "functional_malefic",
         "odir": "unfavorable", "oint": "weak",
         "odoms": ["wealth", "fame_reputation"],
         "desc": "Sun as 11th lord for Libra has a mildly malefic functional nature — upachaya ownership without trikona; Sun is debilitated in Libra's sign (Libra contains H1 for this lagna, not relevant to Sun's ownership); Sun dasha brings gains but the functional nature is not strongly beneficial."},
        # Moon → H10 (kendra, natural benefic)
        {"planet": "moon",    "houses": [10],     "func": "kendradhipati",
         "odir": "neutral",   "oint": "weak",
         "odoms": ["career_status", "fame_reputation"],
         "desc": "Moon as 10th lord for Libra suffers kendradhipati dosha — natural benefic owning kendra H10 loses natural beneficence; Moon dasha produces career and public recognition themes with mixed outcomes."},
        # Mars → H2+H7 (both marakas)
        {"planet": "mars",    "houses": [2, 7],   "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "marriage"],
         "desc": "Mars as 2nd and 7th lord for Libra owns both maraka houses — Mars is the strongest maraka for Libra lagna; its dasha can bring significant longevity challenges and partnership disruptions; Mars is also the temporal enemy of Venus-ruled Libra."},
        # Mercury → H9+H12 (trikona + dusthana)
        {"planet": "mercury", "houses": [9, 12],  "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth", "foreign_travel"],
         "desc": "Mercury as 9th and 12th lord for Libra — H9 trikona lordship makes Mercury a functional benefic despite H12 dusthana co-ownership; Mercury dasha produces dharmic advancement and fortune, with foreign travel or spiritual retreat themes from H12."},
        # Jupiter → H3+H6 (upachaya + dusthana)
        {"planet": "jupiter", "houses": [3, 6],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "physical_health"],
         "desc": "Jupiter as 3rd and 6th lord for Libra is a functional malefic — H6 dusthana ownership is particularly problematic; Jupiter's natural beneficence is undermined by dusthana lordship; its dasha can produce enemies, health issues, and conflict despite Jupiter's natural good nature."},
        # Venus → H1+H8 (lagna lord + dusthana)
        {"planet": "venus",   "houses": [1, 8],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Venus as lagna lord for Libra — lagna lordship is paramount; Venus dasha is generally favorable for Libra natives; H8 co-ownership introduces longevity themes and transformative events but lagna lordship of Venus dominates the functional nature."},
        # Saturn → H4+H5 (kendra + trikona) = YOGAKARAKA
        {"planet": "saturn",  "houses": [4, 5],   "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "intelligence_education", "property_vehicles"],
         "desc": "Saturn as 4th and 5th lord is the yogakaraka for Libra lagna — owning kendra (H4: property/happiness) and trikona (H5: intelligence/purva punya), Saturn's dasha produces outstanding results in domestic happiness, property, intellectual achievements, and wealth for Libra natives."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Libra lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Libra lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "scorpio": [
        # Sun → H10 (kendra, natural malefic)
        {"planet": "sun",     "houses": [10],     "func": "kendra_lord",
         "odir": "favorable",  "oint": "weak",
         "odoms": ["career_status", "fame_reputation"],
         "desc": "Sun as 10th lord for Scorpio lagna — a natural malefic owning kendra H10 gains temporal strength; Sun dasha produces career advancement and public recognition themes; not a yogakaraka (no trikona owned) but has beneficial temporal influence."},
        # Moon → H9 (trikona)
        {"planet": "moon",    "houses": [9],      "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Moon as 9th lord for Scorpio is a functional benefic — H9 trikona ownership makes Moon's dasha produce fortune, dharmic blessings, and spiritual inclinations for Scorpio natives."},
        # Mars → H1+H6 (lagna lord + dusthana)
        {"planet": "mars",    "houses": [1, 6],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Mars as lagna lord and 6th lord for Scorpio — lagna lordship is paramount; Mars dasha is significant for Scorpio natives, activating drive, intensity, and transformation; H6 co-ownership introduces conflict and competition themes, which Mars handles well as a natural malefic."},
        # Mercury → H8+H11 (dusthana + upachaya)
        {"planet": "mercury", "houses": [8, 11],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Mercury as 8th and 11th lord for Scorpio is a functional malefic — H8 severe dusthana ownership makes Mercury's dasha produce longevity concerns, sudden transformative events, and hidden obstacles despite the gains (H11) dimension."},
        # Jupiter → H2+H5 (maraka + trikona)
        {"planet": "jupiter", "houses": [2, 5],   "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["intelligence_education", "progeny", "wealth"],
         "desc": "Jupiter as 2nd and 5th lord for Scorpio — H5 trikona lordship makes Jupiter a functional benefic; its dasha produces intelligence, purva punya, and children themes; H2 maraka ownership applies but trikona lordship of H5 dominates the functional benefic classification."},
        # Venus → H7+H12 (maraka + dusthana)
        {"planet": "venus",   "houses": [7, 12],  "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "marriage", "foreign_travel"],
         "desc": "Venus as 7th and 12th lord for Scorpio is a maraka — H7 lordship confers maraka status and H12 dusthana ownership adds loss/expenditure themes; Venus dasha for Scorpio carries longevity concerns, partnership challenges, and foreign separation themes."},
        # Saturn → H3+H4 (upachaya + kendra)
        {"planet": "saturn",  "houses": [3, 4],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["mental_health", "property_vehicles"],
         "desc": "Saturn as 3rd and 4th lord for Scorpio — Saturn is a natural enemy of Mars-ruled Scorpio; despite owning kendra H4, the lack of trikona ownership and natural enmity makes Saturn a functional malefic; its dasha produces domestic discord, property challenges, and mental strain."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Scorpio lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Scorpio lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "sagittarius": [
        # Sun → H9 (trikona)
        {"planet": "sun",     "houses": [9],      "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth", "fame_reputation"],
         "desc": "Sun as 9th lord for Sagittarius is a functional benefic — H9 trikona lordship makes Sun's dasha produce dharma, fortune, and divine blessings; Sun is exalted in Aries and naturally favors Sagittarius; its dasha elevates status and brings paternal blessings."},
        # Moon → H8 (dusthana)
        {"planet": "moon",    "houses": [8],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "mental_health"],
         "desc": "Moon as 8th lord for Sagittarius is a functional malefic — H8 severe dusthana ownership makes Moon's dasha produce longevity concerns, sudden events, and psychological turbulence."},
        # Mars → H5+H12 (trikona + dusthana)
        {"planet": "mars",    "houses": [5, 12],  "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["progeny", "intelligence_education", "foreign_travel"],
         "desc": "Mars as 5th and 12th lord for Sagittarius — H5 trikona lordship makes Mars a functional benefic; its dasha produces intelligence, purva punya, and children themes; H12 co-ownership adds foreign travel or spiritual retreat dimensions."},
        # Mercury → H7+H10 (two kendras, natural benefic) = strong kendradhipati
        {"planet": "mercury", "houses": [7, 10],  "func": "kendradhipati",
         "odir": "neutral",   "oint": "moderate",
         "odoms": ["marriage", "career_status"],
         "desc": "Mercury as 7th and 10th lord for Sagittarius suffers strong kendradhipati dosha — owning two kendra houses as a natural benefic; Mercury dasha produces mixed career and marriage results; H7 lordship also makes Mercury a maraka for Sagittarius."},
        # Jupiter → H1+H4 (lagna lord + kendra, natural benefic)
        {"planet": "jupiter", "houses": [1, 4],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament", "property_vehicles"],
         "desc": "Jupiter as lagna lord for Sagittarius — Jupiter dasha is highly significant; it activates wisdom, philosophy, and dharmic themes central to Sagittarius nature; H4 co-ownership creates minor kendradhipati but lagna lordship of Jupiter dominates overwhelmingly."},
        # Venus → H6+H11 (dusthana + upachaya)
        {"planet": "venus",   "houses": [6, 11],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "wealth"],
         "desc": "Venus as 6th and 11th lord for Sagittarius is a functional malefic — H6 dusthana ownership makes Venus's dasha produce conflict, health issues, and service themes; H11 gains themes are present but subordinate to the H6 functional malefic nature."},
        # Saturn → H2+H3 (maraka + upachaya)
        {"planet": "saturn",  "houses": [2, 3],   "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Saturn as 2nd and 3rd lord for Sagittarius lagna is a maraka — H2 lordship confers death-inflicting potential; Saturn dasha for Sagittarius carries longevity concerns; H3 upachaya ownership adds effort-related themes; Saturn is also a natural enemy of Jupiter-ruled Sagittarius."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Sagittarius lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Sagittarius lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "capricorn": [
        # Sun → H8 (dusthana)
        {"planet": "sun",     "houses": [8],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "physical_health"],
         "desc": "Sun as 8th lord for Capricorn is a functional malefic — H8 severe dusthana ownership makes Sun's dasha produce longevity concerns, obstacles, and transformative upheavals."},
        # Moon → H7 (maraka + kendra, natural benefic)
        {"planet": "moon",    "houses": [7],      "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "marriage"],
         "desc": "Moon as 7th lord for Capricorn is a maraka — H7 lordship confers death-inflicting potential and kendradhipati dosha (natural benefic owning kendra); Moon dasha carries longevity concerns and partnership themes for Capricorn natives."},
        # Mars → H4+H11 (kendra + upachaya)
        {"planet": "mars",    "houses": [4, 11],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["property_vehicles", "mental_health"],
         "desc": "Mars as 4th and 11th lord for Capricorn — despite owning kendra H4, Mars is a natural enemy of Saturn-ruled Capricorn; lacking trikona ownership, Mars is a functional malefic whose dasha produces domestic discord and property challenges."},
        # Mercury → H6+H9 (dusthana + trikona)
        {"planet": "mercury", "houses": [6, 9],   "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Mercury as 6th and 9th lord for Capricorn — H9 trikona lordship gives Mercury some functional beneficence despite H6 dusthana co-ownership; Mercury dasha produces dharmic themes and fortune with conflict/service subthemes from H6."},
        # Jupiter → H3+H12 (upachaya + dusthana)
        {"planet": "jupiter", "houses": [3, 12],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["foreign_travel", "mental_health"],
         "desc": "Jupiter as 3rd and 12th lord for Capricorn is a functional malefic — H12 dusthana ownership and the natural debilitation of Jupiter in Capricorn's sign (H1) makes Jupiter unfavorable; its dasha produces foreign separation, expenditure, and loss of fortune themes."},
        # Venus → H5+H10 (trikona + kendra) = YOGAKARAKA
        {"planet": "venus",   "houses": [5, 10],  "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "fame_reputation", "progeny"],
         "desc": "Venus as 5th and 10th lord is the yogakaraka for Capricorn lagna — owning trikona (H5: intelligence/purva punya) and kendra (H10: career/status), Venus dasha produces exceptional results in career, recognition, wealth, and creative achievement for Capricorn natives."},
        # Saturn → H1+H2 (lagna lord + maraka)
        {"planet": "saturn",  "houses": [1, 2],   "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament", "longevity"],
         "desc": "Saturn as lagna lord for Capricorn — Saturn dasha is highly significant; it activates discipline, endurance, and structural achievement themes central to Capricorn nature; H2 co-ownership makes Saturn also a maraka but lagna lordship of Saturn dominates the functional nature."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Capricorn lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Capricorn lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "aquarius": [
        # Sun → H7 (maraka + kendra)
        {"planet": "sun",     "houses": [7],      "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "marriage"],
         "desc": "Sun as 7th lord for Aquarius lagna is a maraka — H7 lordship confers death-inflicting potential; Sun dasha carries longevity concerns and partnership themes; H7 kendra ownership also gives some temporal activation energy but maraka status dominates."},
        # Moon → H6 (dusthana)
        {"planet": "moon",    "houses": [6],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "physical_health"],
         "desc": "Moon as 6th lord for Aquarius is a functional malefic — H6 dusthana ownership makes Moon's dasha produce conflict, health issues, and service/debt themes for Aquarius natives."},
        # Mars → H3+H10 (upachaya + kendra)
        {"planet": "mars",    "houses": [3, 10],  "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["career_status", "character_temperament"],
         "desc": "Mars as 3rd and 10th lord for Aquarius — despite owning kendra H10, Mars is a natural enemy of Saturn-ruled Aquarius and lacks trikona ownership; its dasha produces aggressive career themes but is functionally malefic due to natural enmity and lack of trikona."},
        # Mercury → H5+H8 (trikona + dusthana)
        {"planet": "mercury", "houses": [5, 8],   "func": "trikona_dusthana",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["intelligence_education", "progeny", "longevity"],
         "desc": "Mercury as 5th and 8th lord for Aquarius — H5 trikona lordship makes Mercury a functional benefic; its dasha produces intelligence, purva punya, and analytical prowess themes; H8 co-ownership introduces occult, longevity, and transformative subthemes."},
        # Jupiter → H2+H11 (maraka + upachaya)
        {"planet": "jupiter", "houses": [2, 11],  "func": "maraka",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "wealth"],
         "desc": "Jupiter as 2nd and 11th lord for Aquarius lagna is a maraka — H2 lordship confers death-inflicting potential; despite being a natural benefic, Jupiter's dasha for Aquarius carries longevity concerns; H11 ownership provides material gains subtheme."},
        # Venus → H4+H9 (kendra + trikona) = YOGAKARAKA
        {"planet": "venus",   "houses": [4, 9],   "func": "yogakaraka",
         "odir": "favorable",  "oint": "strong",
         "odoms": ["career_status", "wealth", "spirituality", "property_vehicles"],
         "desc": "Venus as 4th and 9th lord is the yogakaraka for Aquarius lagna — owning kendra (H4: domestic happiness/property) and trikona (H9: dharma/fortune), Venus dasha produces exceptional raja yoga results including property, fortune, and spiritual advancement for Aquarius natives."},
        # Saturn → H1+H12 (lagna lord + dusthana)
        {"planet": "saturn",  "houses": [1, 12],  "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament"],
         "desc": "Saturn as lagna lord for Aquarius — Saturn dasha activates Aquarian themes of discipline, humanitarian service, and systematic achievement; H12 co-ownership introduces foreign or spiritual retreat subthemes but lagna lordship of Saturn is the dominant functional designation."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Aquarius lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Aquarius lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],

    "pisces": [
        # Sun → H6 (dusthana)
        {"planet": "sun",     "houses": [6],      "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["enemies_litigation", "physical_health"],
         "desc": "Sun as 6th lord for Pisces is a functional malefic — H6 dusthana ownership makes Sun's dasha produce conflict, health issues, and adversarial conditions for Pisces natives."},
        # Moon → H5 (trikona)
        {"planet": "moon",    "houses": [5],      "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["progeny", "intelligence_education", "mental_health"],
         "desc": "Moon as 5th lord for Pisces is a functional benefic — H5 trikona lordship makes Moon's dasha produce intelligence, purva punya, and children-related blessings; Moon's natural beneficence combines favorably with trikona lordship for Pisces."},
        # Mars → H2+H9 (maraka + trikona)
        {"planet": "mars",    "houses": [2, 9],   "func": "trikona_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["spirituality", "wealth"],
         "desc": "Mars as 2nd and 9th lord for Pisces — H9 trikona lordship makes Mars a functional benefic; its dasha produces fortune, dharmic energy, and courageous spiritual seeking; H2 maraka status applies but trikona lordship of H9 dominates."},
        # Mercury → H4+H7 (two kendras, natural benefic) = strong kendradhipati
        {"planet": "mercury", "houses": [4, 7],   "func": "kendradhipati",
         "odir": "neutral",   "oint": "moderate",
         "odoms": ["marriage", "property_vehicles", "mental_health"],
         "desc": "Mercury as 4th and 7th lord for Pisces suffers strong kendradhipati dosha — owning two kendra houses as a natural benefic; Mercury is debilitated in Pisces (H1 for this lagna) which compounds issues; its dasha produces mixed domestic and marriage results; H7 lordship makes Mercury a maraka."},
        # Jupiter → H1+H10 (lagna lord + kendra, natural benefic)
        {"planet": "jupiter", "houses": [1, 10],  "func": "lagna_lord",
         "odir": "favorable",  "oint": "moderate",
         "odoms": ["physical_health", "character_temperament", "career_status"],
         "desc": "Jupiter as lagna lord for Pisces — Jupiter dasha is highly significant, activating wisdom, spiritual depth, and benevolence central to Pisces nature; H10 kendra co-ownership creates minor kendradhipati technically but lagna lordship of Jupiter overwhelmingly dominates the functional classification."},
        # Venus → H3+H8 (upachaya + dusthana)
        {"planet": "venus",   "houses": [3, 8],   "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["longevity", "physical_health"],
         "desc": "Venus as 3rd and 8th lord for Pisces is a functional malefic — H8 severe dusthana ownership makes Venus's dasha produce longevity concerns, transformative events, and hidden health issues; Venus is also debilitated in Virgo (H7 for this lagna, relevant to placement, not lordship)."},
        # Saturn → H11+H12 (upachaya + dusthana)
        {"planet": "saturn",  "houses": [11, 12], "func": "functional_malefic",
         "odir": "unfavorable", "oint": "moderate",
         "odoms": ["foreign_travel", "wealth"],
         "desc": "Saturn as 11th and 12th lord for Pisces is a functional malefic — H12 dusthana ownership makes Saturn's dasha produce foreign isolation, expenditure, and loss themes; Saturn is a natural enemy of Jupiter-ruled Pisces, compounding its malefic functional nature."},
        {"planet": "rahu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["character_temperament"],
         "desc": "Rahu for Pisces lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
        {"planet": "ketu",    "houses": [],       "func": "chameleon",
         "odir": "neutral",   "oint": "conditional",
         "odoms": ["spirituality"],
         "desc": "Ketu for Pisces lagna is a chameleon — its functional nature and dasha results depend on its sign dispositor."},
    ],
}

# Verse references per lagna (best-effort; see PHASE1B_RULE_CONTRACT.md §verse_ref)
_VERSE_REF = {
    "aries": "Ch.1 v.1", "taurus": "Ch.1 v.2", "gemini": "Ch.1 v.3",
    "cancer": "Ch.1 v.4", "leo": "Ch.1 v.5", "virgo": "Ch.1 v.6",
    "libra": "Ch.1 v.7", "scorpio": "Ch.1 v.8", "sagittarius": "Ch.1 v.9",
    "capricorn": "Ch.1 v.10", "aquarius": "Ch.1 v.11", "pisces": "Ch.1 v.12",
}

# Lagna order (for rule ID assignment)
_LAGNAS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]


def _build_rules() -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    rule_num = 1

    for lagna in _LAGNAS:
        verse_ref = _VERSE_REF[lagna]
        planets = _TABLE[lagna]  # exactly 9 entries

        for entry in planets:
            rid = f"LPF{rule_num:03d}"
            planet = entry["planet"]
            func = entry["func"]
            houses = entry["houses"]

            # Build primary_condition
            primary_condition = {
                "planet": planet,
                "placement_type": "house_lordship",
                "placement_value": houses,
                "for_lagna": lagna,
            }

            # Build tags
            tags = ["lpf", "parashari", "laghu_parashari", "functional_nature",
                    lagna, planet, func]

            # Chapter reference
            chapter = "Ch.1–2"

            # Confidence: base 0.6 + verse_ref bonus 0.05
            confidence = 0.65

            rules.append(RuleRecord(
                rule_id=rid,
                source="LaghuParashari",
                chapter=chapter,
                school="parashari",
                category="functional_nature",
                description=(
                    f"[Laghu Parashari — {lagna.capitalize()} lagna, {planet.capitalize()}] "
                    + entry["desc"]
                ),
                confidence=confidence,
                verse=f"LP sutras on {lagna} lagna temporal lordships",
                tags=tags,
                implemented=False,
                engine_ref="",
                # Phase 1B fields
                primary_condition=primary_condition,
                modifiers=[],
                exceptions=[],
                outcome_domains=entry["odoms"],
                outcome_direction=entry["odir"],
                outcome_intensity=entry["oint"],
                outcome_timing="dasha_dependent",
                lagna_scope=[lagna],
                dasha_scope=[],
                verse_ref=verse_ref,
                concordance_texts=[],
                divergence_notes="",
                phase="1B_conditional",
                system="natal",
            ))
            rule_num += 1

    return rules


# ── Registry ─────────────────────────────────────────────────────────────────
LAGHU_PARASHARI_FUNCTIONAL_REGISTRY = CorpusRegistry()

for _rule in _build_rules():
    LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.add(_rule)
