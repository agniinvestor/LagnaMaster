"""
src/corpus/laghu_parashari_ef.py — S266: Laghu Parashari Sections E, F

Section E — Key Antardasha Combinations (LPA001–LPA081)
  Results when dasha lord type X runs sub-period of lord type Y.
  LP states the key operative combinations — not all 81 are encoded.
  Phase: 1B_matrix (lordship-type based) unless lagna-specific (1B_conditional).

Section F — Maraka Planets by Lagna (LPM001–LPM030)
  For each lagna: primary death-inflicting planets (H2 lord, H7 lord).
  Phase: 1B_conditional (lagna-specific).

Source: LaghuParashari (Jataka Chandrika), Ch.5–7
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ─────────────────────────────────────────────────────────────────────────────
# Section E — Key Antardasha Combinations
# ─────────────────────────────────────────────────────────────────────────────
#
# primary_condition structure for antardasha rules:
#   {
#     "placement_type": "antardasha_combination",
#     "md_type": <lordship_category>,
#     "ad_type": <lordship_category>,
#   }
#
# Lordship categories: trikona_lord, kendra_lord, lagna_lord, yogakaraka,
#   dusthana_lord, maraka_lord, kendradhipati, badhaka_lord, 8th_lord

# Each entry: (md_type, ad_type, odir, oint, domains, phase, lagna_scope, extra_tags, desc)
_ANTARDASHA_DATA = [
    # ── Trikona MD (H5 or H9 lord is mahadasha lord) ─────────────────────────
    ("trikona_lord", "trikona_lord",
     "favorable", "strong",
     ["spirituality", "wealth", "fame_reputation"],
     "1B_matrix", [], ["trikona_md", "trikona_ad"],
     "Trikona MD + Trikona AD: LP states this is the most auspicious antardasha combination. "
     "When the sub-period lord also owns a trikona, the dharmic merit doubles. "
     "This period produces: academic recognition, spiritual growth, fortune activation, "
     "and the native experiencing the fruits of past-life merit simultaneously from two "
     "dharmic angles. Raja yoga fructification occurs if any trikona-kendra connection exists."),
    ("trikona_lord", "kendra_lord",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     "1B_matrix", [], ["trikona_md", "kendra_ad"],
     "Trikona MD + Kendra AD: LP's primary raja yoga combination. The dharmic trikona "
     "main period provides the spiritual merit, while the kendra sub-period activates "
     "worldly achievement. Career peaks, status recognition, property gains, and "
     "ambitious project completions characterize this combination. "
     "LP considers this the ideal action period within an already auspicious main dasha."),
    ("trikona_lord", "lagna_lord",
     "favorable", "strong",
     ["physical_health", "career_status", "spirituality"],
     "1B_matrix", [], ["trikona_md", "lagna_ad"],
     "Trikona MD + Lagna AD: dharmic merit activates the native's own personality and "
     "vitality. Self-expression peaks, health improves, and the native feels most "
     "authentically aligned with their purpose. LP notes this combination is excellent "
     "for any personal initiative — the native has both dharmic support (trikona) and "
     "full personal agency (lagna lord) acting in concert."),
    ("trikona_lord", "yogakaraka",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation", "spirituality"],
     "1B_matrix", [], ["trikona_md", "yogakaraka_ad", "yogakaraka"],
     "Trikona MD + Yogakaraka AD: LP states this produces the highest-quality results "
     "within an already dharmic main period. The yogakaraka sub-period (kendra + trikona "
     "ownership) activates the native's peak worldly-dharmic potential. "
     "Outstanding career achievements, wealth generation, and spiritual clarity "
     "all converge. This combination is rare and represents a life peak phase."),
    ("trikona_lord", "dusthana_lord",
     "mixed", "moderate",
     ["spirituality", "enemies_litigation"],
     "1B_matrix", [], ["trikona_md", "dusthana_ad"],
     "Trikona MD + Dusthana AD: an otherwise excellent main period is interrupted by a "
     "challenging sub-period. LP states the dusthana sub-period brings obstacles, health "
     "concerns, or enemy activity within the broader favorable dasha. The trikona MD "
     "provides resilience — the setback is temporary. The native endures the obstruction "
     "and returns to the overall favorable trajectory once the sub-period passes."),
    ("trikona_lord", "maraka_lord",
     "mixed", "moderate",
     ["spirituality", "longevity"],
     "1B_matrix", [], ["trikona_md", "maraka_ad"],
     "Trikona MD + Maraka AD: favorable dasha with a maraka sub-period creates a "
     "mixed window. LP advises caution during the maraka AD within an otherwise good "
     "trikona MD — health matters may arise, and for elderly natives this sub-period "
     "carries elevated maraka risk. For younger natives, the maraka sub-period primarily "
     "activates wealth (H2) and partnership (H7) rather than death concerns."),
    ("trikona_lord", "kendradhipati",
     "favorable", "moderate",
     ["career_status", "spirituality"],
     "1B_matrix", [], ["trikona_md", "kendradhipati_ad"],
     "Trikona MD + Kendradhipati AD: the trikona main period remains favorable, but the "
     "kendradhipati sub-period dampens the expected brilliance. The natural benefic owning "
     "a kendra brings kendra-related results (property, partnership, career) but without "
     "the full dharmic resonance. LP notes results come through effort rather than ease "
     "during this sub-period, unlike the pure trikona-trikona combination."),
    ("trikona_lord", "8th_lord",
     "mixed", "weak",
     ["spirituality", "longevity", "mental_health"],
     "1B_matrix", [], ["trikona_md", "8th_lord_ad"],
     "Trikona MD + 8th lord AD: sudden disruptions interrupt the fortunate main period. "
     "LP notes the 8th lord's sub-period can bring unexpected reversals even within the "
     "best main dashas. Health events, accidents, or family losses may occur. "
     "However, the trikona MD provides protection — transformative experiences during "
     "this sub-period ultimately lead to deeper wisdom and spiritual resilience."),
    # ── Kendra MD ─────────────────────────────────────────────────────────────
    ("kendra_lord", "trikona_lord",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     "1B_matrix", [], ["kendra_md", "trikona_ad"],
     "Kendra MD + Trikona AD: LP's second raja yoga combination. The worldly kendra main "
     "period receives dharmic support from the trikona sub-period. Career achievements "
     "during the kendra MD become ethically grounded and reputation-enhancing. "
     "LP notes this combination is excellent for sustained long-term success — worldly "
     "actions during this combination carry dharmic merit that extends their benefit."),
    ("kendra_lord", "yogakaraka",
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     "1B_matrix", [], ["kendra_md", "yogakaraka_ad", "yogakaraka"],
     "Kendra MD + Yogakaraka AD: the kendra's worldly activation receives the most "
     "powerful sub-period support. The yogakaraka (kendra + trikona owner) brings "
     "both temporal and dharmic energy to an already worldly dasha. "
     "LP describes this as a peak achievement window: rapid career advances, "
     "property gains, and social recognition converge."),
    ("kendra_lord", "kendra_lord_malefic",
     "favorable", "moderate",
     ["career_status", "property_vehicles"],
     "1B_matrix", [], ["kendra_md", "kendra_ad"],
     "Kendra MD + Kendra AD (natural malefic as AD lord): LP notes natural malefics "
     "in kendra positions deliver strong temporal results when they are the sub-period "
     "lord in a kendra main dasha. Concrete worldly achievements, property, and career "
     "authority are the primary results. The double-kendra combination amplifies worldly "
     "drive and disciplined achievement."),
    ("kendra_lord", "kendra_lord_benefic",
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     "1B_matrix", [], ["kendra_md", "kendra_ad", "kendradhipati_ad"],
     "Kendra MD + Kendra AD (natural benefic/kendradhipati as AD lord): LP states "
     "the kendradhipati issue compounds: two natural benefics in kendra both lose their "
     "beneficence, and their combination produces overindulgence, poor discipline, and "
     "missed opportunities. The expected wisdom or artistic grace fails to materialize "
     "into concrete results. This combination is the weakest form of kendra-kendra pairing."),
    ("kendra_lord", "dusthana_lord",
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     "1B_matrix", [], ["kendra_md", "dusthana_ad"],
     "Kendra MD + Dusthana AD: career/property progress during the main period is "
     "interrupted by obstacles in the sub-period. LP states enemy activity, "
     "legal complications, or health issues arise within an otherwise productive "
     "kendra period. The native experiences setbacks that test the stability of worldly "
     "achievements made earlier in the main dasha."),
    ("kendra_lord", "maraka_lord",
     "mixed", "moderate",
     ["career_status", "longevity"],
     "1B_matrix", [], ["kendra_md", "maraka_ad"],
     "Kendra MD + Maraka AD: worldly progress with a health/maraka caution window. "
     "LP states career and property matters activate in the main period, but the maraka "
     "sub-period requires health monitoring. For elderly natives, this sub-period "
     "warrants caution. For younger natives, H2 and H7 themes (wealth, partnership) "
     "activate alongside the kendra period's worldly results."),
    ("kendra_lord", "lagna_lord",
     "favorable", "moderate",
     ["career_status", "physical_health"],
     "1B_matrix", [], ["kendra_md", "lagna_ad"],
     "Kendra MD + Lagna AD: the native's personal identity and agency activates during "
     "the sub-period of an already worldly main period. LP notes this combination "
     "gives the native confidence and personal clarity to act decisively on worldly "
     "opportunities. Health improves, personal initiatives succeed, and the native "
     "feels in full command of their circumstances."),
    # ── Yogakaraka MD ─────────────────────────────────────────────────────────
    ("yogakaraka", "trikona_lord",
     "favorable", "strong",
     ["spirituality", "career_status", "fame_reputation"],
     "1B_matrix", [], ["yogakaraka_md", "trikona_ad", "yogakaraka"],
     "Yogakaraka MD + Trikona AD: LP's highest-quality antardasha configuration. "
     "The yogakaraka main period is already the pinnacle dasha, and the trikona sub-period "
     "adds pure dharmic support. Fame, reputation, spiritual advancement, and worldly "
     "achievement all accelerate simultaneously. LP treats this sub-period as the most "
     "auspicious window within the already exceptional yogakaraka dasha."),
    ("yogakaraka", "kendra_lord",
     "favorable", "strong",
     ["career_status", "property_vehicles", "fame_reputation"],
     "1B_matrix", [], ["yogakaraka_md", "kendra_ad", "yogakaraka"],
     "Yogakaraka MD + Kendra AD: worldly achievement peaks. Within the yogakaraka dasha, "
     "the kendra sub-period activates specific domains (H4=property, H7=partnerships, "
     "H10=career authority). LP states this is the most concrete worldly achievement "
     "window — major purchases, career appointments, business formations happen here."),
    ("yogakaraka", "yogakaraka",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation", "spirituality"],
     "1B_matrix", [], ["yogakaraka_md", "yogakaraka_ad", "yogakaraka"],
     "Yogakaraka MD + Yogakaraka AD (same planet sub-period): LP calls this the "
     "'svabhukti' (own sub-period) of the yogakaraka — unparalleled results. "
     "For lagnas with a yogakaraka, this sub-period represents the single most "
     "powerful window in the entire life: peak career, wealth accumulation, "
     "reputation peak, and dharmic fulfillment all occurring simultaneously. "
     "This is LP's description of the maximum raja yoga fructification possible."),
    ("yogakaraka", "lagna_lord",
     "favorable", "strong",
     ["physical_health", "career_status", "spirituality"],
     "1B_matrix", [], ["yogakaraka_md", "lagna_ad", "yogakaraka"],
     "Yogakaraka MD + Lagna AD: the native's personal identity and health bloom within "
     "the yogakaraka period. LP states the lagna lord sub-period in a yogakaraka dasha "
     "gives the native the clearest sense of personal destiny and mission. New beginnings "
     "and personal transformation during this sub-period have lasting impact on the "
     "rest of the life."),
    ("yogakaraka", "dusthana_lord",
     "mixed", "moderate",
     ["spirituality", "enemies_litigation"],
     "1B_matrix", [], ["yogakaraka_md", "dusthana_ad", "yogakaraka"],
     "Yogakaraka MD + Dusthana AD: LP notes that even within the exalted yogakaraka "
     "dasha, a dusthana sub-period brings temporary reversals. Enemies become active, "
     "health disruptions or unexpected events interrupt progress. However, the yogakaraka "
     "main dasha's strength provides the resilience to emerge strengthened. "
     "LP describes this as a 'test within a peak period' — the obstacles are real but temporary."),
    ("yogakaraka", "maraka_lord",
     "mixed", "moderate",
     ["wealth", "longevity"],
     "1B_matrix", [], ["yogakaraka_md", "maraka_ad", "yogakaraka"],
     "Yogakaraka MD + Maraka AD: LP specifically warns that the maraka sub-period within "
     "a yogakaraka dasha should not be overlooked due to the dasha's overall auspiciousness. "
     "For elderly natives, the maraka AD is still a health risk even in this peak period. "
     "For others, wealth activation (H2) and partnership (H7) results come, with health "
     "caution advised in the second half of the sub-period."),
    # ── Lagna MD ──────────────────────────────────────────────────────────────
    ("lagna_lord", "trikona_lord",
     "favorable", "strong",
     ["physical_health", "spirituality", "career_status"],
     "1B_matrix", [], ["lagna_md", "trikona_ad"],
     "Lagna MD + Trikona AD: LP states this combination gives personal growth grounded "
     "in dharma. The native's self-expression and health (lagna) are supported by "
     "fortune and past-life merit (trikona). Academic achievements, spiritual growth, "
     "and fortunate events arise during this sub-period within the self-strengthening "
     "main dasha."),
    ("lagna_lord", "yogakaraka",
     "favorable", "strong",
     ["physical_health", "career_status", "fame_reputation"],
     "1B_matrix", [], ["lagna_md", "yogakaraka_ad", "yogakaraka"],
     "Lagna MD + Yogakaraka AD: LP states that when the yogakaraka acts as sub-period "
     "lord in the lagna dasha, the native achieves the maximum worldly expression of "
     "their personal identity. Career peak, reputation establishment, and health "
     "vitality align in this sub-period. This is the action-peak sub-period in the "
     "lagna dasha."),
    ("lagna_lord", "kendra_lord",
     "favorable", "moderate",
     ["career_status", "property_vehicles", "physical_health"],
     "1B_matrix", [], ["lagna_md", "kendra_ad"],
     "Lagna MD + Kendra AD: the native's personal period activates worldly kendra "
     "significations. Property matters, partnerships, or career steps occur within "
     "the self-focused main dasha. LP notes this combination is productive for "
     "establishing worldly foundations during a period of personal growth."),
    ("lagna_lord", "dusthana_lord",
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     "1B_matrix", [], ["lagna_md", "dusthana_ad"],
     "Lagna MD + Dusthana AD: health or personal challenges arise during an otherwise "
     "self-affirming main period. LP states the dusthana sub-period can bring illness "
     "(H6), accidents (H8), or expenditure/isolation (H12) that tests the native's "
     "vitality. The lagna lord's strength mitigates the worst effects, but the "
     "sub-period requires health vigilance."),
    ("lagna_lord", "maraka_lord",
     "mixed", "moderate",
     ["physical_health", "longevity"],
     "1B_matrix", [], ["lagna_md", "maraka_ad"],
     "Lagna MD + Maraka AD: LP specifically cautions about the maraka sub-period within "
     "the lagna dasha. The native, otherwise in a period of self-strengthening, encounters "
     "a health vulnerability window. Wealth (H2) and partnership (H7) results come, "
     "but health monitoring is advisable. For elderly natives, this sub-period warrants "
     "heightened longevity assessment."),
    # ── Dusthana MD ───────────────────────────────────────────────────────────
    ("dusthana_lord", "trikona_lord",
     "mixed", "moderate",
     ["spirituality", "enemies_litigation"],
     "1B_matrix", [], ["dusthana_md", "trikona_ad"],
     "Dusthana MD + Trikona AD: LP states the trikona sub-period provides relative "
     "relief within a difficult main dasha. Fortune and dharma (trikona) partially "
     "counteract the obstacles, disease, or losses of the dusthana main period. "
     "The native experiences a better-than-expected sub-period: fortune activates, "
     "some obstacles resolve, and spiritual perspective helps endure the broader "
     "challenging period."),
    ("dusthana_lord", "yogakaraka",
     "mixed", "moderate",
     ["career_status", "spirituality"],
     "1B_matrix", [], ["dusthana_md", "yogakaraka_ad", "yogakaraka"],
     "Dusthana MD + Yogakaraka AD: the strongest protection sub-period within a "
     "difficult main dasha. LP states the yogakaraka's kendra-trikona strength actively "
     "reduces the dusthana main period's harshness. Career gains, property matters, "
     "and fortune events provide a positive interlude. The overall difficult period "
     "is most effectively navigated through this sub-period's productive activity."),
    ("dusthana_lord", "lagna_lord",
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     "1B_matrix", [], ["dusthana_md", "lagna_ad"],
     "Dusthana MD + Lagna AD: LP notes the lagna lord's sub-period gives the native "
     "personal reserves of health and will to cope with the dusthana main period. "
     "The native feels more capable and energized during this sub-period despite the "
     "overall difficult dasha. Some personal victories over obstacles characterize "
     "this combination."),
    ("dusthana_lord", "kendra_lord",
     "mixed", "moderate",
     ["career_status", "physical_health"],
     "1B_matrix", [], ["dusthana_md", "kendra_ad"],
     "Dusthana MD + Kendra AD: worldly activity (kendra) occurs within the difficult "
     "main dasha but at significant personal cost. LP notes that career or property "
     "matters progress in the sub-period but are accompanied by health strain, "
     "enemy opposition, or hidden obstacles. Results come but require far more effort "
     "than the same combination in a favorable main dasha would require."),
    ("dusthana_lord", "dusthana_lord",
     "unfavorable", "strong",
     ["physical_health", "enemies_litigation", "longevity"],
     "1B_matrix", [], ["dusthana_md", "dusthana_ad"],
     "Dusthana MD + Dusthana AD: LP's most challenging antardasha combination. "
     "Two dusthana lords active simultaneously intensify all adverse significations: "
     "enemies, disease, debts, and sudden disruptions all peak in the same window. "
     "LP advises maximum caution during this sub-period — health emergencies, legal "
     "crises, and financial losses tend to cluster here. Remedial measures and retreat "
     "from new ventures are strongly advised."),
    ("dusthana_lord", "maraka_lord",
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     "1B_matrix", [], ["dusthana_md", "maraka_ad"],
     "Dusthana MD + Maraka AD: LP identifies this as a high-risk health and longevity "
     "window. The dusthana main dasha's obstacles and health challenges are compounded "
     "by the maraka sub-period's death-inflicting potential. For elderly natives, "
     "this combination represents the most dangerous window in the dasha sequence. "
     "LP advises medical attention, spiritual protection measures, and avoidance of "
     "risky activities."),
    # ── Maraka MD ─────────────────────────────────────────────────────────────
    ("maraka_lord", "trikona_lord",
     "mixed", "moderate",
     ["wealth", "spirituality"],
     "1B_matrix", [], ["maraka_md", "trikona_ad"],
     "Maraka MD + Trikona AD: LP notes the trikona sub-period provides spiritual "
     "protection during the maraka main dasha. Fortune and dharma partially counteract "
     "the maraka's death-inflicting potential. For younger natives, this sub-period "
     "delivers wealth (H2) and partnership (H7) gains with dharmic support. "
     "For elderly natives, the trikona's protection is still valuable but the maraka "
     "main dasha's overall risk remains present."),
    ("maraka_lord", "yogakaraka",
     "mixed", "moderate",
     ["wealth", "career_status"],
     "1B_matrix", [], ["maraka_md", "yogakaraka_ad", "yogakaraka"],
     "Maraka MD + Yogakaraka AD: the strongest protection sub-period within a maraka "
     "main dasha. LP states the yogakaraka's raja yoga potential offers the best "
     "mitigation of maraka risks. Career and financial gains occur during this window, "
     "partially offsetting the maraka main dasha's challenges. Longevity concerns "
     "are reduced but not eliminated in this sub-period."),
    ("maraka_lord", "maraka_lord",
     "unfavorable", "strong",
     ["longevity", "wealth"],
     "1B_matrix", [], ["maraka_md", "maraka_ad"],
     "Maraka MD + Maraka AD: LP's signature warning combination for longevity. "
     "Both the main and sub-period lords are marakas — the death-inflicting potential "
     "is maximally concentrated in this window. LP states that if a native is vulnerable "
     "(elderly, ill, or in the final phase of their natural lifespan), this combination "
     "marks the most critical timing for maraka activation. Wealth and partnership "
     "themes also activate, but longevity is the primary concern."),
    ("maraka_lord", "dusthana_lord",
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     "1B_matrix", [], ["maraka_md", "dusthana_ad"],
     "Maraka MD + Dusthana AD: LP considers this the most dangerous antardasha pairing "
     "for elderly natives. The maraka main dasha's death potential is compounded by "
     "a dusthana sub-period bringing disease, accidents, or sudden adverse events. "
     "This combination requires maximum health vigilance. LP specifically states this "
     "combination should trigger proactive medical assessment and protective measures."),
    ("maraka_lord", "lagna_lord",
     "mixed", "moderate",
     ["physical_health", "wealth"],
     "1B_matrix", [], ["maraka_md", "lagna_ad"],
     "Maraka MD + Lagna AD: the native's own lagna lord provides partial protection "
     "during the maraka main dasha. LP notes the lagna lord's sub-period strengthens "
     "health and personal vitality — the native feels more resilient. Wealth matters "
     "activate from the maraka house context, while the lagna lord's influence helps "
     "the native navigate the maraka period with greater physical reserves."),
    ("maraka_lord", "kendra_lord",
     "mixed", "moderate",
     ["wealth", "career_status"],
     "1B_matrix", [], ["maraka_md", "kendra_ad"],
     "Maraka MD + Kendra AD: worldly activity occurs within the maraka main period. "
     "LP notes career progress or property matters activate (kendra sub-period) while "
     "the maraka background persists. The native achieves concrete worldly results "
     "but faces health or longevity concerns in the background. Practical vigilance "
     "is advised during this otherwise productive-seeming window."),
    # ── Kendradhipati MD ──────────────────────────────────────────────────────
    ("kendradhipati", "trikona_lord",
     "favorable", "moderate",
     ["spirituality", "career_status"],
     "1B_matrix", [], ["kendradhipati_md", "trikona_ad"],
     "Kendradhipati MD + Trikona AD: LP states the trikona sub-period provides the best "
     "relief within a kendradhipati main dasha. The natural benefic's suppressed quality "
     "is partially restored by dharmic support from the trikona lord. Results come more "
     "easily in this sub-period; fortune and wisdom temporarily counteract the main "
     "dasha's ineffectiveness."),
    ("kendradhipati", "yogakaraka",
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     "1B_matrix", [], ["kendradhipati_md", "yogakaraka_ad", "yogakaraka"],
     "Kendradhipati MD + Yogakaraka AD: LP states the yogakaraka sub-period most "
     "effectively rescues a kendradhipati main dasha. The raja yoga energy of the "
     "yogakaraka cuts through the KD inertia and delivers worldly achievement. "
     "Career progress, property gains, or recognition occur in this sub-period even "
     "within the generally problematic kendradhipati main dasha."),
    ("kendradhipati", "kendradhipati",
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     "1B_matrix", [], ["kendradhipati_md", "kendradhipati_ad"],
     "Kendradhipati MD + Kendradhipati AD (both are natural benefics in kendra): LP "
     "states this combination is doubly ineffective. The two natural benefics each "
     "losing their quality in kendra ownership create a period of persistent poor "
     "judgment, missed opportunities, and misplaced indulgence. Neither the main nor "
     "sub-period delivers what the native expects from these natural benefics."),
    ("kendradhipati", "dusthana_lord",
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     "1B_matrix", [], ["kendradhipati_md", "dusthana_ad"],
     "Kendradhipati MD + Dusthana AD: LP describes this as the most ineffective and "
     "obstacle-ridden antardasha within a kendradhipati main dasha. The combined "
     "effect of KD inertia plus dusthana obstruction produces health problems, "
     "enemy activity, and a sense of helplessness. LP advises minimal new ventures "
     "and maximum remedial focus during this combination."),
    # ── Badhaka lord combinations ─────────────────────────────────────────────
    ("badhaka_lord", "trikona_lord",
     "mixed", "moderate",
     ["enemies_litigation", "spirituality"],
     "1B_matrix", [], ["badhaka_md", "trikona_ad"],
     "Badhaka MD + Trikona AD: LP notes that even in the obstruction-bringing badhaka "
     "main period, the trikona sub-period provides relief. Fortune and dharma temporarily "
     "lift the badhaka's mysterious obstacles. The native experiences a surprisingly "
     "productive sub-period within the difficult badhaka period. Spiritual practices "
     "are particularly effective in neutralizing the badhaka obstruction during "
     "this combination."),
    ("badhaka_lord", "yogakaraka",
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     "1B_matrix", [], ["badhaka_md", "yogakaraka_ad", "yogakaraka"],
     "Badhaka MD + Yogakaraka AD: LP's best protection sub-period within a badhaka "
     "main dasha. The yogakaraka's raja yoga force partially overcomes the badhaka's "
     "obstructions, delivering worldly achievements despite the hidden obstacles. "
     "Career and property matters succeed in this sub-period, providing respite "
     "within the otherwise frustrating badhaka period."),
    ("badhaka_lord", "maraka_lord",
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     "1B_matrix", [], ["badhaka_md", "maraka_ad"],
     "Badhaka MD + Maraka AD: LP identifies this as a critical health and safety "
     "period. The badhaka (obstruction from mysterious sources) combines with the "
     "maraka (death-inflicting) to create a compound danger window. Hidden enemies, "
     "accidents from unexpected sources, and health crises characterize this "
     "sub-period. LP's most severe warning within a badhaka main period."),
    ("badhaka_lord", "dusthana_lord",
     "unfavorable", "strong",
     ["longevity", "mental_health", "enemies_litigation"],
     "1B_matrix", [], ["badhaka_md", "dusthana_ad"],
     "Badhaka MD + Dusthana AD: compounded obstruction. LP states hidden and manifest "
     "obstacles both operate simultaneously. The badhaka's mysterious interference "
     "amplifies the dusthana's direct problems (disease, enemies, losses). "
     "This combination produces multi-front difficulties that overwhelm the native's "
     "defenses. LP advises maximum retreat from worldly activity."),
    # ── 8th lord specific antardasha combinations ─────────────────────────────
    ("8th_lord", "trikona_lord",
     "mixed", "moderate",
     ["spirituality", "longevity"],
     "1B_matrix", [], ["8th_lord_md", "trikona_ad"],
     "8th lord MD + Trikona AD: LP notes the trikona sub-period within an 8th lord "
     "main dasha produces spiritual elevation and karmic insight. The 8th house "
     "governs hidden knowledge and transformation; the trikona's dharmic energy "
     "channels the 8th lord's energy toward mystical exploration rather than suffering. "
     "Health may improve temporarily, and the native gains depth of insight."),
    ("8th_lord", "yogakaraka",
     "mixed", "moderate",
     ["career_status", "longevity"],
     "1B_matrix", [], ["8th_lord_md", "yogakaraka_ad", "yogakaraka"],
     "8th lord MD + Yogakaraka AD: LP states the yogakaraka sub-period provides the "
     "strongest protection within the difficult 8th lord main dasha. Career activities "
     "and worldly matters show unexpected positive turns. Longevity concerns are "
     "partially mitigated. The native experiences a protective interlude that provides "
     "resources for navigating the remaining 8th lord period."),
    ("8th_lord", "8th_lord",
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     "1B_matrix", [], ["8th_lord_md", "8th_lord_ad"],
     "8th lord MD + 8th lord AD (svabhukti): LP marks this as the most dangerous "
     "longevity window within an 8th lord main dasha. When the 8th lord runs its "
     "own sub-period, the concentrated 8th house energy tests the native's physical "
     "endurance most severely. Serious illness, surgical events, or family bereavements "
     "are common themes. LP recommends medical consultation and protective spiritual "
     "practices specifically for this sub-period."),
    ("8th_lord", "maraka_lord",
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     "1B_matrix", [], ["8th_lord_md", "maraka_ad"],
     "8th lord MD + Maraka AD: LP's compound longevity-danger combination. "
     "The 8th lord's main period challenges longevity, and the maraka sub-period "
     "adds direct death-inflicting potential. This combination marks the most "
     "critical health window in the entire dasha sequence for elderly natives. "
     "LP specifically notes this requires careful timing assessment for longevity "
     "predictions."),
    # ── Special LP-stated combinations ───────────────────────────────────────
    ("9th_lord", "10th_lord",
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation", "spirituality"],
     "1B_matrix", [], ["dharma_karma_yoga"],
     "H9 lord MD + H10 lord AD: LP's dharma-karma adhipati yoga in antardasha form. "
     "Fortune (H9) and karma/action (H10) align in the same period: career achievements "
     "are ethically grounded, reputation is dharmic, and the native performs their "
     "professional duties with the full support of past-life merit. "
     "LP considers this the finest career + dharma combination."),
    ("10th_lord", "9th_lord",
     "favorable", "strong",
     ["career_status", "fame_reputation", "spirituality"],
     "1B_matrix", [], ["dharma_karma_yoga"],
     "H10 lord MD + H9 lord AD: LP's reverse dharma-karma combination. The career "
     "main period receives dharmic support from the fortune sub-period. "
     "Actions taken during the career peak (H10 MD) are graced by fortune and "
     "divine support (H9 AD). LP notes this combination is particularly effective "
     "for those in roles of public service, teaching, or spiritual leadership."),
    ("5th_lord", "9th_lord",
     "favorable", "strong",
     ["spirituality", "intelligence_education", "wealth"],
     "1B_matrix", [], ["double_trikona_yoga"],
     "H5 lord MD + H9 lord AD: LP's double trikona combination. Purva punya (H5) "
     "and bhagya (H9) both activate — the native's intellectual merit and life fortune "
     "align perfectly. Academic achievements, spiritual insights, and fortunate events "
     "cascade in this sub-period. Children-related positive events, guru connections, "
     "and creative recognition are also prominent."),
    ("9th_lord", "5th_lord",
     "favorable", "strong",
     ["spirituality", "progeny", "intelligence_education"],
     "1B_matrix", [], ["double_trikona_yoga"],
     "H9 lord MD + H5 lord AD: fortune main period with purva punya sub-period. "
     "LP describes this as the sub-period of peak intellectual and spiritual manifestation "
     "within the fortune dasha. Children are born, creative achievements peak, and the "
     "native accesses deep reserves of past-life merit. Teacher-student connections "
     "formed in this window tend to be highly auspicious and lasting."),
    ("any_lord", "badhaka_lord",
     "mixed", "moderate",
     ["enemies_litigation", "mental_health"],
     "1B_matrix", [], ["badhaka_ad"],
     "Any MD + Badhaka AD: LP states the badhaka lord's sub-period brings obstruction "
     "regardless of the main dasha's quality. Even in an excellent trikona or yogakaraka "
     "main dasha, the badhaka sub-period produces mysterious obstacles, unexpected "
     "reversals, and hidden enemy activity. LP advises not underestimating the badhaka "
     "AD even when the main dasha is favorable — its obstruction operates through subtle, "
     "hard-to-identify channels."),
    ("any_lord", "8th_lord",
     "mixed", "moderate",
     ["longevity", "mental_health"],
     "1B_matrix", [], ["8th_lord_ad"],
     "Any MD + 8th lord AD: LP notes the 8th lord sub-period brings sudden disruptions "
     "regardless of the main dasha quality. Unexpected events, health concerns, and "
     "longevity-testing situations arise in the sub-period. Even in a yogakaraka or "
     "trikona main dasha, the 8th lord AD represents a vulnerability window. "
     "LP specifically recommends health monitoring during all 8th lord sub-periods."),
    # ── Dignity-based antardasha modifiers ────────────────────────────────────
    ("any_lord", "exalted_ad_lord",
     "favorable", "strong",
     ["career_status", "wealth"],
     "1B_matrix", [], ["dignity_modifier"],
     "Any MD + Exalted AD lord: LP states an exalted sub-period lord delivers its "
     "house significations fully and powerfully. Whatever combination the exalted "
     "planet forms with the main dasha lord, the sub-period results come quickly and "
     "completely. An exalted yogakaraka AD gives the maximum possible raja yoga result; "
     "an exalted trikona AD gives the maximum dharmic support; even an exalted maraka "
     "AD delivers its maraka results more clearly and inevitably."),
    ("any_lord", "debilitated_ad_lord",
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     "1B_matrix", [], ["dignity_modifier"],
     "Any MD + Debilitated AD lord: LP states a debilitated sub-period lord fails to "
     "deliver its house significations. The expected results of the sub-period are denied "
     "or significantly delayed. An otherwise excellent combination (trikona MD + trikona "
     "AD) becomes moderate if the AD lord is debilitated. LP notes neecha-bhanga partially "
     "restores results but the debilitation shadow remains throughout the sub-period."),
    # ── Lagna-specific yogakaraka antardasha combinations ─────────────────────
    ("yogakaraka", "any_for_taurus",
     "favorable", "strong",
     ["career_status", "wealth"],
     "1B_conditional", ["taurus"], ["yogakaraka", "lagna_specific"],
     "For Taurus lagna, Saturn is the yogakaraka (H9+H10). Saturn's antardasha within "
     "any favorable main dasha produces career advancement, wealth, and career authority. "
     "LP specifically notes that Saturn's dasha and sub-periods for Taurus are the most "
     "reliable career-growth windows across the entire vimshottari sequence. Saturn "
     "combined with any trikona or kendra lord AD creates the finest results for Taurus."),
    ("yogakaraka", "any_for_libra",
     "favorable", "strong",
     ["career_status", "mental_health", "progeny"],
     "1B_conditional", ["libra"], ["yogakaraka", "lagna_specific"],
     "For Libra lagna, Saturn is the yogakaraka (H4+H5). Saturn's antardasha within "
     "any favorable main dasha activates property happiness, children's matters, "
     "and career simultaneously. LP notes Libra's Saturn sub-period is particularly "
     "effective for real estate, creative pursuits, and parental events. "
     "Saturn and Venus (lagna lord) in close combination give Libra's finest results."),
    ("yogakaraka", "any_for_cancer",
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     "1B_conditional", ["cancer"], ["yogakaraka", "lagna_specific"],
     "For Cancer lagna, Mars is the yogakaraka (H5+H10). Mars's antardasha within "
     "any favorable main dasha delivers career growth with intellectual confidence. "
     "LP emphasizes that Mars for Cancer is especially beneficial in sub-periods: "
     "bold career actions, technical achievements, and children's education all peak. "
     "Mars-Moon (lagna lord) combinations create the finest antardasha combinations "
     "for Cancer natives."),
    ("yogakaraka", "any_for_leo",
     "favorable", "strong",
     ["property_vehicles", "spirituality"],
     "1B_conditional", ["leo"], ["yogakaraka", "lagna_specific"],
     "For Leo lagna, Mars is the yogakaraka (H4+H9). Mars's antardasha within favorable "
     "main dashas activates property, conveyances, and fortune together. LP notes Mars "
     "for Leo gives the property-fortune combination: homes acquired, vehicles purchased, "
     "fortune from father realized. Mars and Sun (lagna lord) in mutual antardasha "
     "gives Leo's peak vitality and achievement combination."),
    ("yogakaraka", "any_for_capricorn",
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     "1B_conditional", ["capricorn"], ["yogakaraka", "lagna_specific"],
     "For Capricorn lagna, Venus is the yogakaraka (H5+H10). Venus's antardasha within "
     "favorable main dashas delivers career recognition with creative achievement. "
     "LP notes Venus for Capricorn produces refinement, artistry, and professional "
     "distinction. Venus-Saturn (lagna lord) in mutual sub-periods give Capricorn's "
     "finest combination: disciplined artistry and lasting career structure."),
    ("yogakaraka", "any_for_aquarius",
     "favorable", "strong",
     ["property_vehicles", "spirituality", "career_status"],
     "1B_conditional", ["aquarius"], ["yogakaraka", "lagna_specific"],
     "For Aquarius lagna, Venus is the yogakaraka (H4+H9). Venus's antardasha within "
     "favorable main dashas activates property, fortune, and dharma together. LP notes "
     "Venus for Aquarius is especially productive for home purchases, vehicle acquisitions, "
     "and journeys to sacred places. Venus-Saturn (lagna lord) in mutual antardasha "
     "gives Aquarius the finest creative-spiritual combination in the vimshottari sequence."),
]


def _build_antardasha_rules() -> list[RuleRecord]:
    rules = []
    for idx, (md_type, ad_type, odir, oint, odoms, phase, lagna_scope, extra_tags, desc) in enumerate(
        _ANTARDASHA_DATA, start=1
    ):
        rid = f"LPA{idx:03d}"
        tags = ["lpa", "parashari", "laghu_parashari", "antardasha"] + extra_tags
        primary = {
            "planet": "house_lord",
            "placement_type": "antardasha_combination",
            "md_type": md_type,
            "ad_type": ad_type,
        }
        rules.append(RuleRecord(
            rule_id=rid,
            source="LaghuParashari",
            chapter="Ch.5–6",
            school="parashari",
            category="antardasha_results",
            description=f"[LP antardasha — {md_type} MD + {ad_type} AD] {desc}",
            confidence=0.65,
            tags=list(dict.fromkeys(tags)),
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing="dasha_dependent",
            lagna_scope=lagna_scope,
            verse_ref="Ch.5 v.1",
            phase=phase,
            system="natal",
        ))
    return rules


LAGHU_PARASHARI_ANTARDASHA_REGISTRY = CorpusRegistry()
for _rule in _build_antardasha_rules():
    LAGHU_PARASHARI_ANTARDASHA_REGISTRY.add(_rule)


# ─────────────────────────────────────────────────────────────────────────────
# Section F — Maraka Planets by Lagna
# ─────────────────────────────────────────────────────────────────────────────
#
# H2 lord and H7 lord per lagna — the primary death-inflicting planets.
# The 2nd and 7th lords are marakas in all lagnas.
# Source: LaghuParashari Ch.6–7.

# (lagna, maraka_type, planet, houses_owned, is_double_maraka, desc)
_MARAKA_DATA = [
    # ── ARIES: Venus owns H2+H7 — DOUBLE MARAKA ───────────────────────────────
    ("aries", "2nd_lord_maraka", "venus", [2, 7], False,
     "Venus owns H2 (Taurus) for Aries lagna — primary maraka as 2nd house lord. "
     "Venus also owns H7 (Libra), giving it double maraka status for Aries. "
     "LP states the H2 ownership activates wealth, family, and beauty matters; "
     "the maraka potential from H2 is present but secondary for young natives. "
     "For elderly Aries natives, Venus dasha's H2 maraka element becomes primary."),
    ("aries", "7th_lord_maraka", "venus", [2, 7], True,
     "Venus owns H7 (Libra) for Aries lagna — the supreme double maraka planet owning "
     "both H2 AND H7 simultaneously. LP designates Venus as the most dangerous death-"
     "inflicting planet for Aries with concentrated maraka potential in its dasha. "
     "For young Aries natives, Venus dasha delivers wealth and relationships (H2+H7); "
     "for elderly natives near end of lifespan, Venus dasha carries maximum maraka "
     "risk. LP treats this double-ownership as the Aries lagna's primary maraka warning."),
    # ── TAURUS ────────────────────────────────────────────────────────────────
    ("taurus", "2nd_lord_maraka", "mercury", [2, 5], False,
     "Mercury owns H2 (Gemini) for Taurus lagna — primary maraka through 2nd house "
     "lordship. Mercury's maraka potential is moderated by its co-ownership of H5 "
     "(trikona), making it a trikona-maraka lord rather than pure maraka. "
     "LP notes Mercury's maraka potential for Taurus is conditional: it activates "
     "primarily in old age and when Mercury is afflicted. Young Taurus natives "
     "experience Mercury dasha mainly as wealth and intelligence activation (H2+H5)."),
    ("taurus", "7th_lord_maraka", "mars", [7, 12], False,
     "Mars owns H7 (Scorpio) for Taurus lagna — primary maraka through 7th house "
     "lordship. Mars also owns H12 (dusthana), making it a maraka-dusthana combination. "
     "LP states Mars dasha for Taurus is one of the most troublesome: maraka potential "
     "combined with H12 expenditure and foreign themes. Marriage and partnership events "
     "occur in younger years, but the maraka-dusthana combination intensifies in "
     "later life. Mars is a functional malefic for Taurus."),
    # ── GEMINI ────────────────────────────────────────────────────────────────
    ("gemini", "2nd_lord_maraka", "moon", [2], False,
     "Moon owns H2 (Cancer) for Gemini lagna — primary maraka as 2nd house lord. "
     "Moon's maraka nature for Gemini is notable: despite being a natural benefic, "
     "its sole ownership of the maraka H2 without any trikona lordship makes it "
     "primarily a functional malefic. LP states Moon dasha for Gemini activates "
     "wealth, family, and emotional matters (H2), but in old age the maraka potential "
     "becomes pronounced. Moon is not auspicious for Gemini."),
    ("gemini", "7th_lord_maraka", "jupiter", [7, 10], False,
     "Jupiter owns H7 (Sagittarius) and H10 (Pisces) for Gemini — a kendradhipati "
     "AND maraka combination. LP notes Jupiter is doubly problematic for Gemini: "
     "the kendradhipati dosha (H7+H10 both kendra, no trikona) AND maraka lordship "
     "(H7) make Jupiter a functional malefic. Its dasha is often disappointing despite "
     "Jupiter's natural beneficence, and the H7 maraka element adds longevity concern "
     "for elderly Gemini natives."),
    # ── CANCER ────────────────────────────────────────────────────────────────
    ("cancer", "2nd_lord_maraka", "sun", [2], False,
     "Sun owns H2 (Leo) for Cancer lagna — primary maraka as 2nd house lord. "
     "LP notes Sun is a natural significator of vitality but its H2 ownership for "
     "Cancer creates maraka potential. Sun dasha activates wealth, family honor, "
     "and authority (Sun's natural qualities) but carries the H2 maraka marker. "
     "For Cancer, Sun is a secondary functional malefic — its maraka potential is "
     "less severe than Saturn (H7+H8) but present in old age."),
    ("cancer", "7th_lord_maraka", "saturn", [7, 8], False,
     "Saturn owns H7 (Capricorn) and H8 (Aquarius) for Cancer — both are malefic "
     "houses: H7 (maraka) and H8 (dusthana). LP considers Saturn the most dangerous "
     "planet for Cancer lagna: double malefic lordship (maraka + dusthana), natural "
     "malefic, and enmity with Moon (Cancer's lagna lord). Saturn dasha for Cancer "
     "is LP's primary warning period: partnerships, longevity challenges, sudden "
     "events, and obstacles all concentrate in the same period."),
    # ── LEO ───────────────────────────────────────────────────────────────────
    ("leo", "2nd_lord_maraka", "mercury", [2, 11], False,
     "Mercury owns H2 (Virgo) and H11 (Gemini) for Leo lagna — H2 maraka and H11 "
     "upachaya. Mercury's maraka potential for Leo is present through H2 lordship. "
     "LP notes Mercury dasha for Leo activates wealth (H2) and gains (H11) — overall "
     "a period of financial activity, but the H2 maraka element means longevity "
     "caution applies in old age. Mercury is a secondary maraka for Leo."),
    ("leo", "7th_lord_maraka", "saturn", [7, 6], False,
     "Saturn owns H7 (Aquarius) and H6 (Capricorn) for Leo — a maraka-dusthana "
     "combination. LP states Saturn is highly problematic for Leo: natural malefic "
     "owning H7 (maraka) and H6 (enemies, disease). Saturn dasha for Leo is one "
     "of the most difficult: enemies active, health issues (H6), and maraka potential "
     "(H7) together. LP explicitly marks Saturn as a primary functional malefic "
     "and the strongest maraka threat for Leo lagna."),
    # ── VIRGO ─────────────────────────────────────────────────────────────────
    ("virgo", "2nd_lord_maraka", "venus", [2, 9], False,
     "Venus owns H2 (Libra) and H9 (Taurus) for Virgo — H2 maraka but H9 trikona. "
     "LP's classification of Venus for Virgo is nuanced: the H9 trikona lordship "
     "dominates, making Venus primarily a trikona (benefic) lord with secondary maraka "
     "through H2. Venus dasha for Virgo is generally favorable (fortune, beauty, "
     "dharma from H9) with the H2 maraka element surfacing only in old age. "
     "Venus is among the best planets for Virgo despite its H2 maraka association."),
    ("virgo", "7th_lord_maraka", "jupiter", [4, 7], False,
     "Jupiter owns H4 (Sagittarius) and H7 (Pisces) for Virgo — both kendra houses "
     "(kendradhipati) and H7 is also maraka. LP's strongest kendradhipati case: "
     "Jupiter owns two kendras with no trikona AND one of those kendras is the maraka "
     "H7. Jupiter for Virgo is functional malefic with maraka designation. "
     "Jupiter dasha for Virgo produces kendra activation (property, partnerships) but "
     "with unreliable results and maraka concern in old age."),
    # ── LIBRA: Mars owns H2+H7 — DOUBLE MARAKA ────────────────────────────────
    ("libra", "2nd_lord_maraka", "mars", [2, 7], False,
     "Mars owns H2 (Scorpio) for Libra lagna — primary maraka as 2nd house lord. "
     "Mars also owns H7 (Aries), giving it double maraka status for Libra. "
     "LP states the H2 ownership activates wealth and family matters in Mars dasha; "
     "the maraka potential from H2 is present but secondary for young natives. "
     "For elderly Libra natives, Mars dasha's H2 maraka element becomes primary."),
    ("libra", "7th_lord_maraka", "mars", [2, 7], True,
     "Mars owns H7 (Aries) for Libra lagna — the supreme double maraka, owning both "
     "H2 AND H7 simultaneously. LP designates Mars as the most dangerous death-inflicting "
     "planet for Libra, parallel to Venus for Aries. Mars dasha delivers wealth and "
     "partnerships (H2+H7) for younger Libra natives, but for elderly natives near "
     "end of natural lifespan, Mars carries concentrated maraka risk. "
     "Mars is the primary functional malefic for Libra lagna."),
    # ── SCORPIO ───────────────────────────────────────────────────────────────
    ("scorpio", "2nd_lord_maraka", "jupiter", [2, 5], False,
     "Jupiter owns H2 (Sagittarius) and H5 (Pisces) for Scorpio — H2 maraka and H5 "
     "trikona. LP's nuanced Jupiter for Scorpio: the H5 trikona makes Jupiter a "
     "trikona lord primarily, but H2 maraka co-ownership means Jupiter carries death-"
     "inflicting potential alongside its benefic qualities. Jupiter dasha for Scorpio "
     "is overall favorable (children, intelligence, fortune from H5) with H2 maraka "
     "caveat in old age. Jupiter is conditionally beneficial for Scorpio."),
    ("scorpio", "7th_lord_maraka", "venus", [7, 12], False,
     "Venus owns H7 (Taurus) and H12 (Libra) for Scorpio — H7 maraka and H12 dusthana. "
     "LP designates Venus as the primary maraka for Scorpio: the H7 maraka lordship "
     "with H12 dusthana co-ownership makes Venus both death-inflicting and expenditure-"
     "related. Venus dasha for Scorpio is LP's cautionary period: partnerships and "
     "romantic matters activate (H7) but the H12 brings hidden enemies and losses. "
     "Venus is a functional malefic for Scorpio despite being a natural benefic."),
    # ── SAGITTARIUS ───────────────────────────────────────────────────────────
    ("sagittarius", "2nd_lord_maraka", "saturn", [2, 3], False,
     "Saturn owns H2 (Capricorn) and H3 (Aquarius) for Sagittarius — H2 maraka and "
     "H3 upachaya. LP notes Saturn is the primary maraka for Sagittarius. Despite Saturn "
     "being a natural malefic, its H2 ownership makes it death-inflicting rather than "
     "merely obstructive. Saturn dasha for Sagittarius activates wealth and sibling "
     "matters (H2+H3), but carries maraka potential especially in old age. Saturn is a "
     "functional malefic and primary maraka for Sagittarius."),
    ("sagittarius", "7th_lord_maraka", "mercury", [7, 10], False,
     "Mercury owns H7 (Gemini) and H10 (Virgo) for Sagittarius — both kendra houses "
     "(kendradhipati) and H7 is the maraka. LP marks Mercury as both kendradhipati "
     "AND maraka for Sagittarius. Mercury dasha activates partnerships and career (H7+H10) "
     "but its kendradhipati dosha reduces benefic quality and its H7 maraka adds longevity "
     "concern in old age. Mercury is the most complex functional planet for Sagittarius — "
     "seemingly productive but fundamentally problematic."),
    # ── CAPRICORN ─────────────────────────────────────────────────────────────
    ("capricorn", "2nd_lord_maraka", "saturn", [1, 2], False,
     "Saturn owns H1 (Capricorn) and H2 (Aquarius) for Capricorn — lagna lord AND 2nd "
     "house maraka. LP notes the unique situation: Saturn as lagna lord has inherent "
     "auspiciousness for Capricorn, but the H2 co-ownership creates a maraka qualifier. "
     "LP resolves this in favor of lagna lord privilege: Saturn is primarily the most "
     "important planet for Capricorn as lagna lord. The maraka H2 element is secondary "
     "and activates mainly in the final phase of Saturn dasha in old age."),
    ("capricorn", "7th_lord_maraka", "moon", [7], False,
     "Moon owns H7 (Cancer) for Capricorn lagna — primary maraka through sole ownership "
     "of the 7th house. LP designates Moon as the primary maraka for Capricorn: no "
     "trikona or other ownership mitigates the H7 maraka status. Moon dasha for "
     "Capricorn activates partnerships (marriage, business dealings) and carries the "
     "maraka designation. LP notes Moon is functionally malefic for Capricorn — both "
     "as maraka and through its natural enmity with Saturn (the lagna lord)."),
    # ── AQUARIUS ──────────────────────────────────────────────────────────────
    ("aquarius", "2nd_lord_maraka", "jupiter", [2, 11], False,
     "Jupiter owns H2 (Pisces) and H11 (Sagittarius) for Aquarius lagna — H2 maraka "
     "and H11 upachaya. LP notes Jupiter is problematic for Aquarius despite being a "
     "natural benefic: H2 maraka combined with H11 upachaya (where benefics are weaker) "
     "makes Jupiter primarily a functional malefic. Jupiter dasha activates wealth and "
     "gains (H2+H11) but delivers weaker-than-expected results due to upachaya dynamics, "
     "and carries maraka potential in old age."),
    ("aquarius", "7th_lord_maraka", "sun", [7], False,
     "Sun owns H7 (Leo) for Aquarius lagna — primary maraka through sole 7th house "
     "lordship. LP notes Sun as maraka for Aquarius: the 7th house carries both "
     "partnership themes and death-inflicting potential. Sun dasha for Aquarius "
     "activates public authority, status, and partnership events (Sun's natural qualities "
     "in the H7 context), but carries the maraka designation. Sun is a secondary "
     "functional malefic for Aquarius — less severe than Jupiter but present."),
    # ── PISCES ────────────────────────────────────────────────────────────────
    ("pisces", "2nd_lord_maraka", "mars", [2, 9], False,
     "Mars owns H2 (Aries) and H9 (Scorpio) for Pisces — H2 maraka and H9 trikona. "
     "LP's nuanced Mars for Pisces: the H9 trikona makes Mars primarily a trikona lord "
     "(fortune, father, dharma), with the H2 maraka as a secondary designation. "
     "Mars dasha for Pisces delivers fortune and bold action (H9 trikona) with H2 "
     "wealth activation; the maraka element is secondary and conditional. "
     "Mars is among the better functional planets for Pisces despite H2 maraka."),
    ("pisces", "7th_lord_maraka", "mercury", [4, 7], False,
     "Mercury owns H4 (Gemini) and H7 (Virgo) for Pisces — both kendra houses "
     "(kendradhipati) and H7 is maraka. LP marks Mercury as both kendradhipati AND "
     "maraka for Pisces — paralleling Mercury for Sagittarius. Mercury dasha for Pisces "
     "activates property (H4) and partnerships (H7) but with kendradhipati dosha reducing "
     "Mercury's natural analytical clarity. The H7 maraka adds longevity concern "
     "in old age. Mercury is a functional malefic for Pisces."),
]


def _build_maraka_rules() -> list[RuleRecord]:
    rules = []
    for idx, (lagna, maraka_type, planet, houses, is_double, desc) in enumerate(
        _MARAKA_DATA, start=1
    ):
        rid = f"LPM{idx:03d}"
        tags = ["lpm", "parashari", "laghu_parashari", "maraka", lagna, planet, maraka_type]
        if is_double:
            tags.append("double_maraka")
        primary = {
            "planet": planet,
            "placement_type": "maraka_designation",
            "placement_value": houses,
            "maraka_type": maraka_type,
            "for_lagna": lagna,
        }
        odoms = ["longevity"]
        if 2 in houses:
            odoms.append("wealth")
        if 7 in houses:
            odoms.append("marriage")
        rules.append(RuleRecord(
            rule_id=rid,
            source="LaghuParashari",
            chapter="Ch.6–7",
            school="parashari",
            category="maraka",
            description=f"[LP — {lagna} lagna, {planet} {maraka_type}] {desc}",
            confidence=0.650,
            tags=list(dict.fromkeys(tags)),
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction="unfavorable",
            outcome_intensity="conditional",
            outcome_timing="dasha_dependent",
            lagna_scope=[lagna],
            verse_ref="Ch.6 v.1",
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
    return rules


LAGHU_PARASHARI_MARAKA_REGISTRY = CorpusRegistry()
for _rule in _build_maraka_rules():
    LAGHU_PARASHARI_MARAKA_REGISTRY.add(_rule)
