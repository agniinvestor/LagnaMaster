"""Phase 1: Lagna and planet position correctness across diverse charts."""
import pytest

pytestmark = [pytest.mark.phase1, pytest.mark.smoke]


class TestLagna:
    def test_lagna_degree(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("lagna_degree")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        assert abs(computed_chart.lagna - verdict["pjh"]) < verdict["tolerance"]

    def test_lagna_sign(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("lagna_sign")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        assert computed_chart.lagna_sign == verdict["pjh"]


class TestPlanetPositions:
    PLANETS = ["sun", "moon", "mars", "mercury", "jupiter",
               "venus", "saturn", "rahu", "ketu"]

    def test_planet_longitudes(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"longitude_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            pos = computed_chart.planets[planet.capitalize()]
            assert abs(pos.longitude - verdict["pjh"]) < verdict["tolerance"], (
                f"{planet}: {pos.longitude} vs {verdict['pjh']}"
            )

    def test_planet_signs(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"sign_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            pos = computed_chart.planets[planet.capitalize()]
            assert pos.sign == verdict["pjh"], (
                f"{planet}: {pos.sign} vs {verdict['pjh']}"
            )


class TestRandomDisagreements:
    @pytest.mark.xfail(strict=False, reason="unresolved engine disagreement")
    def test_position_disagreements(self, verified_chart, computed_chart):
        """Track random disagreements — goal is to reach zero."""
        failures = []
        for field, verdict in verified_chart["verdicts"].items():
            if verdict["status"] == "random_disagreement":
                failures.append(
                    f"{field}: LM={verdict.get('lm')} PJH={verdict.get('pjh')}"
                )
        if failures:
            pytest.fail("\n".join(failures))
