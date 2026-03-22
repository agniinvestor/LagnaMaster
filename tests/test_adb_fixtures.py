"""
tests/test_adb_fixtures.py
Tests using real Astro-Databank verified birth charts.

These replace the India 1947 monoculture with real diverse charts
spanning different Lagnas, planetary configurations, and life events.

Charts sourced from Astro-Databank (astro.com) — Rodden AA/A rated.
Copyright: ADB data free for research use per astro.com copyright notice.
"""
import json
import os
import pytest

FIXTURES_DIR = "tests/fixtures/adb_charts"
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def load_adb_fixture(key: str) -> dict:
    path = os.path.join(FIXTURES_DIR, f"{key}.json")
    if not os.path.exists(path):
        pytest.skip(f"ADB fixture {key} not yet fetched — run: python3 tools/adb_scraper.py --manual")
    with open(path) as f:
        return json.load(f)


def compute_from_fixture(fixture: dict):
    """Run LagnaMaster engine on an ADB fixture's birth data."""
    bd = fixture["birth_data"]
    from src.ephemeris import compute_chart
    return compute_chart(
        year=bd["year"], month=bd["month"], day=bd["day"],
        hour=bd["hour"], lat=bd["lat"], lon=bd["lon"],
        tz_offset=bd["tz_offset"], ayanamsha=bd.get("ayanamsha", "lahiri"),
    )


# ─── Fixture availability ─────────────────────────────────────────────────────

class TestADBFixtureLibrary:

    def test_fixture_dir_exists(self):
        os.makedirs(FIXTURES_DIR, exist_ok=True)
        assert os.path.isdir(FIXTURES_DIR)

    def test_manual_fixtures_present(self):
        """At minimum the manually verified AA fixtures should be present."""
        fixtures = [f for f in os.listdir(FIXTURES_DIR) if f.endswith('.json')] \
            if os.path.isdir(FIXTURES_DIR) else []
        if len(fixtures) == 0:
            pytest.skip("No ADB fixtures yet — run: python3 tools/adb_scraper.py --manual")
        assert len(fixtures) >= 1

    def test_all_fixtures_have_birth_data(self):
        if not os.path.isdir(FIXTURES_DIR):
            pytest.skip("No ADB fixtures")
        for fname in os.listdir(FIXTURES_DIR):
            if not fname.endswith('.json'):
                continue
            with open(os.path.join(FIXTURES_DIR, fname)) as f:
                fixture = json.load(f)
            bd = fixture.get("birth_data", {})
            assert "year" in bd, f"{fname}: missing year"
            assert "lat" in bd, f"{fname}: missing lat"
            assert "hour" in bd, f"{fname}: missing hour"

    def test_rodden_rating_filter(self):
        """Only AA and A rated fixtures should be used for regression."""
        if not os.path.isdir(FIXTURES_DIR):
            pytest.skip("No ADB fixtures")
        for fname in os.listdir(FIXTURES_DIR):
            if not fname.endswith('.json'):
                continue
            with open(os.path.join(FIXTURES_DIR, fname)) as f:
                fixture = json.load(f)
            rating = fixture.get("rodden_rating", "Unknown")
            # Warn on low-quality data — DD should never be used
            assert rating != "DD", \
                f"{fname}: Rodden DD (dirty data) must not be in fixtures"


# ─── Mahatma Gandhi chart ─────────────────────────────────────────────────────

class TestGandhiChart:

    @pytest.fixture(scope="class")
    def fixture(self):
        return load_adb_fixture("gandhi_mahatma")

    @pytest.fixture(scope="class")
    def chart(self, fixture):
        return compute_from_fixture(fixture)

    def test_birth_data_rodden_aa(self, fixture):
        assert fixture["rodden_rating"] == "AA"

    def test_lagna_sign(self, chart, fixture):
        expected = fixture.get("expected", {}).get("lagna_sign")
        if expected:
            assert chart.lagna_sign == expected, \
                f"Gandhi Lagna: expected {expected}, got {chart.lagna_sign}"

    def test_all_planets_computed(self, chart):
        expected_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
        assert set(chart.planets.keys()) >= expected_planets

    def test_longitudes_in_range(self, chart):
        for name, p in chart.planets.items():
            assert 0 <= p.longitude < 360, f"Gandhi {name}: longitude out of range"

    def test_ayanamsha_reasonable(self, chart):
        # Lahiri ayanamsha in late 19th century should be ~22°
        assert 21.0 < chart.ayanamsha_value < 23.5, \
            f"Ayanamsha out of range: {chart.ayanamsha_value}"

    def test_scoring_runs(self, chart):
        from src.scoring import score_chart
        result = score_chart(chart)
        assert result is not None
        assert len(result.houses) == 12


# ─── Jawaharlal Nehru chart ────────────────────────────────────────────────────

class TestNehruChart:

    @pytest.fixture(scope="class")
    def fixture(self):
        return load_adb_fixture("nehru_jawaharlal")

    @pytest.fixture(scope="class")
    def chart(self, fixture):
        return compute_from_fixture(fixture)

    def test_birth_data_valid(self, fixture):
        bd = fixture["birth_data"]
        assert bd["year"] == 1889
        assert bd["month"] == 11
        assert bd["day"] == 14

    def test_lagna_sign_capricorn(self, chart, fixture):
        if not fixture.get("assert_lagna", False):
            pytest.skip(fixture.get("trust_note", "low trust — no Lagna assertion"))
        expected = fixture.get("expected", {}).get("lagna_sign")
        if expected:
            assert chart.lagna_sign == expected


# ─── Swami Vivekananda chart ──────────────────────────────────────────────────

class TestVivekanandaChart:

    @pytest.fixture(scope="class")
    def fixture(self):
        return load_adb_fixture("vivekananda_swami")

    @pytest.fixture(scope="class")
    def chart(self, fixture):
        return compute_from_fixture(fixture)

    def test_birth_year(self, fixture):
        assert fixture["birth_data"]["year"] == 1863

    def test_scoring_complete(self, chart):
        from src.scoring import score_chart
        result = score_chart(chart)
        for h in range(1, 13):
            assert h in result.houses, f"H{h} missing from Vivekananda scores"

    def test_functional_dignity_available(self, chart):
        from src.calculations.functional_dignity import compute_functional_classifications
        fc = compute_functional_classifications(chart.lagna_sign_index)
        assert len(fc) == 9  # 9 planets classified


# ─── Albert Einstein chart ────────────────────────────────────────────────────

class TestEinsteinChart:

    @pytest.fixture(scope="class")
    def fixture(self):
        return load_adb_fixture("einstein_albert")

    @pytest.fixture(scope="class")
    def chart(self, fixture):
        return compute_from_fixture(fixture)

    def test_birth_data(self, fixture):
        bd = fixture["birth_data"]
        assert bd["year"] == 1879
        assert fixture["rodden_rating"] == "AA"

    def test_lagna_gemini(self, chart, fixture):
        if not fixture.get("assert_lagna", False):
            pytest.skip(fixture.get("trust_note", "low trust — no Lagna assertion"))
        expected = fixture.get("expected", {}).get("lagna_sign")
        if expected:
            assert chart.lagna_sign == expected


# ─── Nelson Mandela chart ─────────────────────────────────────────────────────

class TestMandelaChart:

    @pytest.fixture(scope="class")
    def fixture(self):
        return load_adb_fixture("mandela_nelson")

    @pytest.fixture(scope="class")
    def chart(self, fixture):
        return compute_from_fixture(fixture)

    def test_birth_data(self, fixture):
        assert fixture["birth_data"]["year"] == 1918
        assert fixture["rodden_rating"] == "AA"

    def test_south_latitude(self, fixture):
        assert fixture["birth_data"]["lat"] < 0  # South Africa is south

    def test_scoring_runs(self, chart):
        from src.scoring import score_chart
        result = score_chart(chart)
        assert result is not None


# ─── Cross-chart diversity tests ──────────────────────────────────────────────

class TestChartDiversity:
    """Verify that the ADB fixture library covers diverse conditions."""

    def _all_computed_charts(self):
        """Load all fixtures that have computed chart data."""
        charts = []
        if not os.path.isdir(FIXTURES_DIR):
            return charts
        for fname in os.listdir(FIXTURES_DIR):
            if not fname.endswith('.json'):
                continue
            with open(os.path.join(FIXTURES_DIR, fname)) as f:
                fixture = json.load(f)
            if fixture.get("chart"):
                charts.append(fixture)
        return charts

    def test_lagna_diversity(self):
        """Real charts should cover more than just one Lagna."""
        charts = self._all_computed_charts()
        if len(charts) < 3:
            pytest.skip("Need at least 3 computed charts to test diversity")
        lagnas = set(c["chart"]["lagna_sign"] for c in charts)
        assert len(lagnas) >= 2, \
            f"Only 1 Lagna represented: {lagnas}. Need more chart diversity."

    def test_century_diversity(self):
        """Fixtures should span multiple centuries."""
        if not os.path.isdir(FIXTURES_DIR):
            pytest.skip("No ADB fixtures")
        years = []
        for fname in os.listdir(FIXTURES_DIR):
            if not fname.endswith('.json'):
                continue
            with open(os.path.join(FIXTURES_DIR, fname)) as f:
                fixture = json.load(f)
            years.append(fixture["birth_data"]["year"])
        if not years:
            pytest.skip("No fixtures loaded")
        assert max(years) - min(years) > 50, \
            f"All fixtures within {max(years)-min(years)} years — not diverse enough"
