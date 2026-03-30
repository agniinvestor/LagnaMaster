"""
src/corpus/bhavartha_ratnakara_1.py — S267: Bhavartha Ratnakara, Aries + Taurus

Bhavartha Ratnakara (Bhava-artha Ratnakara) by Ramanujacharya.
Lagna-conditional predictions: every rule has lagna_scope populated.
Phase 1B_conditional throughout.

Chapter 1 — Aries (Mesha) lagna: BVR001–BVR065
Chapter 2 — Taurus (Vrishabha) lagna: BVR066–BVR130

Functional classification reference (from LPF / Laghu Parashari):
  Aries: Sun=H5(trikona), Moon=H4(KD), Mars=H1+H8(lagna lord), Mercury=H3+H6(malefic),
         Jupiter=H9+H12(trikona-dusthana), Venus=H2+H7(double maraka), Saturn=H10+H11
  Taurus: Sun=H4(kendra), Moon=H3(malefic), Mars=H7+H12(maraka-dusthana),
          Mercury=H2+H5(trikona), Jupiter=H8+H11(malefic), Venus=H1+H6(lagna lord),
          Saturn=H9+H10(yogakaraka)
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ─────────────────────────────────────────────────────────────────────────────
# Data format: (planet, placement_type, house_or_label, lord_of_houses,
#              odir, oint, domains, extra_tags, verse_ref, desc)
# placement_type: "house_placement" | "yoga" | "conjunction" | "dignity"
# ─────────────────────────────────────────────────────────────────────────────

# ── Chapter 1: Aries (Mesha) lagna ───────────────────────────────────────────
# Functional context: Mars is lagna lord; Sun is prime trikona lord (H5);
# Jupiter is trikona-dusthana (H9+H12); Venus is double maraka (H2+H7).

_ARIES_DATA = [
    # ── Sun (H5 lord — trikona lord) ──────────────────────────────────────────
    ("sun", "house_placement", 1, [5],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "trikona_lord_in_lagna"],
     "Ch.1 v.1",
     "Sun as H5 (trikona) lord placed in H1 (lagna) for Aries: the dharmic intelligence "
     "and creative force of the 5th house floods the native's personality. BR states "
     "Aries natives with Sun in lagna develop strong authority, government connections, "
     "and leadership roles. Children bring pride. The native's intelligence and dharmic "
     "merit manifest in the personality directly. Excellent for politics and public roles."),
    ("sun", "house_placement", 5, [5],
     "favorable", "strong",
     ["progeny", "intelligence_education", "spirituality"],
     ["sun", "trikona_lord_in_trikona"],
     "Ch.1 v.2",
     "Sun in H5 (own-functional house) for Aries: trikona lord in trikona — BR states "
     "this is the finest placement for Aries Sun. Children succeed, creative achievements "
     "peak, intelligence is razor-sharp, and past-life merit (purva punya) bears fruit "
     "immediately. Speculative investments succeed. Academic recognition comes readily. "
     "Sun here gives an exceptionally creative and intellectually bright native."),
    ("sun", "house_placement", 9, [5],
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     ["sun", "trikona_lord_in_trikona", "double_trikona"],
     "Ch.1 v.3",
     "Sun as H5 lord placed in H9 (trikona) for Aries: double trikona activation. "
     "BR states fortune is outstanding, father is highly respected or holds authority, "
     "and the native achieves recognition in dharmic, governmental, or educational fields. "
     "Pilgrimage journeys and spiritual pursuits are well-supported. This placement "
     "combines H5 intelligence with H9 fortune — the native is both wise and lucky."),
    ("sun", "house_placement", 10, [5],
     "favorable", "strong",
     ["career_status", "fame_reputation", "intelligence_education"],
     ["sun", "trikona_lord_in_kendra", "dharmakarmayoga"],
     "Ch.1 v.4",
     "Sun as H5 lord in H10 (kendra) for Aries: dharma-karma yoga. BR states career "
     "advancement through intelligence, creativity, or government service. The native "
     "achieves prominence in professional life, often in education, politics, or "
     "creative fields. Public recognition for intellectual contributions. "
     "Sun in H10 for Aries = peak career through merit and creative authority."),
    ("sun", "house_placement", 4, [5],
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["sun"],
     "Ch.1 v.5",
     "Sun as H5 lord in H4 (kendra) for Aries: property and happiness through "
     "intelligence and government. BR notes the native acquires property and vehicles "
     "through merit and official connections. Mother is respected or holds official "
     "status. Domestic happiness is tied to educational and creative achievements. "
     "Overall favorable for property but not as peak as 1st/5th/9th/10th placements."),
    ("sun", "house_placement", 3, [5],
     "neutral", "moderate",
     ["career_status", "character_temperament"],
     ["sun"],
     "Ch.1 v.6",
     "Sun as H5 lord in H3 for Aries: creativity expressed through communication, "
     "writing, short travels. BR states the native may work in media, publishing, "
     "or as a communicator. Siblings may be in government or creative professions. "
     "The H5 creative energy finds expression through effort and communication "
     "channels — workable but not as directly powerful as the kendra/trikona placements."),
    ("sun", "house_placement", 6, [5],
     "mixed", "moderate",
     ["intelligence_education", "enemies_litigation"],
     ["sun"],
     "Ch.1 v.7",
     "Sun as H5 lord in H6 (dusthana) for Aries: BR states intelligence may be applied "
     "toward enemies or competitive fields (law, medicine, sports). Children may face "
     "health challenges. The native excels in competitive examinations and service roles "
     "but the 5th house significations are partially obstructed by the dusthana placement. "
     "Fame comes through overcoming obstacles rather than ease."),
    ("sun", "house_placement", 12, [5],
     "mixed", "weak",
     ["spirituality", "foreign_travel"],
     ["sun"],
     "Ch.1 v.8",
     "Sun as H5 lord in H12 for Aries: BR notes loss or limitation in 5th house matters. "
     "Children may be born abroad or have health concerns. The native may seek spiritual "
     "knowledge in foreign lands. Past-life merit is spent in foreign places rather than "
     "at home. However, for spiritual seekers, this placement is excellent — the H5 "
     "intelligence is channeled into moksha-oriented pursuits."),
    # ── Moon (H4 lord — kendradhipati) ───────────────────────────────────────
    ("moon", "house_placement", 1, [4],
     "mixed", "moderate",
     ["mental_health", "physical_health"],
     ["moon", "kendradhipati_in_lagna"],
     "Ch.1 v.9",
     "Moon as H4 (kendradhipati) lord in H1 for Aries: BR states emotional sensitivity "
     "and mental fluctuations define the personality. Kendradhipati dosha in the lagna "
     "means the native's mind and emotions are primary drivers but with instability. "
     "Health is connected to emotional state — Moon's KD nature makes this a mixed "
     "placement. Physical appearance is pleasant (Moon's natural influence) but the "
     "mind causes health disruptions."),
    ("moon", "house_placement", 4, [4],
     "mixed", "moderate",
     ["property_vehicles", "mental_health"],
     ["moon", "kendradhipati_own_house"],
     "Ch.1 v.10",
     "Moon in H4 (own functional house, Cancer = H4 for Aries) for Aries: Moon in own "
     "sign is strong but BR notes the KD dosha is still operative. Domestic life is "
     "comfortable and mother is close to the native. Property may be acquired but "
     "emotional complications in the domestic sphere. The mind is strong but unstable — "
     "the native fluctuates between comfort and dissatisfaction at home."),
    ("moon", "house_placement", 5, [4],
     "favorable", "moderate",
     ["progeny", "mental_health", "intelligence_education"],
     ["moon"],
     "Ch.1 v.11",
     "Moon as H4 lord in H5 (trikona) for Aries: BR states domestic happiness and "
     "trikona trikona connection — mother and children have a strong, positive bond. "
     "The native's mind becomes oriented toward learning and children. Emotional "
     "intelligence is heightened. Trikona placement partially mitigates KD dosha — "
     "Moon's negative KD quality is softened by the dharmic 5th house context."),
    ("moon", "house_placement", 9, [4],
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["moon"],
     "Ch.1 v.12",
     "Moon as H4 lord in H9 for Aries: happiness and domestic contentment connected "
     "to fortune and dharmic pursuits. BR states the native finds emotional fulfillment "
     "through spiritual journeys and father's blessings. Mother may be dharmic or "
     "spiritually inclined. Property acquired in sacred or auspicious locations. "
     "The trikona placement reduces KD's negative impact significantly."),
    ("moon", "house_placement", 10, [4],
     "mixed", "moderate",
     ["career_status", "mental_health"],
     ["moon", "kendradhipati_in_kendra"],
     "Ch.1 v.13",
     "Moon as H4 lord in H10 for Aries: double kendra — KD in kendra placement. "
     "BR states career involves domestic, maternal, or emotional themes (hospitality, "
     "real estate, education). But the KD dosha compounds: both the Moon's natural "
     "benefic quality and the career significations are partially compromised. "
     "Emotional fluctuations affect professional life. Results come with effort."),
    ("moon", "house_placement", 7, [4],
     "mixed", "moderate",
     ["marriage", "mental_health"],
     ["moon"],
     "Ch.1 v.14",
     "Moon as H4 lord in H7 (maraka kendra) for Aries: emotional partnerships and "
     "domestic matters merge in the marriage house. BR states the native seeks emotional "
     "security through marriage — spouse plays a nurturing role. However, H7 is a maraka "
     "house, and Moon here adds an emotional maraka element. Partnership happiness is "
     "real but emotionally intense; health concerns may manifest through partnership "
     "stress."),
    # ── Mars (H1+H8 lord — lagna lord) ───────────────────────────────────────
    ("mars", "house_placement", 1, [1, 8],
     "favorable", "strong",
     ["physical_health", "character_temperament", "career_status"],
     ["mars", "lagna_lord_in_lagna"],
     "Ch.1 v.15",
     "Mars as lagna lord in H1 for Aries: the strongest self-placement. BR states the "
     "Aries native with Mars in lagna is courageous, physically robust, and assertively "
     "successful. Leadership comes naturally. The native acts decisively and achieves "
     "goals through direct effort. Though Mars also rules H8 (obstacles), the lagna "
     "lord's strength in its own house overwhelmingly dominates — this is the most "
     "powerful configuration for Aries."),
    ("mars", "house_placement", 3, [1, 8],
     "favorable", "strong",
     ["career_status", "character_temperament"],
     ["mars"],
     "Ch.1 v.16",
     "Mars as lagna lord in H3 (upachaya) for Aries: BR states exceptional courage, "
     "initiative, and effort-based success. Siblings are supportive or prosperous. "
     "Mars in the upachaya house gives improving results over time. The native wins "
     "through persistent effort, short expeditions, and bold communication. "
     "Success in competitive, physically demanding, or communication-based careers."),
    ("mars", "house_placement", 5, [1, 8],
     "favorable", "strong",
     ["intelligence_education", "progeny", "career_status"],
     ["mars", "lagna_lord_in_trikona"],
     "Ch.1 v.17",
     "Mars as lagna lord in H5 (trikona) for Aries: BR states outstanding intelligence "
     "and courage combined. Children are successful, especially in competitive or "
     "technical fields. The native achieves recognition through both intellectual and "
     "physical prowess. Speculative investments succeed when approached with courage. "
     "Lagna lord in trikona is an excellent disposition for Aries."),
    ("mars", "house_placement", 9, [1, 8],
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     ["mars", "lagna_lord_in_trikona"],
     "Ch.1 v.18",
     "Mars as lagna lord in H9 for Aries: fortune and dharma support the entire self. "
     "BR states the native is blessed by father, fortune, and guru. Journeys abroad "
     "or to sacred places are successful. The native achieves recognition through "
     "dharmic causes, athletic or military service, or pioneering adventures. "
     "Excellent for those in physical, competitive, or exploratory professions."),
    ("mars", "house_placement", 10, [1, 8],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "lagna_lord_in_kendra"],
     "Ch.1 v.19",
     "Mars as lagna lord in H10 for Aries: career peak through direct, courageous action. "
     "BR states the native achieves highest career positions through effort, leadership, "
     "and decisive action. Government service, military, engineering, or sports careers "
     "are favored. Public recognition is outstanding. Lagna lord in karma kendra gives "
     "the most pronounced career activation for Aries."),
    ("mars", "house_placement", 4, [1, 8],
     "mixed", "moderate",
     ["property_vehicles", "longevity"],
     ["mars"],
     "Ch.1 v.20",
     "Mars as lagna lord (H1) + H8 lord in H4 (kendra) for Aries: property and vehicles "
     "are acquired but with some obstacles. BR notes the H8 co-lordship brings hidden "
     "challenges to domestic life — unexpected events, renovation needs, or property "
     "disputes. The lagna lord's strength provides resilience but the H8 element "
     "means domestic circumstances are tested. Mother's health may require attention."),
    ("mars", "house_placement", 6, [1, 8],
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["mars"],
     "Ch.1 v.21",
     "Mars as lagna lord in H6 (dusthana) for Aries: BR states enemies are overcome "
     "through raw courage and competitive spirit. Mars in H6 gives victory over "
     "opponents in competitions, legal battles, and physical conflicts. Health is "
     "robust overall but accidents or injuries are possible. The lagna lord in dusthana "
     "means the native must continually fight for position and health."),
    ("mars", "house_placement", 7, [1, 8],
     "mixed", "moderate",
     ["marriage", "longevity"],
     ["mars", "lagna_lord_in_maraka"],
     "Ch.1 v.22",
     "Mars as lagna lord in H7 (maraka) for Aries: BR notes partnerships are bold and "
     "passionate but the maraka house placement creates self-maraka concerns. The native "
     "may take risks in partnerships or business dealings that affect health. Marriage "
     "involves a courageous or competitive partner. Longevity assessment requires care "
     "during Mars dasha with Mars in H7."),
    ("mars", "house_placement", 8, [1, 8],
     "mixed", "moderate",
     ["longevity", "mental_health"],
     ["mars", "8th_lord_own_house"],
     "Ch.1 v.23",
     "Mars in H8 (own functional house, H8 lord in H8) for Aries: BR notes longevity "
     "strength through the 8th house's ayushkaraka nature. However, Mars here also "
     "causes sudden events, surgical interventions, and accidents. The lagna lord's "
     "co-ownership partially mitigates through personal resilience. The native has "
     "strong survival instincts but faces periodic health crises."),
    ("mars", "house_placement", 11, [1, 8],
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mars"],
     "Ch.1 v.24",
     "Mars as lagna lord in H11 (upachaya, gains) for Aries: BR states gains through "
     "bold action, elder siblings' support, and competitive ventures. The native earns "
     "through effort and courage. Elder siblings are supportive and may be in competitive "
     "professions. Aspirations are fulfilled through direct, assertive pursuit. "
     "Upachaya placement gives improving results over the full Mars dasha period."),
    ("mars", "house_placement", 12, [1, 8],
     "mixed", "weak",
     ["foreign_travel", "spirituality"],
     ["mars"],
     "Ch.1 v.25",
     "Mars as lagna lord in H12 for Aries: BR warns of physical depletion and "
     "loss of vitality when lagna lord goes to H12. Foreign residence is possible, "
     "and the native may achieve in foreign lands. Expenditure on health is elevated. "
     "The lagna lord in H12 weakens personal authority and health reserves. "
     "For spiritual seekers, foreign retreats or ashram life brings fulfillment."),
    # ── Mercury (H3+H6 lord — functional malefic) ────────────────────────────
    ("mercury", "house_placement", 1, [3, 6],
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     ["mercury"],
     "Ch.1 v.26",
     "Mercury as H3+H6 lord in H1 for Aries: BR states enemies cause health issues "
     "and the native becomes combative in communication. The H6 co-ownership in the "
     "lagna creates a personality prone to disputes, overanalysis, and nervous tension. "
     "The native may face sibling-related conflicts and health issues from stress or "
     "overwork. Mercury as functional malefic in the lagna is unfavorable for Aries."),
    ("mercury", "house_placement", 3, [3, 6],
     "neutral", "moderate",
     ["career_status", "character_temperament"],
     ["mercury"],
     "Ch.1 v.27",
     "Mercury in H3 (own functional house) for Aries: BR notes communication talents "
     "are present but the H6 co-ownership creates enemies through words. The native "
     "is clever but may use intelligence for competitive or litigious purposes. "
     "Siblings may be in service or health professions. Courage and communication "
     "combine but with a contentious edge."),
    ("mercury", "house_placement", 5, [3, 6],
     "mixed", "moderate",
     ["intelligence_education", "enemies_litigation"],
     ["mercury"],
     "Ch.1 v.28",
     "Mercury as H3+H6 lord in H5 (trikona) for Aries: BR notes the native's "
     "intelligence is acute and analytical but directed toward competitive matters. "
     "Excellent for law, medicine, or research. Children may have health concerns. "
     "Intelligence activates but with a disputatious quality — the native argues "
     "brilliantly but may create enemies through intellectual overreach."),
    ("mercury", "house_placement", 6, [3, 6],
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     ["mercury", "6th_lord_own_house"],
     "Ch.1 v.29",
     "Mercury in H6 (own functional H6) for Aries: BR states service, health professions, "
     "and competitive fields are active themes. Enemies are overcome through intelligence "
     "and analysis. The native may work in health, law, or detail-oriented service. "
     "However, health issues from overwork and nervous system strain are possible. "
     "Victory over enemies through analytical means."),
    ("mercury", "house_placement", 7, [3, 6],
     "unfavorable", "moderate",
     ["marriage", "enemies_litigation"],
     ["mercury"],
     "Ch.1 v.30",
     "Mercury as H3+H6 lord in H7 for Aries: BR warns of disputes in partnerships — "
     "the H6 malefic quality in the marriage house causes arguments, legal disputes with "
     "partners, and contentious business dealings. The native may attract a clever but "
     "critical partner. Business partnerships are intellectually productive but "
     "argumentative. Marriage harmony is challenged by the native's critical nature."),
    ("mercury", "house_placement", 10, [3, 6],
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["mercury"],
     "Ch.1 v.31",
     "Mercury as H3+H6 lord in H10 for Aries: career in fields related to communication, "
     "service, or analytics. BR notes the native achieves career success through "
     "intelligence and detail orientation but faces competition and disputes at work. "
     "H6 influence in the karma house means the native's career involves continuous "
     "competitive effort. Success in law, medicine, writing, or administrative roles."),
    ("mercury", "house_placement", 4, [3, 6],
     "unfavorable", "moderate",
     ["property_vehicles", "mental_health"],
     ["mercury"],
     "Ch.1 v.32",
     "Mercury as H3+H6 lord in H4 for Aries: BR notes domestic disputes, family "
     "enemies, and property litigation. The H6 malefic quality in the happiness house "
     "disrupts domestic peace. Mother may have health issues. Property matters involve "
     "legal complications. The native's analytical mind finds reasons for domestic "
     "dissatisfaction. Unfavorable for family harmony."),
    # ── Jupiter (H9+H12 lord — trikona-dusthana) ─────────────────────────────
    ("jupiter", "house_placement", 1, [9, 12],
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     ["jupiter", "trikona_lord_in_lagna"],
     "Ch.1 v.33",
     "Jupiter as H9 lord (trikona) in H1 for Aries: BR states fortune and divine "
     "blessings manifest directly in the personality. The native is philosophical, "
     "fortunate, and respected. H12 co-ownership adds a spiritual dimension — the "
     "native is oriented toward higher knowledge and eventually liberation. "
     "Despite the H12 dusthana element, the H9 trikona dominates when Jupiter is "
     "in the lagna. Excellent for dharmic and educational roles."),
    ("jupiter", "house_placement", 5, [9, 12],
     "favorable", "strong",
     ["spirituality", "intelligence_education", "progeny"],
     ["jupiter", "trikona_lord_in_trikona"],
     "Ch.1 v.34",
     "Jupiter as H9 lord in H5 (trikona) for Aries: double trikona — BR states "
     "exceptional wisdom, many children (especially sons), great scholarship, and "
     "strong purva punya. The native becomes learned in philosophy, jurisprudence, "
     "or theology. Guru connections are transformative. Fortune and intelligence "
     "combine powerfully. One of the finest Jupiter placements for Aries."),
    ("jupiter", "house_placement", 9, [9, 12],
     "favorable", "strong",
     ["spirituality", "wealth", "fame_reputation"],
     ["jupiter", "trikona_lord_in_own_house"],
     "Ch.1 v.35",
     "Jupiter in H9 (own functional house, Sagittarius) for Aries: BR states "
     "outstanding fortune and dharmic merit. Father is respected and possibly a "
     "spiritual figure. The native receives guru's blessings abundantly. "
     "H12 co-ownership adds moksha orientation — the native is both fortunate in "
     "worldly matters and spiritually inclined. Pilgrimages are frequent and auspicious."),
    ("jupiter", "house_placement", 10, [9, 12],
     "favorable", "strong",
     ["career_status", "fame_reputation", "spirituality"],
     ["jupiter", "trikona_lord_in_kendra", "dharmakarmayoga"],
     "Ch.1 v.36",
     "Jupiter as H9 lord in H10 for Aries: BR's prime dharma-karma yoga. Career "
     "achievements carry dharmic weight — the native works in spirituality, education, "
     "law, or advisory roles. Public recognition for wisdom and moral conduct. "
     "The father's legacy supports the native's career. This placement makes the "
     "native a respected public figure whose work has lasting ethical impact."),
    ("jupiter", "house_placement", 4, [9, 12],
     "favorable", "moderate",
     ["property_vehicles", "spirituality"],
     ["jupiter"],
     "Ch.1 v.37",
     "Jupiter as H9 lord in H4 for Aries: domestic happiness through fortune and "
     "wisdom. BR states the native's home has a spiritual, philosophical atmosphere. "
     "Mother is wise and educated. Property is acquired in auspicious circumstances. "
     "The H12 co-ownership adds some hidden expenses in property matters, but "
     "overall favorable for domestic contentment and educational pursuits at home."),
    ("jupiter", "house_placement", 12, [9, 12],
     "mixed", "moderate",
     ["spirituality", "foreign_travel"],
     ["jupiter", "12th_lord_own_house"],
     "Ch.1 v.38",
     "Jupiter in H12 (own functional H12) for Aries: BR notes the H12 lord in H12 "
     "gives strong moksha orientation and foreign travel for spiritual purposes. "
     "Expenditure is generous (Jupiter's largesse in H12). H9 trikona co-ownership "
     "means the foreign/spiritual journeys are dharmic and fortunate. "
     "The native may settle abroad or establish a spiritual community. Good for "
     "spiritual retreat, ashram life, and liberation-oriented practices."),
    ("jupiter", "house_placement", 6, [9, 12],
     "mixed", "weak",
     ["spirituality", "enemies_litigation"],
     ["jupiter"],
     "Ch.1 v.39",
     "Jupiter as H9 lord in H6 (dusthana) for Aries: BR warns of fortune diminished "
     "by enemies and health challenges. The native's philosophical nature may attract "
     "adversaries. Jupiter's wisdom is used in disputes or service contexts. "
     "Foreign journeys for health-related reasons. The H9 trikona's power is reduced "
     "by the H6 placement — fortune comes but with struggle and competition."),
    ("jupiter", "house_placement", 7, [9, 12],
     "mixed", "moderate",
     ["marriage", "spirituality"],
     ["jupiter"],
     "Ch.1 v.40",
     "Jupiter as H9 lord in H7 for Aries: spouse is learned, philosophical, or from "
     "a respected family. BR states partnerships are dharmic and the spouse is wise "
     "and fortunate. However, H12 co-ownership with H7 placement adds foreign "
     "connection to marriage or expenditure through partnerships. Marriage may occur "
     "after foreign travel or with a partner from a different culture."),
    # ── Venus (H2+H7 lord — double maraka) ───────────────────────────────────
    ("venus", "house_placement", 1, [2, 7],
     "mixed", "moderate",
     ["physical_health", "longevity"],
     ["venus", "maraka_in_lagna"],
     "Ch.1 v.41",
     "Venus as double maraka (H2+H7) in H1 for Aries: BR notes the native is "
     "beautiful, charming, and fond of comfort, but the maraka energy in the lagna "
     "creates health vulnerabilities and self-indulgence. Wealth matters (H2) and "
     "relationship energy (H7) manifest in the personality directly — the native is "
     "attractive and financially oriented. Maraka concern for longevity in old age."),
    ("venus", "house_placement", 2, [2, 7],
     "mixed", "moderate",
     ["wealth", "longevity"],
     ["venus", "maraka_own_house"],
     "Ch.1 v.42",
     "Venus in H2 (own functional maraka house) for Aries: wealth is acquired but "
     "with maraka intensification. BR states financial gains are real and family "
     "life is pleasant, but Venus's double-maraka nature means wealth accumulation "
     "and maraka potential are simultaneously activated. The native accumulates "
     "resources but the 2nd house maraka element is concentrated here."),
    ("venus", "house_placement", 4, [2, 7],
     "mixed", "moderate",
     ["property_vehicles", "longevity"],
     ["venus"],
     "Ch.1 v.43",
     "Venus as maraka lord in H4 for Aries: domestic comforts and vehicles are "
     "acquired but with maraka undercurrent. BR states the home is beautiful and "
     "the native enjoys luxury, but the maraka lord in a kendra house creates "
     "concerns about domestic stability. Mother's health requires attention. "
     "Property is acquired but with expenditure concerns related to Venus's H12 "
     "adjacent significations."),
    ("venus", "house_placement", 5, [2, 7],
     "mixed", "moderate",
     ["progeny", "wealth"],
     ["venus"],
     "Ch.1 v.44",
     "Venus as H7 lord in H5 for Aries: BR notes children are beautiful and "
     "artistically gifted. Romantic connections outside marriage are possible (H7 "
     "lord in H5 — love affairs). Speculative investments show gains but the maraka "
     "element of H7 in the trikona means wealth from speculation should be approached "
     "carefully. Creative and artistic talents are strong."),
    ("venus", "house_placement", 7, [2, 7],
     "mixed", "moderate",
     ["marriage", "longevity"],
     ["venus", "maraka_own_house"],
     "Ch.1 v.45",
     "Venus in H7 (own functional H7 maraka) for Aries: marriage occurs with a "
     "beautiful, artistic partner. BR states domestic happiness through relationships "
     "is real but the intensified maraka (Venus as H2+H7 lord in H7) means the "
     "partnership house maraka potential is fully concentrated. Life events in "
     "partnership domain carry elevated maraka risk in old age."),
    ("venus", "house_placement", 9, [2, 7],
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["venus"],
     "Ch.1 v.46",
     "Venus as double maraka in H9 (fortune) for Aries: BR notes wealth and fortune "
     "are available through partnerships and family connections, but the maraka lord "
     "in the fortune house creates a mixed picture. Artistic and creative talents "
     "find fortunate expression. Foreign romance or partner from a different faith/culture. "
     "Fortune comes through relationship and wealth matters but with some maraka overtones."),
    ("venus", "house_placement", 10, [2, 7],
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["venus"],
     "Ch.1 v.47",
     "Venus as maraka lord in H10 for Aries: career in artistic, financial, or "
     "relationship-oriented fields. BR states the native achieves professional "
     "recognition through creativity, beauty, or financial expertise. However, "
     "the maraka H2+H7 lord in the karma kendra means career success has a "
     "maraka dimension — health challenges during peak career years are possible."),
    ("venus", "house_placement", 11, [2, 7],
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["venus"],
     "Ch.1 v.48",
     "Venus as maraka lord in H11 for Aries: gains through partnerships and "
     "financial dealings. BR states financial gains are substantial (H11 gains "
     "with Venus's H2 wealth association). Elder siblings may be in artistic or "
     "financial fields. The maraka element in the upachaya house is relatively "
     "less dangerous — wealth gains with manageable maraka concern."),
    # ── Saturn (H10+H11 lord) ─────────────────────────────────────────────────
    ("saturn", "house_placement", 1, [10, 11],
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["saturn"],
     "Ch.1 v.49",
     "Saturn as H10+H11 lord in H1 for Aries: BR states career focus and disciplined "
     "personality. The native is hardworking, serious, and career-oriented from early life. "
     "H10+H11 in lagna gives ambition and gain-orientation in the personality. "
     "However, Saturn in Aries (enemy sign) creates friction — the disciplined, "
     "delayed energy of Saturn conflicts with Aries's speed and impulsiveness."),
    ("saturn", "house_placement", 3, [10, 11],
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["saturn"],
     "Ch.1 v.50",
     "Saturn as H10+H11 lord in H3 for Aries: career gains through persistent effort "
     "and communication. BR states elder siblings are in career or business fields. "
     "The native achieves professional success through consistent, disciplined effort. "
     "Gains (H11) through media, communication, or trade. Saturn in upachaya H3 "
     "improves over time — career achievements compound with age."),
    ("saturn", "house_placement", 7, [10, 11],
     "mixed", "moderate",
     ["career_status", "marriage"],
     ["saturn"],
     "Ch.1 v.51",
     "Saturn as H10+H11 lord in H7 (maraka) for Aries: career through partnerships "
     "and negotiation. BR states the native achieves career success through business "
     "partnerships and contractual dealings. Spouse may be in an established career. "
     "However, Saturn in H7 (maraka) creates delays in marriage and some partnership "
     "difficulties. Career gains are real but marriage comes late or with age difference."),
    ("saturn", "house_placement", 10, [10, 11],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["saturn", "10th_lord_own_house"],
     "Ch.1 v.52",
     "Saturn in H10 (Capricorn, own sign — H10 lord in H10) for Aries: BR states "
     "outstanding career achievement through sustained effort and discipline. "
     "The native reaches high positions in established institutions, government, "
     "or business. Saturn's own sign strength in H10 makes this a peak career placement. "
     "Gains (H11) also come through career achievements. Late but lasting success."),
    ("saturn", "house_placement", 11, [10, 11],
     "favorable", "strong",
     ["wealth", "career_status"],
     ["saturn", "11th_lord_own_house"],
     "Ch.1 v.53",
     "Saturn in H11 (Aquarius, own sign — H11 lord in H11) for Aries: BR states "
     "excellent gains and fulfillment of long-term aspirations. Saturn's own sign "
     "in the gains house gives sustained, structured financial growth. Elder siblings "
     "are prosperous. Career (H10) and gains (H11) both in own signs — rare excellence "
     "in worldly achievement for Aries."),
    ("saturn", "house_placement", 9, [10, 11],
     "favorable", "moderate",
     ["career_status", "spirituality"],
     ["saturn", "dharmakarmayoga"],
     "Ch.1 v.54",
     "Saturn as H10 lord in H9 (fortune/dharma) for Aries: dharma-karma yoga. "
     "BR states career is grounded in ethical, dharmic principles. The native may "
     "work in law, religion, established institutions, or governance. Fortune "
     "supports the career over time. Father may be in a prestigious or governmental "
     "role. Gains through disciplined dharmic action."),
    # ── Yoga rules for Aries ──────────────────────────────────────────────────
    ("mars", "yoga", "lagna_lord_exalted", [1, 8],
     "favorable", "strong",
     ["physical_health", "career_status", "fame_reputation"],
     ["mars", "yoga", "exalted"],
     "Ch.1 v.55",
     "Mars exalted (in Capricorn, H10 for Aries): BR states the lagna lord exalted "
     "in the karma kendra is among the finest Aries configurations. Outstanding career "
     "through disciplined action, government or military success, physical peak. "
     "The exalted Mars in H10 delivers the lagna lord's strength directly to the "
     "career house — recognition, authority, and lasting professional legacy."),
    ("saturn", "yoga", "yogakaraka_absent_compensation", [10, 11],
     "neutral", "moderate",
     ["career_status", "wealth"],
     ["saturn", "yoga"],
     "Ch.1 v.56",
     "For Aries lagna (no yogakaraka): BR notes that the nearest functional equivalent "
     "to a yogakaraka is Saturn (H10+H11) combined with Sun (H5). When Saturn and Sun "
     "form a relationship (conjunction, mutual aspect, exchange), Aries natives "
     "achieve career and dharmic results approaching yogakaraka quality. "
     "This combination is the primary raja yoga equivalent for Aries."),
    ("sun", "yoga", "sun_mars_combination", [5],
     "favorable", "strong",
     ["career_status", "fame_reputation", "intelligence_education"],
     ["sun", "mars", "yoga", "dharma_karma"],
     "Ch.1 v.57",
     "Sun (H5) + Mars (lagna lord) conjunction or mutual aspect for Aries: BR states "
     "the combination of trikona lord and lagna lord produces outstanding intelligence "
     "and courageous leadership. Children of the native achieve great positions. "
     "The native is a natural authority figure with both intelligence (Sun) and "
     "courage (Mars). Government success and creative leadership are indicated."),
    ("jupiter", "yoga", "jupiter_sun_combination", [9, 12],
     "favorable", "strong",
     ["spirituality", "wealth", "fame_reputation"],
     ["jupiter", "sun", "yoga"],
     "Ch.1 v.58",
     "Jupiter (H9) + Sun (H5) for Aries: double trikona lords in relationship. "
     "BR states the combination of fortune (H9) and intelligence (H5) lords "
     "produces a highly fortunate, wise, and respected native. Both trikona lords "
     "active simultaneously create sustained dharmic merit. Spiritual, academic, "
     "or governmental achievements of lasting significance."),
    ("mars", "yoga", "mars_jupiter_trikona", [1, 8],
     "favorable", "strong",
     ["wealth", "spirituality", "career_status"],
     ["mars", "jupiter", "yoga"],
     "Ch.1 v.59",
     "Mars (lagna lord) + Jupiter (H9 trikona lord) in mutual relationship for Aries: "
     "BR states the combination of personal strength and dharmic fortune creates a "
     "powerful, virtuous leader. The native's courageous action is blessed by fortune "
     "and divine grace. Success in ventures requiring both initiative (Mars) and "
     "wisdom (Jupiter). Natural dharmic warrior archetype."),
    ("venus", "yoga", "venus_saturn_unfavorable", [2, 7],
     "unfavorable", "moderate",
     ["longevity", "character_temperament"],
     ["venus", "saturn", "yoga", "maraka"],
     "Ch.1 v.60",
     "Venus (double maraka H2+H7) + Saturn (H10+H11) in H1 or mutual aspect for "
     "Aries: BR warns this combination creates financial discipline issues, health "
     "concerns from overindulgence, and delayed relationship success. The maraka "
     "(Venus) combined with Saturn's slow, heavy energy in the lagna area creates "
     "a depleting pattern. Career ambition conflicts with relationship needs."),
    ("mercury", "yoga", "mercury_functional_malefic_yoga", [3, 6],
     "unfavorable", "moderate",
     ["enemies_litigation", "physical_health"],
     ["mercury", "yoga", "functional_malefic"],
     "Ch.1 v.61",
     "Mercury (H3+H6 double dusthana) in kendra position (H1/H4/H7/H10) for Aries: "
     "BR warns of compound enemy activity and health issues when the functional malefic "
     "Mercury occupies a kendra. Disputes, litigation, and sibling conflicts manifest "
     "prominently. The native's analytical mind creates adversaries in the kendra areas "
     "of life — home, partnerships, or career all affected by Mercury's H6 nature."),
    ("mars", "yoga", "mars_saturn_exchange", [1, 8],
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mars", "saturn", "yoga", "exchange"],
     "Ch.1 v.62",
     "Mars (lagna lord) and Saturn (H10+H11) in sign exchange (parivartana) for Aries: "
     "BR states this exchange creates a powerful career-self alignment. Mars goes to "
     "Saturn's sign (Capricorn/Aquarius) and Saturn goes to Mars's sign (Aries/Scorpio). "
     "Career achievement and personal vitality are mutually reinforced. A rare, "
     "excellent exchange for Aries that compensates for the absence of a yogakaraka."),
    ("sun", "yoga", "sun_in_lagna_mars_in_10", [5],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "yoga"],
     "Ch.1 v.63",
     "Sun (H5) in H1 AND Mars (lagna lord) in H10 for Aries: BR states this dual "
     "configuration gives both trikona activation in lagna and lagna lord in karma kendra. "
     "Career recognition is exceptional and intelligence-based leadership is outstanding. "
     "Government positions, creative authority, and public fame combine in one native. "
     "One of the finest dual-planet configurations for Aries."),
    ("jupiter", "yoga", "jupiter_kendra_trikon_aries", [9, 12],
     "favorable", "strong",
     ["career_status", "wealth", "spirituality"],
     ["jupiter", "sun", "mars", "yoga", "raja_yoga"],
     "Ch.1 v.64",
     "When lagna lord Mars, trikona lord Sun (H5), and fortune lord Jupiter (H9) "
     "all connect (any two in conjunction or mutual aspect), BR states Aries native "
     "achieves outstanding life results — wealth, name, fame, and spiritual merit "
     "all in one lifetime. This triple planetary connection is BR's highest "
     "potential configuration for Aries."),
    ("moon", "yoga", "moon_saturn_difficult", [4],
     "unfavorable", "moderate",
     ["mental_health", "longevity"],
     ["moon", "saturn", "yoga"],
     "Ch.1 v.65",
     "Moon (H4 kendradhipati) + Saturn (H10+H11) conjunction or opposition for Aries: "
     "BR warns of mental health challenges, delayed emotional fulfillment, and domestic "
     "austerity. The kendradhipati Moon's emotional instability combines with Saturn's "
     "delays and restrictions — the native's mind is troubled and domestic life is "
     "cold or austere. This combination requires specific remedial attention for "
     "Aries natives."),
]

# ── Chapter 2: Taurus (Vrishabha) lagna ──────────────────────────────────────
# Functional context: Saturn=yogakaraka (H9+H10); Venus=lagna lord (H1+H6);
# Mercury=trikona lord (H2+H5); Jupiter=functional malefic (H8+H11);
# Moon=functional malefic (H3); Mars=maraka-dusthana (H7+H12);
# Sun=kendra lord (H4).

_TAURUS_DATA = [
    # ── Sun (H4 lord — kendra lord) ──────────────────────────────────────────
    ("sun", "house_placement", 1, [4],
     "mixed", "moderate",
     ["physical_health", "career_status"],
     ["sun", "kendra_lord_in_lagna"],
     "Ch.2 v.1",
     "Sun as H4 (kendra) lord in H1 for Taurus: BR states a strong, dignified personality "
     "with connection to property and domestic authority. However, Sun's natural kendra "
     "energy in the lagna creates some egoistic quality. The native has good physical "
     "presence and authority, but the H4 kendra lord nature means results come with some "
     "kendradhipati-like effort. Sun in lagna for Taurus gives leadership but not the "
     "pure dharmic quality of a trikona lord."),
    ("sun", "house_placement", 4, [4],
     "favorable", "moderate",
     ["property_vehicles", "career_status"],
     ["sun", "kendra_lord_own_house"],
     "Ch.2 v.2",
     "Sun in H4 (own functional house, Leo) for Taurus: BR states domestic authority "
     "and property acquisition are strong. The native may have a large, impressive home "
     "and authoritative mother. Government connections to property. Sun in own kendra "
     "gives concrete domestic achievements. Career (H10 for Taurus is Saturn's — "
     "Sun and Saturn are enemies) — there may be career tensions with authority figures."),
    ("sun", "house_placement", 9, [4],
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["sun"],
     "Ch.2 v.3",
     "Sun as H4 lord in H9 for Taurus: domestic happiness connected to fortune and "
     "father. BR notes property and vehicles acquired through fortunate circumstances. "
     "Father or family lineage is in a prestigious position. The native connects "
     "domestic life with dharmic pursuits — the home is a place of learning and "
     "spiritual practice. Overall favorable for property and fortune."),
    ("sun", "house_placement", 10, [4],
     "mixed", "moderate",
     ["career_status", "property_vehicles"],
     ["sun"],
     "Ch.2 v.4",
     "Sun as H4 lord in H10 for Taurus: property and career intersect — real estate "
     "business, government property, or career through domestic/agricultural work. "
     "BR notes the native achieves in career through connection to property, heritage, "
     "or maternal matters. Sun and Saturn (yogakaraka, H10 lord) are enemies — their "
     "relationship creates a career tension that requires resolution through discipline."),
    ("sun", "house_placement", 5, [4],
     "favorable", "moderate",
     ["intelligence_education", "property_vehicles"],
     ["sun"],
     "Ch.2 v.5",
     "Sun as H4 lord in H5 (trikona) for Taurus: domestic happiness and property "
     "expressed through intelligence and children. BR states the native achieves "
     "academic recognition that supports property acquisition. Children are connected "
     "to the family home and its traditions. Creative and intellectual work supports "
     "domestic stability. Generally favorable — kendra lord in trikona is productive."),
    # ── Moon (H3 lord — functional malefic) ──────────────────────────────────
    ("moon", "house_placement", 1, [3],
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "functional_malefic_in_lagna"],
     "Ch.2 v.6",
     "Moon as H3 (functional malefic) lord in H1 for Taurus: BR warns of emotional "
     "instability and mental fluctuations affecting health and personality. H3 lord "
     "in lagna makes the native restless, communicative but unreliable. Short journeys "
     "and sibling matters dominate the life. Moon's functional malefic status for "
     "Taurus means this placement is unfavorable despite Moon's natural benefic nature."),
    ("moon", "house_placement", 3, [3],
     "neutral", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "functional_malefic_own_house"],
     "Ch.2 v.7",
     "Moon in H3 (own functional house) for Taurus: BR states siblings and short "
     "travels are active themes. Communication is emotionally driven. The native "
     "expresses courage and initiative through emotional channels. As H3 functional "
     "malefic in its own house, the results are mixed — sibling relationships are "
     "close but emotionally complicated."),
    ("moon", "house_placement", 5, [3],
     "mixed", "moderate",
     ["progeny", "intelligence_education"],
     ["moon"],
     "Ch.2 v.8",
     "Moon as H3 lord in H5 for Taurus: BR notes intelligence and creativity activated "
     "through communication and effort. Children may have artistic or communicative "
     "talents. The functional malefic quality of Moon in trikona creates an intelligent "
     "but emotionally restless mind. Purva punya manifests through communication skills "
     "and short-distance efforts."),
    ("moon", "house_placement", 11, [3],
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["moon"],
     "Ch.2 v.9",
     "Moon as H3 lord in H11 (upachaya) for Taurus: gains through communications, "
     "trading, and sibling support. BR states financial gains from media, writing, "
     "or short-distance business. The upachaya house mitigates the H3 malefic quality "
     "somewhat — gains are real but come through continuous effort and communication."),
    # ── Mars (H7+H12 lord — maraka-dusthana) ─────────────────────────────────
    ("mars", "house_placement", 1, [7, 12],
     "unfavorable", "moderate",
     ["physical_health", "longevity"],
     ["mars", "maraka_in_lagna"],
     "Ch.2 v.10",
     "Mars as maraka (H7) + dusthana (H12) lord in H1 for Taurus: BR warns of health "
     "challenges and an aggressive, conflict-prone personality. The maraka lord in the "
     "lagna creates self-directed maraka energy — health events and vitality losses. "
     "The H12 co-ownership adds expenditure and foreign themes. Mars in lagna for "
     "Taurus is among the more challenging placements despite Mars's natural courage."),
    ("mars", "house_placement", 3, [7, 12],
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["mars"],
     "Ch.2 v.11",
     "Mars as maraka-dusthana lord in H3 for Taurus: courage and initiative "
     "come with conflict. BR notes sibling disputes and competitive ventures dominate "
     "when the maraka lord is in the house of courage. Short travels may involve "
     "conflict. Career success in competitive fields but the H7+H12 maraka-dusthana "
     "combination means these efforts carry hidden costs."),
    ("mars", "house_placement", 6, [7, 12],
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["mars"],
     "Ch.2 v.12",
     "Mars as maraka lord in H6 for Taurus: BR notes victory over enemies through "
     "bold action, but health issues from conflict and injury. The maraka lord in "
     "the house of enemies creates competitive intensity. Success in sports, law, "
     "or competitive fields. H12 co-ownership with H6 placement adds expenditure "
     "on health and possible hospitalization themes."),
    ("mars", "house_placement", 7, [7, 12],
     "unfavorable", "strong",
     ["marriage", "longevity"],
     ["mars", "maraka_own_house"],
     "Ch.2 v.13",
     "Mars in H7 (own functional maraka house) for Taurus: BR's primary maraka "
     "warning for Taurus. Mars in its own maraka house concentrates death-inflicting "
     "potential. Marriage occurs with a courageous or aggressive partner. Partnership "
     "disputes are likely. For elderly Taurus natives, Mars dasha or Mars-related "
     "timing during this placement warrants maximum longevity assessment."),
    ("mars", "house_placement", 12, [7, 12],
     "mixed", "moderate",
     ["foreign_travel", "longevity"],
     ["mars", "dusthana_own_house"],
     "Ch.2 v.14",
     "Mars in H12 (own functional dusthana house) for Taurus: foreign residence "
     "with conflict, expenditure on competitive ventures, and maraka in hidden house. "
     "BR states the native may settle abroad but face conflicts in foreign lands. "
     "H7 maraka co-ownership means the foreign environments carry maraka potential. "
     "Spiritual retreats or ashram life in foreign places is possible but not without "
     "physical challenges."),
    ("mars", "house_placement", 10, [7, 12],
     "mixed", "moderate",
     ["career_status", "longevity"],
     ["mars"],
     "Ch.2 v.15",
     "Mars as maraka lord in H10 (Saturn's yogakaraka house) for Taurus: BR notes "
     "career activation through bold, competitive action. The native achieves career "
     "recognition in sports, military, surgery, or competitive business. However, "
     "the maraka lord in the karma kendra means career peak years carry health "
     "concerns and possible burnout. Saturn (yogakaraka, H10 lord) + Mars in H10 "
     "creates a complex karma-maraka dynamic."),
    # ── Mercury (H2+H5 lord — trikona lord) ──────────────────────────────────
    ("mercury", "house_placement", 1, [2, 5],
     "favorable", "strong",
     ["wealth", "intelligence_education", "career_status"],
     ["mercury", "trikona_lord_in_lagna"],
     "Ch.2 v.16",
     "Mercury as H5 trikona lord (also H2 wealth lord) in H1 for Taurus: BR states "
     "outstanding intelligence, communication skills, and financial acumen in the "
     "personality. The native is sharp-minded, articulate, and financially savvy. "
     "H2 wealth lord in lagna gives focus on accumulation. H5 trikona in lagna gives "
     "intellectual brilliance. The combination makes Mercury in lagna excellent for Taurus."),
    ("mercury", "house_placement", 2, [2, 5],
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["mercury", "wealth_lord_own_house"],
     "Ch.2 v.17",
     "Mercury in H2 (own functional house, Gemini) for Taurus: wealth accumulation "
     "through intelligence and communication. BR states the native builds substantial "
     "financial reserves through analytical and communicative skills. H5 trikona "
     "co-ownership means the wealth is dharmic and well-earned. Family life is "
     "intellectually active. Speech is eloquent and financially effective."),
    ("mercury", "house_placement", 5, [2, 5],
     "favorable", "strong",
     ["intelligence_education", "progeny", "wealth"],
     ["mercury", "trikona_lord_own_house"],
     "Ch.2 v.18",
     "Mercury in H5 (own functional trikona, Virgo) for Taurus: BR's finest Mercury "
     "placement for Taurus. Trikona lord in trikona gives outstanding intelligence, "
     "children who are academically gifted, wealth from speculative or analytical "
     "work, and strong purva punya. The native excels in mathematics, writing, "
     "medicine, or analytical fields. Highly auspicious for Taurus."),
    ("mercury", "house_placement", 9, [2, 5],
     "favorable", "strong",
     ["wealth", "spirituality", "intelligence_education"],
     ["mercury", "trikona_lord_in_trikona", "double_trikona"],
     "Ch.2 v.19",
     "Mercury as H5 trikona lord in H9 for Taurus: double trikona — BR states "
     "exceptional intellectual and financial fortune. The native achieves academic "
     "or scholarly eminence and fortune comes through knowledge-based work. "
     "Philosophical and analytical prowess combines with dharmic merit. "
     "Writing, teaching, or intellectual pursuits bring both wealth and fame."),
    ("mercury", "house_placement", 10, [2, 5],
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     ["mercury", "trikona_lord_in_kendra", "dharmakarmayoga"],
     "Ch.2 v.20",
     "Mercury as H5 (trikona) lord in H10 (kendra) for Taurus: dharma-karma yoga. "
     "BR states career peak through analytical intelligence, financial expertise, or "
     "communication. The native achieves public recognition for intellectual work. "
     "Wealth (H2) and career (H10) both activated through Mercury — an excellent "
     "combination for business, finance, or knowledge-based careers."),
    ("mercury", "house_placement", 4, [2, 5],
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["mercury"],
     "Ch.2 v.21",
     "Mercury as trikona lord in H4 for Taurus: domestic intelligence and property "
     "through analytical work. BR states property acquired through financial acumen "
     "and communication-related work. The home has an intellectual atmosphere. "
     "Mother is educated. Real estate or financial dealings in property sector succeed."),
    ("mercury", "house_placement", 7, [2, 5],
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["mercury"],
     "Ch.2 v.22",
     "Mercury as trikona lord in H7 for Taurus: spouse is intelligent and commercially "
     "savvy. BR notes business partnerships are intellectually grounded and financially "
     "productive. However, H7 carries maraka potential for any planet — Mercury's "
     "trikona quality softens this but doesn't eliminate it. Business partnerships "
     "succeed and marriage brings intellectual companionship."),
    ("mercury", "house_placement", 11, [2, 5],
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury"],
     "Ch.2 v.23",
     "Mercury as H2+H5 lord in H11 (gains) for Taurus: BR states sustained financial "
     "gains through intellectual work and trading. Elder siblings may be in business "
     "or analytical fields. The combination of H2 wealth, H5 intelligence, and H11 "
     "gains makes this a financially productive placement. Long-term aspirations in "
     "financial or educational fields are fulfilled."),
    # ── Jupiter (H8+H11 lord — functional malefic) ───────────────────────────
    ("jupiter", "house_placement", 1, [8, 11],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["jupiter", "functional_malefic_in_lagna"],
     "Ch.2 v.24",
     "Jupiter as H8+H11 (functional malefic) lord in H1 for Taurus: BR warns of "
     "health complications despite Jupiter's natural benefic appearance. H8 lord "
     "in the lagna creates hidden health issues and unexpected obstacles in the "
     "personality. The native may appear wise and philosophical (Jupiter) but "
     "faces recurring obstacles and longevity concerns. H11 gains are present "
     "but the H8 cost accompanies them."),
    ("jupiter", "house_placement", 4, [8, 11],
     "unfavorable", "moderate",
     ["property_vehicles", "longevity"],
     ["jupiter"],
     "Ch.2 v.25",
     "Jupiter as H8+H11 lord in H4 for Taurus: domestic happiness is pursued but "
     "BR warns of property complications (H8 hidden issues) alongside gains (H11). "
     "Mother may have health concerns. Property transactions involve hidden complications. "
     "The native acquires property but with unexpected problems in the acquisition "
     "process. H8 in kendra H4 is generally unfavorable for Taurus."),
    ("jupiter", "house_placement", 5, [8, 11],
     "mixed", "moderate",
     ["progeny", "longevity"],
     ["jupiter"],
     "Ch.2 v.26",
     "Jupiter as H8 lord in H5 (trikona) for Taurus: BR notes children's matters "
     "involve unexpected challenges — longevity concerns for children, hidden genetic "
     "issues, or sudden changes in children's circumstances. Intelligence is present "
     "but the H8 element in the trikona creates an undercurrent of instability "
     "in 5th house significations."),
    ("jupiter", "house_placement", 8, [8, 11],
     "mixed", "moderate",
     ["longevity", "spirituality"],
     ["jupiter", "8th_lord_own_house"],
     "Ch.2 v.27",
     "Jupiter in H8 (own functional house) for Taurus: BR notes a spiritual, "
     "philosophically inclined native who faces longevity tests. H8 lord in H8 "
     "concentrates transformation themes — deep occult knowledge, inheritance "
     "matters, and sudden life reversals. Jupiter's wisdom is channeled toward "
     "esoteric subjects. Longevity may be extended by Jupiter's natural association "
     "with long life (ayushkaraka), but tests are real."),
    ("jupiter", "house_placement", 11, [8, 11],
     "mixed", "moderate",
     ["wealth", "longevity"],
     ["jupiter", "11th_lord_own_house"],
     "Ch.2 v.28",
     "Jupiter in H11 (own sign context for Sagittarius? No — H11 from Taurus is "
     "Pisces = Jupiter's own sign). Jupiter in H11 for Taurus: gains are significant "
     "but the H8 co-ownership adds a 'gains with cost' pattern — income comes with "
     "health expenditure or hidden losses. BR states elder siblings are educated "
     "or philosophical. Financial aspirations are mostly fulfilled but with Jupiter's "
     "H8 complications lurking."),
    ("jupiter", "house_placement", 9, [8, 11],
     "mixed", "moderate",
     ["spirituality", "longevity"],
     ["jupiter"],
     "Ch.2 v.29",
     "Jupiter as H8 lord in H9 (fortune) for Taurus: BR notes fortune and "
     "philosophical depth come with longevity concerns embedded in the fortune house. "
     "Spiritual pursuits are deep and transformative (H8 in H9). Father may have "
     "health issues or sudden reversals. The combination of fortune and the 8th lord "
     "creates a 'fortune through crisis' pattern — the native's biggest fortunate "
     "events come after significant transformations."),
    # ── Venus (H1+H6 lord — lagna lord) ──────────────────────────────────────
    ("venus", "house_placement", 1, [1, 6],
     "favorable", "strong",
     ["physical_health", "career_status", "fame_reputation"],
     ["venus", "lagna_lord_in_lagna"],
     "Ch.2 v.30",
     "Venus as lagna lord in H1 (own sign Taurus) for Taurus: BR states outstanding "
     "physical beauty, artistic talent, and personal magnetism. The lagna lord in its "
     "own sign in the lagna — the finest personal placement. The native is naturally "
     "charming, artistically gifted, and financially astute. H6 co-ownership adds "
     "a service/enemy element but lagna lord dominance prevails. Long life and "
     "pleasant personality are indicated."),
    ("venus", "house_placement", 4, [1, 6],
     "favorable", "moderate",
     ["property_vehicles", "physical_health"],
     ["venus"],
     "Ch.2 v.31",
     "Venus as lagna lord in H4 for Taurus: domestic luxury and beautiful home. "
     "BR states property acquisitions are prominent and the native's home environment "
     "is aesthetically refined. Mother is beautiful or artistically inclined. "
     "Vehicles are acquired easily. H6 co-ownership adds some service or health "
     "theme to domestic matters but lagna lord in kendra is favorable overall."),
    ("venus", "house_placement", 5, [1, 6],
     "favorable", "strong",
     ["progeny", "intelligence_education", "physical_health"],
     ["venus", "lagna_lord_in_trikona"],
     "Ch.2 v.32",
     "Venus as lagna lord in H5 (trikona) for Taurus: BR states excellent creative "
     "expression, beautiful children, artistic achievements, and personal vitality. "
     "Lagna lord in trikona is a naturally auspicious configuration. The native achieves "
     "through creative and artistic talents. Romance and creative work are intertwined. "
     "H6 co-ownership adds health service or competitive element to 5th house matters."),
    ("venus", "house_placement", 9, [1, 6],
     "favorable", "strong",
     ["wealth", "spirituality", "physical_health"],
     ["venus", "lagna_lord_in_trikona"],
     "Ch.2 v.33",
     "Venus as lagna lord in H9 for Taurus: BR states the native is beautiful, "
     "fortunate, and dharmic. Personal appearance and personality are blessed by "
     "fortune. Father or guru has aesthetic and artistic inclinations. The native "
     "achieves through dharmic and artistic work — a graceful, fortunate life. "
     "Lagna lord in trikona gives strong personal dharmic fortune."),
    ("venus", "house_placement", 2, [1, 6],
     "mixed", "moderate",
     ["wealth", "physical_health"],
     ["venus"],
     "Ch.2 v.34",
     "Venus as lagna lord in H2 (Mercury's functional house) for Taurus: wealth "
     "accumulation with artistic and financial focus. BR notes Venus in H2 makes "
     "wealth a primary life theme. The native is skilled in accumulating resources. "
     "H6 co-ownership means some of the wealth comes through service, health, or "
     "competitive work. Family life is pleasant but Mercury (H2 lord) and Venus "
     "have a complex functional relationship for Taurus."),
    ("venus", "house_placement", 6, [1, 6],
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     ["venus", "6th_lord_own_house"],
     "Ch.2 v.35",
     "Venus in H6 (own functional H6) for Taurus: lagna lord in dusthana — BR warns "
     "of health complications despite lagna lord's natural strength. The H6 placement "
     "of the lagna lord means health challenges are intrinsic to the life path. "
     "Victory over enemies is possible (Venus's charm overcomes adversaries), but "
     "the native must manage health actively. Service roles or health professions "
     "may suit this placement."),
    ("venus", "house_placement", 10, [1, 6],
     "mixed", "moderate",
     ["career_status", "physical_health"],
     ["venus"],
     "Ch.2 v.36",
     "Venus as lagna lord in H10 for Taurus: career in artistic, financial, or "
     "beauty-related fields. BR states career peak through Venus's natural significations. "
     "However, Venus and Saturn (yogakaraka owning H9+H10) have a complex relationship "
     "— Venus in Saturn's H10 requires disciplined artistic expression rather than "
     "pure indulgence. Health must be maintained actively for career success."),
    # ── Saturn (H9+H10 lord — yogakaraka) ────────────────────────────────────
    ("saturn", "house_placement", 1, [9, 10],
     "favorable", "strong",
     ["career_status", "fame_reputation", "spirituality"],
     ["saturn", "yogakaraka_in_lagna"],
     "Ch.2 v.37",
     "Saturn as yogakaraka (H9+H10) in H1 for Taurus: BR states outstanding "
     "personality for career achievement and dharmic conduct. The yogakaraka in lagna "
     "combines fortune (H9) and karma (H10) in the native's identity — naturally "
     "disciplined, responsible, and career-oriented. Despite Saturn's delay energy, "
     "the yogakaraka placement in lagna gives sustained, lasting success."),
    ("saturn", "house_placement", 4, [9, 10],
     "favorable", "strong",
     ["property_vehicles", "career_status"],
     ["saturn", "yogakaraka_in_kendra"],
     "Ch.2 v.38",
     "Saturn as yogakaraka in H4 for Taurus: BR states property and domestic stability "
     "through disciplined effort and fortune. The native acquires significant property "
     "and vehicles through sustained career work. Domestic environment reflects "
     "professional success. Mother may be in a career or dharmic role. "
     "Yogakaraka in kendra gives concrete worldly achievement."),
    ("saturn", "house_placement", 5, [9, 10],
     "favorable", "strong",
     ["intelligence_education", "progeny", "spirituality"],
     ["saturn", "yogakaraka_in_trikona"],
     "Ch.2 v.39",
     "Saturn as yogakaraka in H5 (trikona) for Taurus: BR states excellent children "
     "(disciplined, career-oriented), sharp analytical intelligence, and dharmic "
     "merit combined with career focus. The yogakaraka in trikona produces some of "
     "the finest results: past-life merit and present karma align. Children achieve "
     "career success; the native's intelligence serves career and dharma simultaneously."),
    ("saturn", "house_placement", 9, [9, 10],
     "favorable", "strong",
     ["wealth", "spirituality", "fame_reputation"],
     ["saturn", "yogakaraka_own_house", "fortune_dasha"],
     "Ch.2 v.40",
     "Saturn in H9 (own functional trikona, Capricorn) for Taurus: BR states "
     "outstanding fortune through disciplined dharmic action. Father is in a prestigious "
     "or governmental position. The native achieves through patience, ethics, and "
     "perseverance. H10 karma connection makes fortune and career deeply intertwined — "
     "the native earns fortune through career excellence. One of the finest yogakaraka "
     "placements for Taurus."),
    ("saturn", "house_placement", 10, [9, 10],
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["saturn", "yogakaraka_own_house", "career_peak"],
     "Ch.2 v.41",
     "Saturn in H10 (own sign Aquarius — yogakaraka in own career house) for Taurus: "
     "BR's peak career configuration for Taurus. The yogakaraka in its own house in "
     "the karma kendra gives the highest career achievement. Government, corporate, "
     "or institutional leadership. Sustained professional success, public recognition, "
     "and career legacy. One of LP's finest configurations for worldly achievement."),
    ("saturn", "house_placement", 7, [9, 10],
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["saturn", "yogakaraka_in_maraka"],
     "Ch.2 v.42",
     "Saturn as yogakaraka in H7 for Taurus: BR notes career through partnerships "
     "and the spouse is in a career or dharmic role. However, Saturn as yogakaraka "
     "in the maraka H7 creates a 'yogakaraka in maraka house' tension — fortune and "
     "career (H9+H10) activate through partnership but the maraka environment adds "
     "longevity concern. Marriage comes late or to an older/disciplined partner. "
     "Partnership results are excellent but with Saturn's delays."),
    ("saturn", "house_placement", 2, [9, 10],
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["saturn"],
     "Ch.2 v.43",
     "Saturn as yogakaraka in H2 (Mercury's house) for Taurus: BR states disciplined "
     "wealth accumulation through career. Fortune (H9) and career (H10) together "
     "build steady financial resources. The native accumulates wealth slowly but "
     "surely. Family wealth is connected to professional standing. Mercury (H2+H5 "
     "lord) and Saturn (yogakaraka) in exchange or alignment is excellent for Taurus."),
    ("saturn", "house_placement", 11, [9, 10],
     "favorable", "strong",
     ["wealth", "career_status"],
     ["saturn"],
     "Ch.2 v.44",
     "Saturn as yogakaraka in H11 for Taurus: gains through sustained career work "
     "and fortune. BR states financial aspirations are fulfilled through disciplined "
     "professional effort. Elder siblings may be in established careers. The yogakaraka "
     "in the gains house gives a 'career produces wealth' pattern — the native's "
     "professional excellence translates directly into financial gain."),
    ("saturn", "house_placement", 3, [9, 10],
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["saturn"],
     "Ch.2 v.45",
     "Saturn as yogakaraka in H3 for Taurus: career through communication, effort, "
     "and perseverance. BR states the native achieves through disciplined effort and "
     "consistent communication. Siblings may be in career fields. Short travels are "
     "career-oriented. The yogakaraka's dharma-karma energy expressed through the "
     "upachaya H3 improves over time."),
    # ── Yoga rules for Taurus ─────────────────────────────────────────────────
    ("saturn", "yoga", "saturn_mercury_combination", [9, 10],
     "favorable", "strong",
     ["career_status", "wealth", "intelligence_education"],
     ["saturn", "mercury", "yoga"],
     "Ch.2 v.46",
     "Saturn (yogakaraka H9+H10) + Mercury (trikona lord H2+H5) in combination "
     "for Taurus: BR states this is the finest planetary pairing for Taurus. "
     "The yogakaraka (fortune + career) combined with the trikona (wealth + intelligence) "
     "lord produces outstanding career success grounded in intellectual excellence. "
     "Financial and professional achievements are substantial and well-earned."),
    ("saturn", "yoga", "saturn_venus_lagna_combo", [9, 10],
     "favorable", "strong",
     ["career_status", "physical_health", "fame_reputation"],
     ["saturn", "venus", "yoga"],
     "Ch.2 v.47",
     "Saturn (yogakaraka) + Venus (lagna lord) in combination for Taurus: BR states "
     "the native achieves career excellence with personal grace and artistic talent. "
     "Lagna lord + yogakaraka is the fundamental self-career alignment. The Taurus "
     "native expresses Venus's beauty and Saturn's discipline together — an aesthetically "
     "refined, career-successful personality. Marriage often to a career-oriented partner."),
    ("mercury", "yoga", "mercury_saturn_exchange", [2, 5],
     "favorable", "strong",
     ["career_status", "wealth"],
     ["mercury", "saturn", "yoga", "exchange"],
     "Ch.2 v.48",
     "Mercury (H2+H5) and Saturn (H9+H10) in sign exchange (parivartana) for Taurus: "
     "BR states this exchange creates one of the most powerful configurations for Taurus — "
     "the trikona lord (Mercury) and yogakaraka (Saturn) exchange signs, mutually "
     "strengthening each other. Wealth, intelligence, fortune, and career all "
     "activated simultaneously. Outstanding life achievement is indicated."),
    ("mars", "yoga", "mars_jupiter_malefic_combo", [7, 12],
     "unfavorable", "strong",
     ["longevity", "foreign_travel"],
     ["mars", "jupiter", "yoga"],
     "Ch.2 v.49",
     "Mars (maraka H7+H12) + Jupiter (H8+H11) in combination for Taurus: BR states "
     "this dual functional-malefic combination creates compound maraka-dusthana energy. "
     "Both Mars and Jupiter are functional malefics for Taurus — their conjunction "
     "or mutual aspect produces periods of health crisis, financial losses, and "
     "foreign complications. LP's warning configuration for Taurus."),
    ("venus", "yoga", "venus_saturn_taurus_raja_yoga", [1, 6],
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     ["venus", "saturn", "yoga", "raja_yoga"],
     "Ch.2 v.50",
     "When Venus (lagna lord) and Saturn (yogakaraka) mutually aspect or conjoin "
     "for Taurus: BR states the finest raja yoga for Taurus activates. Lagna lord "
     "aligned with yogakaraka produces peak career, personal success, and reputation. "
     "This is the foundational raja yoga combination that LP uses to define "
     "Taurus's highest potential — beauty and discipline united."),
    ("saturn", "yoga", "saturn_strong_exalted", [9, 10],
     "favorable", "strong",
     ["career_status", "wealth", "spirituality"],
     ["saturn", "yoga", "exalted", "yogakaraka"],
     "Ch.2 v.51",
     "Saturn exalted (in Libra, H6 for Taurus) for Taurus: BR notes that even "
     "in H6 (dusthana), Saturn exalted as yogakaraka delivers strong results — "
     "the exaltation sign in H6 gives victory over enemies through career excellence. "
     "The yogakaraka's exaltation compensates for the dusthana placement. Career "
     "success through competitive excellence and disciplined service."),
    ("mercury", "yoga", "mercury_in_lagna_saturn_in_9", [2, 5],
     "favorable", "strong",
     ["career_status", "wealth", "intelligence_education"],
     ["mercury", "saturn", "yoga"],
     "Ch.2 v.52",
     "Mercury (H5 trikona) in H1 AND Saturn (H9 fortune) in H9 simultaneously "
     "for Taurus: BR states the trikona lord in lagna + yogakaraka in own house "
     "gives an exceptionally fortunate and intelligent Taurus native. Personal "
     "intelligence is peak (H5 in H1), and fortune is at maximum (yogakaraka in H9). "
     "This dual placement represents Taurus at its most intellectually and karmically blessed."),
    ("moon", "yoga", "moon_mars_both_malefics", [3],
     "unfavorable", "strong",
     ["physical_health", "mental_health", "enemies_litigation"],
     ["moon", "mars", "yoga"],
     "Ch.2 v.53",
     "Moon (H3 functional malefic) + Mars (H7+H12 maraka-dusthana) in combination "
     "for Taurus: BR warns of the two most difficult functional planets for Taurus "
     "combining. Mental instability (Moon H3) + maraka-dusthana energy (Mars H7+H12) "
     "creates health crises, emotional volatility, and dangerous periods. This "
     "combination requires maximum health vigilance for Taurus natives."),
    ("saturn", "yoga", "saturn_debilitated_compensation", [9, 10],
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["saturn", "yoga", "debilitated", "neecha_bhanga"],
     "Ch.2 v.54",
     "Saturn debilitated (in Aries, H12 for Taurus) with neecha-bhanga (cancellation): "
     "BR notes the yogakaraka's debilitation in H12 is challenging but neecha-bhanga "
     "partially restores results. When Mars (debilitation lord) is strong, the neecha "
     "is cancelled and the yogakaraka's results come — though with some delay and "
     "foreign/H12 context. Career and fortune come through foreign lands or hidden "
     "means rather than directly."),
    ("venus", "yoga", "venus_mercury_intellectual_beauty", [1, 6],
     "favorable", "strong",
     ["physical_health", "intelligence_education", "wealth"],
     ["venus", "mercury", "yoga"],
     "Ch.2 v.55",
     "Venus (lagna lord) + Mercury (H5 trikona lord) in conjunction or mutual "
     "aspect for Taurus: BR states the most pleasant and intellectually gracious "
     "Taurus configuration. Lagna lord + trikona lord aligns personal identity "
     "with dharmic intelligence. The native is beautiful, articulate, and financially "
     "successful. Creative and analytical talents combine — excellence in art, music, "
     "mathematics, or financial analysis."),
    ("jupiter", "yoga", "jupiter_malefic_warning", [8, 11],
     "unfavorable", "moderate",
     ["longevity", "physical_health"],
     ["jupiter", "yoga", "functional_malefic"],
     "Ch.2 v.56",
     "Jupiter in kendra (H1/H4/H7/H10) for Taurus: BR specifically warns that "
     "Jupiter as H8+H11 functional malefic in kendra positions amplifies hidden "
     "obstacles and longevity concerns. Jupiter's natural benefic appearance misleads — "
     "for Taurus natives, a prominent Jupiter in kendra is a warning sign for "
     "health events (H8) arriving unexpectedly in what appears to be a fortunate period."),
    ("saturn", "yoga", "saturn_sun_9_10_lords", [9, 10],
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["saturn", "sun", "yoga"],
     "Ch.2 v.57",
     "Saturn (yogakaraka H9+H10) + Sun (H4 kendra lord) in combination for Taurus: "
     "BR notes that Saturn and Sun are mutual enemies, so their combination creates "
     "a career-authority tension. The yogakaraka's career drive conflicts with Sun's "
     "ego and authority. Career success is possible but with friction from authority "
     "figures or father. The native must navigate the tension between discipline (Saturn) "
     "and pride (Sun) in the career arena."),
    ("mercury", "yoga", "mercury_yogakaraka_dharmakarmayoga", [2, 5],
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     ["mercury", "saturn", "yoga", "dharmakarmayoga"],
     "Ch.2 v.58",
     "Mercury (H5 trikona lord) + Saturn (H10 karma lord) in conjunction, mutual "
     "aspect, or exchange for Taurus: BR's dharma-karma yoga for Taurus. The "
     "dharmic intelligence of Mercury (H5) aligns with the career action of Saturn "
     "(H10). This combination is the functional equivalent of yoga karaka's best "
     "expression for intellectually gifted Taurus natives. Career excellence through "
     "analytical and structured work."),
    ("venus", "yoga", "venus_in_5_saturn_in_9", [1, 6],
     "favorable", "strong",
     ["career_status", "spirituality", "wealth"],
     ["venus", "saturn", "yoga"],
     "Ch.2 v.59",
     "Venus (lagna lord) in H5 AND Saturn (yogakaraka) in H9 for Taurus: "
     "BR states this dual placement gives the native peak creative talent (Venus H5) "
     "with outstanding fortune (Saturn H9 yogakaraka in own house). The native "
     "achieves through artistic excellence backed by Fortune's support. A rare, "
     "highly auspicious configuration producing fame, wealth, and dharmic satisfaction."),
    ("mars", "yoga", "mars_in_10_venus_lagna", [7, 12],
     "mixed", "moderate",
     ["career_status", "longevity"],
     ["mars", "venus", "yoga"],
     "Ch.2 v.60",
     "Mars (maraka H7+H12) in H10 for Taurus: BR specifically notes this as a "
     "career-maraka tension. The maraka lord in Saturn's yogakaraka H10 creates "
     "professional success through competitive, bold action (Mars) but with health "
     "risks during the career peak. The native achieves career recognition through "
     "Mars-type work (surgery, sports, military, engineering) but must manage "
     "the maraka energy that accompanies the career achievement."),
    ("saturn", "yoga", "saturn_in_lagna_mercury_in_5", [9, 10],
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     ["saturn", "mercury", "yoga"],
     "Ch.2 v.61",
     "Saturn (yogakaraka) in H1 AND Mercury (H5 trikona) in H5 for Taurus: "
     "BR states yogakaraka in lagna combined with trikona lord in own trikona "
     "gives one of Taurus's finest dual placements. The native's personality (lagna) "
     "is fully yogakaraka-infused while intelligence and purva punya (H5) are maximized. "
     "Career, fortune, and intellectual achievement align from birth."),
    ("moon", "yoga", "moon_in_11_upachaya_taurus", [3],
     "neutral", "moderate",
     ["wealth", "career_status"],
     ["moon", "yoga"],
     "Ch.2 v.62",
     "Moon (H3 functional malefic) in H11 for Taurus: BR notes that the functional "
     "malefic Moon in the upachaya gains house gives monetary results that improve "
     "over time — a somewhat neutral placement. The H3 malefic in H11 upachaya means "
     "gains come through effort and communication but with some emotional instability "
     "or sibling involvement in financial matters. Better than most Moon placements "
     "for Taurus."),
    ("saturn", "yoga", "saturn_mercury_exchange_impact", [9, 10],
     "favorable", "strong",
     ["career_status", "wealth", "spirituality"],
     ["saturn", "mercury", "yoga", "raja_yoga", "exchange"],
     "Ch.2 v.63",
     "Saturn-Mercury parivartana (exchange) for Taurus creates a special raja yoga: "
     "BR states when Saturn is in Gemini or Virgo (Mercury's signs) and Mercury is "
     "in Capricorn or Aquarius (Saturn's signs), the mutual exchange powerfully "
     "connects the yogakaraka with the trikona lord. The native achieves both fortune "
     "and career excellence through intellectual and disciplined work. One of the "
     "most sought-after configurations for Taurus."),
    ("venus", "yoga", "venus_strong_in_lagna", [1, 6],
     "favorable", "strong",
     ["physical_health", "fame_reputation", "wealth"],
     ["venus", "yoga", "exalted"],
     "Ch.2 v.64",
     "Venus exalted (in Pisces, H11 for Taurus) for Taurus: lagna lord exalted in H11 "
     "— BR states outstanding personality, financial gains, and gracious fortune. "
     "The exalted lagna lord in the gains house gives the native maximum personal charm "
     "and financial success. Elder siblings may be distinguished. All Venus-related "
     "significations (beauty, art, finance, relationships) peak for this native."),
    ("mercury", "yoga", "mercury_sun_trikona_kendra", [2, 5],
     "mixed", "moderate",
     ["career_status", "property_vehicles"],
     ["mercury", "sun", "yoga"],
     "Ch.2 v.65",
     "Mercury (H5 trikona lord) + Sun (H4 kendra lord) in combination for Taurus: "
     "BR notes that Sun and Mercury are often conjunct (Budha-Aditya yoga). For "
     "Taurus, this combination activates both intelligence (H5) and domestic/property "
     "matters (H4). Career in education or government property sectors. The Budha-Aditya "
     "yoga is generally auspicious but the specific results for Taurus are mixed — "
     "Sun's kendra lordship creates effort, while Mercury's trikona provides support."),
]


def _make_rules(lagna: str, data: list, start_num: int, chapter: str) -> list[RuleRecord]:
    rules = []
    num = start_num
    for entry in data:
        (planet, ptype, house_or_label, lord_of,
         odir, oint, odoms, extra_tags, vref, desc) = entry
        rid = f"BVR{num:03d}"
        # Build primary_condition
        if ptype == "house_placement":
            primary = {
                "planet": planet,
                "placement_type": "house_placement",
                "placement_value": [house_or_label] if isinstance(house_or_label, int) else [],
                "house": house_or_label if isinstance(house_or_label, int) else 0,
                "planet_lord_of": lord_of,
                "for_lagna": lagna,
            }
        else:
            primary = {
                "planet": planet,
                "placement_type": ptype,
                "placement_value": lord_of,
                "yoga_label": house_or_label if isinstance(house_or_label, str) else str(house_or_label),
                "for_lagna": lagna,
            }
        tags = (["bvr", "parashari", "bhavartha_ratnakara", lagna, planet, ptype]
                + extra_tags)
        rules.append(RuleRecord(
            rule_id=rid,
            source="BhavarthaRatnakara",
            chapter=chapter,
            school="parashari",
            category=f"lagna_predictions_{lagna}",
            description=f"[BR — {lagna} lagna, {planet}] {desc}",
            confidence=0.65,
            tags=list(dict.fromkeys(tags)),
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing="dasha_dependent",
            lagna_scope=[lagna],
            verse_ref=vref,
            phase="1B_conditional",
            system="natal",
            prediction_type="event",
            gender_scope="universal",
            certainty_level="definite",
            strength_condition="any",
            house_system="sign_based",
            ayanamsha_sensitive=False,
            evaluation_method="placement_check",
            last_modified_session="S305",
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    aries_rules = _make_rules("aries", _ARIES_DATA, 1, "Ch.1")
    taurus_rules = _make_rules("taurus", _TAURUS_DATA, len(_ARIES_DATA) + 1, "Ch.2")
    return aries_rules + taurus_rules


BHAVARTHA_RATNAKARA_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    BHAVARTHA_RATNAKARA_1_REGISTRY.add(_rule)
