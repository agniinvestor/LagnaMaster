"""
src/ui/chart_visual.py
=======================
South Indian chart SVG renderer.

Exposes two public functions:
  south_indian_svg(chart, name="") → D1 natal chart SVG
  navamsha_svg(d9_data, lagna_sign_index) → D9 navamsha chart SVG

Layout — 4×4 grid, signs are fixed positions (traditional South Indian format):

    Pi  Ar  Ta  Ge
    Aq  [center ]  Ca
    Cp  [center ]  Le
    Sg  Sc  Li  Vi

The 12 outer cells hold signs + planets; the 4 center cells show chart info.
Lagna cell is highlighted in indigo.
"""

from __future__ import annotations
from src.ephemeris import BirthChart, SIGNS

# ── Layout constants ──────────────────────────────────────────────────────────

CELL = 130  # px per cell
W = 4 * CELL  # 520
H = 4 * CELL  # 520

# sign_index → (row, col)  — 0-indexed
_SIGN_POS: dict[int, tuple[int, int]] = {
    11: (0, 0),  # Pisces
    0: (0, 1),  # Aries
    1: (0, 2),  # Taurus
    2: (0, 3),  # Gemini
    10: (1, 0),  # Aquarius
    3: (1, 3),  # Cancer
    9: (2, 0),  # Capricorn
    4: (2, 3),  # Leo
    8: (3, 0),  # Sagittarius
    7: (3, 1),  # Scorpio
    6: (3, 2),  # Libra
    5: (3, 3),  # Virgo
}

_SIGN_ABBR = ["Ar", "Ta", "Ge", "Ca", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

_PLANET_ABBR: dict[str, str] = {
    "Sun": "Su",
    "Moon": "Mo",
    "Mars": "Ma",
    "Mercury": "Me",
    "Jupiter": "Ju",
    "Venus": "Ve",
    "Saturn": "Sa",
    "Rahu": "Ra",
    "Ketu": "Ke",
}

# Natural benefics displayed in green, malefics in dark red
_BENEFIC = {"Moon", "Mercury", "Jupiter", "Venus"}
_P_COLOR = {p: "#1a7a1a" if p in _BENEFIC else "#8b0000" for p in _PLANET_ABBR}

# Theme
_BG = "#F9F6FF"
_CELL_BG = "#FEFEFE"
_LAGNA_BG = "#EDE7FF"
_LAGNA_STO = "#4B0082"
_GRID_STO = "#C8B8E8"
_SIGN_CLR = "#9985BC"
_CTR_BG = "#F5F0FF"
_CTR_TXT = "#4B0082"


def south_indian_svg(chart: BirthChart, name: str = "") -> str:
    """
    Return a South Indian birth chart as an SVG string.

    Parameters
    ----------
    chart : BirthChart
    name  : optional label shown in center panel
    """
    lagna_idx = chart.lagna_sign_index

    # Build sign → planets mapping
    sign_planets: dict[int, list[str]] = {i: [] for i in range(12)}
    for pname, p in chart.planets.items():
        abbr = _PLANET_ABBR.get(pname, pname[:2])
        if p.is_retrograde and pname not in ("Rahu", "Ketu"):
            abbr += "℞"
        sign_planets[p.sign_index].append((pname, abbr))

    lines: list[str] = []
    lines.append(
        f'<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"'
        f' style="font-family: Georgia, serif; background:{_BG};">'
    )

    # ── Background ──────────────────────────────────────────────────────────
    lines.append(f'<rect width="{W}" height="{H}" fill="{_BG}"/>')

    # ── Sign cells ──────────────────────────────────────────────────────────
    for si, (row, col) in _SIGN_POS.items():
        x = col * CELL
        y = row * CELL
        is_lagna = si == lagna_idx
        bg = _LAGNA_BG if is_lagna else _CELL_BG
        stk = _LAGNA_STO if is_lagna else _GRID_STO
        sw = 2 if is_lagna else 1

        # Cell background
        lines.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'fill="{bg}" stroke="{stk}" stroke-width="{sw}"/>'
        )

        # Sign abbreviation — top-left
        lines.append(
            f'<text x="{x + 6}" y="{y + 15}" font-size="11" fill="{_SIGN_CLR}">'
            f"{_SIGN_ABBR[si]}</text>"
        )

        # Lagna marker — top-right
        if is_lagna:
            lines.append(
                f'<text x="{x + CELL - 38}" y="{y + 15}" font-size="10" '
                f'fill="{_LAGNA_STO}" font-weight="bold">Lag</text>'
            )
            # Lagna degree
            deg = chart.lagna_degree_in_sign
            lines.append(
                f'<text x="{x + 6}" y="{y + 27}" font-size="9" fill="{_LAGNA_STO}">'
                f"{deg:.2f}°</text>"
            )

        # Planets in this sign
        planets_here = sign_planets.get(si, [])
        top_offset = 30 if is_lagna else 22
        for i, (pname, abbr) in enumerate(planets_here):
            py = y + top_offset + i * 17
            clr = _P_COLOR.get(pname, "#333")
            lines.append(
                f'<text x="{x + 8}" y="{py}" font-size="13" '
                f'fill="{clr}" font-weight="600">{abbr}</text>'
            )

    # ── Center 4 cells (2×2 info panel) ─────────────────────────────────────
    cx = 1 * CELL
    cy = 1 * CELL
    cw = 2 * CELL
    ch = 2 * CELL

    lines.append(
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" '
        f'fill="{_CTR_BG}" stroke="{_GRID_STO}" stroke-width="1"/>'
    )

    # Diagonal cross lines (traditional South Indian decoration)
    lines.append(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + cw}" y2="{cy + ch}" '
        f'stroke="{_GRID_STO}" stroke-width="1" opacity="0.5"/>'
    )
    lines.append(
        f'<line x1="{cx + cw}" y1="{cy}" x2="{cx}" y2="{cy + ch}" '
        f'stroke="{_GRID_STO}" stroke-width="1" opacity="0.5"/>'
    )

    # Chart label
    mid_x = cx + cw // 2
    mid_y = cy + ch // 2

    labels = ["🪐 LagnaMaster"]
    if name:
        labels.append(name)
    lagna_label = f"{SIGNS[lagna_idx]} Lagna"
    labels.append(lagna_label)

    for i, lbl in enumerate(labels):
        fy = mid_y - 12 * (len(labels) - 1) + i * 22
        fw = "bold" if i == 0 else "normal"
        fs = 13 if i == 0 else 11
        lines.append(
            f'<text x="{mid_x}" y="{fy}" font-size="{fs}" fill="{_CTR_TXT}" '
            f'text-anchor="middle" font-weight="{fw}">{lbl}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


def navamsha_svg(
    d9_data: dict[str, int], lagna_d9_si: int, label: str = "D9 Navamsha"
) -> str:
    """
    Render the Navamsha (D9) chart as a South Indian SVG.

    Parameters
    ----------
    d9_data      : dict mapping planet names → D9 sign index (0=Aries)
                   e.g. {"Sun": 11, "Moon": 4, "Mars": 8, …}
    lagna_d9_si  : D9 sign index of the lagna/ascendant
    label        : text shown in center panel (default "D9 Navamsha")

    Returns
    -------
    SVG string at the same 520×520px dimensions as south_indian_svg().
    """
    # Build sign → planets mapping for D9
    sign_planets: dict[int, list[str]] = {i: [] for i in range(12)}
    for pname, si in d9_data.items():
        if pname == "lagna":
            continue  # lagna handled separately
        abbr = _PLANET_ABBR.get(pname, pname[:2])
        sign_planets[si].append((pname, abbr))

    lines: list[str] = []
    lines.append(
        f'<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"'
        f' style="font-family: Georgia, serif; background:{_BG};">'
    )
    lines.append(f'<rect width="{W}" height="{H}" fill="{_BG}"/>')

    for si, (row, col) in _SIGN_POS.items():
        x = col * CELL
        y = row * CELL
        is_lagna = si == lagna_d9_si
        bg = _LAGNA_BG if is_lagna else _CELL_BG
        stk = _LAGNA_STO if is_lagna else _GRID_STO
        sw = 2 if is_lagna else 1

        lines.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'fill="{bg}" stroke="{stk}" stroke-width="{sw}"/>'
        )
        lines.append(
            f'<text x="{x + 6}" y="{y + 15}" font-size="11" fill="{_SIGN_CLR}">'
            f"{_SIGN_ABBR[si]}</text>"
        )
        if is_lagna:
            lines.append(
                f'<text x="{x + CELL - 38}" y="{y + 15}" font-size="10" '
                f'fill="{_LAGNA_STO}" font-weight="bold">Lag</text>'
            )

        planets_here = sign_planets.get(si, [])
        top_offset = 25 if is_lagna else 22
        for i, (pname, abbr) in enumerate(planets_here):
            py = y + top_offset + i * 17
            clr = _P_COLOR.get(pname, "#333")
            lines.append(
                f'<text x="{x + 8}" y="{py}" font-size="13" '
                f'fill="{clr}" font-weight="600">{abbr}</text>'
            )

    # Center panel
    cx, cy = 1 * CELL, 1 * CELL
    cw, ch = 2 * CELL, 2 * CELL
    lines.append(
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" '
        f'fill="{_CTR_BG}" stroke="{_GRID_STO}" stroke-width="1"/>'
    )
    lines.append(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + cw}" y2="{cy + ch}" '
        f'stroke="{_GRID_STO}" stroke-width="1" opacity="0.5"/>'
    )
    lines.append(
        f'<line x1="{cx + cw}" y1="{cy}" x2="{cx}" y2="{cy + ch}" '
        f'stroke="{_GRID_STO}" stroke-width="1" opacity="0.5"/>'
    )
    mid_x, mid_y = cx + cw // 2, cy + ch // 2
    lagna_label = f"{SIGNS[lagna_d9_si]} Lagna"
    for i, lbl in enumerate([label, lagna_label]):
        fy = mid_y - 8 + i * 20
        fw = "bold" if i == 0 else "normal"
        fs = 13 if i == 0 else 11
        lines.append(
            f'<text x="{mid_x}" y="{fy}" font-size="{fs}" fill="{_CTR_TXT}" '
            f'text-anchor="middle" font-weight="{fw}">{lbl}</text>'
        )
    lines.append("</svg>")
    return "\n".join(lines)
