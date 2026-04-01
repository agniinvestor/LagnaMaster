"""src/corpus/bphs_v2_ch25.py — BPHS Ch.25: Effects of Non-Luminous Planets.

S312: BPHS Phase 1B — Upagraha placements in 12 houses.
7 upagrahas (Dhuma, Vyatipata, Paridhi, Chapa, Dhwaja, Gulika, Pranapada)
× 12 houses = 84 placement rules + 2 concluding principles.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.236-254.
Verse audit: data/verse_audits/ch25_audit.json (101 claims, 87 slokas).

Note: Upagrahas are not in the canonical planet list (T1-3). Conditions use
empty list with signal_group carrying the placement specificity. These are
trait predictions, not rule-firing candidates (upagrahas are not computed
in the current engine). They serve as corpus entries for concordance and
future upagraha module development.
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.25", category="upagraha_effects",
    id_start=2558, session="S312", sloka_count=87,
    chapter_tags=["upagraha", "non_luminous"],
    entity_target="native",
    prediction_type="trait",
    min_ratio=0.85,  # 84 placements from 87 slokas + 2 principles
)


def _upa(upagraha: str, house: int, signal: str, direction: str,
         intensity: str, domains: list[str], claim: str,
         verse_ref: str, desc: str, commentary: str,
         concordance: list[str] | None = None,
         **kwargs) -> None:
    """Helper to add a upagraha-in-house rule with consistent structure."""
    b.add(
        conditions=[],
        signal_group=f"{upagraha}_h{house}_{signal}",
        direction=direction, intensity=intensity,
        domains=domains,
        predictions=[{"entity": "native", "claim": claim,
                       "domain": domains[0], "direction": direction,
                       "magnitude": 0.5 if direction == "mixed" else (0.6 if direction in ("favorable", "unfavorable") else 0.4)}],
        verse_ref=verse_ref,
        description=f"{upagraha.capitalize()} in {house}th house: {desc}",
        commentary_context=commentary,
        concordance_texts=concordance or [],
        **kwargs,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DHUMA IN HOUSES 1-12 (Slokas 2-13, pp.237-239)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("dhuma", 1, "valiant_short_tempered", "mixed", "moderate",
     ["character_temperament"], "valiant_beautiful_eyes_stupefied_unkind_wicked_short_tempered",
     "Ch.25 v.2", "valiant, endowed with beautiful eyes, stupefied in disposition, unkind, wicked and highly short-tempered.",
     "Santhanam: Before declaring results due to placements of non-luminous planets (Dhuma etc.), the student will do well to refer to the sage's instruction in the concluding verses. Consider lordships (or secondary lordships) of these also for each sign. Results mature in the Dasa periods of their dispositors.")

_upa("dhuma", 2, "sickly_wealthy", "mixed", "moderate",
     ["wealth", "physical_health"], "sickly_wealthy_royal_humiliation_dullwitted_eunuch",
     "Ch.25 v.3", "sickly, wealthy, devoid of a limb, will incur humiliation at royal level, be dullwitted and be a eunuch.",
     "Santhanam: No separate note for Dhuma in the 2th house. Mixed result — wealth alongside physical/mental deficiencies.")

_upa("dhuma", 3, "intelligent_bold", "favorable", "moderate",
     ["intelligence_education", "wealth"], "intelligent_bold_delighted_eloquent_wealthy",
     "Ch.25 v.4", "intelligent, very bold, delighted, eloquent, and endowed with men and wealth.",
     "Santhanam: No separate note for Dhuma in the 3th house. Favourable placement for Dhuma.")

_upa("dhuma", 4, "grieved_learned", "mixed", "moderate",
     ["intelligence_education", "marriage"], "grieved_by_female_giving_up_but_learned_all_sastras",
     "Ch.25 v.5", "grieved on account of being given up by his female but will be learned in all sastras.",
     "Santhanam: No separate note for Dhuma in the 4th house. Mixed — scholarly attainment alongside marital distress.")

_upa("dhuma", 5, "limited_progeny", "unfavorable", "moderate",
     ["progeny", "wealth"], "limited_progeny_devoid_wealth_eat_anything_bereft_friends_mantras",
     "Ch.25 v.6", "limited progeny, devoid of wealth, be great, will eat anything and be bereft of friends and Mantras.",
     "Santhanam: No separate note for Dhuma in the 5th house. The 5th house placement of Dhuma denies children and wealth.")

_upa("dhuma", 6, "conquer_enemies", "favorable", "strong",
     ["enemies_litigation", "physical_health"], "strong_conquer_enemies_brilliant_famous_free_diseases",
     "Ch.25 v.7", "strong, will conquer his enemies, be very brilliant, famous and free from diseases.",
     "Santhanam: No separate note for Dhuma in the 6th house. Favourable — Dhuma in an upachaya house.")

_upa("dhuma", 7, "penniless_sensuous", "unfavorable", "moderate",
     ["wealth", "character_temperament"], "penniless_sensuous_others_females_devoid_brilliance",
     "Ch.25 v.8", "penniless, be ever sensuous, skilful in going to others' females and be always devoid of brilliance.",
     "Santhanam: No separate note for Dhuma in the 7th house. Unfavourable for wealth and character.")

_upa("dhuma", 8, "bereft_courage", "mixed", "moderate",
     ["character_temperament"], "bereft_courage_enthusiastic_truthful_disagreeable_selfish",
     "Ch.25 v.9", "bereft of courage but be enthusiastic, be truthful, disagreeable, hard-hearted and selfish.",
     "Santhanam: No separate note for Dhuma in the 8th house. Mixed traits — truthful but selfish.")

_upa("dhuma", 9, "sons_fortunes", "favorable", "strong",
     ["wealth", "spirituality"], "sons_fortunes_rich_honourable_kind_religious_disposed_relatives",
     "Ch.25 v.10", "endowed with sons and fortunes, be rich, honourable, kind, religious and well disposed to his relatives.",
     "Santhanam: No separate note for Dhuma in the 9th house. Highly favourable — the 9th house enhances Dhuma's positive traits.")

_upa("dhuma", 10, "sons_intelligent", "favorable", "moderate",
     ["wealth", "intelligence_education"], "sons_fortunes_delighted_intelligent_happy_truthful",
     "Ch.25 v.11", "endowed with sons and fortunes, be delighted, intelligent, happy and truthful.",
     "Santhanam: No separate note for Dhuma in the 10th house. Favourable placement.")

_upa("dhuma", 11, "wealth_arts", "favorable", "moderate",
     ["wealth", "fame_reputation"], "wealth_grains_gold_beautiful_arts_modest_singing",
     "Ch.25 v.12", "endowed with wealth, grains and gold, be beautiful, will have knowledge of arts, be modest and be skilful in singing.",
     "Santhanam: No separate note for Dhuma in the 11th house. Favourable — 11th is gains house.")

_upa("dhuma", 12, "morally_fallen", "unfavorable", "strong",
     ["character_temperament"], "morally_fallen_sinful_others_wives_vices_unkind_crafty",
     "Ch.25 v.13", "morally fallen, will indulge in sinful acts, be interested in others' wives, addicted to vices, unkind and crafty.",
     "Santhanam: No separate note for Dhuma in the 12th house. Strongly unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# VYATIPATA IN HOUSES 1-12 (Slokas 14-25, pp.239-241)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("vyatipata", 1, "troubled_miseries", "unfavorable", "moderate",
     ["character_temperament"], "troubled_miseries_cruel_destructive_foolish_ill_disposed_relatives",
     "Ch.25 v.14", "troubled by miseries, be cruel, will indulge in destructive acts, be foolish and will be ill-disposed to his relatives.",
     "Santhanam: No separate note for Vyatipata in the 1th house. Vyatipata (also known as Pata) in ascendant brings misery.")

_upa("vyatipata", 2, "morally_crooked", "unfavorable", "moderate",
     ["character_temperament"], "morally_crooked_bilious_enjoy_pleasures_unkind_grateful_wicked",
     "Ch.25 v.15", "morally crooked, be bilious, will enjoy pleasures, be unkind but grateful, wicked and sinful.",
     "Santhanam: No separate note for Vyatipata in the 2th house. Mixed moral character.")

_upa("vyatipata", 3, "warrior_rich", "favorable", "strong",
     ["career_status", "wealth"], "firm_disposition_warrior_liberal_very_rich_dear_king_head_army",
     "Ch.25 v.16", "firm in disposition, be a warrior, be liberal, very rich, dear to king, and be head of an army.",
     "Santhanam: No separate note for Vyatipata in the 3th house. Strongly favourable in the 3rd (valour house).")

_upa("vyatipata", 4, "relatives_not_sons", "mixed", "moderate",
     ["progeny"], "endowed_relatives_but_not_sons_and_fortunes",
     "Ch.25 v.17", "endowed with relatives etc. but not sons and fortunes.",
     "Santhanam: No separate note for Vyatipata in the 4th house. Relatives present but progeny/fortune denied.")

_upa("vyatipata", 5, "poor_charming", "unfavorable", "moderate",
     ["wealth", "physical_health"], "poor_charming_imbalances_phlegm_bile_wind_hard_hearted_shameless",
     "Ch.25 v.18", "poor, be charming in appearance, will have imbalances of phlegm, bile and wind, be hard-hearted and shameless.",
     "Santhanam: No separate note for Vyatipata in the 5th house. Unfavourable for health and wealth in the 5th.")

_upa("vyatipata", 6, "overcome_enemies", "favorable", "strong",
     ["enemies_litigation"], "overcome_enemies_physically_mighty_skilful_weapons_arts_peaceful",
     "Ch.25 v.19", "overcome his enemies, be physically mighty, skilful in use of all kinds of weapons and in arts, and be peaceful in disposition.",
     "Santhanam: No separate note for Vyatipata in the 6th house. Favourable — enemies vanquished, martial skills.")

_upa("vyatipata", 7, "bereft_wealth", "unfavorable", "strong",
     ["wealth", "marriage"], "bereft_wealth_wife_sons_subdue_females_miserable_sensuous_shameless",
     "Ch.25 v.20", "bereft of wealth, wife and sons, will subdue to females, be miserable, sensuous, shameless and friendly to others.",
     "Santhanam: No separate note for Vyatipata in the 7th house. Strongly unfavourable in the 7th.")

_upa("vyatipata", 8, "deformity_eyes", "unfavorable", "strong",
     ["physical_health"], "deformity_eyes_ugly_unfortunate_spiteful_brahmins_blood_disorders",
     "Ch.25 v.21", "have deformity of eyes, be ugly, unfortunate, spiteful to Brahmins and be troubled by disorders of blood.",
     "Santhanam: No separate note for Vyatipata in the 8th house. Strongly unfavourable for health.")

_upa("vyatipata", 9, "many_friends", "favorable", "moderate",
     ["wealth", "marriage"], "many_business_friends_very_learned_well_disposed_wife_eloquent",
     "Ch.25 v.22", "have many kinds of business and many friends, be very learned, well-disposed to his wife and be eloquent.",
     "Santhanam: No separate note for Vyatipata in the 9th house. Favourable placement.")

_upa("vyatipata", 10, "rich_religious", "favorable", "strong",
     ["career_status", "spirituality"], "rich_religious_peaceful_skilful_religious_acts_learned_farsighted",
     "Ch.25 v.23", "rich, religious, peaceful, skilful in religious acts, very learned and farsighted.",
     "Santhanam: No separate note for Vyatipata in the 10th house. Strongly favourable in the 10th.")

_upa("vyatipata", 11, "extremely_opulent", "favorable", "strong",
     ["wealth"], "extremely_opulent_honourable_truthful_firm_policy_many_horses_singing",
     "Ch.25 v.24", "extremely opulent, honourable, truthful, firm in policy, endowed with many horses and be interested in singing.",
     "Santhanam: No separate note for Vyatipata in the 11th house. Very favourable in the 11th (gains house).")

_upa("vyatipata", 12, "anger_disabled", "unfavorable", "moderate",
     ["character_temperament"], "anger_many_activities_disabled_irreligious_hate_own_relatives",
     "Ch.25 v.25", "given to anger, associated with many activities, disabled, irreligious and will hate his own relatives.",
     "Santhanam: No separate note for Vyatipata in the 12th house. Unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# PARIDHI IN HOUSES 1-12 (Slokas 26-37, pp.241-243)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("paridhi", 1, "learned_peaceful", "favorable", "strong",
     ["intelligence_education", "character_temperament"], "learned_truthful_peaceful_rich_sons_pure_charitable_dear_elders",
     "Ch.25 v.26", "learned, truthful, peaceful, rich, endowed with sons, pure, charitable and dear to elders.",
     "Santhanam: No separate note for Paridhi in the 1th house. Highly favourable — Paridhi (or Parivesha) in ascendant.")

_upa("paridhi", 2, "wealthy_religious", "favorable", "moderate",
     ["wealth", "spirituality"], "wealthy_charming_happy_very_religious_be_a_lord",
     "Ch.25 v.27", "wealthy, charming, will enjoy pleasures, be happy, very religious and be a lord.",
     "Santhanam: No separate note for Paridhi in the 2th house. Favourable placement.")

_upa("paridhi", 3, "fond_wife_pious", "favorable", "moderate",
     ["marriage", "character_temperament"], "fond_wife_charming_pious_well_disposed_men_servant_respectful",
     "Ch.25 v.28", "very charming, fond of his wife, pious, well disposed to his men, be a servant and be respectful of his elders.",
     "Santhanam: No separate note for Paridhi in the 3th house. Generally favourable with a note of servitude.")

_upa("paridhi", 4, "wonderstruck_kind", "favorable", "moderate",
     ["character_temperament"], "wonderstruck_helpful_enemies_kind_endowed_everything_singing",
     "Ch.25 v.29", "wonderstruck, helpful to enemies as well, kind, endowed with everything and be skilful in singing.",
     "Santhanam: No separate note for Paridhi in the 4th house. Favourable placement.")

_upa("paridhi", 5, "affluent_virtuous", "favorable", "strong",
     ["wealth", "spirituality"], "affluent_virtuous_splendorous_affectionate_religious_dear_wife",
     "Ch.25 v.30", "affluent, virtuous, splendorous, affectionate, religious and dear to his wife.",
     "Santhanam: No separate note for Paridhi in the 5th house. Strongly favourable.")

_upa("paridhi", 6, "famous_conquer", "favorable", "strong",
     ["fame_reputation", "enemies_litigation"], "famous_wealthy_sons_pleasures_helpful_all_conquer_enemies",
     "Ch.25 v.31", "famous and wealthy, be endowed with sons and pleasures, be helpful to all and will conquer his enemies.",
     "Santhanam: No separate note for Paridhi in the 6th house. Favourable in the 6th.")

_upa("paridhi", 7, "limited_children", "unfavorable", "moderate",
     ["progeny", "marriage"], "limited_children_devoid_happiness_mediocre_intelligence_sickly_wife",
     "Ch.25 v.32", "have a limited number of children, be devoid of happiness, be of mediocre intelligence, very hard-hearted, and have a sickly wife.",
     "Santhanam: No separate note for Paridhi in the 7th house. Unfavourable for progeny and marriage.")

_upa("paridhi", 8, "spiritually_disposed", "favorable", "moderate",
     ["spirituality"], "spiritually_disposed_peaceful_strong_bodied_firm_decision_religious_gentle",
     "Ch.25 v.33", "spiritually disposed, peaceful, strong-bodied, firm in decision, religious and gentle.",
     "Santhanam: No separate note for Paridhi in the 8th house. Unusually favourable for the 8th house — spiritual dimension activated.")

_upa("paridhi", 9, "happy_brilliant", "favorable", "strong",
     ["wealth"], "happy_brilliant_affluent_sons_devoid_excessive_passion_honourable",
     "Ch.25 v.34", "happy, brilliant, affluent, endowed with sons, devoid of excessive passion, be honourable.",
     "Santhanam: No separate note for Paridhi in the 9th house. Highly favourable in the 9th.")

_upa("paridhi", 10, "versed_arts", "favorable", "moderate",
     ["career_status", "intelligence_education"], "versed_arts_enjoy_pleasures_strong_bodied_learned_all_sastras",
     "Ch.25 v.35", "versed in arts, will enjoy pleasures, be strong-bodied, and be learned in all sastras.",
     "Santhanam: No separate note for Paridhi in the 10th house. Favourable for career and learning.")

_upa("paridhi", 11, "pleasures_women", "mixed", "moderate",
     ["character_temperament", "physical_health"], "pleasures_through_women_virtuous_intelligent_digestive_fire_disorders",
     "Ch.25 v.36", "enjoy pleasures through women, be virtuous, intelligent, dear to his people and will suffer disorders of digestive fire.",
     "Santhanam: No separate note for Paridhi in the 11th house. Mixed — favourable traits alongside health issue.")

_upa("paridhi", 12, "spendthrift_firm", "unfavorable", "moderate",
     ["wealth"], "spendthrift_miserable_firm_dishonour_elders",
     "Ch.25 v.37", "always be a spendthrift, be miserable, firm and will dishonour elders.",
     "Santhanam: No separate note for Paridhi in the 12th house. Unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPA (INDRA DHANUS) IN HOUSES 1-12 (Slokas 38-49, pp.243-245)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("chapa", 1, "wealth_grains", "favorable", "moderate",
     ["wealth"], "wealth_grains_gold_grateful_agreeable_devoid_afflictions",
     "Ch.25 v.38", "endowed with wealth, grains and gold, be grateful, agreeable and devoid of all afflictions.",
     "Santhanam: No separate note for Chapa in the 1th house. Favourable placement.")

_upa("chapa", 2, "speak_affably", "favorable", "moderate",
     ["wealth", "intelligence_education"], "speak_affably_very_rich_modest_learned_charming_religious",
     "Ch.25 v.39", "speak affably, be very rich, modest, learned, charming and religious.",
     "Santhanam: No separate note for Chapa in the 2th house. Favourable placement.")

_upa("chapa", 3, "miser_thieving", "unfavorable", "moderate",
     ["character_temperament"], "miser_versed_many_arts_thieving_devoid_limb_unfriendly",
     "Ch.25 v.40", "a miser, versed in many arts, will indulge in thieving, be devoid of some limb and be unfriendly.",
     "Santhanam: No separate note for Chapa in the 3th house. Unfavourable despite arts skill.")

_upa("chapa", 4, "happy_honoured", "favorable", "moderate",
     ["property_vehicles", "physical_health"], "happy_quadrupeds_wealth_grains_honoured_king_devoid_sickness",
     "Ch.25 v.41", "happy, endowed with quadrupeds, wealth, grains etc., be honoured by the king and be devoid of sickness.",
     "Santhanam: No separate note for Chapa in the 4th house. Favourable placement.")

_upa("chapa", 5, "splendorous_pious", "favorable", "moderate",
     ["character_temperament"], "splendorous_farsighted_pious_affable_prosperity_all_undertakings",
     "Ch.25 v.42", "splendorous, pious, affable and will acquire prosperity in all his undertakings.",
     "Santhanam: No separate note for Chapa in the 5th house. Favourable placement.")

_upa("chapa", 6, "overcome_enemies_pure", "favorable", "strong",
     ["enemies_litigation"], "overcome_enemies_happy_affectionate_pure_plentifulness_undertakings",
     "Ch.25 v.43", "overcome his enemies, be happy, affectionate, pure and will achieve plentifulness in all his undertakings.",
     "Santhanam: No separate note for Chapa in the 6th house. Strongly favourable in the 6th.")

_upa("chapa", 7, "wealthy_virtues", "favorable", "moderate",
     ["wealth"], "wealthy_all_virtues_learned_sastras_religious_agreeable",
     "Ch.25 v.44", "wealthy, endowed with all virtues, learned in sastras, religious, and agreeable.",
     "Santhanam: No separate note for Chapa in the 7th house. Favourable placement.")

_upa("chapa", 8, "others_jobs_cruel", "unfavorable", "moderate",
     ["character_temperament"], "interested_others_jobs_cruel_others_wives_defective_limbed",
     "Ch.25 v.45", "interested in other's jobs, be cruel, interested in other's wives and be defective limbed.",
     "Santhanam: No separate note for Chapa in the 8th house. Unfavourable in the 8th.")

_upa("chapa", 9, "penance_famous", "favorable", "strong",
     ["spirituality", "fame_reputation"], "penance_religious_observations_highly_learned_famous",
     "Ch.25 v.46", "will perform penance, will take to religious observations, be highly learned, and be famous among men.",
     "Santhanam: No separate note for Chapa in the 9th house. Strongly favourable in the 9th.")

_upa("chapa", 10, "many_sons_wealth", "favorable", "strong",
     ["wealth", "progeny"], "many_sons_abundant_wealth_cows_buffaloes_famous",
     "Ch.25 v.47", "endowed with many sons, abundant wealth, cows, buffaloes etc. and will be famous among men.",
     "Santhanam: No separate note for Chapa in the 10th house. Strongly favourable in the 10th.")

_upa("chapa", 11, "gainful_mantras", "favorable", "strong",
     ["wealth", "physical_health"], "gainful_free_diseases_fiery_disposition_affectionate_wife_mantras_weapons",
     "Ch.25 v.48", "gainful, free from diseases, very fiery in disposition, affectionate to his wife and will have knowledge of mantras and weapons.",
     "Santhanam: No separate note for Chapa in the 11th house. Favourable in the 11th.")

_upa("chapa", 12, "wicked_poor", "unfavorable", "strong",
     ["character_temperament"], "wicked_honourable_evil_disposition_shameless_others_females_poor",
     "Ch.25 v.49", "wicked, very honourable, evil in disposition, shameless, will go to other's females and be ever poor.",
     "Santhanam: No separate note for Chapa in the 12th house. Strongly unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# DHWAJA (SIKHI/UPAKETU) IN HOUSES 1-12 (Slokas 50-61, pp.245-247)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("dhwaja", 1, "skilful_learning", "favorable", "moderate",
     ["intelligence_education"], "skilful_all_learning_happy_efficient_speech_agreeable_affectionate",
     "Ch.25 v.50", "skilful in all branches of learning, be happy, efficient in speech, agreeable and very affectionate.",
     "Santhanam: No separate note for Dhwaja in the 1th house. Favourable placement for Dhwaja (also called Sikhi or Upaketu).")

_upa("dhwaja", 2, "good_speaker_poetry", "favorable", "moderate",
     ["intelligence_education", "fame_reputation"], "good_speaker_splendorous_write_poetry_scholarly_conveyances",
     "Ch.25 v.51", "a good and affable speaker, be splendorous, will write poetry, be scholarly, honourable, modest and endowed with conveyances.",
     "Santhanam: No separate note for Dhwaja in the 2th house. Favourable for speech and creative writing.")

_upa("dhwaja", 3, "miserly_poor", "unfavorable", "moderate",
     ["wealth", "physical_health"], "miserly_cruel_acts_thin_bodied_poor_severe_diseases",
     "Ch.25 v.52", "miserly, cruel in acts, thin-bodied, poor and will incur severe diseases.",
     "Santhanam: No separate note for Dhwaja in the 3th house. Unfavourable placement.")

_upa("dhwaja", 4, "charming_vedas", "favorable", "moderate",
     ["character_temperament", "spirituality"], "charming_very_virtuous_gentle_interested_vedas_always_happy",
     "Ch.25 v.53", "charming, very virtuous, gentle, interested in Vedas and be always happy.",
     "Santhanam: No separate note for Dhwaja in the 4th house. Favourable placement.")

_upa("dhwaja", 5, "happy_pleasures", "favorable", "moderate",
     ["intelligence_education"], "happy_enjoy_pleasures_versed_arts_skilled_expedients_intelligent_eloquent",
     "Ch.25 v.54", "happy, will enjoy pleasures, be versed in arts, skilled in expedients, intelligent, eloquent and will respect elders.",
     "Santhanam: No separate note for Dhwaja in the 5th house. Favourable in the 5th.")

_upa("dhwaja", 6, "win_enemies_valiant", "favorable", "moderate",
     ["enemies_litigation"], "ominous_maternal_relatives_win_enemies_many_relatives_valiant_skilful",
     "Ch.25 v.55", "be ominous for maternal relatives, will win over his enemies, be endowed with many relatives, valiant, splendorous and skilful.",
     "Santhanam: No separate note for Dhwaja in the 6th house. Favourable for overcoming enemies, though maternal relatives suffer.")

_upa("dhwaja", 7, "gambling_sensuous", "unfavorable", "moderate",
     ["character_temperament"], "interested_gambling_sensuous_enjoy_pleasures_befriend_prostitutes",
     "Ch.25 v.56", "interested in gambling, be sensuous, will enjoy pleasures and will befriend prostitutes.",
     "Santhanam: No separate note for Dhwaja in the 7th house. Unfavourable morally.")

_upa("dhwaja", 8, "sinful_shameless", "unfavorable", "moderate",
     ["character_temperament", "marriage"], "base_acts_sinful_shameless_blame_others_lack_marital_happiness",
     "Ch.25 v.57", "interested in base acts, be sinful, shameless, will blame others, lack in marital bliss and will take others' side.",
     "Santhanam: No separate note for Dhwaja in the 8th house. Unfavourable in the 8th.")

_upa("dhwaja", 9, "religious_helpful", "favorable", "moderate",
     ["spirituality"], "wear_religious_badges_delighted_helpful_all_skilled_religious_deeds",
     "Ch.25 v.58", "wear (religious) badges, be delighted, helpfully disposed to all and be skilled in religious deeds.",
     "Santhanam: No separate note for Dhwaja in the 9th house. Favourable in the 9th.")

_upa("dhwaja", 10, "happiness_fortunes", "favorable", "moderate",
     ["wealth", "spirituality"], "happiness_fortunes_fond_females_charitable_befriend_brahmins",
     "Ch.25 v.59", "endowed with happiness and fortunes, be fond of females, be charitable and will befriend Brahmins.",
     "Santhanam: No separate note for Dhwaja in the 10th house. Favourable placement.")

_upa("dhwaja", 11, "ever_acquire_gains", "favorable", "strong",
     ["wealth", "spirituality"], "ever_acquire_gains_very_religious_honourable_affluent_valiant_sacrificial",
     "Ch.25 v.60", "ever acquire gains, be very religious, honourable, affluent, fortunate, valiant and skilled in sacrificial rites.",
     "Santhanam: No separate note for Dhwaja in the 11th house. Strongly favourable in the 11th.")

_upa("dhwaja", 12, "sinful_untrustworthy", "unfavorable", "moderate",
     ["character_temperament"], "sinful_acts_valiant_untrustworthy_unkind_others_females_short_tempered",
     "Ch.25 v.61", "interested in sinful acts, be valiant, untrustworthy, unkind, interested in others' females and be short-tempered.",
     "Santhanam: No separate note for Dhwaja in the 12th house. Unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# GULIKA IN HOUSES 1-12 (Slokas 62-73, pp.247-251)
# Extensive Santhanam notes — most significant upagraha.
# ═══════════════════════════════════════════════════════════════════════════════

_upa("gulika", 1, "afflicted_diseases", "unfavorable", "strong",
     ["physical_health", "character_temperament"], "afflicted_diseases_lustful_sinful_crafty_wicked_miserable",
     "Ch.25 v.62", "afflicted by diseases, be lustful, sinful, crafty, wicked and very miserable.",
     "Santhanam: Out of all the non-luminous planets, Gulika deserves a special consideration in natal horoscopy as well as horary astrology. This is also a very important factor in birth time rectification. If Gulika is in the ascendant, the native will incur severe defects of eyes. He will take to bad acts like thieving. He will disregard religion, be deprived of progeny and his longevity will incur a severe cut. He will not have a good house to live in. His last days will be miserable and death will be painful after a long confinement.",
     modifiers=[{"condition": "severe_eye_defects_thieving_disregard_religion_longevity_cut", "effect": "amplifies", "strength": "strong"}])

_upa("gulika", 2, "unsightly_penniless", "unfavorable", "strong",
     ["wealth", "character_temperament"], "unsightly_miserable_given_vices_shameless_penniless",
     "Ch.25 v.63", "unsightly in appearance, miserable, given to vices, shameless and penniless.",
     "Santhanam: Should Gulika be in the 2nd house, the native will further be unfortunate. His learning will be obstructed off and on. He will have speech defects, be harsh in speech, will not have family happiness, be untruthful, will involve in a scandal, be unfit to move among others and will in the Dasa periods of the 2nd lord face troubles equal to death.")

_upa("gulika", 3, "charming_head_village", "favorable", "moderate",
     ["fame_reputation"], "charming_head_village_fond_virtuous_men_honoured_by_king",
     "Ch.25 v.64", "charming in appearance, will head a village, be fond of virtuous men, and be honoured by the king.",
     "Santhanam: With Gulika in the 3rd house, one will face destruction of co-born. Though fairly rich, he will feel distressed.")

_upa("gulika", 4, "sickly_sinful", "unfavorable", "strong",
     ["physical_health"], "sickly_devoid_happiness_sinful_afflicted_windy_bilious_excesses",
     "Ch.25 v.65", "sickly, devoid of happiness, sinful and afflicted due to windy and bilious excesses.",
     "Santhanam: The native will not befriend anybody but be inimical to others inclusive of his relatives. He will be devoid of conveyances or will face risks through conveyances.")

_upa("gulika", 5, "not_praiseworthy", "unfavorable", "strong",
     ["progeny", "longevity"], "not_praiseworthy_poor_short_lived_spiteful_mean_eunuch_subdued_wife",
     "Ch.25 v.66", "not praiseworthy, be poor, short-lived, spiteful, mean, be a eunuch, subdued by his wife and be a heterodox.",
     "Santhanam: The native's virility or progenic ability will be significantly affected by Gulika's occupying the house of progeny. He will not be in a position to obtain issues unless Jupiter and the 5th lord are favourable. Gulika in this house will make one devoid of God-fearing tendency and be at the disposal of his wife. His personal disposition will not be agreeable.",
     exceptions=["unless_jupiter_and_5th_lord_favourable_then_issues_possible"])

_upa("gulika", 6, "devoid_enemies", "favorable", "moderate",
     ["enemies_litigation"], "devoid_enemies_strong_bodied_spleenorous_liked_wife_enthusiastic_helpful",
     "Ch.25 v.67", "devoid of enemies, be strong-bodied, spleenorous, liked by his wife, enthusiastic, very friendly and helpful in disposition.",
     "Santhanam: When Gulika is in the 6th house, the native will be interested in controlling evil spirits and make a livelihood from such achievements. He will obtain children. He will be very courageous. There will be freedom from diseases if the 6th house containing Gulika is a benefic sign.",
     modifiers=[{"condition": "freedom_from_diseases_if_6th_house_is_benefic_sign", "effect": "conditionalizes", "strength": "moderate"}])

_upa("gulika", 7, "subdue_spouse", "unfavorable", "strong",
     ["marriage"], "subdue_spouse_sinful_others_females_emaciated_devoid_friendship_wife_wealth",
     "Ch.25 v.68", "subdue to his spouse, be sinful, will go to others' females, be emaciated, devoid of friendship and will live on wife's (or a female's) wealth.",
     "Santhanam: Gulika occupying the 7th house, will make the native thrive on a female's wealth or through the contributions of his own spouse. His conjugal life will not cause him any happiness. He will possibly have more than one marriage. His knowledge will not be quite much. In relation to public dealings, he will incur misunderstandings and enmity.")

_upa("gulika", 8, "troubled_hunger", "unfavorable", "strong",
     ["wealth", "physical_health"], "troubled_hunger_miserable_cruel_short_tempered_unkind_poor",
     "Ch.25 v.69", "troubled by hunger, be miserable, cruel, very much short-tempered, very unkind, poor and bereft of good qualities.",
     "Santhanam: The native will find it difficult to get even a square meal. His face will be ugly. His eyes will be diseased. His teeth will be yellowish. He will be quite short in stature. These are additional effects as due to the 8th house position of Gulika, son of Saturn.")

_upa("gulika", 9, "undergo_ordeals", "unfavorable", "strong",
     ["character_temperament"], "undergo_ordeals_emaciated_evil_acts_very_unkind_sluggish_talebearer",
     "Ch.25 v.70", "undergo many ordeals, be emaciated, will perform evil acts, be very unkind, sluggish and be a tale-bearer.",
     "Santhanam: If Gulika is in the 9th house one will be devoid of paternal bliss and good fortunes. His father will pass away in the native's childhood itself. None of the native's undertakings will bear fruits.",
     modifiers=[{"condition": "devoid_paternal_bliss_father_passes_childhood_no_undertakings_bear_fruit", "effect": "amplifies", "strength": "strong"}])

_upa("gulika", 10, "endowed_sons_happy", "favorable", "moderate",
     ["progeny", "spirituality"], "endowed_sons_happy_enjoy_many_things_worship_gods_fire_meditation",
     "Ch.25 v.71", "endowed with sons, be happy, will enjoy many things, be fond of worshipping gods and fire and will practise meditation and religion.",
     "Santhanam: The placement of Gulika in the 10th house will prove favourable for Yoga, Meditation and such other achievements. The native, at one stage, will turn into a heterodox and discard his religious code.")

_upa("gulika", 11, "enjoy_women_leader", "mixed", "moderate",
     ["wealth", "fame_reputation"], "enjoy_women_class_leader_men_helpful_relatives_short_emperor",
     "Ch.25 v.72", "enjoy women of class, be a leader of men, be helpful to his relatives, be short in stature and be an emperor.",
     "Santhanam: If Gulika is in the 11th house, the subject will be in the company of many females. He will be devoid of good character. He will enjoy progenic happiness, wealth status etc. and be charming in appearance.",
     modifiers=[{"condition": "company_many_females_devoid_good_character_but_progenic_happiness", "effect": "conditionalizes", "strength": "moderate"}])

_upa("gulika", 12, "base_deeds_sinful", "unfavorable", "strong",
     ["character_temperament"], "indulge_base_deeds_sinful_defective_limbed_unfortunate_indolent_mean_people",
     "Ch.25 v.73", "indulge in base deeds, be sinful, defective-limbed, unfortunate, indolent, and will join mean people.",
     "Santhanam: Gulika's tenancy in the 12th house at birth will bring innumerable misfortunes and cause loss of wealth on evil missions. One will, however, enjoy progenic happiness.",
     modifiers=[{"condition": "innumerable_misfortunes_loss_wealth_but_enjoy_progenic_happiness", "effect": "conditionalizes", "strength": "moderate"}])


# ═══════════════════════════════════════════════════════════════════════════════
# PRANAPADA IN HOUSES 1-12 (Slokas 74-85, pp.251-253)
# ═══════════════════════════════════════════════════════════════════════════════

_upa("pranapada", 1, "weak_sickly", "unfavorable", "strong",
     ["physical_health"], "weak_sickly_dullwitted_defective_limbed_miserable_emaciated",
     "Ch.25 v.74", "weak, sickly, dumb, lunatic, defective-limbed, miserable and emaciated.",
     "Santhanam: Pranapada is a special ascendant. How to calculate this special sensitive point could be found on p. 47 supra. Pranapada will fall in a certain degree and its relation with reference to natal ascendant will portend many an event as tersely shown in the present 12 verses.")

_upa("pranapada", 2, "abundant_grains", "favorable", "strong",
     ["wealth"], "abundant_grains_wealth_children_attendants_fortunate",
     "Ch.25 v.75", "endowed with abundant grains (rice, wheat etc.), abundant wealth, abundant children, abundant attendants, and be fortunate.",
     "Santhanam: No separate note for Pranapada in the 2th house. Strongly favourable in the 2nd.")

_upa("pranapada", 3, "injurious_proud", "unfavorable", "moderate",
     ["character_temperament"], "injurious_mischievous_proud_hard_hearted_dirty_no_respect_elders",
     "Ch.25 v.76", "injurious (or mischievous), proud, hard-hearted, very dirty and be devoid of respect for elders.",
     "Santhanam: No separate note for Pranapada in the 3th house. Unfavourable placement.")

_upa("pranapada", 4, "happy_truthful", "favorable", "moderate",
     ["character_temperament"], "happy_attached_females_elders_soft_truthful",
     "Ch.25 v.77", "happy, friendly, attached to females and elders, soft and truthful.",
     "Santhanam: No separate note for Pranapada in the 4th house. Favourable placement.")

_upa("pranapada", 5, "good_acts_kind", "favorable", "moderate",
     ["character_temperament"], "happy_do_good_acts_kind_very_affectionate",
     "Ch.25 v.78", "happy, will do good acts, be kind and very affectionate.",
     "Santhanam: No separate note for Pranapada in the 5th house. Favourable placement.")

_upa("pranapada", 6, "subdued_sickly", "unfavorable", "moderate",
     ["physical_health", "longevity"], "subdued_relatives_enemies_sharp_defective_digestive_fire_sickly_shortlived",
     "Ch.25 v.79", "subdued by his relatives and enemies, be sharp, will have defective digestive fire, be wicked, sickly, affluent and shortlived.",
     "Santhanam: No separate note for Pranapada in the 6th house. Unfavourable for health and longevity.")

_upa("pranapada", 7, "green_eyed_fierce", "unfavorable", "moderate",
     ["character_temperament"], "green_eyed_ever_libidinous_fierce_appearance_not_worth_respect",
     "Ch.25 v.80", "green-eyed, ever libidinous, fierce in appearance, and not worth respect and be ill-disposed.",
     "Santhanam: No separate note for Pranapada in the 7th house. Unfavourable placement.")

_upa("pranapada", 8, "afflicted_diseases_misery", "unfavorable", "strong",
     ["physical_health"], "afflicted_diseases_troubled_incur_misery_king_relatives_servants_sons",
     "Ch.25 v.81", "afflicted by diseases, be troubled and will incur misery on account of the king, relatives, servants and sons.",
     "Santhanam: No separate note for Pranapada in the 8th house. Strongly unfavourable in the 8th.")

_upa("pranapada", 9, "endowed_sons_rich", "favorable", "strong",
     ["wealth", "progeny"], "endowed_sons_very_rich_fortunate_charming_serve_others_skilful",
     "Ch.25 v.82", "endowed with sons, be very rich, fortunate, charming, will serve others and not be wicked but be skilful.",
     "Santhanam: No separate note for Pranapada in the 9th house. Strongly favourable in the 9th.")

_upa("pranapada", 10, "heroic_intelligent", "favorable", "strong",
     ["career_status"], "heroic_intelligent_skilful_expert_royal_orders_worship_gods",
     "Ch.25 v.83", "heroic, intelligent, skilful, be an expert in carrying out royal orders, and will worship gods.",
     "Santhanam: No separate note for Pranapada in the 10th house. Strongly favourable in the 10th.")

_upa("pranapada", 11, "famous_learned", "favorable", "strong",
     ["fame_reputation", "wealth"], "famous_virtuous_learned_wealthy_fair_complexioned_attached_mother",
     "Ch.25 v.84", "famous, virtuous, learned, wealthy, fair-complexioned and attached to mother.",
     "Santhanam: No separate note for Pranapada in the 11th house. Strongly favourable in the 11th.")

_upa("pranapada", 12, "mean_defective", "unfavorable", "strong",
     ["physical_health"], "mean_wicked_defective_limbed_hate_brahmins_relatives_eye_diseases",
     "Ch.25 v.85", "mean, wicked, defective-limbed, will hate Brahmins and relatives, will suffer eye diseases or be one-eyed.",
     "Santhanam: No separate note for Pranapada in the 12th house. Strongly unfavourable in the 12th.")


# ═══════════════════════════════════════════════════════════════════════════════
# CONCLUDING PRINCIPLES (Slokas 86-87, pp.253-254)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[],
    signal_group="upagraha_dispositor_strength_principle",
    direction="neutral", intensity="conditional",
    domains=["wealth"],
    predictions=[{"entity": "general", "claim": "upagraha_results_modified_by_dispositor_strength_and_aspects",
                   "domain": "wealth", "direction": "neutral", "magnitude": 0.5}],
    entity_target="general",
    verse_ref="Ch.25 v.86-87",
    description="Before declaring results for Dhooma, Gulika etc., consider the Sun and other planets' effects, strength, relations and aspects. Check dispositors of upagrahas.",
    commentary_context="Santhanam: We are advised to look upto the Sun and others while declaring the effects due to Dhooma, Gulika etc. So to say the dispositors of Dhooma etc. Should be scrutinized to know the extent of effects. For example if Gulika is due to give bad effects, but his dispositor is well-placed, well-aspected or well-related, the evils are minimised. We should balance the results of Dhooma etc. with the results due to the planets from Sun to Saturn (and of course the nodes).",
    prediction_type="trait",
    modifiers=[{"condition": "dispositor_well_placed_aspected_minimises_evils_weak_dispositor_blocks_good", "effect": "conditionalizes", "strength": "strong"}],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH25_REGISTRY = b.build()
