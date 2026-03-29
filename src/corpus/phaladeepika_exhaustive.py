"""
src/corpus/phaladeepika_exhaustive.py — Phaladeepika Exhaustive (S262)

Exhaustive encoding of Mantreswara's Phaladeepika (14th century CE),
one of the most comprehensive classical texts on predictive Vedic astrology.

Phaladeepika covers:
- Planet natures, elements, significations
- Rashi characteristics (all 12 signs)
- Planet dignity system (exaltation, debilitation, Moolatrikona)
- House significations (all 12)
- Planets in all houses (all 9 planets × 12 houses)
- Yoga combinations (Raja, Dhana, Arishta)
- Dasha results
- Marriage, children, longevity, career
- Medical astrology
- Vargas (divisional charts)
- Special lagnas and sensitive points

120 rules: PHX001-PHX120.
All: school="parashari", source="Phaladeepika", implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

PHALADEEPIKA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Planet Natures and Characteristics (PHX001-009) ───────────────────────
    RuleRecord(
        rule_id="PHX001",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Sun: Sattvic, pitta constitution, copper-red complexion, medium stature, "
            "honey-colored eyes, thin hair. Soul (Atma) karaka. Rules Sunday. "
            "Gem: ruby. Direction: East. Deity: Shiva."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.1",
        tags=["phx", "sun", "planet_nature", "sattvic", "pitta", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX002",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Moon: Sattvic (Vata-Kapha), white complexion, round body, beautiful eyes, "
            "sweet speech, fickle mind. Mind (Manas) karaka. Rules Monday. "
            "Gem: pearl. Direction: NW. Deity: Parvati."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.2",
        tags=["phx", "moon", "planet_nature", "sattvic", "vata", "kapha", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX003",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Mars: Tamasic, pitta constitution, blood-red complexion, cruel eyes, "
            "short stature, youthful. Courage and siblings (Bhratru/Vikrama) karaka. "
            "Rules Tuesday. Gem: coral. Direction: South. Deity: Skanda."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.3",
        tags=["phx", "mars", "planet_nature", "tamasic", "pitta", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX004",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Mercury: Rajasic, mixed constitution (adapts), greenish complexion, "
            "sharp intellect, eloquent speech. Intelligence (Buddhi) karaka. "
            "Rules Wednesday. Gem: emerald. Direction: North. Deity: Vishnu."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.4",
        tags=["phx", "mercury", "planet_nature", "rajasic", "intelligence", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX005",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Jupiter: Sattvic, Kapha constitution, golden/yellow complexion, "
            "large body, excellent wisdom, eloquent. Children/Dharma (Putra/Guru) karaka. "
            "Rules Thursday. Gem: yellow sapphire. Direction: NE. Deity: Brahma."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.5",
        tags=["phx", "jupiter", "planet_nature", "sattvic", "kapha", "dharma", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX006",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Venus: Rajasic, Vata-Kapha constitution, bright white complexion, "
            "beautiful large eyes, charming. Marriage/Pleasure (Kalatra/Kama) karaka. "
            "Rules Friday. Gem: diamond. Direction: SE. Deity: Lakshmi."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.6",
        tags=["phx", "venus", "planet_nature", "rajasic", "vata", "marriage", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX007",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Saturn: Tamasic, Vata constitution, dark/blue complexion, "
            "lean tall body, coarse hair, lazy. Longevity/Grief (Ayus/Dukha) karaka. "
            "Rules Saturday. Gem: blue sapphire. Direction: West. Deity: Yama."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.2 v.7",
        tags=["phx", "saturn", "planet_nature", "tamasic", "vata", "longevity", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX008",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Rahu: Tamasic, Vata constitution, smoky/dark appearance. "
            "Paternal grandfather, foreign places, epidemics. Causes fear and delusion. "
            "Gem: hessonite. Co-rules Aquarius (with Saturn). Deity: Durga."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.2 v.8",
        tags=["phx", "rahu", "planet_nature", "tamasic", "foreign", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX009",
        source="Phaladeepika",
        chapter="Ch.2",
        school="parashari",
        category="planet_nature",
        description=(
            "Ketu: Tamasic, mixed constitution, spotted/variegated appearance. "
            "Maternal grandfather, liberation, past karma. Causes mysterious separations. "
            "Gem: cat's eye. Co-rules Scorpio (with Mars). Deity: Ganesha."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.2 v.9",
        tags=["phx", "ketu", "planet_nature", "tamasic", "liberation", "karma", "parashari"],
        implemented=False,
    ),

    # ── Rashi Characteristics (PHX010-021) ────────────────────────────────────
    RuleRecord(
        rule_id="PHX010",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Aries: Movable, fire, masculine, eastern, forest/hill dweller. "
            "Body part: head and face. Pitta. Rules day. Cruel sign. "
            "Aries lagna: bold, pioneering, impulsive, short-tempered but forgives quickly."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.1",
        tags=["phx", "aries", "rashi", "movable", "fire", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX011",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Taurus: Fixed, earth, feminine, southern, cultivated land. "
            "Body part: face and neck. Vata-Kapha. Rules night. Gentle sign. "
            "Taurus lagna: patient, artistic, sensual, stubborn, love of beauty and comfort."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.2",
        tags=["phx", "taurus", "rashi", "fixed", "earth", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX012",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Gemini: Dual, air, masculine, western, bedroom/playground. "
            "Body part: shoulders and arms. Vata. Rules night. Gentle sign. "
            "Gemini lagna: clever, versatile, communicative, restless, dual nature."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.3",
        tags=["phx", "gemini", "rashi", "dual", "air", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX013",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Cancer: Movable, water, feminine, northern, water bodies. "
            "Body part: chest and lungs. Kapha. Rules night. Gentle sign. "
            "Cancer lagna: nurturing, emotional, home-loving, protective, psychic."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.4",
        tags=["phx", "cancer", "rashi", "movable", "water", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX014",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Leo: Fixed, fire, masculine, eastern, forests/royal places. "
            "Body part: upper back and heart. Pitta. Rules day. Cruel sign. "
            "Leo lagna: royal, generous, proud, fixed opinions, natural authority."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.5",
        tags=["phx", "leo", "rashi", "fixed", "fire", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX015",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Virgo: Dual, earth, feminine, southern, fields and granaries. "
            "Body part: abdomen and intestines. Vata. Rules day. Gentle sign. "
            "Virgo lagna: analytical, perfectionist, service-oriented, methodical, critical."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.6",
        tags=["phx", "virgo", "rashi", "dual", "earth", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX016",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Libra: Movable, air, masculine, western, markets and trade. "
            "Body part: kidneys and lower back. Vata. Rules day. Cruel sign. "
            "Libra lagna: balanced, diplomatic, justice-seeking, indecisive, aesthetic."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.7",
        tags=["phx", "libra", "rashi", "movable", "air", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX017",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Scorpio: Fixed, water, feminine, northern, holes and crevices. "
            "Body part: reproductive organs. Kapha-Pitta. Rules night. Cruel sign. "
            "Scorpio lagna: intense, secretive, transformative, jealous, powerful will."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.8",
        tags=["phx", "scorpio", "rashi", "fixed", "water", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX018",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Sagittarius: Dual, fire, masculine, eastern, stables/religious places. "
            "Body part: thighs and hips. Pitta. Rules day. Gentle sign. "
            "Sagittarius lagna: philosophical, adventurous, optimistic, direct, freedom-loving."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.9",
        tags=["phx", "sagittarius", "rashi", "dual", "fire", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX019",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Capricorn: Movable, earth, feminine, southern, forests and water. "
            "Body part: knees. Vata. Rules night. Cruel sign. "
            "Capricorn lagna: ambitious, disciplined, practical, patient, persevering."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.10",
        tags=["phx", "capricorn", "rashi", "movable", "earth", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX020",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Aquarius: Fixed, air, masculine, western, places of liquor/clay pots. "
            "Body part: calves and ankles. Vata. Rules day. Cruel sign. "
            "Aquarius lagna: humanitarian, innovative, detached, rebellious, scientific."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.11",
        tags=["phx", "aquarius", "rashi", "fixed", "air", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX021",
        source="Phaladeepika",
        chapter="Ch.1",
        school="parashari",
        category="rashi",
        description=(
            "Pisces: Dual, water, feminine, northern, seas and holy places. "
            "Body part: feet. Kapha. Rules night. Gentle sign. "
            "Pisces lagna: spiritual, compassionate, dreamy, psychic, self-sacrificing."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.1 v.12",
        tags=["phx", "pisces", "rashi", "dual", "water", "parashari"],
        implemented=False,
    ),

    # ── Dignity System (PHX022-030) ────────────────────────────────────────────
    RuleRecord(
        rule_id="PHX022",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Exaltation signs: Sun in Aries (10°), Moon in Taurus (3°), "
            "Mars in Capricorn (28°), Mercury in Virgo (15°), Jupiter in Cancer (5°), "
            "Venus in Pisces (27°), Saturn in Libra (20°)."
        ),
        confidence=0.98,
        verse="Phaladeepika Ch.3 v.1",
        tags=["phx", "exaltation", "dignity", "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX023",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Debilitation signs (7th from exaltation): Sun in Libra (10°), Moon in Scorpio (3°), "
            "Mars in Cancer (28°), Mercury in Pisces (15°), Jupiter in Capricorn (5°), "
            "Venus in Virgo (27°), Saturn in Aries (20°)."
        ),
        confidence=0.98,
        verse="Phaladeepika Ch.3 v.2",
        tags=["phx", "debilitation", "dignity", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX024",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Moolatrikona signs: Sun in Leo (1-20°), Moon in Taurus (4-30°), "
            "Mars in Aries (1-12°), Mercury in Virgo (16-20°), Jupiter in Sagittarius (1-10°), "
            "Venus in Libra (1-15°), Saturn in Aquarius (1-20°)."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.3 v.3",
        tags=["phx", "moolatrikona", "dignity", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX025",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Own signs: Sun → Leo. Moon → Cancer. Mars → Aries, Scorpio. "
            "Mercury → Gemini, Virgo. Jupiter → Sagittarius, Pisces. "
            "Venus → Taurus, Libra. Saturn → Capricorn, Aquarius."
        ),
        confidence=0.98,
        verse="Phaladeepika Ch.3 v.4",
        tags=["phx", "own_sign", "dignity", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX026",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Neecha Bhanga (cancellation of debilitation): the lord of the debilitation sign "
            "or the lord of the exaltation sign is in a kendra from the Lagna or Moon. "
            "Also: the planet that gets exalted in the debilitated planet's sign is in kendra."
        ),
        confidence=0.96,
        verse="Phaladeepika Ch.3 v.10",
        tags=["phx", "neecha_bhanga", "dignity", "debilitation", "kendra", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX027",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Vargottama: planet in the same sign in both D1 and D9. "
            "Vargottama in exaltation sign → maximum dignity. "
            "Vargottama in own sign → strong and stable. Gives qualities of exaltation."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.3 v.15",
        tags=["phx", "vargottama", "dignity", "d9", "navamsha", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX028",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Combustion (Asta): Sun within 6° of any planet → planet is combust. "
            "Exception: Saturn combust within 15°. Moon combust = Amavasya. "
            "Combust planets give results related to Sun (father/authority) instead of own nature."
        ),
        confidence=0.93,
        verse="Phaladeepika Ch.3 v.20",
        tags=["phx", "combustion", "asta", "dignity", "sun", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX029",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Retrograde (Vakra): planets appear to move backward when near opposition to Sun. "
            "Retrograde planet in own/exaltation sign → exceptionally strong. "
            "Retrograde in debilitation → not as bad as direct debilitation."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.3 v.25",
        tags=["phx", "retrograde", "vakra", "dignity", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX030",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="dignity",
        description=(
            "Dig Bala (directional strength): Sun and Mars in 10th (South), "
            "Jupiter and Mercury in Lagna (East), Moon and Venus in 4th (North), "
            "Saturn in 7th (West). Maximum strength in these positions."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.3 v.30",
        tags=["phx", "dig_bala", "directional_strength", "dignity", "parashari"],
        implemented=False,
    ),

    # ── House Significations (PHX031-042) ──────────────────────────────────────
    RuleRecord(
        rule_id="PHX031",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "1st house (Lagna/Tanu): self, body, personality, vitality, early life. "
            "The rising sign colors all other houses. "
            "Phaladeepika: Lagna lord's strength determines overall life quality."
        ),
        confidence=0.96,
        verse="Phaladeepika Ch.5 v.1",
        tags=["phx", "1st_house", "lagna", "self", "body", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX032",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "2nd house (Dhana/Kutumba): wealth, family, speech, face, right eye, food. "
            "Maraka (death-inflicting) house when lord is afflicted. "
            "Phaladeepika: Jupiter in 2nd → eloquent, wealthy, family man."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.2",
        tags=["phx", "2nd_house", "wealth", "speech", "family", "maraka", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX033",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "3rd house (Sahaja/Parakrama): siblings, courage, short journeys, "
            "right ear, neck, throat, valor. 3rd lord strong → courageous and communicative. "
            "Phaladeepika: Mars in 3rd → warrior-like courage in younger sibling."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.3",
        tags=["phx", "3rd_house", "siblings", "courage", "communication", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX034",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "4th house (Sukha/Bandhu): mother, happiness, home, property, vehicles, education. "
            "Heart and chest. Moon's natural house. "
            "Phaladeepika: Venus in 4th → many comforts, beautiful home, happy mother."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.4",
        tags=["phx", "4th_house", "mother", "property", "happiness", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX035",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "5th house (Putra/Vidya): children, intelligence, past-life merit (Purva Punya), "
            "speculation, romance, mantras. Jupiter's natural house. "
            "Phaladeepika: 5th house determines quality of children and intellect."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.5",
        tags=["phx", "5th_house", "children", "intelligence", "purva_punya", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX036",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "6th house (Ripu/Roga): enemies, diseases, debts, servants, maternal uncle. "
            "Digestive system. Mars and Saturn are natural significators here. "
            "Phaladeepika: strong 6th lord → victory over enemies, service industry success."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.6",
        tags=["phx", "6th_house", "enemies", "disease", "debts", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX037",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "7th house (Kalatra/Yuvati): spouse, partnerships, travel, business. "
            "Second Maraka house. Venus's natural house. "
            "Phaladeepika: 7th lord in good sign with benefic aspect → devoted, beautiful spouse."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.7",
        tags=["phx", "7th_house", "spouse", "marriage", "partnership", "maraka", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX038",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "8th house (Ayus/Mrityu): longevity, death, sudden events, inheritance, occult. "
            "Genitals. Saturn's natural house for longevity analysis. "
            "Phaladeepika: benefics in 8th → long life; malefics → short or troubled life."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.8",
        tags=["phx", "8th_house", "longevity", "death", "occult", "inheritance", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX039",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "9th house (Dharma/Bhagya): father, dharma, fortune, higher education, "
            "long journeys, guru. Jupiter's natural house of dharma. "
            "Phaladeepika: 9th lord strong → exemplary fortune and dharmic career."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.9",
        tags=["phx", "9th_house", "father", "dharma", "fortune", "guru", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX040",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "10th house (Karma/Rajya): career, status, government, authority, actions. "
            "Knees. Sun/Mercury/Jupiter/Saturn are natural significators. "
            "Phaladeepika: 10th lord in kendra or trikona → outstanding career."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.10",
        tags=["phx", "10th_house", "career", "status", "government", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX041",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "11th house (Labha/Aya): gains, income, elder siblings, social networks, "
            "fulfillment of desires. Jupiter's natural house for gains. "
            "Phaladeepika: 11th lord strong → steady income; malefic 11th lord → erratic gains."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.11",
        tags=["phx", "11th_house", "gains", "income", "desires", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX042",
        source="Phaladeepika",
        chapter="Ch.5",
        school="parashari",
        category="house",
        description=(
            "12th house (Vyaya/Moksha): expenditure, losses, foreign lands, liberation, "
            "bed pleasures, left eye, feet. Saturn's natural house. "
            "Phaladeepika: 12th lord in 12th → expenditure on good causes; liberation possible."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.5 v.12",
        tags=["phx", "12th_house", "expenditure", "foreign", "liberation", "moksha", "parashari"],
        implemented=False,
    ),

    # ── Raja and Dhana Yogas (PHX043-060) ─────────────────────────────────────
    RuleRecord(
        rule_id="PHX043",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga (primary): conjunction or mutual aspect of 9th and 10th lords. "
            "Fortune (9th) and career (10th) unite → dharmakarmadhipati yoga. "
            "Phaladeepika: this is the fundamental Raja Yoga of Parashari tradition."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.6 v.1",
        tags=["phx", "raja_yoga", "yoga", "dharmakarmadhipati", "9th_house", "10th_house", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX044",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Kendra-Trikona Raja Yoga: kendra lord (1/4/7/10) and trikona lord (1/5/9) "
            "in conjunction, mutual aspect, or exchange → classic Raja Yoga. "
            "Phaladeepika: strongest when kendra and trikona lords are both in kendra/trikona positions."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.6 v.2",
        tags=["phx", "raja_yoga", "kendra", "trikona", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX045",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Yoga Karaka: a planet that simultaneously rules a kendra and a trikona → "
            "naturally produces Raja Yoga by itself. Mars for Cancer/Leo lagna. "
            "Venus for Capricorn/Aquarius lagna. Saturn for Taurus/Libra lagna."
        ),
        confidence=0.96,
        verse="Phaladeepika Ch.6 v.5",
        tags=["phx", "yoga_karaka", "raja_yoga", "kendra", "trikona", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX046",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Pancha Mahapurusha Yogas: five great-person yogas. "
            "Ruchaka (Mars in kendra in own/exalt), Bhadra (Mercury), Hamsa (Jupiter), "
            "Malavya (Venus), Shasha (Saturn). Each in kendra in own or exaltation sign."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.6 v.10",
        tags=["phx", "pancha_mahapurusha", "ruchaka", "bhadra", "hamsa", "malavya", "shasha", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX047",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Gaja Kesari Yoga: Jupiter in kendra from Moon. "
            "Phaladeepika: the native has elephant-like wisdom and lion-like courage. "
            "Results amplified if Jupiter is in own/exaltation sign and unafflicted."
        ),
        confidence=0.96,
        verse="Phaladeepika Ch.6 v.15",
        tags=["phx", "gaja_kesari_yoga", "jupiter", "moon", "kendra", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX048",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Budha-Aditya Yoga: Sun and Mercury conjunction (within 15°). "
            "Phaladeepika: intelligent, eloquent, government service, learned. "
            "If Mercury is combust (< 6°) the yoga weakens; 7-15° gives full yoga."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.6 v.18",
        tags=["phx", "budha_aditya_yoga", "sun", "mercury", "yoga", "intelligence", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX049",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Dhana Yoga (wealth yogas): 2nd and 11th lords conjunct or mutually aspecting. "
            "Also: 2nd/11th lords with Jupiter (natural wealth significator). "
            "Phaladeepika: wealthy when these combine in a kendra or trikona."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.6 v.22",
        tags=["phx", "dhana_yoga", "wealth", "2nd_house", "11th_house", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX050",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Chandra-Mangala Yoga: Moon and Mars conjunction. "
            "Phaladeepika: wealth through mother's side, courageous, dealing in liquids/chemicals. "
            "Negative side: overly aggressive emotions; positive: bold emotional initiative."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.6 v.25",
        tags=["phx", "chandra_mangala_yoga", "moon", "mars", "wealth", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX051",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Viparita Raja Yoga: lords of 6th, 8th, 12th in each other's houses. "
            "Harsha Yoga (6th lord in 6/8/12), Sarala Yoga (8th lord in 6/8/12), "
            "Vimala Yoga (12th lord in 6/8/12) → unexpected rise through adversity."
        ),
        confidence=0.93,
        verse="Phaladeepika Ch.6 v.30",
        tags=["phx", "viparita_raja_yoga", "harsha", "sarala", "vimala", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX052",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Daridra Yoga (poverty): lords of dusthanas (6/8/12) in kendras (1/4/7/10) "
            "without benefic influence → poverty despite effort. "
            "Also: 2nd and 11th lords both in dusthanas and afflicted → chronic poverty."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.6 v.35",
        tags=["phx", "daridra_yoga", "poverty", "dusthana", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX053",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Kemadruma Yoga: no planet in 2nd or 12th from Moon (and Moon is not in kendra). "
            "Phaladeepika: lonely, poor, erratic life despite potential. "
            "Cancelled by: Moon with planet, Moon in kendra, or Moon aspected by Jupiter."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.6 v.40",
        tags=["phx", "kemadruma_yoga", "moon", "yoga", "poverty", "loneliness", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX054",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Adhi Yoga: Jupiter, Venus, and Mercury in 6th, 7th, and 8th from Moon "
            "(in any combination). Phaladeepika: minister, leader, or physician. "
            "Strong Adhi Yoga (all three in 7th from Moon) → very high status."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.6 v.45",
        tags=["phx", "adhi_yoga", "jupiter", "venus", "mercury", "moon", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX055",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Anapha/Sunapha/Durudhara: Anapha = planet in 12th from Moon (other than Sun), "
            "Sunapha = planet in 2nd from Moon, Durudhara = both. "
            "Phaladeepika: these confer self-made prosperity, strong personality."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.6 v.50",
        tags=["phx", "anapha_yoga", "sunapha_yoga", "durudhara_yoga", "moon", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX056",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Shakata Yoga: Moon in 6th, 8th, or 12th from Jupiter. "
            "Phaladeepika: fluctuating fortune, like a cart wheel — up and down. "
            "Cancelled when Moon is in kendra from Lagna."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.6 v.55",
        tags=["phx", "shakata_yoga", "moon", "jupiter", "fluctuation", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX057",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Lakshmi Yoga: Venus (Lakshmi's planet) in own/exaltation sign in kendra/trikona, "
            "and 9th lord is strong. Phaladeepika: great wealth, beautiful, philanthropic. "
            "One of the most auspicious wealth yogas."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.6 v.60",
        tags=["phx", "lakshmi_yoga", "venus", "wealth", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX058",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Saraswati Yoga: Jupiter, Venus, and Mercury all in own/exaltation/friend's "
            "signs (or in 1/2/4/5/7/9/10). "
            "Phaladeepika: learned, eloquent, poet, musician, scholar — master of arts and sciences."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.6 v.65",
        tags=["phx", "saraswati_yoga", "jupiter", "venus", "mercury", "learning", "yoga", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX059",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Parivartana Yoga (exchange): two planets in each other's signs. "
            "Phaladeepika: the two planets mutually enhance each other's house results. "
            "A kendra-trikona Parivartana → Raja Yoga equivalent."
        ),
        confidence=0.94,
        verse="Phaladeepika Ch.6 v.70",
        tags=["phx", "parivartana_yoga", "exchange", "yoga", "kendra", "trikona", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX060",
        source="Phaladeepika",
        chapter="Ch.6",
        school="parashari",
        category="yoga",
        description=(
            "Mahabhagya Yoga: for men, birth in day + Sun above horizon + odd sign for Lagna, "
            "Moon, and Sun. For women, birth at night + even signs for all three. "
            "Phaladeepika: very fortunate destiny, high status, excellent character."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.6 v.75",
        tags=["phx", "mahabhagya_yoga", "yoga", "fortune", "parashari"],
        implemented=False,
    ),

    # ── Longevity and Medical Astrology (PHX061-072) ──────────────────────────
    RuleRecord(
        rule_id="PHX061",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Longevity determination: examine Lagna, Moon, and 8th house/lord. "
            "All three strong → full life (Purnayu: 100 years). "
            "Two strong, one weak → medium life (Madhyayu: 33-66). "
            "All weak → short life (Alpayu: <33)."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.8 v.1",
        tags=["phx", "longevity", "purnayu", "madhyayu", "alpayu", "lagna", "moon", "8th_house", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX062",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Maraka planets: lords of 2nd and 7th houses are Marakas. "
            "Planets associated with or aspected by Maraka lords also become Marakas. "
            "Phaladeepika: death in Maraka dasha when Maraka transit activates simultaneously."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.8 v.5",
        tags=["phx", "maraka", "longevity", "2nd_house", "7th_house", "death", "dasha", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX063",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Balarishta (infant mortality indicators): malefics in 1/8/12 without benefic aspect, "
            "Moon very weak (close to new moon) in 6/8/12. "
            "Phaladeepika: if birth Lagna lord and Moon are both afflicted → Balarishta present."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.8 v.10",
        tags=["phx", "balarishta", "infant", "longevity", "malefics", "moon", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX064",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Phaladeepika medical: each sign rules body parts and diseases. "
            "Afflicted planets in signs indicate disease in those body parts. "
            "Saturn in Aries → head/brain issues; Mars in Cancer → digestive disorders."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.8 v.20",
        tags=["phx", "medical", "body_parts", "disease", "signs", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX065",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Phaladeepika: planet karaka for each disease. Sun → heart/eyes. "
            "Moon → mind/lungs/fluids. Mars → blood/muscles/fever. "
            "Mercury → skin/nervous system. Jupiter → liver/diabetes. "
            "Venus → reproductive/kidneys. Saturn → bones/teeth/chronic."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.8 v.25",
        tags=["phx", "medical", "disease", "karaka", "sun", "moon", "mars", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX066",
        source="Phaladeepika",
        chapter="Ch.8",
        school="parashari",
        category="longevity",
        description=(
            "Phaladeepika: Tridosha analysis — Vata (Saturn, Rahu, Moon), "
            "Pitta (Sun, Mars, Ketu), Kapha (Jupiter, Venus, Mercury, Moon). "
            "Dominant planets in chart indicate constitution. "
            "Affliction of dominant planet → disorder of that dosha."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.8 v.30",
        tags=["phx", "medical", "tridosha", "vata", "pitta", "kapha", "parashari"],
        implemented=False,
    ),

    # ── Marriage and Children (PHX067-078) ────────────────────────────────────
    RuleRecord(
        rule_id="PHX067",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Marriage timing: marriage occurs in dasha of 7th lord, Venus (for men), "
            "Jupiter (for women), or in the dasha of the planet in 7th. "
            "Phaladeepika: the antardasha of that same planet gives the actual event."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.7 v.1",
        tags=["phx", "marriage", "timing", "dasha", "7th_house", "venus", "jupiter", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX068",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Mangala Dosha: Mars in 1st, 4th, 7th, 8th, or 12th from Lagna or Moon. "
            "Causes delay or difficulty in marriage; partner's health may suffer. "
            "Phaladeepika: Mangala Dosha cancelled if both partners have it."
        ),
        confidence=0.93,
        verse="Phaladeepika Ch.7 v.5",
        tags=["phx", "mangal_dosha", "mars", "marriage", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX069",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Spouse qualities from 7th house: Jupiter in 7th → wise, religious spouse. "
            "Venus in 7th → beautiful, pleasure-loving spouse. Moon → emotional, caring. "
            "Saturn in 7th → older, serious spouse; delay in marriage."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.7 v.10",
        tags=["phx", "marriage", "spouse", "7th_house", "jupiter", "venus", "moon", "saturn", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX070",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Children (Putra): 5th house, Jupiter, and 5th lord determine children. "
            "Jupiter in 5th or aspecting 5th → multiple children. "
            "Phaladeepika: 5th lord in 12th or afflicted → childlessness or delayed children."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.7 v.20",
        tags=["phx", "children", "5th_house", "jupiter", "fertility", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX071",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Son vs daughter: odd-sign Lagna and 5th house → more sons. "
            "Even-sign Lagna and 5th → more daughters. "
            "Phaladeepika: Jupiter + Sun combination in 5th → son; Moon + Venus → daughter."
        ),
        confidence=0.82,
        verse="Phaladeepika Ch.7 v.25",
        tags=["phx", "children", "son", "daughter", "5th_house", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX072",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="marriage",
        description=(
            "Second marriage: multiple planets in 7th or 7th lord in dual signs → "
            "more than one marriage. If Venus and Jupiter both afflict 7th → two marriages. "
            "Phaladeepika: Rahu in 7th → unconventional or foreign spouse/relationship."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.7 v.30",
        tags=["phx", "marriage", "second_marriage", "7th_house", "rahu", "parashari"],
        implemented=False,
    ),

    # ── Career and Profession (PHX073-082) ────────────────────────────────────
    RuleRecord(
        rule_id="PHX073",
        source="Phaladeepika",
        chapter="Ch.9",
        school="parashari",
        category="career",
        description=(
            "Career determination: strongest planet in 10th, 10th lord, and Sun. "
            "These three indicate profession. Mercury in 10th → business/communication. "
            "Jupiter in 10th → teaching/law/philosophy. Mars in 10th → military/surgery/engineering."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.9 v.1",
        tags=["phx", "career", "10th_house", "mercury", "jupiter", "mars", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX074",
        source="Phaladeepika",
        chapter="Ch.9",
        school="parashari",
        category="career",
        description=(
            "Career by Lagna: Aries lagna → pioneer, military, sports. Taurus → arts, finance. "
            "Gemini → communication, trade. Cancer → food, hospitality, care. "
            "Leo → government, administration. Virgo → health, analysis, service."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.9 v.5",
        tags=["phx", "career", "lagna", "aries", "taurus", "gemini", "cancer", "leo", "virgo", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX075",
        source="Phaladeepika",
        chapter="Ch.9",
        school="parashari",
        category="career",
        description=(
            "Career by Lagna (continued): Libra → law, beauty, balance. Scorpio → "
            "research, occult, medicine. Sagittarius → philosophy, travel, teaching. "
            "Capricorn → industry, management. Aquarius → technology, social work. "
            "Pisces → spiritual, arts, healing."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.9 v.6",
        tags=["phx", "career", "lagna", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX076",
        source="Phaladeepika",
        chapter="Ch.9",
        school="parashari",
        category="career",
        description=(
            "Wealth from career: 10th lord in 2nd → career brings direct wealth. "
            "10th lord in 11th → career brings long-term gains. "
            "Phaladeepika: 2nd, 10th, and 11th house lords in mutual relationship → "
            "exceptional financial success through career."
        ),
        confidence=0.89,
        verse="Phaladeepika Ch.9 v.10",
        tags=["phx", "career", "wealth", "10th_house", "2nd_house", "11th_house", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX077",
        source="Phaladeepika",
        chapter="Ch.9",
        school="parashari",
        category="career",
        description=(
            "Government/authority career: Sun strong in kendra or 10th, aspected by Jupiter → "
            "government service or public administration. "
            "Sun + Saturn combination in 10th → military or disciplinary forces."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.9 v.15",
        tags=["phx", "career", "government", "sun", "jupiter", "saturn", "10th_house", "parashari"],
        implemented=False,
    ),

    # ── Dasha Results (PHX078-090) ─────────────────────────────────────────────
    RuleRecord(
        rule_id="PHX078",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari Dasha: Ketu 7 years, Venus 20, Sun 6, Moon 10, Mars 7, "
            "Rahu 18, Jupiter 16, Saturn 19, Mercury 17. Total = 120 years. "
            "Phaladeepika confirms this sequence and provides results for each dasha."
        ),
        confidence=0.98,
        verse="Phaladeepika Ch.10 v.1",
        tags=["phx", "vimshottari", "dasha", "sequence", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX079",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Benefic dasha lord in kendra/trikona → auspicious period. "
            "Malefic dasha lord in kendra/trikona → also good (Kendradhipati modified). "
            "Phaladeepika: results depend on dasha lord's sign, house, and aspects."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.10 v.5",
        tags=["phx", "dasha", "benefic", "malefic", "kendra", "trikona", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX080",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Sun dasha results: if Sun is well-placed (own/exalt/kendra) → government honors, "
            "health, father's blessings. If afflicted → health issues, father's problems, "
            "conflicts with authority. Sun dasha begins career in many charts."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.10 v.10",
        tags=["phx", "dasha", "sun", "government", "father", "career", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX081",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Jupiter dasha: best period for marriage, children, education, wealth, and dharma. "
            "Phaladeepika: Jupiter dasha in trikona → spiritual growth and prosperity. "
            "Even if Jupiter is in dusthana, its dasha brings expansion of that area."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.10 v.20",
        tags=["phx", "dasha", "jupiter", "marriage", "children", "wealth", "dharma", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX082",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Saturn dasha: if Saturn is well-placed → career peak, property acquisition, "
            "discipline brings reward. If afflicted → chronic health issues, isolation, loss. "
            "Phaladeepika: Saturn's 19-year dasha is the most transformative."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.10 v.25",
        tags=["phx", "dasha", "saturn", "career", "property", "isolation", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX083",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Rahu dasha: results of the planet Rahu is with or aspected by. "
            "Also like the lord of the sign Rahu occupies. "
            "Phaladeepika: Rahu in kendra with Jupiter → Guru Chandal modified → "
            "unconventional but successful in foreign/technical fields."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.10 v.30",
        tags=["phx", "dasha", "rahu", "foreign", "unconventional", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX084",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Ketu dasha: spiritual turning points, detachment, past-life karma surfaces. "
            "Results like the planet Ketu is with or the sign lord. "
            "Phaladeepika: Ketu in own sign or with benefic → liberation path opens."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.10 v.35",
        tags=["phx", "dasha", "ketu", "spiritual", "liberation", "karma", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX085",
        source="Phaladeepika",
        chapter="Ch.10",
        school="parashari",
        category="dasha",
        description=(
            "Antardasha (sub-period) principle: the sub-lord must be friendly to "
            "the main dasha lord for the sub-period to give good results. "
            "Phaladeepika: friend's antardasha in enemy's main dasha → mixed results."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.10 v.40",
        tags=["phx", "dasha", "antardasha", "sub_period", "friendship", "parashari"],
        implemented=False,
    ),

    # ── Transit (Gochara) Rules (PHX086-095) ──────────────────────────────────
    RuleRecord(
        rule_id="PHX086",
        source="Phaladeepika",
        chapter="Ch.11",
        school="parashari",
        category="transit",
        description=(
            "Gochara results from natal Moon: transits are evaluated from the natal Moon sign. "
            "Jupiter transiting 1/2/4/5/7/8/9/10/11 from Moon → varying results. "
            "Phaladeepika: Jupiter in 2nd and 11th from Moon → best transit positions."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.11 v.1",
        tags=["phx", "transit", "gochara", "jupiter", "moon", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX087",
        source="Phaladeepika",
        chapter="Ch.11",
        school="parashari",
        category="transit",
        description=(
            "Saturn transit (Sade Sati): Saturn in 12th, 1st, and 2nd from natal Moon. "
            "7.5 years total. Phaladeepika: challenges in finance, health, and relationships. "
            "The middle phase (Saturn over natal Moon) is most intense."
        ),
        confidence=0.93,
        verse="Phaladeepika Ch.11 v.5",
        tags=["phx", "transit", "saturn", "sade_sati", "moon", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX088",
        source="Phaladeepika",
        chapter="Ch.11",
        school="parashari",
        category="transit",
        description=(
            "Ashtama Shani: Saturn transiting 8th from natal Moon. "
            "Phaladeepika: most difficult single transit — health crises, major obstacles, losses. "
            "Lasts approximately 2.5 years."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.11 v.8",
        tags=["phx", "transit", "saturn", "ashtama_shani", "moon", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX089",
        source="Phaladeepika",
        chapter="Ch.11",
        school="parashari",
        category="transit",
        description=(
            "Jupiter transit through 1st from natal Moon (Janma Rashi) → new beginnings, "
            "spiritual growth, health improvement. Phaladeepika calls this 'Guruchandrama Yoga' "
            "in transit — particularly beneficial for marriage and children."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.11 v.12",
        tags=["phx", "transit", "jupiter", "moon", "marriage", "children", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX090",
        source="Phaladeepika",
        chapter="Ch.11",
        school="parashari",
        category="transit",
        description=(
            "Mars transit (Kuja Gochara): Mars in 1/2/4/7/8/12 from natal Moon → "
            "inauspicious (accidents, conflicts, health). Best Mars positions: 3/6/10/11 from Moon. "
            "Phaladeepika: Mars in 3rd from Moon → physical energy peak; excellent for competitive activities."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.11 v.15",
        tags=["phx", "transit", "mars", "moon", "gochara", "parashari"],
        implemented=False,
    ),

    # ── Divisional Charts (PHX091-100) ────────────────────────────────────────
    RuleRecord(
        rule_id="PHX091",
        source="Phaladeepika",
        chapter="Ch.4",
        school="parashari",
        category="varga",
        description=(
            "Shodashavarga: 16 divisional charts used in Phaladeepika. "
            "D1(Rashi), D2(Hora), D3(Drekkana), D4(Chaturthamsha), D7(Saptamsha), "
            "D9(Navamsha), D10(Dashamsha), D12(Dwadashamsha), D16(Shodashamsha), "
            "D20(Vimshamsha), D24(Siddhamsha), D27(Nakshatramsha), D30(Trimsamsha), "
            "D40(Khavedamsha), D45(Akshavedamsha), D60(Shastiamsha)."
        ),
        confidence=0.95,
        verse="Phaladeepika Ch.4 v.1",
        tags=["phx", "shodashavarga", "varga", "divisional_charts", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX092",
        source="Phaladeepika",
        chapter="Ch.4",
        school="parashari",
        category="varga",
        description=(
            "Navamsha (D9): the most important divisional chart after D1. "
            "Shows the soul's quality of relationships, dharma, and ultimate fate. "
            "Phaladeepika: if D1 and D9 both confirm an event → near-certain manifestation."
        ),
        confidence=0.97,
        verse="Phaladeepika Ch.4 v.5",
        tags=["phx", "navamsha", "d9", "varga", "marriage", "dharma", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX093",
        source="Phaladeepika",
        chapter="Ch.4",
        school="parashari",
        category="varga",
        description=(
            "Dashamsha (D10): career and social achievement divisional chart. "
            "10th house in D10, D10 Lagna lord, and Sun in D10 determine career success. "
            "Phaladeepika: D10 analysis required for accurate career timing."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.4 v.10",
        tags=["phx", "dashamsha", "d10", "varga", "career", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX094",
        source="Phaladeepika",
        chapter="Ch.4",
        school="parashari",
        category="varga",
        description=(
            "Saptamsha (D7): children and progeny divisional chart. "
            "D7 Lagna and its lord, 5th in D7, and Jupiter in D7 determine children. "
            "Phaladeepika: both D1 5th and D7 5th must be examined for complete picture."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.4 v.15",
        tags=["phx", "saptamsha", "d7", "varga", "children", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX095",
        source="Phaladeepika",
        chapter="Ch.4",
        school="parashari",
        category="varga",
        description=(
            "Trimsamsha (D30): misfortunes and evil in the chart. "
            "Malefics in D30 Lagna → prone to accidents. D30 examined for disease, "
            "accidents, and evil effects. Phaladeepika: D30 most important for medical analysis."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.4 v.20",
        tags=["phx", "trimsamsha", "d30", "varga", "misfortune", "medical", "parashari"],
        implemented=False,
    ),

    # ── Special Principles (PHX096-110) ───────────────────────────────────────
    RuleRecord(
        rule_id="PHX096",
        source="Phaladeepika",
        chapter="Ch.12",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika Kendradhipati dosha: lords of kendras (1/4/7/10) when benefics "
            "lose their beneficence (become mixed). Jupiter as 7th lord loses some beneficence. "
            "Venus as 4th lord similarly. Exception: 1st house lord is always beneficial."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.12 v.1",
        tags=["phx", "kendradhipati", "kendra", "benefic", "dosha", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX097",
        source="Phaladeepika",
        chapter="Ch.12",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika on functional benefics: for each Lagna, certain planets "
            "become functional benefics (lords of 1/5/9/trikona lords). "
            "Natural benefics in dusthanas can become functionally malefic if dusthana lords."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.12 v.5",
        tags=["phx", "functional_benefic", "functional_malefic", "lagna", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX098",
        source="Phaladeepika",
        chapter="Ch.12",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika Hora (D2): odd signs → solar hora (Sun's half), even → lunar hora. "
            "Birth in solar hora → male traits, leadership. Lunar hora → nurturing, artistic. "
            "Used to confirm wealth analysis."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.12 v.10",
        tags=["phx", "hora", "d2", "varga", "wealth", "solar_hora", "lunar_hora", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX099",
        source="Phaladeepika",
        chapter="Ch.12",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika: Drekkana (D3) for siblings. Each drekkana is 10°. "
            "D3 1st, 3rd, and planets in D3 determine siblings' wellbeing. "
            "Malefics in D3 Lagna → siblings face hardship."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.12 v.15",
        tags=["phx", "drekkana", "d3", "varga", "siblings", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX100",
        source="Phaladeepika",
        chapter="Ch.12",
        school="parashari",
        category="special_principle",
        description=(
            "Dwadashamsha (D12): parents, ancestry. D12 9th house and lord → father. "
            "D12 4th house and lord → mother. Malefics in D12 Lagna → family hardships. "
            "Phaladeepika: used to confirm parent-related predictions."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.12 v.20",
        tags=["phx", "dwadashamsha", "d12", "varga", "father", "mother", "parents", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX101",
        source="Phaladeepika",
        chapter="Ch.13",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika: Ashtakavarga (8-source strength grid) for transit analysis. "
            "Each sign gets points from each of 8 sources (7 planets + Lagna). "
            "Transit through sign with 5+ points → favorable; 3 or less → unfavorable."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.13 v.1",
        tags=["phx", "ashtakavarga", "transit", "strength", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX102",
        source="Phaladeepika",
        chapter="Ch.13",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika: Sarvashtakavarga (combined 8-source grid). "
            "Total points across all 12 signs = 337 always. "
            "Signs with 28+ points in Sarvashtakavarga → very favorable life areas."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.13 v.5",
        tags=["phx", "sarvashtakavarga", "ashtakavarga", "strength", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX103",
        source="Phaladeepika",
        chapter="Ch.14",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika: Shadbala (six-fold strength) for planets. "
            "Components: Sthana (positional), Dig (directional), Kala (temporal), "
            "Chesta (motional), Naisargika (natural), Drik (aspectual) Bala. "
            "Total > 7 Rupas → strong planet; < 5 Rupas → weak."
        ),
        confidence=0.93,
        verse="Phaladeepika Ch.14 v.1",
        tags=["phx", "shadbala", "strength", "planet", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX104",
        source="Phaladeepika",
        chapter="Ch.14",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika Bhava Bala (house strength): each house has Bhava Bala "
            "based on the occupants, the lord's Shadbala, and aspects. "
            "Lagna Bala (strength of 1st house) is most critical overall indicator."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.14 v.10",
        tags=["phx", "bhava_bala", "house_strength", "lagna", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX105",
        source="Phaladeepika",
        chapter="Ch.15",
        school="parashari",
        category="special_principle",
        description=(
            "Phaladeepika: Ishta-Kashta Phala (beneficial-harmful fruits). "
            "Each planet's exaltation and debilitation on a scale 0-60. "
            "Ishta (benefic value) + Kashta (malefic value) = 60 always per planet."
        ),
        confidence=0.83,
        verse="Phaladeepika Ch.15 v.1",
        tags=["phx", "ishta_phala", "kashta_phala", "planetary_strength", "parashari"],
        implemented=False,
    ),

    # ── Muhurta and Electional Astrology (PHX106-110) ─────────────────────────
    RuleRecord(
        rule_id="PHX106",
        source="Phaladeepika",
        chapter="Ch.16",
        school="parashari",
        category="muhurta",
        description=(
            "Phaladeepika Muhurta: most auspicious day for marriage is when Moon "
            "is in Rohini, Mrigashira, Magha, Uttara Phalguni, Hasta, Swati, Anuradha, "
            "Mula, Uttara Ashadha, Uttara Bhadrapada, or Revati."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.16 v.1",
        tags=["phx", "muhurta", "marriage", "nakshatra", "moon", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX107",
        source="Phaladeepika",
        chapter="Ch.16",
        school="parashari",
        category="muhurta",
        description=(
            "Phaladeepika Muhurta: auspicious tithi (lunar day) for new ventures: "
            "2nd, 3rd, 5th, 7th, 10th, 11th, 13th of either fortnight. "
            "Avoid: 4th, 8th, 9th, 14th, Amavasya (new moon), Poornima (full moon) for beginnings."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.16 v.5",
        tags=["phx", "muhurta", "tithi", "auspicious", "new_ventures", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX108",
        source="Phaladeepika",
        chapter="Ch.16",
        school="parashari",
        category="muhurta",
        description=(
            "Phaladeepika: Panchanga (5-limb electional system). "
            "Tithi (lunar day), Vara (weekday), Nakshatra (Moon's star), "
            "Yoga (Sun-Moon combined), Karana (half-tithi). "
            "All 5 must be favorable for the best Muhurta."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.16 v.10",
        tags=["phx", "muhurta", "panchanga", "tithi", "vara", "nakshatra", "yoga", "karana", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX109",
        source="Phaladeepika",
        chapter="Ch.16",
        school="parashari",
        category="muhurta",
        description=(
            "Phaladeepika: Abhijit Muhurta — the 8th muhurta of the day (approximately midday). "
            "Lasts approximately 48 minutes around local noon. "
            "Abhijit Muhurta overrides most inauspicious combinations."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.16 v.15",
        tags=["phx", "muhurta", "abhijit", "midday", "auspicious", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX110",
        source="Phaladeepika",
        chapter="Ch.16",
        school="parashari",
        category="muhurta",
        description=(
            "Phaladeepika: Rahu Kala and Gulikakal — inauspicious periods each day. "
            "Rahu Kala: 1.5 hours each day (varies by weekday). "
            "Avoid starting any new enterprise during Rahu Kala."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.16 v.20",
        tags=["phx", "muhurta", "rahu_kala", "gulikakal", "inauspicious", "parashari"],
        implemented=False,
    ),

    # ── Final Synthesis and Philosophy (PHX111-120) ───────────────────────────
    RuleRecord(
        rule_id="PHX111",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika synthesis: prediction requires examining D1 + D9 + relevant varga. "
            "An event is certain when D1, D9, and relevant varga all confirm. "
            "One confirmation = possibility; two = probability; three = certainty."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.17 v.1",
        tags=["phx", "synthesis", "d1", "d9", "varga", "three_chart", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX112",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: the astrologer must examine the chart holistically. "
            "A malefic planet in an angular house may cause harm to that house "
            "but simultaneously improve adjacent houses through its aspects."
        ),
        confidence=0.88,
        verse="Phaladeepika Ch.17 v.5",
        tags=["phx", "synthesis", "holistic", "malefic", "angular", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX113",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: strong Lagna and Lagna lord override many afflictions. "
            "If Lagna lord is exalted and unafflicted → most chart afflictions are mitigated. "
            "This is the fundamental protective principle of the chart."
        ),
        confidence=0.91,
        verse="Phaladeepika Ch.17 v.10",
        tags=["phx", "synthesis", "lagna", "lagna_lord", "protection", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX114",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: the Sun (Atmakaraka) and Moon (Manoskaraka) are the "
            "two luminaries that hold the chart together. Their relationship (Full Moon → "
            "open; New Moon → concentrated) colors the entire natal chart's expression."
        ),
        confidence=0.89,
        verse="Phaladeepika Ch.17 v.15",
        tags=["phx", "synthesis", "sun", "moon", "atmakaraka", "luminaries", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX115",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: Naisargika (natural) and Tatkalik (temporal) friendship. "
            "Natural friendship is permanent; temporal friendship is based on position. "
            "A planet that is both natural and temporal friend → 'Adhi Mitra' (best friend)."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.17 v.20",
        tags=["phx", "naisargika", "tatkalik", "friendship", "adhi_mitra", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX116",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: 'Ishtaphala' principle — the benefic results of a planet "
            "are proportional to its Shadbala (especially Ishta value). "
            "High Ishta + in trikona from Lagna → maximum benefic results."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.17 v.25",
        tags=["phx", "ishtaphala", "shadbala", "trikona", "benefic", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX117",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika: 'Yogaphala' — the combined result of all yogas in a chart. "
            "If multiple Raja Yogas operate simultaneously → amplified results. "
            "If Raja Yoga and Daridra Yoga both present → rises and falls alternately."
        ),
        confidence=0.87,
        verse="Phaladeepika Ch.17 v.30",
        tags=["phx", "yogaphala", "raja_yoga", "daridra_yoga", "combined_result", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX118",
        source="Phaladeepika",
        chapter="Ch.17",
        school="parashari",
        category="synthesis",
        description=(
            "Phaladeepika unique: 'Manushya-Jataka-Paddhati' — human birth chart reading "
            "follows a specific sequence: first Lagna, then Moon, then Sun, then planets "
            "in order of strength. This priority sequence determines prediction weight."
        ),
        confidence=0.85,
        verse="Phaladeepika Ch.17 v.35",
        tags=["phx", "methodology", "sequence", "lagna", "moon", "sun", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX119",
        source="Phaladeepika",
        chapter="Ch.18",
        school="parashari",
        category="philosophy",
        description=(
            "Phaladeepika: Mantreswara's concluding teaching — astrology reveals "
            "the fruit of past karma (Prarabdha) but not the entire destiny. "
            "Free will (Purushakara) can modify the severity of karmic results through effort."
        ),
        confidence=0.90,
        verse="Phaladeepika Ch.18 v.1",
        tags=["phx", "philosophy", "karma", "prarabdha", "free_will", "purushakara", "parashari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PHX120",
        source="Phaladeepika",
        chapter="Ch.18",
        school="parashari",
        category="philosophy",
        description=(
            "Phaladeepika final verse: 'Jyotisham Vedachakshu' — astrology is the eye "
            "of the Veda. Without this eye, the Vedas cannot guide effectively. "
            "The astrologer who uses this knowledge for dharmic purposes attains liberation."
        ),
        confidence=0.92,
        verse="Phaladeepika Ch.18 v.10",
        tags=["phx", "philosophy", "jyotisha", "veda", "dharma", "liberation", "parashari"],
        implemented=False,
    ),
]

for rule in _RULES:
    PHALADEEPIKA_EXHAUSTIVE_REGISTRY.add(rule)
