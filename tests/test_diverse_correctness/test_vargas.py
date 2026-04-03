"""Phase 3: D9 Navamsha correctness across diverse charts."""
import pytest

from src.calculations.varga import compute_varga

pytestmark = pytest.mark.phase3

PLANET_NAMES = ["sun", "moon", "mars", "mercury", "jupiter", "venus",
                "saturn", "rahu", "ketu"]


class TestNavamsha:
    def test_d9_lagna(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("d9_lagna")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        vc = compute_varga(computed_chart)
        d9 = vc.d9()
        assert d9.varga_lagna_sign == verdict["pjh"], (
            f"D9 Lagna: LM={d9.varga_lagna_sign} vs PJH={verdict['pjh']}"
        )

    def test_d9_planet_signs(self, verified_chart, computed_chart):
        vc = compute_varga(computed_chart)
        d9 = vc.d9()
        for planet in PLANET_NAMES:
            key = f"d9_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            p = d9.planets.get(planet.capitalize())
            if p:
                assert p.varga_sign == verdict["pjh"], (
                    f"D9 {planet}: LM={p.varga_sign} vs PJH={verdict['pjh']}"
                )
