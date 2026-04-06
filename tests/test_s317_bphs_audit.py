"""
tests/test_s317_bphs_audit.py — BPHS Foundation Audit Regression Tests

Every test cites a specific BPHS verse number and page reference
(Santhanam Vol 1). These protect the 14 bug fixes from S317.

Sources:
  BPHS Ch.3 v.49-54 (dignities, Moolatrikona)
  BPHS Ch.3 v.55 (Naisargika friendship, p.40)
  BPHS Ch.3 v.61-64 (Upagrahas, pp.43-44)
  BPHS Ch.26 v.6-8 (Drishti speculum, pp.255-262)
  BPHS Ch.34 v.19-44 (Yogakarakas + functional malefics, pp.347-356)
  BPHS Ch.49 v.12-18 (Neecha Bhanga conditions)
"""

import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.3 v.55 — Naisargika Friendship (p.40 table)
# ═══════════════════════════════════════════════════════════════════════════════


class TestNaisargikaFriendship:
    """BPHS Ch.3 v.55: permanent planetary relationships, verified against
    the table on p.40 of Santhanam Vol 1."""

    @pytest.fixture(autouse=True)
    def _load(self):
        from src.calculations.dignity import _NAISARGIKA

        self.n = _NAISARGIKA
        from src.calculations.panchadha_maitri import naisargika_relation

        self.nr = naisargika_relation

    # ── The 4 entries corrected in S317 ────────────────────────────────────

    def test_jupiter_saturn_neutral(self):
        """Jupiter→Saturn: Neutral (Saturn is both friend and enemy → neutral)."""
        assert self.n[("Jupiter", "Saturn")] == "Neutral"
        assert self.nr("Jupiter", "Saturn") == "Neutral"

    def test_jupiter_venus_enemy(self):
        """Jupiter→Venus: Enemy (Venus lords 6th/7th from Sagittarius MT)."""
        assert self.n[("Jupiter", "Venus")] == "Enemy"
        assert self.nr("Jupiter", "Venus") == "Enemy"

    def test_venus_moon_enemy(self):
        """Venus→Moon: Enemy (Moon lords 10th from Libra MT)."""
        assert self.n[("Venus", "Moon")] == "Enemy"
        assert self.nr("Venus", "Moon") == "Enemy"

    def test_saturn_mars_enemy(self):
        """Saturn→Mars: Enemy (Mars lords 3rd/10th from Aquarius MT)."""
        assert self.n[("Saturn", "Mars")] == "Enemy"
        assert self.nr("Saturn", "Mars") == "Enemy"

    # ── Consistency: dignity.py and panchadha_maitri.py must agree ──────

    def test_all_42_pairs_consistent(self):
        """Both friendship tables must agree on all 42 asymmetric pairs."""
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        for p1 in planets:
            for p2 in planets:
                if p1 == p2:
                    continue
                dig = self.n.get((p1, p2), "Neutral")
                pan = self.nr(p1, p2)
                assert dig == pan, f"{p1}→{p2}: dignity={dig}, panchadha={pan}"

    # ── Spot-checks on unchanged entries ───────────────────────────────────

    def test_sun_friends(self):
        assert self.n[("Sun", "Moon")] == "Friend"
        assert self.n[("Sun", "Mars")] == "Friend"
        assert self.n[("Sun", "Jupiter")] == "Friend"

    def test_moon_no_enemies(self):
        """BPHS p.41: Moon does not consider anyone as her enemy."""
        planets = ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        for p in planets:
            assert self.n.get(("Moon", p), "Neutral") != "Enemy", f"Moon→{p}"


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.3 v.49-54 — Dignities and Moolatrikona (pp.38-39)
# ═══════════════════════════════════════════════════════════════════════════════


class TestDignitiesCh3:
    """BPHS Ch.3 v.49-54: exaltation, debilitation, Moolatrikona ranges."""

    def test_mercury_mt_range_is_15_to_20(self):
        """Ch.3 v.51-54 (p.39): 'first 15° exaltation, next 5° Moolatrikona'."""
        from src.calculations.dignity import MOOLTRIKONA_RANGES

        sign, start, end = MOOLTRIKONA_RANGES["Mercury"]
        assert sign == 5, "Mercury MT should be in Virgo (index 5)"
        assert start == 15.0, "Mercury MT starts at 15°, not 16°"
        assert end == 20.0, "Mercury MT ends at 20°"

    def test_moon_own_signs_cancer_only(self):
        """Ch.3 v.49-50: Moon's own sign is Cancer. Taurus is exaltation."""
        from src.calculations.dignity import OWN_SIGNS

        assert OWN_SIGNS["Moon"] == [3], "Moon owns only Cancer (index 3)"
        assert 1 not in OWN_SIGNS["Moon"], "Taurus (1) is exaltation, not own"

    def test_exaltation_signs_match_bphs(self):
        """Ch.3 v.49: 'signs of exaltation are Aries, Taurus, Capricorn,
        Virgo, Cancer, Pisces and Libra' for Sun through Saturn."""
        from src.calculations.dignity import EXALT_SIGN

        expected = {
            "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
            "Jupiter": 3, "Venus": 11, "Saturn": 6,
        }
        for planet, sign in expected.items():
            assert EXALT_SIGN[planet] == sign, f"{planet} exaltation"

    def test_paramotcha_degrees_match_bphs(self):
        """Ch.3 v.49 (p.38-39): 'deepest exaltation degrees are 10, 3, 28,
        15, 5, 27 and 20'."""
        from src.calculations.dignity import PARAMOTCHA_DEGREE

        expected = {
            "Sun": 10.0, "Moon": 3.0, "Mars": 28.0, "Mercury": 15.0,
            "Jupiter": 5.0, "Venus": 27.0, "Saturn": 20.0,
        }
        for planet, deg in expected.items():
            assert PARAMOTCHA_DEGREE[planet] == deg, f"{planet} paramotcha"


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.3 v.61-64 — Upagraha formulas (pp.43-44)
# ═══════════════════════════════════════════════════════════════════════════════


class TestUpagrahasCh3:
    """BPHS Ch.3 v.61-64: derived upagraha computation, verified against
    the worked example on p.43-44 (Sun at Taurus 10° = 40°)."""

    @pytest.fixture(autouse=True)
    def _compute(self):
        from src.calculations.upagrahas_derived import compute_derived_upagrahas

        self.r = compute_derived_upagrahas(40.0)

    def test_dhuma(self):
        """Sun + 133°20' = 173°20'."""
        assert abs(self.r.dhuma - 173.333) < 0.01

    def test_vyatipata(self):
        """Dhuma + 53°20' = 226°40' (per worked example, p.43)."""
        assert abs(self.r.vyatipata - 226.667) < 0.01

    def test_parivesha(self):
        """Vyatipata + 180° = 406°40' = 46°40'."""
        assert abs(self.r.parivesha - 46.667) < 0.01

    def test_indrachapa(self):
        """Parivesha - 53°20' = 353°20'."""
        assert abs(self.r.indrachapa - 353.333) < 0.01

    def test_upaketu(self):
        """Chapa + 16°40' = 10°."""
        assert abs(self.r.upaketu - 10.0) < 0.01

    @pytest.mark.parametrize("sun_lon", [0.0, 40.0, 100.0, 200.0, 350.0])
    def test_upaketu_plus_30_equals_sun(self, sun_lon):
        """Self-check from p.44: Upaketu + 30° = Sun's longitude."""
        from src.calculations.upagrahas_derived import compute_derived_upagrahas

        r = compute_derived_upagrahas(sun_lon)
        reconstructed = (r.upaketu + 30) % 360
        assert abs(reconstructed - sun_lon) < 0.01


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.26 v.6-8 — Drishti Speculum (pp.255-262)
# ═══════════════════════════════════════════════════════════════════════════════


class TestDrishtiSpeculum:
    """BPHS Ch.26 v.6-8: continuous aspect strength function, verified
    against the Speculum of Aspectual Values (pp.258-262)."""

    @pytest.fixture(autouse=True)
    def _load(self):
        from src.calculations.sputa_drishti import (
            bphs_drishti_virupas,
            bphs_drishti_with_specials,
        )

        self.base = bphs_drishti_virupas
        self.special = bphs_drishti_with_specials

    # ── House-center values (the classical 1/4, 1/2, 3/4, full) ───────

    def test_3rd_house_quarter(self):
        """60° = 15 virupas = 1/4 of full."""
        assert abs(self.base(60.0) - 15.0) < 0.01

    def test_4th_house_three_quarter(self):
        """90° = 45 virupas = 3/4 of full."""
        assert abs(self.base(90.0) - 45.0) < 0.01

    def test_5th_house_half(self):
        """120° = 30 virupas = 1/2 of full."""
        assert abs(self.base(120.0) - 30.0) < 0.01

    def test_7th_house_full(self):
        """180° = 60 virupas = full aspect."""
        assert abs(self.base(180.0) - 60.0) < 0.01

    def test_10th_house_quarter(self):
        """270° = 15 virupas = 1/4 of full."""
        assert abs(self.base(270.0) - 15.0) < 0.01

    # ── Zero-aspect zones ──────────────────────────────────────────────

    def test_no_aspect_below_30(self):
        assert self.base(0.0) == 0.0
        assert self.base(15.0) == 0.0
        assert self.base(29.9) == 0.0

    def test_no_aspect_above_300(self):
        assert self.base(300.0) == 0.0
        assert self.base(330.0) == 0.0

    def test_no_aspect_at_150(self):
        """150° (6th house) = 0 virupas."""
        assert self.base(150.0) == 0.0

    # ── Intermediate speculum values ───────────────────────────────────

    @pytest.mark.parametrize(
        "angle,expected",
        [
            (30.5, 0.25),
            (33.0, 1.50),
            (45.0, 7.50),
            (50.0, 10.00),
            (70.0, 25.00),
            (80.0, 35.00),
            (100.0, 40.00),
            (110.0, 35.00),
            (130.0, 20.00),
            (140.0, 10.00),
            (155.0, 10.00),
            (165.0, 30.00),
            (170.0, 40.00),
            (190.0, 55.00),
            (200.0, 50.00),
            (250.0, 25.00),
        ],
    )
    def test_speculum_value(self, angle, expected):
        """Verified against BPHS speculum table (pp.258-262)."""
        assert abs(self.base(angle) - expected) < 0.01

    # ── Continuity at segment boundaries ───────────────────────────────

    @pytest.mark.parametrize("boundary", [30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 300.0])
    def test_continuity_at_boundary(self, boundary):
        """Function must be continuous at each piecewise boundary."""
        left = self.base(boundary - 0.001)
        right = self.base(boundary + 0.001)
        at = self.base(boundary)
        assert abs(left - at) < 0.1, f"Discontinuity at {boundary}° (left)"
        assert abs(right - at) < 0.1, f"Discontinuity at {boundary}° (right)"

    # ── Special aspects ────────────────────────────────────────────────

    @pytest.mark.parametrize(
        "planet,angle",
        [
            ("Mars", 90.0),
            ("Mars", 210.0),
            ("Jupiter", 120.0),
            ("Jupiter", 240.0),
            ("Saturn", 60.0),
            ("Saturn", 270.0),
        ],
    )
    def test_special_aspect_full_at_center(self, planet, angle):
        """Special aspects reach full strength (60 virupas) at house center."""
        assert abs(self.special(planet, angle) - 60.0) < 0.01

    def test_non_special_planet_no_boost(self):
        """Sun at 90° gets base strength only (45), no special boost."""
        assert abs(self.special("Sun", 90.0) - 45.0) < 0.01


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.34 v.19-44 — Yogakarakas (pp.347-356)
# ═══════════════════════════════════════════════════════════════════════════════


class TestYogakarakasCh34:
    """BPHS Ch.34: yogakaraka = single planet ruling both kendra AND trikona."""

    @pytest.fixture(autouse=True)
    def _load(self):
        from src.calculations.functional_dignity import KNOWN_YOGAKARAKAS

        self.yk = KNOWN_YOGAKARAKAS

    # ── True yogakarakas (rule both kendra + trikona) ──────────────────

    def test_taurus_saturn(self):
        """v.23: Saturn rules H9(T)+H10(K)."""
        assert self.yk[1] == ["Saturn"]

    def test_cancer_mars(self):
        """v.27: Mars rules H5(T)+H10(K)."""
        assert self.yk[3] == ["Mars"]

    def test_leo_mars(self):
        """v.29: Mars rules H4(K)+H9(T)."""
        assert self.yk[4] == ["Mars"]

    def test_libra_saturn(self):
        """v.33: Saturn rules H4(K)+H5(T)."""
        assert self.yk[6] == ["Saturn"]

    def test_capricorn_venus(self):
        """v.39: Venus rules H5(T)+H10(K)."""
        assert self.yk[9] == ["Venus"]

    def test_aquarius_venus(self):
        """v.41: Venus rules H4(K)+H9(T)."""
        assert self.yk[10] == ["Venus"]

    # ── Lagnas with NO strict yogakaraka ───────────────────────────────

    @pytest.mark.parametrize(
        "lagna,name",
        [(0, "Aries"), (2, "Gemini"), (5, "Virgo"), (7, "Scorpio"),
         (8, "Sagittarius"), (11, "Pisces")],
    )
    def test_no_yogakaraka(self, lagna, name):
        """These lagnas have no single planet ruling both K and T."""
        assert self.yk[lagna] == [], f"{name} should have empty yogakaraka list"

    # ── Specifically removed entries (S317 fixes) ──────────────────────

    def test_aries_sun_not_yogakaraka(self):
        """Sun rules only H5 for Aries — no kendra lordship."""
        assert "Sun" not in self.yk[0]

    def test_virgo_venus_not_yogakaraka(self):
        """Venus rules H2+H9 for Virgo — H2 is not a kendra."""
        assert "Venus" not in self.yk[5]

    def test_scorpio_jupiter_not_yogakaraka(self):
        """Jupiter rules H2+H5 for Scorpio — H2 is not a kendra."""
        assert "Jupiter" not in self.yk[7]


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.34 v.19-44 — Functional Malefics (pp.347-356)
# ═══════════════════════════════════════════════════════════════════════════════


class TestFunctionalMaleficsCh34:
    """BPHS Ch.34 v.19-44: per-lagna functional malefic classifications.
    Each test cites the specific verse."""

    @pytest.fixture(autouse=True)
    def _load(self):
        from src.calculations.functional_dignity import KNOWN_FUNCTIONAL_MALEFICS

        self.fm = KNOWN_FUNCTIONAL_MALEFICS

    def _malefics(self, lagna: int) -> set[str]:
        """Return set of functional malefics excluding Rahu/Ketu."""
        return {p for p in self.fm[lagna] if p not in ("Rahu", "Ketu")}

    # ── Per-verse classifications ──────────────────────────────────────

    def test_aries_v19(self):
        """v.19: 'Saturn, Mercury and Venus are malefics'."""
        assert self._malefics(0) == {"Saturn", "Mercury", "Venus"}

    def test_taurus_v23(self):
        """v.23: 'Jupiter, Venus and the Moon are malefics'."""
        assert self._malefics(1) == {"Jupiter", "Venus", "Moon"}

    def test_gemini_v25(self):
        """v.25: 'Mars, Jupiter and the Sun are malefics'."""
        assert self._malefics(2) == {"Mars", "Jupiter", "Sun"}

    def test_cancer_v27(self):
        """v.27: 'Venus and Mercury are malefics'.
        Jupiter is AUSPICIOUS per verse (H6+H9, trikona dominates)."""
        m = self._malefics(3)
        assert m == {"Venus", "Mercury"}
        assert "Jupiter" not in m, "Jupiter is auspicious for Cancer per v.27"

    def test_leo_v29(self):
        """v.29: 'Mercury, Venus and Saturn are malefics'."""
        assert self._malefics(4) == {"Mercury", "Venus", "Saturn"}

    def test_virgo_v31(self):
        """v.31: 'Mars, Jupiter and the Moon are malefics'."""
        assert self._malefics(5) == {"Mars", "Jupiter", "Moon"}

    def test_libra_v33(self):
        """v.33: 'Jupiter, the Sun and Mars are malefics'.
        Mercury is AUSPICIOUS per verse (H9+H12, trikona dominates)."""
        m = self._malefics(6)
        assert m == {"Jupiter", "Sun", "Mars"}
        assert "Mercury" not in m, "Mercury is auspicious for Libra per v.33"

    def test_scorpio_v35(self):
        """v.35: 'Venus, Mercury and Saturn are malefics'."""
        assert self._malefics(7) == {"Venus", "Mercury", "Saturn"}

    def test_sagittarius_v37(self):
        """v.37: 'Only Venus is inauspicious'.
        The word 'only' limits malefics to Venus alone."""
        assert self._malefics(8) == {"Venus"}

    def test_capricorn_v39(self):
        """v.39: 'Mars, Jupiter and the Moon are malefics'."""
        assert self._malefics(9) == {"Mars", "Jupiter", "Moon"}

    def test_aquarius_v41(self):
        """v.41: 'Jupiter, the Moon and Mars are malefics'."""
        assert self._malefics(10) == {"Jupiter", "Moon", "Mars"}

    def test_pisces_v43(self):
        """v.43: 'Saturn, Venus, the Sun and Mercury are malefics'."""
        assert self._malefics(11) == {"Saturn", "Venus", "Sun", "Mercury"}

    # ── Rahu/Ketu always present (sloka 16, p.346) ─────────────────────

    @pytest.mark.parametrize("lagna", range(12))
    def test_rahu_ketu_always_malefic(self, lagna):
        """Sloka 16: Rahu/Ketu act per association, default malefic."""
        assert "Rahu" in self.fm[lagna]
        assert "Ketu" in self.fm[lagna]


# ═══════════════════════════════════════════════════════════════════════════════
# Ch.49 v.12-18 — Neecha Bhanga Conditions
# ═══════════════════════════════════════════════════════════════════════════════


class TestNeechaBhangaCh49:
    """BPHS Ch.49 v.12-18: Neecha Bhanga conditions."""

    def _make_chart(self, lagna_si, **planet_lons):
        """Minimal chart stub for NB testing."""
        from types import SimpleNamespace

        planets = {}
        for name, lon in planet_lons.items():
            si = int(lon / 30) % 12
            deg = lon % 30
            planets[name] = SimpleNamespace(
                longitude=lon, sign_index=si, degree_in_sign=deg, sign="test"
            )
        if "Moon" not in planets:
            planets["Moon"] = SimpleNamespace(
                longitude=0.0, sign_index=0, degree_in_sign=0.0, sign="test"
            )
        return SimpleNamespace(planets=planets, lagna_sign_index=lagna_si)

    def test_parivartana_exchange_not_conjunction(self):
        """NB condition 6: parivartana = mutual sign exchange.
        Mars debilitated in Cancer (Moon's sign) + Moon in Aries (Mars's sign)
        = true exchange. Moon ALSO in Cancer = conjunction, NOT exchange."""
        from src.calculations.dignity import _check_neecha_bhanga

        # True exchange: Mars in Cancer (90°), Moon in Aries (10°)
        chart = self._make_chart(0, Mars=100.0, Moon=10.0)
        result = _check_neecha_bhanga("Mars", chart)
        assert result.nb_parivartana is True, "Mars-Cancer + Moon-Aries = exchange"

        # Conjunction: Mars in Cancer (100°), Moon in Cancer (95°)
        chart2 = self._make_chart(0, Mars=100.0, Moon=95.0)
        result2 = _check_neecha_bhanga("Mars", chart2)
        assert result2.nb_parivartana is False, "Both in Cancer = conjunction, not exchange"

    def test_parivartana_mars_scorpio(self):
        """Moon in Scorpio (Mars's second sign) also counts as exchange."""
        from src.calculations.dignity import _check_neecha_bhanga

        chart = self._make_chart(0, Mars=100.0, Moon=220.0)  # Moon in Scorpio
        result = _check_neecha_bhanga("Mars", chart)
        assert result.nb_parivartana is True

    def test_condition5_special_aspect(self):
        """NB condition 5: debilitation lord aspecting via special aspect.
        Mars debilitated in Cancer. Moon (lord of Cancer) in Aries = 10th
        from Cancer. Moon has no special aspect on 10th, only 7th.
        But if debil lord is Jupiter (Saturn debil in Aries, lord=Mars,
        exalt_in_debil=Sun), we need a planet with special aspects."""
        from src.calculations.dignity import _check_neecha_bhanga

        # Saturn debilitated in Aries (sign 0). Lord of Aries = Mars.
        # Mars in Libra (sign 6) = 7th from Aries → standard aspect ✓
        chart = self._make_chart(0, Saturn=10.0, Mars=190.0, Moon=0.0)
        result = _check_neecha_bhanga("Saturn", chart)
        assert result.nb_aspected_by_lord is True, "Mars in 7th from Saturn = aspect"

        # Mars in Cancer (sign 3) = 4th from Aries.
        # Mars has special 4th house aspect, but Mars is the ASPECTOR here,
        # not the aspected. We check: does debil lord (Mars) aspect Saturn?
        # Mars at sign 3, Saturn at sign 0. Diff = (0-3)%12 = 9.
        # Mars special aspects: {3, 6, 7} (4th, 7th, 8th in 0-indexed diff)
        # Diff 9 is not in Mars's aspects. So no aspect.
        chart2 = self._make_chart(0, Saturn=10.0, Mars=100.0, Moon=0.0)
        result2 = _check_neecha_bhanga("Saturn", chart2)
        assert result2.nb_aspected_by_lord is False

    def test_condition5_mars_8th_aspect(self):
        """Mars's special 8th house aspect should count for NB condition 5.
        Saturn debil in Aries (sign 0). Mars in Virgo (sign 5).
        Diff from Mars to Saturn: (0 - 5) % 12 = 7 → 8th house aspect.
        Mars has special aspect on 8th house (diff=7)."""
        from src.calculations.dignity import _check_neecha_bhanga

        chart = self._make_chart(0, Saturn=10.0, Mars=160.0, Moon=0.0)
        result = _check_neecha_bhanga("Saturn", chart)
        assert result.nb_aspected_by_lord is True, "Mars 8th aspect on Saturn"
