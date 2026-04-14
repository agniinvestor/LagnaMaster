# Practitioner Review Checklist — LagnaMaster Computation Modules

> **For:** Jyotish practitioner/teacher review
> **Purpose:** Verify whether 28 computation modules correctly implement classical rules before wiring them into the prediction pipeline
> **What we need:** Your expert eye on whether the astrological logic is correct per the source texts. We are NOT asking about code — we are asking about whether the system's understanding of Jyotish is right.

---

## How this document works

For each module group below, we describe:
- **What the system currently computes**
- **Which source texts it claims to follow**
- **Specific questions where we need practitioner confirmation**

Please mark each question: ✅ correct / ❌ wrong / ⚠️ partially correct / ❓ depends on school

---

## 1. YOGA DETECTION

**Modules:** yogas_extended, yogas_graha, yogas_pvrnr, nabhasa_yogas
**Claimed sources:** BPHS Ch.35-36, Saravali Ch.15-20, Phaladeepika Ch.6

### Questions for review:

**1.1 Gajakesari Yoga**
- [ ] Our implementation: Jupiter in kendra (1/4/7/10) from Moon. Is this correct per BPHS?
- [ ] Do we need to check: Jupiter not debilitated? Jupiter not combust? Jupiter not in enemy sign?
- [ ] Some practitioners say Jupiter must also not be aspected by malefics. Is this in the verse or practitioner convention?

**1.2 Budhaditya Yoga**
- [ ] Our implementation: Sun and Mercury in the same sign. Is same-sign sufficient or must they be in the same house (sign vs bhava)?
- [ ] Does Mercury need to be unaffilicted/uncombusted for this yoga to be effective? (Mercury is almost always near Sun)
- [ ] Should we check: Mercury not within combustion degrees but in the same sign?

**1.3 Chandra-Mangala Yoga**
- [ ] Our implementation: Moon and Mars in the same house. Correct?
- [ ] Does mutual aspect (7th from each other) also count?
- [ ] Should Moon be waxing for this to be positive? Some texts say waning Moon + Mars is negative.

**1.4 Nabhasa Yogas (32 types per BPHS Ch.35)**
- [ ] We implement: Yava, Chakra, Samudra, Gola, Shringataka, Kedara, Shoola, Yuga, Musala, Nala, Dama, Pasha, Rajju, etc.
- [ ] For Ashraya yogas (Rajju, Musala, Nala): do we correctly count only the 7 visible planets (Sun through Saturn) or include Rahu/Ketu?
- [ ] For Dala yogas (Mala, Sarpa): is it correct that ALL kendras must be occupied for Mala, and ALL panaphara houses for Sarpa?
- [ ] How many of the 32 Nabhasa yogas should a correct implementation detect? BPHS says they are mutually exclusive within subgroups — is this true?

**1.5 Raja Yogas**
- [ ] Our implementation: lord of a kendra (1/4/7/10) conjunct or mutually aspecting lord of a trikona (1/5/9). Correct per BPHS Ch.41?
- [ ] Should kendradhipati dosha (benefic owning a kendra becomes neutral) reduce the yoga strength?
- [ ] For dual lordship (e.g., Saturn owning both a kendra and a trikona for Taurus/Libra lagna) — is this a stronger or different type of raja yoga?

**1.6 Pancha Mahapurusha Yogas**
- [ ] Our implementation: Mars/Mercury/Jupiter/Venus/Saturn in own sign or exaltation AND in a kendra from lagna. Correct?
- [ ] Must the kendra be from lagna specifically, or can it be from Moon?
- [ ] Are there cancellation conditions (e.g., planet combust, or in conjunction with a malefic)?

**1.7 Yoga cancellation (Bhanga)**
- [ ] When a yoga exists but a cancellation condition also exists — does the yoga disappear entirely, or is it weakened?
- [ ] For Neecha Bhanga Raja Yoga: we check 6 conditions per BPHS. Are these the correct 6?
  1. Lord of the sign of debilitation in kendra from lagna or Moon
  2. Lord of the exaltation sign in kendra from lagna or Moon
  3. Planet receiving aspect from the sign lord of debilitation
  4. Planet receiving aspect from the exaltation lord
  5. Planet in parivartana (exchange) with the sign lord
  6. Debilitated planet exalted in navamsha

**1.8 General yoga questions**
- [ ] Should yogas be evaluated from all three references (lagna, Moon, Sun) or only from lagna?
- [ ] When BPHS and Saravali disagree on conditions for the same yoga, which takes precedence in Parashari school?
- [ ] Are yogas evaluated in divisional charts (D9, D10) or only in the rashi chart (D1)?

---

## 2. DIVISIONAL CHART (VARGA) ANALYSIS

**Modules:** divisional_charts, sapta_varga, varga
**Claimed sources:** BPHS Ch.6-8

### Questions for review:

**2.1 Navamsha (D9)**
- [ ] We compute D9 sign as: for odd signs, start from the same sign and count forward by navamsha number. For even signs, start from the 9th sign and count forward. Correct per BPHS Ch.6?
- [ ] For marriage analysis: should we examine the 7th house from D9 lagna, or the 7th lord from D1 in D9?
- [ ] Is "planet in same sign in D1 and D9" (vargottama) a significant strength indicator that should affect ALL predictions for that planet?

**2.2 Dashamsha (D10)**
- [ ] We compute D10 sign using: for odd signs, count from the same sign. For even signs, count from the 9th sign. Each 3° = one dashamsha. Correct?
- [ ] For career analysis: is the 10th house from D10 lagna the primary house, or is it the placement of the 10th lord from D1 in D10?

**2.3 Vimshopak Bala (strength across vargas)**
- [ ] We compute 7-varga Vimshopak (D1=3, D2=2, D3=2, D7=1, D9=5, D10=3, D12=4, total=20). Are these weights correct per BPHS?
- [ ] Alternative: 16-varga Shodasavarga. Which should a Parashari practitioner primarily use?
- [ ] Is Vimshopak bala the correct measure for "how strongly a planet delivers its promise"?

**2.4 Which varga for which life domain?**
- [ ] D9 (Navamsha) → marriage and dharma. Correct?
- [ ] D10 (Dashamsha) → career and profession. Correct?
- [ ] D7 (Saptamsha) → children and progeny. Correct?
- [ ] D4 (Chaturthamsha) → property and vehicles. Correct?
- [ ] D2 (Hora) → wealth. Correct? Or is D2 too crude for wealth analysis?
- [ ] D3 (Drekkana) → siblings and courage. Correct?
- [ ] D12 (Dwadashamsha) → parents. Correct?
- [ ] Are there other varga-domain mappings we are missing?

---

## 3. HOUSE STRENGTH AND PLANET STRENGTH

**Modules:** bhava_bala, ishta_kashta, shadbala_patches, dig_bala
**Claimed sources:** BPHS Ch.27-28

### Questions for review:

**3.1 Shadbala (six-fold strength)**
- [ ] Our six components: Sthana Bala, Dig Bala, Kala Bala, Chesta Bala, Naisargika Bala, Drik Bala. Correct and complete?
- [ ] Sthana Bala sub-components: Uchcha Bala, Saptavargaja Bala, Ojha-Yugma, Kendradi, Drekkana. Are all five correct?
- [ ] For Kala Bala: we include Nathonnata, Paksha, Tribhaga, Vara, Hora, Masa, Abda, Ayana. Is this the complete list?
- [ ] Minimum Shadbala requirements (Rupas): Sun=6.5, Moon=6.0, Mars=5.0, Mercury=7.0, Jupiter=6.5, Venus=5.5, Saturn=5.0. Are these the BPHS values?

**3.2 Bhava Bala (house strength)**
- [ ] Is Bhava Bala = Bhavadhipati Bala + Bhava Drishti Bala + Bhava Dig Bala? Are there other components?
- [ ] How should Bhava Bala interact with planet strength? Does a strong planet in a weak house deliver partially, or does house strength override?

**3.3 Ishta Kashta (benefic/malefic strength ratio)**
- [ ] Ishta Phala = Uchcha Bala × Chesta Bala. Correct formula?
- [ ] Kashta Phala = (60 - Uchcha Bala) × (60 - Chesta Bala) / 60. Correct?
- [ ] Is this the primary indicator for "how much good vs harm a planet does"?

**3.4 Dig Bala (directional strength)**
- [ ] Jupiter/Mercury strongest in lagna (East). Correct?
- [ ] Sun/Mars strongest in 10th house (South). Correct?
- [ ] Saturn strongest in 7th house (West). Correct?
- [ ] Moon/Venus strongest in 4th house (North). Correct?

---

## 4. TRANSIT ANALYSIS (GOCHARA)

**Modules:** gochara, double_transit, av_transit, bhava_and_transit, transit_quality_advanced
**Claimed sources:** BPHS Ch.64-65, Phaladeepika transit chapters

### Questions for review:

**4.1 Basic transit framework**
- [ ] Transit effects are judged from the NATAL MOON sign (not lagna). Correct per BPHS?
- [ ] Or should we also consider transits from lagna for certain purposes?
- [ ] Jupiter transiting the natal lagna sign = broadly favorable. Is this an oversimplification?

**4.2 Vedha (obstruction)**
- [ ] When a benefic planet transits a favorable house but a malefic occupies the vedha point, the benefic result is obstructed. Correct?
- [ ] Vedha pairs per BPHS: Sun/Saturn are mutual vedha. Jupiter/Mercury are mutual vedha. Are we using the correct vedha pairs?
- [ ] Does vedha apply to ALL transits or only to specific planet pairs?

**4.3 Double transit (Jupiter + Saturn)**
- [ ] KN Rao's principle: a major event happens when BOTH Jupiter and Saturn aspect/occupy a house simultaneously. Is this widely accepted?
- [ ] Should double transit be from Moon sign or from lagna?
- [ ] For marriage: double transit over 7th house. For career: double transit over 10th house. Are these the correct house assignments?

**4.4 Sade Sati (Saturn over Moon)**
- [ ] Saturn transiting the 12th, 1st, and 2nd houses from natal Moon = 7.5 year Sade Sati. Correct?
- [ ] Is the effect uniformly negative, or does it depend on Saturn's functional nature for that lagna?
- [ ] Does Saturn in own sign or exalted sign during Sade Sati reduce the negative effects?

**4.5 Ashtakavarga in transit**
- [ ] When Saturn transits a sign with high SAV (Sarvashtakavarga) bindus (≥28), the transit is less harmful. Correct interpretation?
- [ ] When Jupiter transits a sign where its BAV (Bhinnashtakavarga) has ≥5 bindus, the transit gives good results. Correct?
- [ ] Should we use BAV of the transiting planet or SAV of the sign?

---

## 5. JAIMINI SYSTEM

**Modules:** chara_karak, jaimini_full, karakamsha_analysis
**Claimed sources:** Jaimini Sutras

### Questions for review:

**5.1 Chara Karakas (temporal significators)**
- [ ] We rank the 7 planets (Sun through Saturn, excluding Rahu/Ketu) by degree within their sign. Highest degree = Atmakaraka. Correct?
- [ ] Some practitioners use 8 planets (including Rahu). Which system should we follow?
- [ ] Rahu's degree: should it be counted as 30° minus its degree (reverse counting)? Or its actual degree?

**5.2 Karakamsha**
- [ ] Karakamsha = the navamsha sign of the Atmakaraka, placed in the rashi chart. Correct?
- [ ] Planets in or aspecting the karakamsha indicate the native's soul-level purpose. Is this the standard interpretation?
- [ ] Should karakamsha analysis be presented alongside Parashari analysis or kept separate?

**5.3 Jaimini Rashi Drishti (sign aspects)**
- [ ] Movable signs aspect fixed signs (except the adjacent one). Fixed signs aspect movable signs (except the adjacent one). Dual signs aspect each other. Correct?
- [ ] Should Jaimini rashi drishti be used in convergence alongside Parashari graha drishti, or are they alternative frameworks that shouldn't be mixed?

**5.4 Chara Dasha**
- [ ] We compute sign-based dasha periods. Starting sign depends on whether the lagna is odd/even. Correct?
- [ ] Duration of each sign's period: depends on the distance of the sign lord from the sign. Is this the correct methodology?
- [ ] Should we use Iranganti Rangacharya's commentary or KN Rao's interpretation for computation?

---

## 6. DASHA SYSTEM

**Modules:** dasha_activation, ashtottari_dasha, vimshottari_dasa
**Claimed sources:** BPHS Ch.46-47

### Questions for review:

**6.1 Vimshottari Dasha**
- [ ] 120-year cycle, starting nakshatra determined by Moon's longitude. Balance computed from Moon's position within the nakshatra. Correct?
- [ ] Planet-years: Sun=6, Moon=10, Mars=7, Rahu=18, Jupiter=16, Saturn=19, Mercury=17, Ketu=7, Venus=20. Correct per BPHS?
- [ ] Antardasha proportions: sub-period of planet X within MD of planet Y = (X's years / 120) × Y's years. Correct?

**6.2 Dasha activation principle**
- [ ] During a planet's mahadasha, the houses it LORDS are activated. Correct?
- [ ] During antardasha of planet B within MD of planet A: do BOTH planet A's houses and planet B's houses activate? Or only B's?
- [ ] Does the planet's placement (which house it sits in) also get activated during its dasha?

**6.3 Ashtottari Dasha**
- [ ] 108-year cycle. Applicable when Rahu is in a kendra or trikona. Correct applicability condition?
- [ ] Should we offer this as an alternative dasha or use it only when the applicability condition is met?

---

## 7. BIRTH TIME SENSITIVITY

**Module:** confidence_model
**Source:** Astronomical/statistical (not text-based)

### Questions for review:

**7.1 Lagna boundary sensitivity**
- [ ] If lagna is within 1° of a sign boundary, a 5-minute birth time error changes the entire chart interpretation. Should we flag this prominently?
- [ ] What threshold do you use in practice to flag birth time sensitivity? 1°? 2°? 3°?

**7.2 Moon nakshatra boundary**
- [ ] If Moon is near a nakshatra boundary, the mahadasha sequence may change. We flag this when Moon is within 0.5° of a nakshatra cusp. Is 0.5° the right threshold?

**7.3 How do you handle uncertain birth times in practice?**
- [ ] Do you compute charts for ±15 minutes and compare?
- [ ] Do you use life events to rectify the birth time first?
- [ ] Should the system refuse to give predictions for boundary lagna charts, or just add a warning?

---

## 8. GENERAL METHODOLOGY QUESTIONS

**8.1 Whole sign vs Bhava Chalit**
- [ ] We use whole-sign houses for lordship and placement. Bhava Chalit is available but not primary. Is this correct for Parashari analysis?
- [ ] Should any specific analysis (e.g., house strength) use Bhava Chalit instead of whole-sign?

**8.2 Functional benefic/malefic classification**
- [ ] We follow BPHS Ch.34 (Santhanam) for functional benefic/malefic per lagna. Is there a better or more widely accepted source?
- [ ] For Taurus lagna: Mercury, Venus, Saturn are functional benefics. Jupiter, Moon, Mars are functional malefics. Sun is neutral. Does this match your understanding?

**8.3 Convergence principle**
- [ ] Our system counts "how many independent signals confirm a prediction" — D1 analysis, D9 confirmation, corpus text evidence, yoga presence, timing activation. A prediction confirmed by 5 independent signals is stronger than one confirmed by 2. Is this how you evaluate in practice?
- [ ] When natal promise (D1) is strong but D9 does not confirm — how do you interpret this? Weakened promise? Delayed manifestation? Different domain?

**8.4 Practitioner Decision Workflow (MOST IMPORTANT SECTION)**

Our system currently treats all signals (yogas, dashas, transits, strength)
as **parallel and additive** — it counts how many signals agree. A pre-review
suggests this is wrong. Practitioners think **hierarchically** — some checks
gate others, some override others, and the ORDER of evaluation matters.

**Please describe your actual workflow:**

- [ ] Do you follow a fixed sequence when reading a chart? What is it? (e.g., "lagna lord first, then Moon, then karaka, then yogas, then dasha")
- [ ] What do you check FIRST before anything else?
- [ ] What must be TRUE in the natal chart before you even look at timing? (the "natal promise" gate)
- [ ] If the natal promise is absent (e.g., weak 7th house + afflicted Venus + no yoga for marriage) — do you still predict marriage during a relevant dasha? Or do you say "no promise, no event regardless of timing"?
- [ ] What conditions cause you to IGNORE an otherwise valid yoga?
- [ ] What factors OVERRIDE others? (e.g., "strong Jupiter protects even in bad placements", "afflicted Moon destabilizes the entire chart")
- [ ] Which 3-5 signals matter MOST for:
  - Marriage?
  - Career?
  - Wealth?
  - Health?
  - Children?
- [ ] What do you NEVER rely on alone? (e.g., "yogas alone mean nothing without dasha activation")
- [ ] What are your "shortcut heuristics" not found in any textbook?
- [ ] Which things do Jyotish software packages typically get wrong?
- [ ] Do you always check from BOTH lagna AND Moon? Or only specific things from Moon?

**8.5 Karaka-Based Analysis**

Our system focuses on house lords. Pre-review suggests karaka analysis
is equally important but we treat it as secondary.

- [ ] For marriage: do you check Venus (naisargika karaka for marriage) as a SEPARATE lens alongside 7th lord? What specifically do you check about Venus?
- [ ] For children: do you check Jupiter separately? 5th from Jupiter?
- [ ] For career: do you check Sun (authority), Saturn (service), Mercury (commerce) as separate karakas?
- [ ] "Check the house from the karaka" — e.g., 7th from Venus for marriage refinement. Is this standard practice? How much weight vs 7th from lagna?
- [ ] Chara karakas (Jaimini) — Darakaraka for spouse, Putrakaraka for children. Do you use these alongside Parashari karakas? Or only in Jaimini analysis?

**8.6 Unified Planet Condition Assessment**

We check combustion, dignity, retrograde, aspects, etc. as separate flags.
Pre-review says practitioners synthesize these into a single "planet condition."

- [ ] When you assess a planet, do you form a single mental assessment (e.g., "this Jupiter is strong" or "this Venus is afflicted")? What factors go into that?
- [ ] What is the hierarchy? (e.g., "dignity > placement > aspects > combustion"?)
- [ ] Is a debilitated planet in a good house better or worse than an exalted planet in a dusthana?
- [ ] How do avasthas (Baladi, Jagradadi, Lajjitadi) factor in? Are they a tiebreaker, a primary indicator, or rarely used?

**8.7 Event-Specific Workflows**

Pre-review suggests practitioners use predefined evaluation sequences
for specific life questions, not a general-purpose system.

- [ ] For a marriage question, what is your EXACT sequence of checks? (all steps, in order)
- [ ] For a career question, what is your EXACT sequence? 
- [ ] For health/longevity concerns, what is your EXACT sequence?
- [ ] Are these sequences fixed or do they vary by chart?
- [ ] At what point in the sequence do you STOP and say "this event is unlikely"?

**8.8 What we have but may not be using correctly**

Our codebase already computes all of these. We need to know if we're
using them at the right point in the analysis, with the right weight:

- [ ] **Argala** (intervention from 2nd/4th/11th, obstruction from 12th/10th/3rd) — when in your workflow do you check argala? Is it critical or supplementary?
- [ ] **Arudha Lagna** (material perception) — when do you use it? For which questions?
- [ ] **Upapada Lagna** — how central is this to marriage analysis? Can you skip it?
- [ ] **Dispositor chains** — how much weight? Do you trace the full chain or just one step?
- [ ] **Nakshatra lord** — beyond dasha calculation, how much does nakshatra character matter?
- [ ] **Badhaka** — how often does badhaka lord/house explain otherwise puzzling obstacles?
- [ ] **Maraka** — beyond death, how do you use maraka lords for health events?

**8.9 What are we missing entirely?**
- [ ] After reading all the above, what standard practitioner checks have we STILL not mentioned?
- [ ] What would a client find obviously wrong in our output?
- [ ] What is the single most common error in Jyotish software that frustrates practitioners?

---

## How to return feedback

For each question, please indicate:
- ✅ **Correct** — our understanding matches the source texts and your practice
- ❌ **Wrong** — with the correct interpretation and source reference
- ⚠️ **Partially correct** — with what's missing or what needs qualification
- ❓ **Depends on school/tradition** — indicate which traditions differ and which you recommend

Any additional notes, corrections, or "you should also check X" comments are valuable. We would rather know about 50 issues upfront than discover them after building.

**Thank you for your time and expertise.**
