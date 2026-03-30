"""src/corpus/saravali_signs_8.py — S288: Saravali Rahu + Ketu in 12 Signs (Ch.32-33).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_RAHU_ARIES_DATA = [
    ("rahu", "sign_placement", "aries", {}, "mixed", "moderate", ['career_status', 'character_temperament'], ['rahu', 'saravali', 'sign_placement', 'aries'], "Ch.32 v.1", "Rahu in Aries: obsessive ambition, unconventional leadership, desire for recognition at any cost"),
    ("rahu", "sign_placement", "aries", {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'aries'], "Ch.32 v.2", "Rahu in Aries: head injuries, mysterious headaches, nervous system overstimulation"),
    ("rahu", "sign_placement", "aries", {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'aries'], "Ch.32 v.3", "Rahu in Aries: gains through bold ventures, foreign enterprises, unconventional business"),
    ("rahu", "sign_placement", "aries", {}, "unfavorable", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'aries'], "Ch.32 v.4", "Rahu in Aries: deceptive relationships, unconventional partner, sudden attractions and separations"),
    ("rahu", "sign_placement", "aries", {}, "mixed", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'sign_placement', 'aries'], "Ch.32 v.5", "Rahu in Aries: sudden fame or notoriety, controversial public image, unconventional reputation"),
]

_RAHU_TAURUS_DATA = [
    ("rahu", "sign_placement", "taurus", {}, "favorable", "strong", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'taurus'], "Ch.32 v.6", "Rahu exalted in Taurus: obsessive wealth accumulation, gains through foreign luxury goods, material success"),
    ("rahu", "sign_placement", "taurus", {}, "favorable", "moderate", ['physical_appearance'], ['rahu', 'saravali', 'sign_placement', 'taurus'], "Ch.32 v.7", "Rahu exalted in Taurus: attractive and magnetic appearance, alluring personality, exotic beauty"),
    ("rahu", "sign_placement", "taurus", {}, "mixed", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'taurus'], "Ch.32 v.8", "Rahu in Taurus: attraction to foreign or unconventional partner, sensual obsessions, material expectations"),
    ("rahu", "sign_placement", "taurus", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'taurus'], "Ch.32 v.9", "Rahu in Taurus: success in foreign trade, luxury imports, technology, or unconventional finance"),
    ("rahu", "sign_placement", "taurus", {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'taurus'], "Ch.32 v.10", "Rahu in Taurus: throat and neck issues, mysterious allergies, substance sensitivity"),
]

_RAHU_GEMINI_DATA = [
    ("rahu", "sign_placement", "gemini", {}, "favorable", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'sign_placement', 'gemini'], "Ch.32 v.11", "Rahu in Gemini: brilliant unconventional intellect, expertise in technology, foreign languages, or media"),
    ("rahu", "sign_placement", "gemini", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'gemini'], "Ch.32 v.12", "Rahu in Gemini: success in media, technology, communications, or foreign publishing"),
    ("rahu", "sign_placement", "gemini", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'gemini'], "Ch.32 v.13", "Rahu in Gemini: cunning communicator, manipulative speech possible, versatile but deceptive"),
    ("rahu", "sign_placement", "gemini", {}, "mixed", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'gemini'], "Ch.32 v.14", "Rahu in Gemini: intellectual but unreliable partner, communication deception, multiple relationships"),
    ("rahu", "sign_placement", "gemini", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'gemini'], "Ch.32 v.15", "Rahu in Gemini: income through media, technology, or communication — irregular but significant"),
]

_RAHU_CANCER_DATA = [
    ("rahu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'sign_placement', 'cancer'], "Ch.32 v.16", "Rahu in Cancer: emotional obsession, anxiety about security, irrational fears, disturbed peace"),
    ("rahu", "sign_placement", "cancer", {}, "mixed", "moderate", ['property_vehicles'], ['rahu', 'saravali', 'sign_placement', 'cancer'], "Ch.32 v.17", "Rahu in Cancer: unusual property acquisitions, foreign real estate, haunted or disputed homes"),
    ("rahu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'cancer'], "Ch.32 v.18", "Rahu in Cancer: emotionally manipulative relationships, maternal issues projected onto partner"),
    ("rahu", "sign_placement", "cancer", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'cancer'], "Ch.32 v.19", "Rahu in Cancer: income through hospitality, foreign food industry, or emotional manipulation"),
    ("rahu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'cancer'], "Ch.32 v.20", "Rahu in Cancer: stomach disorders, mysterious digestive issues, psychosomatic illness"),
]

_RAHU_LEO_DATA = [
    ("rahu", "sign_placement", "leo", {}, "mixed", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'leo'], "Ch.32 v.21", "Rahu in Leo: obsessive desire for power, unconventional leadership, political ambition"),
    ("rahu", "sign_placement", "leo", {}, "mixed", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'sign_placement', 'leo'], "Ch.32 v.22", "Rahu in Leo: sudden fame or infamy, controversial public figure, dramatic public presence"),
    ("rahu", "sign_placement", "leo", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'leo'], "Ch.32 v.23", "Rahu in Leo: grandiose self-image, dramatic personality, ego inflation, showmanship"),
    ("rahu", "sign_placement", "leo", {}, "unfavorable", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'leo'], "Ch.32 v.24", "Rahu in Leo: heart palpitations, mysterious cardiac symptoms, spine problems"),
    ("rahu", "sign_placement", "leo", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'leo'], "Ch.32 v.25", "Rahu in Leo: gains through entertainment, speculation, or government connections — volatile"),
]

_RAHU_VIRGO_DATA = [
    ("rahu", "sign_placement", "virgo", {}, "favorable", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'sign_placement', 'virgo'], "Ch.32 v.26", "Rahu in Virgo: exceptional analytical ability, unconventional research, technology expertise"),
    ("rahu", "sign_placement", "virgo", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'virgo'], "Ch.32 v.27", "Rahu in Virgo: success in medicine, technology, research, or alternative healing"),
    ("rahu", "sign_placement", "virgo", {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'virgo'], "Ch.32 v.28", "Rahu in Virgo: mysterious digestive issues, nervous complaints, undiagnosable symptoms"),
    ("rahu", "sign_placement", "virgo", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'virgo'], "Ch.32 v.29", "Rahu in Virgo: obsessive perfectionism, anxious disposition, health anxiety"),
    ("rahu", "sign_placement", "virgo", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'virgo'], "Ch.32 v.30", "Rahu in Virgo: income through health technology, alternative medicine, or foreign service"),
]

_RAHU_LIBRA_DATA = [
    ("rahu", "sign_placement", "libra", {}, "favorable", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'libra'], "Ch.32 v.31", "Rahu in Libra: foreign or unconventional spouse, intense romantic attraction, glamorous partnerships"),
    ("rahu", "sign_placement", "libra", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'libra'], "Ch.32 v.32", "Rahu in Libra: success in international diplomacy, foreign trade, fashion, or entertainment"),
    ("rahu", "sign_placement", "libra", {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'libra'], "Ch.32 v.33", "Rahu in Libra: gains through partnerships, international business, luxury trade"),
    ("rahu", "sign_placement", "libra", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'libra'], "Ch.32 v.34", "Rahu in Libra: charming but manipulative, diplomatic deception, social climbing"),
    ("rahu", "sign_placement", "libra", {}, "mixed", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'sign_placement', 'libra'], "Ch.32 v.35", "Rahu in Libra: glamorous public image, famous for beauty or partnerships, social media fame"),
]

_RAHU_SCORPIO_DATA = [
    ("rahu", "sign_placement", "scorpio", {}, "unfavorable", "strong", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'scorpio'], "Ch.32 v.36", "Rahu debilitated in Scorpio: mysterious chronic ailments, poisoning risk, occult dangers"),
    ("rahu", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'sign_placement', 'scorpio'], "Ch.32 v.37", "Rahu debilitated in Scorpio: paranoia, obsessive fears, psychological disturbances"),
    ("rahu", "sign_placement", "scorpio", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'scorpio'], "Ch.32 v.38", "Rahu in Scorpio: gains through insurance, occult, or underground — but with great risk"),
    ("rahu", "sign_placement", "scorpio", {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'sign_placement', 'scorpio'], "Ch.32 v.39", "Rahu in Scorpio: tantra obsession, dangerous occult practices, kundalini complications"),
    ("rahu", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'scorpio'], "Ch.32 v.40", "Rahu debilitated in Scorpio: toxic relationships, betrayal, obsessive attachment"),
]

_RAHU_SAGITTARIUS_DATA = [
    ("rahu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.32 v.41", "Rahu in Sagittarius: foreign religious practices, unconventional spirituality, cult attraction"),
    ("rahu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.32 v.42", "Rahu in Sagittarius: foreign education, unconventional philosophy, heterodox teachings"),
    ("rahu", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['foreign_travel'], ['rahu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.32 v.43", "Rahu in Sagittarius: extensive foreign travel, living abroad, gains through foreign connections"),
    ("rahu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.32 v.44", "Rahu in Sagittarius: success in foreign universities, international law, or unconventional teaching"),
    ("rahu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.32 v.45", "Rahu in Sagittarius: self-righteous unconventionality, challenges to tradition, religious hypocrisy possible"),
]

_RAHU_CAPRICORN_DATA = [
    ("rahu", "sign_placement", "capricorn", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'capricorn'], "Ch.32 v.46", "Rahu in Capricorn: ambitious rise through unconventional means, technology in government, foreign corporate success"),
    ("rahu", "sign_placement", "capricorn", {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'capricorn'], "Ch.32 v.47", "Rahu in Capricorn: gains through foreign corporate work, technology, or unconventional business structures"),
    ("rahu", "sign_placement", "capricorn", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'capricorn'], "Ch.32 v.48", "Rahu in Capricorn: ruthless ambition, pragmatic manipulation, ends justify means mentality"),
    ("rahu", "sign_placement", "capricorn", {}, "mixed", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'sign_placement', 'capricorn'], "Ch.32 v.49", "Rahu in Capricorn: corporate fame, known for unconventional methods, controversial success"),
    ("rahu", "sign_placement", "capricorn", {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'capricorn'], "Ch.32 v.50", "Rahu in Capricorn: knee and joint issues, mysterious bone problems, chronic fatigue"),
]

_RAHU_AQUARIUS_DATA = [
    ("rahu", "sign_placement", "aquarius", {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'aquarius'], "Ch.32 v.51", "Rahu in Aquarius: success in technology, social media, innovation, or unconventional organizations"),
    ("rahu", "sign_placement", "aquarius", {}, "favorable", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'sign_placement', 'aquarius'], "Ch.32 v.52", "Rahu in Aquarius: genius-level innovation, technology mastery, futuristic thinking"),
    ("rahu", "sign_placement", "aquarius", {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'aquarius'], "Ch.32 v.53", "Rahu in Aquarius: income through technology, social networks, or innovative enterprises"),
    ("rahu", "sign_placement", "aquarius", {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'sign_placement', 'aquarius'], "Ch.32 v.54", "Rahu in Aquarius: eccentric genius, rebel without cause, detached from conventions"),
    ("rahu", "sign_placement", "aquarius", {}, "mixed", "moderate", ['marriage'], ['rahu', 'saravali', 'sign_placement', 'aquarius'], "Ch.32 v.55", "Rahu in Aquarius: extremely unconventional relationships, online romance, virtual connections"),
]

_RAHU_PISCES_DATA = [
    ("rahu", "sign_placement", "pisces", {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'sign_placement', 'pisces'], "Ch.32 v.56", "Rahu in Pisces: spiritual confusion, psychic sensitivity without discipline, guru exploitation"),
    ("rahu", "sign_placement", "pisces", {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'sign_placement', 'pisces'], "Ch.32 v.57", "Rahu in Pisces: escapism through substances, fantasy addiction, delusional thinking"),
    ("rahu", "sign_placement", "pisces", {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'sign_placement', 'pisces'], "Ch.32 v.58", "Rahu in Pisces: income through film, imagination, healing, or spiritual enterprise — unstable"),
    ("rahu", "sign_placement", "pisces", {}, "mixed", "moderate", ['career_status'], ['rahu', 'saravali', 'sign_placement', 'pisces'], "Ch.32 v.59", "Rahu in Pisces: success in film, photography, healing arts, or spiritual counseling"),
    ("rahu", "sign_placement", "pisces", {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'sign_placement', 'pisces'], "Ch.32 v.60", "Rahu in Pisces: feet problems, lymphatic disorders, mysterious infections, immune sensitivity"),
]

_KETU_ARIES_DATA = [
    ("ketu", "sign_placement", "aries", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'aries'], "Ch.33 v.1", "Ketu in Aries: past-life warrior, detached courage, spiritual fire, renunciation of ego"),
    ("ketu", "sign_placement", "aries", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'aries'], "Ch.33 v.2", "Ketu in Aries: mysterious head injuries, neurological issues, sudden health crises"),
    ("ketu", "sign_placement", "aries", {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'aries'], "Ch.33 v.3", "Ketu in Aries: detached from ambition, success through surrender, unexpected career turns"),
    ("ketu", "sign_placement", "aries", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'aries'], "Ch.33 v.4", "Ketu in Aries: fearless but directionless, past-life courage, indifferent to competition"),
    ("ketu", "sign_placement", "aries", {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'sign_placement', 'aries'], "Ch.33 v.5", "Ketu in Aries: financial indifference, losses through neglect, detached from material gains"),
]

_KETU_TAURUS_DATA = [
    ("ketu", "sign_placement", "taurus", {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'sign_placement', 'taurus'], "Ch.33 v.6", "Ketu debilitated in Taurus: material detachment causes losses, unable to hold wealth, financial disinterest"),
    ("ketu", "sign_placement", "taurus", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'taurus'], "Ch.33 v.7", "Ketu in Taurus: detached from luxury, ascetic tendencies, values beyond material world"),
    ("ketu", "sign_placement", "taurus", {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'sign_placement', 'taurus'], "Ch.33 v.8", "Ketu in Taurus: emotionally detached partner, lack of sensual interest, cold in intimacy"),
    ("ketu", "sign_placement", "taurus", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'taurus'], "Ch.33 v.9", "Ketu in Taurus: spiritual detachment from material world, renunciation of luxury, inner wealth"),
    ("ketu", "sign_placement", "taurus", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'taurus'], "Ch.33 v.10", "Ketu in Taurus: throat and speech disorders, mysterious food intolerances, skin conditions"),
]

_KETU_GEMINI_DATA = [
    ("ketu", "sign_placement", "gemini", {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'gemini'], "Ch.33 v.11", "Ketu in Gemini: intuitive knowledge without study, past-life intellectual mastery, beyond logic"),
    ("ketu", "sign_placement", "gemini", {}, "unfavorable", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'gemini'], "Ch.33 v.12", "Ketu in Gemini: communication barriers, difficulty in conventional education, career indifference"),
    ("ketu", "sign_placement", "gemini", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'gemini'], "Ch.33 v.13", "Ketu in Gemini: introverted, non-verbal communication preference, telepathic sensitivity"),
    ("ketu", "sign_placement", "gemini", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'gemini'], "Ch.33 v.14", "Ketu in Gemini: transcends intellectual barriers, direct knowing, spiritual communication"),
    ("ketu", "sign_placement", "gemini", {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'sign_placement', 'gemini'], "Ch.33 v.15", "Ketu in Gemini: communication breakdown with partner, detached intellectualism in love"),
]

_KETU_CANCER_DATA = [
    ("ketu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['mental_health'], ['ketu', 'saravali', 'sign_placement', 'cancer'], "Ch.33 v.16", "Ketu in Cancer: emotional detachment, difficulty nurturing, motherless feeling, inner void"),
    ("ketu", "sign_placement", "cancer", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'cancer'], "Ch.33 v.17", "Ketu in Cancer: transcends emotional dependency, spiritual mothering, divine nurturing realized"),
    ("ketu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['property_vehicles'], ['ketu', 'saravali', 'sign_placement', 'cancer'], "Ch.33 v.18", "Ketu in Cancer: property losses, homeless feeling despite having shelter, domestic detachment"),
    ("ketu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'sign_placement', 'cancer'], "Ch.33 v.19", "Ketu in Cancer: emotionally unavailable, domestic disinterest, partner feels neglected"),
    ("ketu", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'cancer'], "Ch.33 v.20", "Ketu in Cancer: stomach disorders, mysterious chest pains, immune system weakness"),
]

_KETU_LEO_DATA = [
    ("ketu", "sign_placement", "leo", {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'leo'], "Ch.33 v.21", "Ketu in Leo: detached from authority, reluctant leader, power without desire for it"),
    ("ketu", "sign_placement", "leo", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'leo'], "Ch.33 v.22", "Ketu in Leo: humble despite capabilities, past-life royalty, ego dissolution"),
    ("ketu", "sign_placement", "leo", {}, "unfavorable", "moderate", ['progeny'], ['ketu', 'saravali', 'sign_placement', 'leo'], "Ch.33 v.23", "Ketu in Leo: challenges with children, detached parenting, unconventional family structure"),
    ("ketu", "sign_placement", "leo", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'leo'], "Ch.33 v.24", "Ketu in Leo: dissolution of ego, spiritual leadership without seeking, divine humility"),
    ("ketu", "sign_placement", "leo", {}, "unfavorable", "moderate", ['fame_reputation'], ['ketu', 'saravali', 'sign_placement', 'leo'], "Ch.33 v.25", "Ketu in Leo: avoids spotlight, reputation fluctuates, spiritual anonymity preferred"),
]

_KETU_VIRGO_DATA = [
    ("ketu", "sign_placement", "virgo", {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'virgo'], "Ch.33 v.26", "Ketu in Virgo: transcends analytical thinking, intuitive healing, past-life medical knowledge"),
    ("ketu", "sign_placement", "virgo", {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'virgo'], "Ch.33 v.27", "Ketu in Virgo: unconventional healing career, alternative medicine, spiritual service"),
    ("ketu", "sign_placement", "virgo", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'virgo'], "Ch.33 v.28", "Ketu in Virgo: mysterious digestive issues, undiagnosable conditions, energy healing needed"),
    ("ketu", "sign_placement", "virgo", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'virgo'], "Ch.33 v.29", "Ketu in Virgo: beyond criticism, accepts imperfection, spiritual surrender to chaos"),
    ("ketu", "sign_placement", "virgo", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'virgo'], "Ch.33 v.30", "Ketu in Virgo: healing through spiritual practice, service as path to liberation"),
]

_KETU_LIBRA_DATA = [
    ("ketu", "sign_placement", "libra", {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'sign_placement', 'libra'], "Ch.33 v.31", "Ketu in Libra: detachment from partnerships, inability to commit, past-life relationship karma"),
    ("ketu", "sign_placement", "libra", {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'libra'], "Ch.33 v.32", "Ketu in Libra: success through unconventional partnerships, detached diplomacy"),
    ("ketu", "sign_placement", "libra", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'libra'], "Ch.33 v.33", "Ketu in Libra: impartial to a fault, detached from social norms, inner balance without external need"),
    ("ketu", "sign_placement", "libra", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'libra'], "Ch.33 v.34", "Ketu in Libra: transcends relationships, finds divine through inner balance, partnership as spiritual practice"),
    ("ketu", "sign_placement", "libra", {}, "mixed", "moderate", ['wealth'], ['ketu', 'saravali', 'sign_placement', 'libra'], "Ch.33 v.35", "Ketu in Libra: financial detachment in partnerships, unexpected gains and losses through others"),
]

_KETU_SCORPIO_DATA = [
    ("ketu", "sign_placement", "scorpio", {}, "favorable", "strong", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'scorpio'], "Ch.33 v.36", "Ketu exalted in Scorpio: supreme spiritual transformation, moksha potential, past-life occult mastery"),
    ("ketu", "sign_placement", "scorpio", {}, "favorable", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'scorpio'], "Ch.33 v.37", "Ketu exalted in Scorpio: deep intuitive research, psychic abilities, occult knowledge without study"),
    ("ketu", "sign_placement", "scorpio", {}, "mixed", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'scorpio'], "Ch.33 v.38", "Ketu in Scorpio: mysterious transformative illness leading to spiritual awakening, kundalini rising"),
    ("ketu", "sign_placement", "scorpio", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'scorpio'], "Ch.33 v.39", "Ketu exalted in Scorpio: detached intensity, fearless about death, profound psychological insight"),
    ("ketu", "sign_placement", "scorpio", {}, "favorable", "moderate", ['fame_reputation'], ['ketu', 'saravali', 'sign_placement', 'scorpio'], "Ch.33 v.40", "Ketu exalted in Scorpio: known for spiritual depth, respected in occult circles, mysterious reputation"),
]

_KETU_SAGITTARIUS_DATA = [
    ("ketu", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.33 v.41", "Ketu in Sagittarius: past-life dharmic mastery, instinctive spiritual knowledge, effortless philosophy"),
    ("ketu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.33 v.42", "Ketu in Sagittarius: transcends conventional education, direct knowing, wisdom beyond books"),
    ("ketu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.33 v.43", "Ketu in Sagittarius: quietly righteous, dharmic without preaching, inner moral compass"),
    ("ketu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.33 v.44", "Ketu in Sagittarius: unconventional teaching, spiritual guidance, detached from academic hierarchy"),
    ("ketu", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['foreign_travel'], ['ketu', 'saravali', 'sign_placement', 'sagittarius'], "Ch.33 v.45", "Ketu in Sagittarius: pilgrimages, spiritual journeys, detached from worldly travel"),
]

_KETU_CAPRICORN_DATA = [
    ("ketu", "sign_placement", "capricorn", {}, "unfavorable", "moderate", ['career_status'], ['ketu', 'saravali', 'sign_placement', 'capricorn'], "Ch.33 v.46", "Ketu in Capricorn: detachment from worldly ambition, career indifference, structural dissolution"),
    ("ketu", "sign_placement", "capricorn", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'capricorn'], "Ch.33 v.47", "Ketu in Capricorn: transcends material ambition, inner authority, spiritual responsibility"),
    ("ketu", "sign_placement", "capricorn", {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'sign_placement', 'capricorn'], "Ch.33 v.48", "Ketu in Capricorn: financial indifference, losses through neglect of material duties"),
    ("ketu", "sign_placement", "capricorn", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'capricorn'], "Ch.33 v.49", "Ketu in Capricorn: spiritual discipline without worldly reward, karma yoga, selfless service"),
    ("ketu", "sign_placement", "capricorn", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'capricorn'], "Ch.33 v.50", "Ketu in Capricorn: bone and joint issues, mysterious knee problems, structural weakness"),
]

_KETU_AQUARIUS_DATA = [
    ("ketu", "sign_placement", "aquarius", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'aquarius'], "Ch.33 v.51", "Ketu in Aquarius: transcends social conventions, spiritual innovation, liberation from group identity"),
    ("ketu", "sign_placement", "aquarius", {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'aquarius'], "Ch.33 v.52", "Ketu in Aquarius: intuitive technology understanding, past-life scientific mastery, beyond logic"),
    ("ketu", "sign_placement", "aquarius", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'aquarius'], "Ch.33 v.53", "Ketu in Aquarius: ultimate detachment, beyond social identity, spiritual individuality"),
    ("ketu", "sign_placement", "aquarius", {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'sign_placement', 'aquarius'], "Ch.33 v.54", "Ketu in Aquarius: extreme detachment in relationships, hermit tendencies, partner feels invisible"),
    ("ketu", "sign_placement", "aquarius", {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'sign_placement', 'aquarius'], "Ch.33 v.55", "Ketu in Aquarius: circulation issues, mysterious nerve problems, energy body disturbances"),
]

_KETU_PISCES_DATA = [
    ("ketu", "sign_placement", "pisces", {}, "favorable", "moderate", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'pisces'], "Ch.33 v.56", "Ketu in Pisces: past-life spiritual mastery, intuitive moksha path, natural meditation ability"),
    ("ketu", "sign_placement", "pisces", {}, "favorable", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'sign_placement', 'pisces'], "Ch.33 v.57", "Ketu in Pisces: psychic knowledge, dreams as guidance, intuitive wisdom beyond logic"),
    ("ketu", "sign_placement", "pisces", {}, "mixed", "moderate", ['mental_health'], ['ketu', 'saravali', 'sign_placement', 'pisces'], "Ch.33 v.58", "Ketu in Pisces: dissolution of boundaries, spiritual crisis possible, ego death journey"),
    ("ketu", "sign_placement", "pisces", {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'sign_placement', 'pisces'], "Ch.33 v.59", "Ketu in Pisces: otherworldly presence, saint-like detachment, compassion without attachment"),
    ("ketu", "sign_placement", "pisces", {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'sign_placement', 'pisces'], "Ch.33 v.60", "Ketu in Pisces: complete material indifference, money flows through, financial negligence"),
]

_NODES_GENERAL_DATA = [
    ("rahu", "sign_condition", "rahu_exalted", {}, "favorable", "strong", ['wealth', 'career_status'], ['rahu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.61", "Rahu exalted in Taurus: maximum obsessive power directed at material acquisition, foreign gains"),
    ("rahu", "sign_condition", "rahu_debilitated", {}, "unfavorable", "strong", ['physical_health', 'mental_health'], ['rahu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.62", "Rahu debilitated in Scorpio: intensified fears, psychological disturbances, occult dangers"),
    ("ketu", "sign_condition", "ketu_exalted", {}, "favorable", "strong", ['spirituality'], ['ketu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.63", "Ketu exalted in Scorpio: supreme spiritual liberation potential, moksha karaka at full strength"),
    ("ketu", "sign_condition", "ketu_debilitated", {}, "unfavorable", "moderate", ['wealth', 'marriage'], ['ketu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.64", "Ketu debilitated in Taurus: material detachment causes real-world losses, relationship neglect"),
    ("rahu", "sign_condition", "rahu_ketu_axis", {}, "mixed", "strong", ['career_status', 'spirituality'], ['rahu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.65", "Rahu-Ketu axis: always opposite signs, material obsession vs spiritual detachment in balance"),
    ("rahu", "sign_condition", "rahu_with_jupiter", {}, "mixed", "moderate", ['spirituality', 'intelligence_education'], ['rahu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.66", "Rahu conjunct Jupiter (Guru Chandal): corrupted wisdom, unconventional teaching, heterodox philosophy"),
    ("ketu", "sign_condition", "ketu_with_mars", {}, "unfavorable", "moderate", ['physical_health', 'enemies_litigation'], ['ketu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.67", "Ketu conjunct Mars: sudden accidents, surgical interventions, mysterious injuries"),
    ("rahu", "sign_condition", "rahu_with_moon", {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.68", "Rahu conjunct Moon: Grahan Yoga, mental disturbances, anxiety, obsessive emotional patterns"),
    ("ketu", "sign_condition", "ketu_with_saturn", {}, "mixed", "moderate", ['longevity', 'spirituality'], ['ketu', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.69", "Ketu conjunct Saturn: extreme renunciation, karmic debts, liberation through suffering"),
    ("nodes", "sign_condition", "nodes_retrograde_always", {}, "mixed", "moderate", ['character_temperament'], ['nodes', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.32 v.70", "Rahu and Ketu always retrograde: their effects unfold through past-life karma, not current volition"),
]


def _make_sign_rules(data: list, start_id: int) -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    for i, t in enumerate(data):
        planet, ptype, pval, extra, direction, intensity, domains, tags, vref, desc = t
        pc = {"planet": planet, "placement_type": ptype, "placement_value": [pval] if ptype == "sign_placement" else [], **extra}
        if ptype == "sign_condition":
            pc["yoga_label"] = pval
        rid = f"SAV{start_id + i}"
        ch = "Ch.32-33"
        rules.append(RuleRecord(
            rule_id=rid, source="Saravali", chapter=ch, school="parashari",
            category="sign_predictions", description=desc, confidence=0.65,
            verse="Saravali " + vref, tags=tags, implemented=False, engine_ref="",
            primary_condition=pc, modifiers=[], exceptions=[],
            outcome_domains=domains, outcome_direction=direction,
            outcome_intensity=intensity, outcome_timing="dasha_dependent",
            lagna_scope=[], dasha_scope=[], verse_ref=vref,
            concordance_texts=[], divergence_notes="",
            phase="1B_matrix", system="natal",
        ))
    return rules


def _build_all_rules() -> list[RuleRecord]:
    all_sign_data = [
        (_RAHU_ARIES_DATA, 2003),
        (_RAHU_TAURUS_DATA, 2008),
        (_RAHU_GEMINI_DATA, 2013),
        (_RAHU_CANCER_DATA, 2018),
        (_RAHU_LEO_DATA, 2023),
        (_RAHU_VIRGO_DATA, 2028),
        (_RAHU_LIBRA_DATA, 2033),
        (_RAHU_SCORPIO_DATA, 2038),
        (_RAHU_SAGITTARIUS_DATA, 2043),
        (_RAHU_CAPRICORN_DATA, 2048),
        (_RAHU_AQUARIUS_DATA, 2053),
        (_RAHU_PISCES_DATA, 2058),
        (_KETU_ARIES_DATA, 2063),
        (_KETU_TAURUS_DATA, 2068),
        (_KETU_GEMINI_DATA, 2073),
        (_KETU_CANCER_DATA, 2078),
        (_KETU_LEO_DATA, 2083),
        (_KETU_VIRGO_DATA, 2088),
        (_KETU_LIBRA_DATA, 2093),
        (_KETU_SCORPIO_DATA, 2098),
        (_KETU_SAGITTARIUS_DATA, 2103),
        (_KETU_CAPRICORN_DATA, 2108),
        (_KETU_AQUARIUS_DATA, 2113),
        (_KETU_PISCES_DATA, 2118),
        (_NODES_GENERAL_DATA, 2123),
    ]
    result: list[RuleRecord] = []
    for data, s in all_sign_data:
        result.extend(_make_sign_rules(data, s))
    return result


SARAVALI_SIGNS_8_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_8_REGISTRY.add(_rule)
