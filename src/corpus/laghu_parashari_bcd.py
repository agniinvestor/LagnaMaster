"""
src/corpus/laghu_parashari_bcd.py — S265: Laghu Parashari Sections B, C, D

Section B — Yogakaraka Designations (LPY001–LPY012)
  One rule per lagna: which planet (if any) is yogakaraka (owns one kendra H4/7/10
  AND one trikona H5/9 simultaneously). 6 lagnas have a yogakaraka; 6 do not.

Section C — Kendradhipati Dosha (LPK001–LPK024)
  Natural benefics (Moon, Mercury, Venus, Jupiter) that own kendra houses without
  also owning a trikona lose their natural beneficence per LP doctrine.

Section D — Dasha Results by Lordship Type (LPD001–LPD045)
  Results during the mahadasha of a planet based on which houses it owns.
  Phase 1B_matrix rules (lordship-type based, lagna-agnostic) unless noted.

Source: LaghuParashari (Jataka Chandrika), Ch.1–6
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ─────────────────────────────────────────────────────────────────────────────
# Section B — Yogakaraka Designations
# ─────────────────────────────────────────────────────────────────────────────

_YOGAKARAKA_DATA = [
    # (lagna, planet_or_none, kendra_houses, trikona_houses, desc)
    ("aries",       None,     [],      [],
     "Aries lagna has no yogakaraka. No single planet owns both a kendra (H4/H7/H10) "
     "and a separate trikona (H5/H9) simultaneously. Mars as lagna lord owns H1+H8; "
     "Jupiter owns H9+H12 (trikona + dusthana); Saturn owns H10+H11 (kendra + upachaya). "
     "The absence of a yogakaraka makes natural benefics and functional trikona lords "
     "the primary benefic factors for Aries."),
    ("taurus",      "saturn", [10],    [9],
     "Saturn is the yogakaraka for Taurus lagna, owning H9 (trikona, dharma) and H10 "
     "(kendra, karma) simultaneously. This dual lordship of a trikona and kendra by the "
     "same natural malefic elevates Saturn to the highest benefic status for Taurus. "
     "Saturn's dasha and antardasha produce raja yoga results: career advancement, "
     "status, and dharmic fulfillment. Saturn placed strongly (own sign Capricorn/Aquarius, "
     "exalted Libra) amplifies these results."),
    ("gemini",      None,     [],      [],
     "Gemini lagna has no yogakaraka. Jupiter owns H7+H10 (both kendra — kendradhipati), "
     "Saturn owns H8+H9 (trikona + dusthana — not yogakaraka), Venus owns H5+H12 "
     "(trikona + dusthana). No planet owns both a kendra and a trikona from separate "
     "houses. The best functional benefic for Gemini is Venus (H5 trikona lord) and "
     "the lagna lord Mercury."),
    ("cancer",      "mars",   [10],    [5],
     "Mars is the yogakaraka for Cancer lagna, owning H5 (trikona, purva punya) and H10 "
     "(kendra, karma) simultaneously. Mars — despite being a natural malefic — becomes "
     "the single most powerful functional benefic for Cancer. Its dasha produces "
     "outstanding career results, recognition, intelligence, and progeny matters. "
     "Mars placed in own sign (Aries/Scorpio) or exalted (Capricorn) for Cancer "
     "gives full yogakaraka results."),
    ("leo",         "mars",   [4],     [9],
     "Mars is the yogakaraka for Leo lagna, owning H4 (kendra, happiness/property) and H9 "
     "(trikona, fortune/dharma) simultaneously. Mars's dasha for Leo gives property gains, "
     "maternal happiness, fortune, father's blessings, and dharmic pursuits. "
     "The combination of kendra + trikona lordship in a natural malefic makes Mars "
     "highly auspicious for Leo despite its natural fiery, combative nature."),
    ("virgo",       None,     [],      [],
     "Virgo lagna has no yogakaraka. Jupiter owns H4+H7 (both kendra — kendradhipati), "
     "Venus owns H2+H9 (trikona + maraka house), Saturn owns H5+H6 (trikona + dusthana). "
     "No single planet owns a kendra AND trikona from separate houses. "
     "Venus as H9 trikona lord (despite H2 co-ownership) and Mercury as lagna lord "
     "are the primary benefic planets for Virgo."),
    ("libra",       "saturn", [4, 5],  [5],
     "Saturn is the yogakaraka for Libra lagna, owning H4 (kendra, happiness) and H5 "
     "(trikona, purva punya/children) simultaneously. Uniquely, H5 is both the trikona "
     "and Saturn's second lordship alongside the kendra H4. Saturn's exaltation in Libra "
     "itself makes it doubly powerful for this lagna. Saturn's dasha: happiness, property, "
     "children, intelligence all activated together — the most auspicious planet for Libra."),
    ("scorpio",     None,     [],      [],
     "Scorpio lagna has no yogakaraka. Jupiter owns H2+H5 (trikona H5, but H2 is maraka), "
     "Moon owns H9 (trikona lord only, no kendra), Sun owns H10 (kendra only, no trikona). "
     "No single planet owns both a kendra and a separate trikona. "
     "Moon (H9 trikona) and Jupiter (H5 trikona, with the H2 maraka caveat) are "
     "the primary functional benefics for Scorpio."),
    ("sagittarius", None,     [],      [],
     "Sagittarius lagna has no yogakaraka. Mercury owns H7+H10 (both kendra — kendradhipati), "
     "Mars owns H5+H12 (trikona + dusthana), Sun owns H9 (trikona only). "
     "No single planet owns a kendra and a trikona from separate houses. "
     "Sun (H9 trikona lord) and the lagna lord Jupiter (H1+H4 — lagna + kendra) "
     "are the primary benefic factors."),
    ("capricorn",   "venus",  [10],    [5],
     "Venus is the yogakaraka for Capricorn lagna, owning H5 (trikona, purva punya) and H10 "
     "(kendra, karma/career) simultaneously. Venus — a natural benefic — becomes the supreme "
     "benefic for Capricorn through this yogakaraka status. Venus's dasha gives career peak, "
     "artistic recognition, children, intelligence, and overall fortune. "
     "Venus exalted in Pisces for Capricorn lagna is the strongest yogakaraka placement."),
    ("aquarius",    "venus",  [4],     [9],
     "Venus is the yogakaraka for Aquarius lagna, owning H4 (kendra, happiness/property) and H9 "
     "(trikona, fortune/dharma) simultaneously. Venus's yogakaraka status for Aquarius means "
     "its dasha activates property, vehicles, maternal happiness, fortune, and dharmic pursuits "
     "together. Venus in own sign (Taurus/Libra) or exalted (Pisces) for Aquarius gives "
     "the most powerful yogakaraka results."),
    ("pisces",      None,     [],      [],
     "Pisces lagna has no yogakaraka. Mars owns H2+H9 (trikona H9, but H2 is maraka — not "
     "yogakaraka since H2 is not a kendra). Jupiter owns H1+H10 (lagna lord + H10 kendra — "
     "important but lagna lordship is different from a separate trikona ownership). "
     "Saturn owns H11+H12 (neither kendra nor trikona). "
     "Mars as H9 trikona lord and Moon as H5 trikona lord are primary benefics for Pisces."),
]

_LAGNAS_ORDER = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]


def _build_yogakaraka_rules() -> list[RuleRecord]:
    rules = []
    for idx, (lagna, planet, kendra_h, trikona_h, desc) in enumerate(_YOGAKARAKA_DATA, start=1):
        rid = f"LPY{idx:03d}"
        has_yk = planet is not None
        tags = ["lpy", "parashari", "laghu_parashari", "yogakaraka_section", lagna]
        if has_yk:
            tags += ["yogakaraka", planet]
            odir = "favorable"
            oint = "strong"
            primary = {
                "planet": planet,
                "placement_type": "yogakaraka_designation",
                "placement_value": kendra_h + trikona_h,
                "kendra_houses": kendra_h,
                "trikona_houses": trikona_h,
                "for_lagna": lagna,
            }
            odoms = ["career_status", "wealth", "fame_reputation", "spirituality"]
        else:
            tags += ["no_yogakaraka"]
            odir = "neutral"
            oint = "weak"
            primary = {
                "planet": "none",
                "placement_type": "yogakaraka_designation",
                "placement_value": [],
                "for_lagna": lagna,
            }
            odoms = []
        rules.append(RuleRecord(
            rule_id=rid,
            source="LaghuParashari",
            chapter="Ch.1–2",
            school="parashari",
            category="yogakaraka",
            description=f"[LP — {lagna} lagna, yogakaraka section] {desc}",
            confidence=0.70,
            tags=tags,
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing="dasha_dependent",
            lagna_scope=[lagna],
            verse_ref="Ch.1 v.3",
            phase="1B_conditional",
            system="natal",
        ))
    return rules


LAGHU_PARASHARI_YOGAKARAKA_REGISTRY = CorpusRegistry()
for _rule in _build_yogakaraka_rules():
    LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.add(_rule)


# ─────────────────────────────────────────────────────────────────────────────
# Section C — Kendradhipati Dosha
# ─────────────────────────────────────────────────────────────────────────────

# Each entry: (lagna, planet, kendra_owned, trikona_owned, kd_type, odir, oint, desc)
# kd_type: "full" = clear KD dosha; "partial" = lagna lord also owns kendra;
#           "exempt" = has trikona, no dosha; "overlap" = maraka + KD
_KD_DATA = [
    # ── Clear KD dosha (natural benefic owns kendra, no trikona) ──────────────
    ("aries",       "moon",    [4],     [],    "full",
     "unfavorable", "moderate",
     "Moon owns H4 (Cancer) for Aries lagna — a kendra with no trikona co-ownership. "
     "As a natural benefic ruling a kendra alone, Moon acquires kendradhipati dosha: "
     "its natural significations (mind, mother, happiness) become unreliable. "
     "Moon dasha for Aries gives mixed results: property matters but emotional instability. "
     "Moon placed well can reduce the dosha, but the functional designation holds."),
    ("gemini",      "jupiter", [7, 10], [],    "full",
     "unfavorable", "strong",
     "Jupiter owns H7 (Sagittarius) and H10 (Pisces) for Gemini — both are kendra houses. "
     "Owning two kendras with no trikona makes Jupiter a strong kendradhipati for Gemini. "
     "Despite being the natural significator of wisdom and dharma, Jupiter's benefic "
     "qualities are severely reduced for Gemini. Jupiter dasha tends toward "
     "overreach, legal issues in partnerships, and career obstacles rather than expansion."),
    ("cancer",      "venus",   [4],     [],    "full",
     "unfavorable", "moderate",
     "Venus owns H4 (Libra) for Cancer lagna — a kendra house with no trikona co-ownership "
     "(Venus also owns H11, an upachaya). Venus becomes a kendradhipati for Cancer: "
     "despite natural beneficence, Venus dasha produces mixed results — property matters "
     "activate but at the cost of some indulgence or comfort-seeking. "
     "Kendradhipati dosha moderates Venus's otherwise pleasant significations."),
    ("leo",         "venus",   [10],    [],    "full",
     "unfavorable", "moderate",
     "Venus owns H10 (Taurus) for Leo lagna — a kendra house, and also H3 (Libra) which "
     "is neither kendra nor trikona. Venus acquires kendradhipati dosha for Leo: "
     "career-related activation during Venus dasha but with obstacles and delays. "
     "Artistic and romantic matters (natural Venus) may conflict with career demands. "
     "Venus is not the most auspicious planet for Leo despite being a natural benefic."),
    ("virgo",       "jupiter", [4, 7],  [],    "full",
     "unfavorable", "strong",
     "Jupiter owns H4 (Sagittarius) and H7 (Pisces) for Virgo — two kendra houses with "
     "no trikona ownership. This is one of the strongest cases of kendradhipati dosha: "
     "Jupiter, the natural karaka of wisdom, children, and expansion, becomes functionally "
     "problematic for Virgo. Jupiter dasha tends toward misplaced optimism, excessive "
     "indulgence, and partnership difficulties rather than wisdom and growth."),
    ("libra",       "moon",    [10],    [],    "full",
     "unfavorable", "moderate",
     "Moon owns H10 (Cancer) for Libra lagna — a kendra, with no trikona. "
     "Moon acquires kendradhipati dosha for Libra: career matters activate in Moon dasha "
     "but the mind becomes turbulent, and the emotional nature creates professional instability. "
     "Moon's natural significations of mother and mind become strained by the burden "
     "of kendra lordship without dharmic support."),
    ("sagittarius", "mercury", [7, 10], [],    "full",
     "unfavorable", "strong",
     "Mercury owns H7 (Gemini) and H10 (Virgo) for Sagittarius — both kendra houses "
     "with no trikona. Mercury's natural benefic qualities are fully displaced by "
     "kendradhipati dosha. Mercury dasha for Sagittarius brings career activity and "
     "partnership dealings but with errors in judgment, contractual disputes, and "
     "intellectual overreach. Mercury is a functional malefic for Sagittarius."),
    ("pisces",      "mercury", [4, 7],  [],    "full",
     "unfavorable", "strong",
     "Mercury owns H4 (Gemini) and H7 (Virgo) for Pisces — both kendra houses with "
     "no trikona. Mercury becomes a functional malefic for Pisces through kendradhipati "
     "dosha. Its dasha activates property and partnerships but with analysis-paralysis, "
     "duplicity in relationships, and difficulty achieving clarity. "
     "Mercury's intellectual nature conflicts with Pisces' intuitive, spiritually-oriented lagna."),
    # ── Maraka + KD overlap ───────────────────────────────────────────────────
    ("aries",       "venus",   [7],     [],    "overlap",
     "unfavorable", "strong",
     "Venus owns H2 (Taurus) and H7 (Libra) for Aries — the classic double-maraka planet. "
     "H7 is also a kendra, so Venus has both maraka and kendradhipati characteristics. "
     "The maraka designation is primary: Venus dasha can bring death or death-like events "
     "especially for elderly native. The kendradhipati aspect adds that Venus's "
     "natural benefic qualities are unreliable for Aries. Venus is the strongest functional "
     "malefic for Aries despite being the natural planet of beauty and relationships."),
    ("scorpio",     "venus",   [7],     [],    "overlap",
     "unfavorable", "strong",
     "Venus owns H7 (Taurus) and H12 (Libra) for Scorpio. H7 is a kendra (also maraka), "
     "H12 is dusthana. Venus has both maraka and some kendradhipati aspect for Scorpio. "
     "Primary designation is maraka: Venus dasha activates partnerships but carries "
     "death-potential especially in older life. The H12 co-ownership adds expenditure "
     "and foreign travel themes. Venus is the most prominent functional malefic for Scorpio."),
    ("capricorn",   "moon",    [7],     [],    "overlap",
     "unfavorable", "strong",
     "Moon owns H7 (Cancer) for Capricorn — a kendra and maraka house. "
     "Moon is the primary maraka for Capricorn. The kendra lordship adds kendradhipati "
     "aspect: Moon's natural beneficence (mind, emotion, mother) is suppressed. "
     "Moon dasha for Capricorn activates partnerships and can bring maraka results "
     "especially combined with 7th house transits. Moon is functionally malefic for Capricorn."),
    # ── Lagna lord also owns kendra (partial KD concern) ─────────────────────
    ("gemini",      "mercury", [1, 4],  [],    "partial",
     "favorable",   "moderate",
     "Mercury as lagna lord owns H1 (Gemini) and H4 (Virgo) for Gemini. "
     "H4 is a kendra — but Mercury is the lagna lord, which confers inherent auspiciousness. "
     "LP notes partial kendradhipati concern: Mercury's H4 ownership without a trikona "
     "means kendra results are available but the natural benefic quality is moderated. "
     "Lagna lord privilege prevents full KD dosha — Mercury remains a functional benefic "
     "for Gemini, but its results are more mixed than a pure trikona lord would be."),
    ("virgo",       "mercury", [1, 10], [],    "partial",
     "favorable",   "moderate",
     "Mercury as lagna lord owns H1 (Virgo) and H10 (Gemini) for Virgo. "
     "H10 is a kendra, adding partial kendradhipati concern. As lagna lord, Mercury "
     "retains functional beneficence but the H10 kendra ownership without trikona "
     "means career matters during Mercury dasha come with some effort and analytical "
     "challenges. Mercury's strong analytical nature serves Virgo well overall, "
     "making it a functional benefic despite the partial KD element."),
    ("sagittarius", "jupiter", [1, 4],  [],    "partial",
     "favorable",   "moderate",
     "Jupiter as lagna lord owns H1 (Sagittarius) and H4 (Pisces) for Sagittarius. "
     "H4 kendra ownership alongside lagna lordship creates a partial kendradhipati note. "
     "Jupiter remains the most important planet for Sagittarius as lagna lord, "
     "but its H4 co-ownership means property matters may have complications. "
     "Lagna lord privilege fully protects Jupiter: it is the functional benefic for Sagittarius."),
    ("pisces",      "jupiter", [1, 10], [],    "partial",
     "favorable",   "moderate",
     "Jupiter as lagna lord owns H1 (Pisces) and H10 (Sagittarius) for Pisces. "
     "H10 kendra co-ownership adds partial kendradhipati concern, but lagna lordship "
     "is the stronger designation. Jupiter's dasha for Pisces gives excellent results: "
     "self-actualization, career peak, spiritual development. The H10 ownership without "
     "a separate trikona is moderated by lagna lord privilege. Jupiter is strongly "
     "functional benefic for Pisces."),
    ("cancer",      "moon",    [1],     [],    "exempt",
     "favorable",   "strong",
     "Moon owns H1 (Cancer) for Cancer lagna — the Moon is the lagna lord itself. "
     "H1 is simultaneously a kendra and a trikona (both classifications apply to the "
     "ascendant). Moon as lagna lord is entirely exempt from kendradhipati dosha. "
     "LP explicitly states that the lagna lord, even when a natural benefic, retains "
     "full beneficence. Moon dasha for Cancer is among the most auspicious periods."),
    ("libra",       "venus",   [1],     [],    "partial",
     "favorable",   "moderate",
     "Venus as lagna lord owns H1 (Libra) and H8 (Taurus) for Libra. "
     "H1 ownership makes Venus the lagna lord — exempt from kendradhipati dosha. "
     "However, H8 co-ownership creates a functional complexity: Venus brings lagna "
     "lord benefits but the H8 dusthana co-ownership adds an element of hidden matters, "
     "sudden transformations, and longevity concerns in Venus dasha. "
     "Venus remains functionally benefic for Libra, with the H8 caveat."),
    ("taurus",      "venus",   [1],     [],    "exempt",
     "favorable",   "strong",
     "Venus as lagna lord owns H1 (Taurus) and H6 (Libra) for Taurus. "
     "As lagna lord, Venus is exempt from kendradhipati dosha despite H6 co-ownership. "
     "Venus dasha for Taurus is generally excellent: self-expression, beauty, comfort, "
     "financial matters (H6 connection brings victory over enemies and competitive "
     "success). Lagna lord privilege is the dominant functional designation."),
    # ── Explicit trikona-holder exemptions (no KD dosha) ─────────────────────
    ("taurus",      "mercury", [2],     [5],   "exempt",
     "favorable",   "moderate",
     "Mercury owns H2 (Gemini) and H5 (Virgo) for Taurus. H5 is a trikona — Mercury's "
     "trikona lordship fully overrides any KD concern from H2. Mercury is a functional "
     "benefic for Taurus as H5 lord; its natural beneficence is retained and enhanced. "
     "Mercury dasha activates intelligence, children, creative output, and some "
     "wealth accumulation. No kendradhipati dosha applies."),
    ("aquarius",    "venus",   [4],     [9],   "exempt",
     "favorable",   "strong",
     "Venus owns H4 (Taurus) and H9 (Libra) for Aquarius — H4 kendra AND H9 trikona "
     "simultaneously. This is the yogakaraka designation: trikona co-ownership fully "
     "protects Venus from kendradhipati dosha and elevates it to the supreme benefic. "
     "No KD dosha whatsoever — Venus is the most auspicious planet for Aquarius."),
    ("cancer",      "jupiter", [6],     [9],   "exempt",
     "favorable",   "moderate",
     "Jupiter owns H6 (Sagittarius) and H9 (Pisces) for Cancer. H9 trikona lordship "
     "saves Jupiter from kendradhipati dosha — there is no kendra involved in Jupiter's "
     "ownership for Cancer. However, H6 dusthana co-ownership creates a trikona-dusthana "
     "classification rather than pure trikona. Jupiter's dasha results are mixed: "
     "fortune and dharma (H9) contend with disease, enemies, debts (H6). "
     "Overall functional benefic but with H6 complications."),
    ("leo",         "jupiter", [5],     [],    "exempt",
     "favorable",   "moderate",
     "Jupiter owns H5 (Sagittarius) and H8 (Pisces) for Leo. H5 trikona lordship "
     "prevents kendradhipati dosha despite H8 dusthana co-ownership. "
     "Jupiter is a trikona-dusthana lord for Leo: its natural beneficence is "
     "retained through H5 but the H8 adds transformation, longevity concerns, and "
     "sudden events to Jupiter's portfolio. Net classification: functional benefic "
     "with some H8 complications."),
    ("scorpio",     "jupiter", [2],     [5],   "exempt",
     "favorable",   "moderate",
     "Jupiter owns H2 (Sagittarius) and H5 (Pisces) for Scorpio. H5 trikona saves "
     "Jupiter from kendradhipati dosha. However, H2 maraka co-ownership means Jupiter "
     "carries the maraka designation alongside its trikona beneficence. "
     "Jupiter dasha for Scorpio: excellent for children, intelligence, dharma (H5) "
     "but with wealth-and-family activation and potential maraka element in old age."),
    ("virgo",       "venus",   [2],     [9],   "exempt",
     "favorable",   "moderate",
     "Venus owns H2 (Libra) and H9 (Taurus) for Virgo. H9 trikona lordship makes Venus "
     "a functional benefic for Virgo — no kendradhipati dosha applies. "
     "Venus as H9 trikona lord gives fortune, dharma, and artistic blessings during "
     "its dasha. H2 co-ownership adds wealth and family activation. "
     "Venus is one of the most auspicious planets for Virgo native."),
]


def _build_kendradhipati_rules() -> list[RuleRecord]:
    rules = []
    for idx, (lagna, planet, kendra_h, trikona_h, kd_type, odir, oint, desc) in enumerate(
        _KD_DATA, start=1
    ):
        rid = f"LPK{idx:03d}"
        tags = ["lpk", "parashari", "laghu_parashari", "kendradhipati_section",
                lagna, planet, kd_type]
        if kd_type == "full":
            tags.append("kendradhipati_dosha")
        elif kd_type == "overlap":
            tags += ["kendradhipati_dosha", "maraka"]
        elif kd_type == "partial":
            tags.append("lagna_lord")
        elif kd_type == "exempt":
            tags.append("kendradhipati_exempt")
        primary = {
            "planet": planet,
            "placement_type": "kendradhipati_doctrine",
            "placement_value": kendra_h + trikona_h,
            "kendra_houses": kendra_h,
            "trikona_houses": trikona_h,
            "kd_classification": kd_type,
            "for_lagna": lagna,
        }
        odoms = ["mental_health", "character_temperament"]
        if "career" in desc.lower() or "H10" in desc or "H4" in desc:
            odoms.append("career_status")
        if "wealth" in desc.lower() or "H2" in desc:
            odoms.append("wealth")
        if kd_type == "overlap":
            odoms.append("longevity")
        odoms = list(dict.fromkeys(odoms))  # deduplicate, preserve order
        rules.append(RuleRecord(
            rule_id=rid,
            source="LaghuParashari",
            chapter="Ch.2–3",
            school="parashari",
            category="kendradhipati",
            description=f"[LP — {lagna} lagna, {planet}] {desc}",
            confidence=0.68,
            tags=tags,
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing="dasha_dependent",
            lagna_scope=[lagna],
            verse_ref="Ch.2 v.1",
            phase="1B_conditional",
            system="natal",
        ))
    return rules


LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY = CorpusRegistry()
for _rule in _build_kendradhipati_rules():
    LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.add(_rule)


# ─────────────────────────────────────────────────────────────────────────────
# Section D — Dasha Results by Lordship Type
# ─────────────────────────────────────────────────────────────────────────────

# Each entry: (rule_id_suffix, houses, lordship_label, odir, oint, domains, phase, lagna_scope, desc)
_DASHA_DATA = [
    # ── 12 base house-lord dasha rules (1B_matrix) ───────────────────────────
    (1, [1], "lagna_lord",
     "favorable", "moderate",
     ["physical_health", "career_status", "character_temperament"],
     "1B_matrix", [],
     "Lagna lord dasha is generally favorable across all lagnas. LP states the lagna lord "
     "activates the native's vitality, self-expression, personal initiative, and overall health. "
     "New beginnings, personal confidence, and identity-related matters come forward. "
     "If the lagna lord is strong and well-placed, the dasha delivers robust health and "
     "clear purpose. The specific domain results vary by which planet and lagna is involved, "
     "but the lagna lord's dasha is always self-sustaining."),
    (2, [2], "2nd_lord",
     "favorable", "moderate",
     ["wealth", "marriage"],
     "1B_matrix", [],
     "2nd lord dasha activates wealth accumulation, family matters, speech, food, and "
     "early education themes. LP states the 2nd house dasha brings financial transactions, "
     "family gatherings, attention to diet, and matters of the second marriage (if applicable). "
     "The 2nd lord's dasha is generally favorable for wealth if the lord is well-placed, "
     "but it also carries the maraka potential — death-related concerns arise especially "
     "for elderly natives or when the 2nd lord is afflicted."),
    (3, [3], "3rd_lord",
     "neutral", "moderate",
     ["career_status", "character_temperament"],
     "1B_matrix", [],
     "3rd lord dasha activates siblings, communication, courage, short travels, and "
     "the native's own effort (parakrama). LP classifies the 3rd house as an upachaya — "
     "results improve over the dasha period. Short journeys, media, writing, trade, and "
     "sibling-related events are prominent. Natural malefics as 3rd lord give better "
     "results for initiative and courage; natural benefics as 3rd lord tend to give "
     "pleasant but moderate results in this dasha."),
    (4, [4], "4th_lord",
     "favorable", "moderate",
     ["property_vehicles", "mental_health"],
     "1B_matrix", [],
     "4th lord dasha activates domestic happiness, property transactions, vehicles, "
     "mother's matters, and emotional contentment. LP states the 4th house dasha "
     "brings home-related changes: purchase or change of residence, acquisition of "
     "vehicles, improvements in domestic environment. Mother's health and wellbeing "
     "are prominent themes. The dasha is generally favorable for mental peace when "
     "the 4th lord is strong; afflicted 4th lord brings domestic tensions and property disputes."),
    (5, [5], "5th_lord",
     "favorable", "strong",
     ["progeny", "intelligence_education", "spirituality"],
     "1B_matrix", [],
     "5th lord dasha is among the most auspicious dashas per LP. The 5th house represents "
     "purva punya (past-life merit), children, intelligence, creative output, and speculative "
     "gains. Its dasha activates all these simultaneously: children may be born, "
     "intelligence sharpens, academic or creative achievements manifest, and the native "
     "connects with dharmic or spiritual practices. This is the prime dasha for intellectual "
     "and dharmic growth per the Laghu Parashari framework."),
    (6, [6], "6th_lord",
     "unfavorable", "moderate",
     ["enemies_litigation", "physical_health"],
     "1B_matrix", [],
     "6th lord dasha is generally unfavorable. LP states enemies become active, health "
     "problems manifest, debts increase, and litigation or service-related conflicts arise. "
     "The 6th house governs disease, enemies, and debts — its dasha activates all three. "
     "However, if the 6th lord is strong and placed in a good house, it can give victory "
     "over enemies and success in competitive fields (e.g., sports, medicine, law). "
     "The net reading is unfavorable unless specific counter-indications apply."),
    (7, [7], "7th_lord",
     "mixed", "moderate",
     ["marriage", "longevity"],
     "1B_matrix", [],
     "7th lord dasha activates marriage, business partnerships, and foreign interactions. "
     "LP emphasizes the dual nature of the 7th lord: it is both the house of partnership "
     "and a maraka (death-inflicting) house. During the 7th lord dasha, marriage may occur, "
     "businesses partnerships form, and the native engages significantly with the public. "
     "For elderly natives or those near the end of their natural lifespan, the 7th lord "
     "dasha can bring maraka activation. Results are mixed depending on dignity and placement."),
    (8, [8], "8th_lord",
     "unfavorable", "moderate",
     ["longevity", "mental_health"],
     "1B_matrix", [],
     "8th lord dasha is generally difficult. LP states obstacles, hidden enemies, sudden "
     "reversals, and longevity challenges arise. The 8th house governs chronic disease, "
     "sudden events, inheritance, and hidden knowledge (occult). Its dasha tests the "
     "native's endurance. However, for those on a spiritual path, the 8th lord dasha "
     "can produce deep esoteric insights and transformative experiences. "
     "The primary reading is unfavorable for worldly matters; conditional for spiritual ones."),
    (9, [9], "9th_lord",
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     "1B_matrix", [],
     "9th lord dasha is among the most auspicious in LP's framework — the 'fortune dasha.' "
     "The 9th house governs luck, dharma, father, higher learning, and blessings of preceptors. "
     "Its dasha produces: father's honor or support, pilgrimage or spiritual journeys, "
     "academic advancement, windfall gains, and overall fortune. LP states that when the "
     "9th lord is strong, this dasha can transform the native's life circumstances upward "
     "dramatically. Combined with the 10th lord, it can produce peak raja yoga results."),
    (10, [10], "10th_lord",
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     "1B_matrix", [],
     "10th lord (karma lord) dasha is the prime career dasha per LP. The 10th house governs "
     "profession, public role, authority, and social status. Its dasha brings career peak, "
     "promotions, public recognition, and exercise of authority. The native may take on "
     "leadership roles or achieve public visibility. LP notes that the 10th lord dasha "
     "is the most decisive for career trajectories — strong 10th lord gives sustained "
     "career growth, weak 10th lord gives career activity but with reversals."),
    (11, [11], "11th_lord",
     "favorable", "moderate",
     ["wealth", "career_status"],
     "1B_matrix", [],
     "11th lord dasha brings gains, fulfillment of long-term desires, profits from trade, "
     "and elder sibling-related matters. LP classifies the 11th as an upachaya: results "
     "improve over time and are better for natural malefics as 11th lord. "
     "The dasha delivers monetary gains, social connections, and achievement of aspirations. "
     "However, LP notes that natural benefics as 11th lord give weaker gains than malefics, "
     "since benefics lose strength in upachaya houses per Parashari doctrine."),
    (12, [12], "12th_lord",
     "mixed", "moderate",
     ["foreign_travel", "spirituality"],
     "1B_matrix", [],
     "12th lord dasha activates expenditure, foreign residence, bed pleasures, and "
     "separation themes. LP gives a nuanced view: the 12th dasha is unfavorable for "
     "worldly accumulation (expenditure exceeds income) but beneficial for those seeking "
     "liberation (moksha), spiritual retreat, or foreign travel. Hospital stays, isolation, "
     "or ashram residence may feature. If the 12th lord is also a trikona lord or connects "
     "with spirituality, the dasha can be deeply transformative for dharmic pursuits."),
    # ── Trikona lord enhancements ─────────────────────────────────────────────
    (13, [5, 9], "trikona_lord",
     "favorable", "strong",
     ["spirituality", "wealth", "fame_reputation"],
     "1B_matrix", [],
     "When the dasha lord owns either the 5th or 9th house (trikona), LP states that "
     "the dasha is inherently dharmic and auspicious regardless of the planet's natural "
     "nature. Trikona lords in dasha bring merit from past actions (purva punya), "
     "blessings of dharma, fortune, and good reputation. The more the trikona lord is "
     "free from dusthana associations, the more purely the dharmic results manifest."),
    (14, [5], "5th_lord_specific",
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     "1B_matrix", [],
     "5th lord dasha specifically (distinct from 9th): LP states children-related "
     "events (birth, education of children), creative achievements, and expressions "
     "of past-life merit are most prominently activated. Academic recognition, creative "
     "work gaining appreciation, and investment gains are 5th lord dasha specialties. "
     "The mind becomes sharp and innovative. This is LP's primary dasha for intellectual "
     "transformation."),
    (15, [9], "9th_lord_specific",
     "favorable", "strong",
     ["wealth", "spirituality"],
     "1B_matrix", [],
     "9th lord dasha specifically: LP distinguishes this as the 'bhagya dasha' — fortune "
     "period. Father's influence and blessings manifest. Pilgrimages and journeys to "
     "sacred places, encounters with teachers and gurus, sudden positive turns in fortune. "
     "The 9th house represents the highest dharmic merit in LP's framework: its dasha is "
     "the supreme testing ground for whether the native's past dharmic actions yield fruit."),
    # ── Kendra lord dasha variations ─────────────────────────────────────────
    (16, [4, 7, 10], "kendra_lord_malefic",
     "favorable", "moderate",
     ["career_status", "property_vehicles"],
     "1B_matrix", [],
     "When a natural malefic (Sun, Mars, Saturn) owns a kendra house (H4, H7, or H10), "
     "LP states its dasha delivers temporal worldly results: career gains, property, "
     "status. Natural malefics in kendra positions lose some malefic quality and deliver "
     "concrete worldly achievements during their dasha. This is the basis for Saturn's "
     "strength in H7/H10 and Mars's strength in H4/H10 for various lagnas."),
    (17, [4, 7, 10], "kendra_lord_benefic_kd",
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     "1B_matrix", [],
     "When a natural benefic (Jupiter, Venus, Mercury, Moon) owns a kendra house "
     "without co-owning a trikona, kendradhipati dosha applies during its dasha. "
     "The dasha activates the kendra's significations but the natural benefic quality "
     "is suppressed: what should be wisdom (Jupiter) or beauty (Venus) becomes "
     "overindulgence, laxity, or poor judgment. LP explicitly states: natural benefics "
     "as kendra lords lose benefic quality proportionate to kendra ownership."),
    (18, [4], "4th_lord_kendra",
     "favorable", "moderate",
     ["property_vehicles", "mental_health"],
     "1B_matrix", [],
     "4th lord dasha (kendra activation): LP notes property purchase, vehicle acquisition, "
     "domestic renovation, and mother-related events as primary. Emotional happiness "
     "and peace of mind are 4th house products. This dasha is favorable for real estate, "
     "agricultural pursuits, and establishing a stable domestic base."),
    (19, [7], "7th_lord_maraka",
     "mixed", "conditional",
     ["marriage", "longevity"],
     "1B_matrix", [],
     "7th lord dasha carries a dual mandate in LP: partnership activation AND maraka "
     "potential. For natives in mid-life, 7th lord dasha primarily gives marriage and "
     "business results. For elderly natives, the maraka potential becomes primary. "
     "LP states the 7th lord's dasha timing must be assessed against longevity "
     "indications — when the native is in a vulnerable phase, 7th lord dasha warrants "
     "caution even while delivering relationship events."),
    (20, [10], "10th_lord_karma",
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     "1B_matrix", [],
     "10th lord (karma bhava) dasha is LP's primary career-peak period. "
     "Authority, leadership, public service, political success, and professional "
     "recognition all manifest. LP notes the 10th dasha is the most publicly visible "
     "of all dashas — whatever the native does during this period tends to receive "
     "public attention. Excellent for entrepreneurs, politicians, and public figures."),
    # ── Dusthana lord variations ──────────────────────────────────────────────
    (21, [6, 8, 12], "dusthana_lord_pure",
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     "1B_matrix", [],
     "When a planet is purely a dusthana lord (owning H6, H8, or H12 without beneficial "
     "co-lordship), LP states its dasha is a period of trials. Enemies, disease, debts, "
     "obstacles, and losses are activated. The specific nature depends on which dusthana: "
     "H6 = enemies/disease, H8 = sudden events/longevity, H12 = expenditure/foreign. "
     "If the planet also owns a kendra or trikona, the dusthana lord effects are moderated."),
    (22, [6], "6th_lord_pure",
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     "1B_matrix", [],
     "Pure 6th lord dasha: enemies become active and confrontational, legal disputes "
     "and service conflicts arise, health issues manifest — particularly those related "
     "to lifestyle (diet, overwork). Debts accumulate. LP notes this dasha tests the "
     "native's ability to manage opposition and illness. A strong 6th lord gives "
     "eventual victory over enemies; a weak one leaves the native overwhelmed by opposition."),
    (23, [8], "8th_lord_pure",
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     "1B_matrix", [],
     "Pure 8th lord dasha is LP's most difficult period for longevity. Sudden, unexpected "
     "events disrupt the life course: accidents, serious illness, surgery, death of close "
     "relatives. The 8th dasha often marks a crisis point. However, LP also notes the "
     "8th house contains 'ayushkaraka' indications — the dasha outcome depends heavily "
     "on whether the 8th lord is strong (indicating transformative survival) or weak "
     "(indicating an actual health/longevity crisis)."),
    (24, [12], "12th_lord_pure",
     "mixed", "moderate",
     ["foreign_travel", "spirituality"],
     "1B_matrix", [],
     "12th lord dasha activates the themes of foreign lands, expenditure, and "
     "endings. LP distinguishes by context: for worldly natives, this dasha brings "
     "financial losses, separation from family, and hospital/prison-related themes. "
     "For spiritually inclined natives, the 12th dasha can be liberation — moksha "
     "practices deepen, overseas residence brings growth, and worldly detachment "
     "becomes a conscious choice rather than a forced condition."),
    # ── Yogakaraka dasha ──────────────────────────────────────────────────────
    (25, [4, 5, 9, 10], "yogakaraka",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation", "spirituality"],
     "1B_matrix", [],
     "Yogakaraka dasha is LP's pinnacle auspicious period. A planet owning both a kendra "
     "(H4/H7/H10) and a trikona (H5/H9) simultaneously produces raja yoga — the combination "
     "of karma and dharma that delivers outstanding worldly and spiritual results. "
     "Career peaks, wealth accumulation, public recognition, and dharmic fulfillment "
     "all manifest together. LP treats yogakaraka dasha as qualitatively different from "
     "mere trikona or kendra lord dashas — it is the highest-grade functional benefic period."),
    (26, [4, 5, 9, 10], "yogakaraka_strong",
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     "1B_matrix", [],
     "When the yogakaraka is strong (own sign, exalted, or in a kendra/trikona house), "
     "its dasha produces the clearest raja yoga fructification. LP states a strong "
     "yogakaraka dasha brings: rapid career advancement, political success, wealth "
     "generation, name and fame in society, and fulfillment of major life ambitions. "
     "This period often marks the peak achievement phase of the native's life."),
    (27, [4, 5, 9, 10], "yogakaraka_weak",
     "favorable", "moderate",
     ["career_status", "wealth"],
     "1B_matrix", [],
     "Even when the yogakaraka is weak (debilitated, in enemy sign, or conjunct malefics), "
     "LP states its dasha retains favorable quality — the raja yoga is reduced in intensity "
     "but not negated. Career progress occurs but with delays and obstacles. "
     "Wealth comes but through harder effort. The yogakaraka's lordship status provides "
     "a floor of auspiciousness that even a weak placement cannot eliminate entirely."),
    # ── Maraka dasha ─────────────────────────────────────────────────────────
    (28, [2], "maraka_2nd_lord",
     "mixed", "conditional",
     ["wealth", "longevity"],
     "1B_matrix", [],
     "2nd lord as maraka dasha: LP states H2 lord activates wealth and family during "
     "the earlier phases of the dasha, but the maraka potential intensifies in the "
     "later phase. For elderly natives completing their natural lifespan, the 2nd lord "
     "dasha can trigger the maraka event (illness, death). For younger natives, "
     "the dasha primarily delivers wealth and family matters with the maraka threat dormant."),
    (29, [7], "maraka_7th_lord",
     "mixed", "conditional",
     ["marriage", "longevity"],
     "1B_matrix", [],
     "7th lord as maraka dasha: LP emphasizes the 7th lord is the second most powerful "
     "maraka after the 2nd lord. The dasha delivers partnership results (marriage, business) "
     "in the primary phase, but as the dasha progresses and especially in old age, "
     "the maraka potential escalates. LP advises examining the 7th lord's strength and "
     "placement carefully to time the maraka risk accurately within this dasha."),
    (30, [2, 7], "maraka_both_lords",
     "unfavorable", "strong",
     ["longevity"],
     "1B_matrix", [],
     "When the same planet owns both H2 and H7 (applies to Aries — Venus; Libra — Mars), "
     "LP designates this planet as the supreme maraka: the strongest death-inflicting "
     "planet for that lagna. Its dasha concentrates maraka potential in one period. "
     "For Aries, Venus dasha is the primary maraka concern; for Libra, Mars dasha. "
     "LP states this double-maraka planet's dasha requires the most careful longevity "
     "assessment, especially when it falls late in the native's life."),
    # ── Kendradhipati planet as dasha lord ────────────────────────────────────
    (31, [4, 7, 10], "kendradhipati_dasha",
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     "1B_matrix", [],
     "Natural benefic (Jupiter, Venus, Mercury, Moon) owning a kendra as dasha lord: "
     "LP states that kendradhipati dosha is most strongly felt during the planet's "
     "own mahadasha. The expected wisdom (Jupiter), beauty (Venus), or intelligence "
     "(Mercury) becomes clouded by the weight of kendra lordship. Overindulgence, "
     "poor discretion, or passive ineffectiveness characterize these dashas. "
     "The native expects the benefic's natural gifts but receives diluted, kendra-bound results."),
    # ── Badhaka lord dasha ────────────────────────────────────────────────────
    (32, [11], "badhaka_movable",
     "unfavorable", "moderate",
     ["enemies_litigation", "mental_health"],
     "1B_matrix", [],
     "For movable lagnas (Aries, Cancer, Libra, Capricorn), the 11th house lord is the "
     "badhaka (obstructing) planet per LP. During the badhaka lord's dasha, unexpected "
     "obstructions arise in all areas: hidden enemies, bureaucratic delays, health "
     "issues from unidentified sources. LP notes the badhaka operates through "
     "mysterious channels — the obstacle's source is often not apparent at first. "
     "This dasha requires patience and avoidance of new risky ventures."),
    (33, [9], "badhaka_fixed",
     "mixed", "moderate",
     ["spirituality", "enemies_litigation"],
     "1B_matrix", [],
     "For fixed lagnas (Taurus, Leo, Scorpio, Aquarius), the 9th house lord is the "
     "badhaka per LP. This creates a paradox: the 9th lord is normally the most "
     "auspicious trikona lord, but as badhaka for fixed lagnas, it simultaneously "
     "carries obstructive potential. LP resolves this by noting the badhaka effect "
     "manifests as unexpected reversals at the peak of fortune periods — when things "
     "seem most favorable, the badhaka obstruction arrives to test the native."),
    (34, [7], "badhaka_dual",
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     "1B_matrix", [],
     "For dual/mutable lagnas (Gemini, Virgo, Sagittarius, Pisces), the 7th house lord "
     "is both the maraka and the badhaka per LP. This makes the 7th lord doubly "
     "dangerous: it carries both death-inflicting (maraka) and obstruction (badhaka) "
     "potential. LP considers this the most powerful functional malefic designation: "
     "the 7th lord dasha for dual lagnas is the period of maximum maraka-badhaka risk, "
     "requiring the most careful timing assessment."),
    # ── Upachaya behaviour ────────────────────────────────────────────────────
    (35, [3, 6, 10, 11], "upachaya_malefic",
     "favorable", "moderate",
     ["career_status", "wealth"],
     "1B_matrix", [],
     "LP states that natural malefics (Sun, Mars, Saturn) as lords of upachaya houses "
     "(H3, H6, H10, H11) give better results during their dasha than natural benefics "
     "in the same positions. The upachaya houses require the competitive, driving energy "
     "of malefics to fully deliver their significations: courage (H3), victory over enemies "
     "(H6), career authority (H10), and sustained gains (H11). Malefic dasha lords for "
     "these houses produce concrete worldly achievements."),
    (36, [3, 6, 11], "upachaya_benefic",
     "neutral", "weak",
     ["career_status"],
     "1B_matrix", [],
     "Natural benefics (Jupiter, Venus, Mercury, Moon) as lords of upachaya houses "
     "(H3, H6, H11) give weaker upachaya results per LP. The gentle, expanding energy "
     "of benefics lacks the drive to fully utilize the competitive upachaya houses. "
     "H6 lord as benefic may lose to enemies rather than defeat them; H3 benefic lord "
     "prefers diplomacy to decisive action. LP treats benefic-in-upachaya as a "
     "functional weakening, reducing the dasha's worldly effectiveness."),
    # ── Dignity modifications ─────────────────────────────────────────────────
    (37, [], "exalted_dasha_lord",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     "1B_matrix", [],
     "LP states that an exalted dasha lord delivers its house significations fully and "
     "powerfully. Whatever houses the planet owns, their themes manifest prominently and "
     "auspiciously during the dasha. Career peaks, wealth gains, recognition — all occur "
     "with ease and momentum. An exalted lagna lord dasha gives peak vitality; "
     "an exalted trikona lord gives peak dharmic results; exalted yogakaraka gives "
     "the most exceptional raja yoga results possible in a lifetime."),
    (38, [], "debilitated_dasha_lord",
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     "1B_matrix", [],
     "A debilitated dasha lord denies or delays its house significations per LP. "
     "The planet's weakness means it cannot fully activate what it owns. A debilitated "
     "lagna lord brings health struggles; debilitated 9th lord denies fortune; "
     "debilitated yogakaraka reduces raja yoga to mild career progress at best. "
     "LP notes that neecha-bhanga (cancellation of debility) partially restores results, "
     "but the debilitation's shadow remains even when cancelled."),
    (39, [], "own_sign_dasha",
     "favorable", "moderate",
     ["career_status", "wealth"],
     "1B_matrix", [],
     "A dasha lord in its own sign (swa-kshetra) delivers its house results reliably and "
     "consistently per LP. The planet in own sign has the confidence and resources to "
     "fulfill its ownership obligations. Results come steadily throughout the dasha rather "
     "than in bursts. LP treats own-sign placement as the baseline for normal, expected "
     "delivery of house significations — neither the peak of exaltation nor the challenge "
     "of debility."),
    (40, [], "retrograde_dasha",
     "mixed", "moderate",
     ["mental_health", "character_temperament"],
     "1B_matrix", [],
     "LP notes that retrograde (vakri) planets during dasha activate internalized, "
     "delayed, or revisited themes. The dasha lord in retrogression causes its house "
     "results to unfold in non-linear ways: matters may resolve after review, "
     "old situations resurface requiring re-examination, or the native revisits "
     "past decisions related to the owned houses. Results eventually arrive but "
     "with a characteristic delay or need for revision."),
    # ── Special ownership combinations ───────────────────────────────────────
    (41, [1, 8], "lagna_dusthana_same",
     "mixed", "moderate",
     ["physical_health", "longevity"],
     "1B_matrix", [],
     "When the lagna lord also owns H8 (e.g., Mars for Aries — H1+H8; Venus for Libra — "
     "H1+H8), LP notes a mixed dasha: the lagna lord's protection of the self is strong, "
     "but the H8 co-ownership brings obstacles, sudden events, and longevity concerns. "
     "The native feels personally energized (lagna) but faces unexpected disruptions (H8). "
     "LP states the lagna lord's protective quality ultimately prevails but the H8 "
     "disruptions cannot be fully avoided during this dasha."),
    (42, [9, 10], "trikona_kendra_combined",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation", "spirituality"],
     "1B_matrix", [],
     "LP explicitly states that when a single planet owns both a trikona (H9) and a "
     "kendra (H10) — the dharma-karma adhipati yoga — its dasha produces outstanding "
     "results. The combination of fortune (H9) and career (H10) in one planet's dasha "
     "aligns dharmic merit with worldly action. This is distinct from yogakaraka (H4/H7/H10 "
     "+ H5/H9) but similarly powerful. Examples: Saturn for Taurus (H9+H10); "
     "any planet in a lagna where H9 and H10 lords happen to be the same."),
    (43, [2, 9], "wealth_fortune_combined",
     "favorable", "moderate",
     ["wealth", "spirituality"],
     "1B_matrix", [],
     "When a planet owns both H2 (wealth) and H9 (fortune), LP notes its dasha delivers "
     "financial prosperity grounded in dharmic merit. The example is Mars for Pisces "
     "(owns H2 Aries + H9 Scorpio). The dasha activates both accumulation (H2) and "
     "fortune (H9) simultaneously, producing sustained wealth gains with a philosophical "
     "or dharmic character. However, H2 maraka element adds a caveat for elderly natives."),
    (44, [3, 6], "double_dusthana_combo",
     "unfavorable", "moderate",
     ["enemies_litigation", "physical_health"],
     "1B_matrix", [],
     "When a planet owns two dusthana-adjacent houses (e.g., H3+H6 or H6+H8), LP notes "
     "that its dasha is doubly challenging. The compounding of obstacle themes "
     "(sibling conflicts + enemies; or enemies + sudden events) makes this among the "
     "more difficult dasha types. However, LP also notes that natural malefics as "
     "H3+H6 lords give battle-hardened energy — the native confronts and often overcomes "
     "the challenges through persistent effort rather than succumbing to them."),
    (45, [6, 9], "trikona_dusthana_dasha",
     "mixed", "conditional",
     ["spirituality", "enemies_litigation"],
     "1B_matrix", [],
     "LP's trikona-dusthana planet (e.g., Jupiter for Cancer owning H6+H9, or Saturn for "
     "Gemini owning H8+H9) creates a complex dasha: fortune and dharma (H9/H5) compete "
     "with obstacle themes (H6/H8/H12) in the same period. The dasha alternates: "
     "some years show fortune and blessings; others show enemies or hidden obstacles. "
     "LP states the trikona portion ultimately prevails for a well-placed planet, "
     "but the dusthana influence cannot be entirely eliminated."),
]


def _build_dasha_rules() -> list[RuleRecord]:
    rules = []
    for (suffix, houses, label, odir, oint, odoms, phase, lagna_scope, desc) in _DASHA_DATA:
        rid = f"LPD{suffix:03d}"
        tags = ["lpd", "parashari", "laghu_parashari", "dasha_results", label]
        for h in houses:
            tags.append(f"house_{h}")
        if "yogakaraka" in label:
            tags.append("yogakaraka")
        if "maraka" in label:
            tags.append("maraka")
        if "badhaka" in label:
            tags.append("badhaka")
        if "kendradhipati" in label:
            tags.append("kendradhipati_dosha")
        rules.append(RuleRecord(
            rule_id=rid,
            source="LaghuParashari",
            chapter="Ch.4–5",
            school="parashari",
            category="dasha_results",
            description=f"[LP — {label} dasha] {desc}",
            confidence=0.65,
            tags=list(dict.fromkeys(tags)),
            implemented=False,
            primary_condition={
                "placement_type": "house_lordship_dasha",
                "placement_value": houses,
                "lordship_label": label,
            },
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing="dasha_dependent",
            lagna_scope=lagna_scope,
            verse_ref="Ch.4 v.1",
            phase=phase,
            system="natal",
        ))
    return rules


LAGHU_PARASHARI_DASHA_REGISTRY = CorpusRegistry()
for _rule in _build_dasha_rules():
    LAGHU_PARASHARI_DASHA_REGISTRY.add(_rule)
