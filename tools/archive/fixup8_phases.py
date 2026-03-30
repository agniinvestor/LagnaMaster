#!/usr/bin/env python3
"""fixup8. Run from ~/LagnaMaster: python3 fixup8_phases.py"""
with open("tests/test_phase0.py") as f:
    lines = f.readlines()

# Replace lines 102-112 (0-indexed: 101-111) with correct content
lines[101:112] = [
    '    def test_sun_at_paramotcha(self):\n',
    '        """Sun at Aries 10deg (Paramotcha) = Uchcha Bala 60."""\n',
    '        from src.calculations.dignity import get_uchcha_bala\n',
    '        bala = get_uchcha_bala("Sun", 10.0)\n',
    '        assert abs(bala - 60.0) < 1.0\n',
    '\n',
    '    def test_moon_mt_start(self):\n',
    '        """Moon 3.99 Taurus: not in MT(4-30), within 5deg of Paramotcha(3) = DEEP_EXALT."""\n',
    '        from src.calculations.dignity import compute_dignity, DignityLevel\n',
    '        chart = make_chart(0.0, Moon=1 * 30 + 3.99)\n',
    '        r = compute_dignity("Moon", chart)\n',
    '        assert r.dignity == DignityLevel.DEEP_EXALT\n',
    '\n',
]

with open("tests/test_phase0.py", "w") as f:
    f.writelines(lines)

print("Fixed. Run: PYTHONPATH=. .venv/bin/pytest tests/test_phase0.py 2>&1 | tail -4")
