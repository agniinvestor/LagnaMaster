"""
src/calculations/north_indian_chart.py
North Indian (Uttara Bharatiya) diamond-grid birth chart SVG generator.
Session 167 (Audit XIX-A).

In North Indian style:
  - House positions are FIXED (H1 always top-centre diamond)
  - Signs ROTATE (the sign number is written inside each fixed house cell)
  - Reading: H1 = top centre, clockwise H2=top-right, H3=right, H4=bottom-right, etc.

Sources:
  Standard North Indian chart convention used across North India, Punjab,
  Rajasthan, Bengal, and the Indian diaspora in UK/North America.
  Reference: BV Raman · Hindu Predictive Astrology, Chart Conventions.
"""
from __future__ import annotations

_SIGN_ABBREV = [
    "Ar", "Ta", "Ge", "Ca", "Le", "Vi",
    "Li", "Sc", "Sa", "Cp", "Aq", "Pi",
]

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_PLANET_ABBREV = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke", "Mandi": "Mn", "Gulika": "Gu",
}

# House cell centres in 600×600 grid
# H1=top (Lagna), going clockwise
_CELL_CENTRES = {
    1:  (300, 100),   # top centre
    2:  (450, 150),   # top right
    3:  (530, 300),   # right
    4:  (450, 450),   # bottom right
    5:  (300, 500),   # bottom centre
    6:  (150, 450),   # bottom left
    7:  (70,  300),   # left
    8:  (150, 150),   # top left
    9:  (220, 220),   # inner top-right
    10: (380, 220),   # inner top-left
    11: (380, 380),   # inner bottom-left
    12: (220, 380),   # inner bottom-right
}

# Diamond polygon points for each house
def _diamond_points(cx, cy, size=90) -> str:
    s = size
    return f"{cx},{cy-s} {cx+s},{cy} {cx},{cy+s} {cx-s},{cy}"


def _house_polygon(house: int) -> str:
    """Returns SVG polygon points for a house cell."""
    cx, cy = _CELL_CENTRES[house]
    return _diamond_points(cx, cy)


# Full chart outline — outer diamond + inner cross
_OUTER_DIAMOND = "300,10 590,300 300,590 10,300"
_INNER_LINES = [
    "M150,150 L450,150 L450,450 L150,450 Z",  # inner square
    "M150,150 L300,10",   # top-left to top
    "M450,150 L590,300",  # top-right to right
    "M450,450 L300,590",  # bottom-right to bottom
    "M150,450 L10,300",   # bottom-left to left
    "M150,150 L300,300",  # inner diagonals
    "M450,150 L300,300",
    "M450,450 L300,300",
    "M150,450 L300,300",
]


def generate_north_indian_svg(
    chart,
    width: int = 600,
    height: int = 620,
    title: str = "",
    show_degrees: bool = True,
    color_scheme: str = "classic",
) -> str:
    """
    Generate a North Indian diamond-grid birth chart as SVG string.

    Args:
        chart: BirthChart object
        width, height: SVG dimensions
        title: Chart title (e.g., native's name)
        show_degrees: if True, show degree in sign next to planet abbreviation
        color_scheme: "classic" (black/white) or "color"

    Returns: SVG string
    Source: BV Raman · Hindu Predictive Astrology, Chart Conventions
    """
    lagna_si = chart.lagna_sign_index

    # Map: house_number → list of planet strings to display
    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}

    # Place Lagna marker
    house_planets[1].append("Lg")

    # Place planets in their houses
    for planet_name, planet_data in chart.planets.items():
        psi = planet_data.sign_index
        house = (psi - lagna_si) % 12 + 1
        abbrev = _PLANET_ABBREV.get(planet_name, planet_name[:2])
        if show_degrees:
            deg = getattr(planet_data, 'degree_in_sign', 0)
            abbrev += f" {deg:.0f}°"
        if getattr(planet_data, 'is_retrograde', False) and planet_name not in ("Rahu", "Ketu"):
            abbrev += "®"
        house_planets[house].append(abbrev)

    # Sign in each house: H1 = Lagna sign, H2 = next, etc.
    house_sign: dict[int, int] = {h: (lagna_si + h - 1) % 12 for h in range(1, 13)}

    # Color scheme
    if color_scheme == "color":
        bg_fill = "#FFFEF5"
        cell_fill = "#F8F4EE"
        cell_stroke = "#8B4513"
        lagna_fill = "#FFF0D0"
        text_color = "#1A1A2E"
        sign_color = "#8B4513"
        planet_color = "#1A5276"
        title_color = "#7B1E2A"
    else:
        bg_fill = "white"
        cell_fill = "white"
        cell_stroke = "black"
        lagna_fill = "#FFFACD"
        text_color = "black"
        sign_color = "#333333"
        planet_color = "#000080"
        title_color = "black"

    lines = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 600 {height}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="North Indian Birth Chart{" — " + title if title else ""}">',
        f'<title>North Indian Birth Chart{" — " + title if title else ""}</title>',
        f'<desc>Vedic Jyotish birth chart in North Indian diamond style. '
        f'Lagna (Ascendant): {_SIGN_NAMES[lagna_si]}. '
        f'Houses are fixed; signs rotate based on Lagna.</desc>',
        f'<rect width="600" height="{height}" fill="{bg_fill}"/>',
        '',
        '<!-- Outer diamond outline -->',
        f'<polygon points="{_OUTER_DIAMOND}" fill="{cell_fill}" stroke="{cell_stroke}" stroke-width="2"/>',
        '',
        '<!-- Inner grid lines -->',
    ]

    for path_d in _INNER_LINES:
        lines.append(f'<path d="{path_d}" stroke="{cell_stroke}" stroke-width="1.5" fill="none"/>')

    lines.append('')
    lines.append('<!-- House cells with sign numbers -->');

    for house in range(1, 13):
        cx, cy = _CELL_CENTRES[house]
        si = house_sign[house]
        sign_abbrev = _SIGN_ABBREV[si]
        is_lagna_house = (house == 1)

        # Lagna house gets slight highlight
        fill = lagna_fill if is_lagna_house else "none"
        if is_lagna_house and fill != "none":
            lines.append(f'<polygon points="{_house_polygon(house)}" '
                         f'fill="{fill}" stroke="none"/>')

        # Sign number (top of cell) and abbreviation
        lines.append(
            f'<text x="{cx}" y="{cy - 25}" text-anchor="middle" '
            f'font-family="Arial" font-size="11" fill="{sign_color}" font-weight="bold">'
            f'{si + 1} {sign_abbrev}</text>'
        )

        # Planets in this house
        planet_list = house_planets.get(house, [])
        for j, pstr in enumerate(planet_list):
            py = cy - 5 + j * 14
            lines.append(
                f'<text x="{cx}" y="{py}" text-anchor="middle" '
                f'font-family="Arial" font-size="10" fill="{planet_color}">'
                f'{pstr}</text>'
            )

    # Title below chart
    if title:
        lines.append(
            f'<text x="300" y="{height - 10}" text-anchor="middle" '
            f'font-family="Arial" font-size="13" font-weight="bold" fill="{title_color}">'
            f'{title}</text>'
        )

    lines.append('</svg>')
    return '\n'.join(lines)


def generate_south_indian_svg(
    chart,
    width: int = 600,
    height: int = 620,
    title: str = "",
    show_degrees: bool = True,
    color_scheme: str = "classic",
) -> str:
    """
    Generate a South Indian fixed-sign grid chart as SVG.

    In South Indian style:
      - Sign positions are FIXED (Aries always top-left, clockwise)
      - Houses rotate based on Lagna sign

    Source: Standard South Indian convention, Tamil Nadu/Andhra Pradesh/Karnataka.
    """
    lagna_si = chart.lagna_sign_index

    # 4×3 grid: top row = Pisces(11), Aries(0), Taurus(1), Gemini(2)
    #           left col = Aquarius(10), ... down
    # Standard layout (12 cells in 4×3):
    _GRID_SIGN_ORDER = [11, 0, 1, 2, 10, -1, -1, 3, 9, -1, -1, 4, 8, 7, 6, 5]
    # 4 columns × 4 rows = 16 positions, 4 are corners (empty)
    _CELL_SIZE = 140
    _GRID_POSITIONS = []  # (col, row) for each sign 0-11

    sign_positions = {}
    row_idx = 0
    col_idx = 0
    for idx, si in enumerate(_GRID_SIGN_ORDER):
        row = idx // 4
        col = idx % 4
        if si >= 0:
            sign_positions[si] = (col, row)

    # Place planets
    sign_planets: dict[int, list[str]] = {si: [] for si in range(12)}
    sign_planets[lagna_si].append("Lg")
    for planet_name, planet_data in chart.planets.items():
        psi = planet_data.sign_index
        abbrev = _PLANET_ABBREV.get(planet_name, planet_name[:2])
        if show_degrees:
            deg = getattr(planet_data, 'degree_in_sign', 0)
            abbrev += f" {deg:.0f}°"
        if getattr(planet_data, 'is_retrograde', False) and planet_name not in ("Rahu", "Ketu"):
            abbrev += "®"
        sign_planets[psi].append(abbrev)

    if color_scheme == "color":
        bg = "#FFFEF5"; stroke = "#8B4513"; text_c = "#1A1A2E"
        sign_c = "#8B4513"; planet_c = "#1A5276"; lagna_fill = "#FFF0D0"
    else:
        bg = "white"; stroke = "black"; text_c = "black"
        sign_c = "#333"; planet_c = "#000080"; lagna_fill = "#FFFACD"

    svg_w, svg_h = 580, height
    lines = [
        f'<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="South Indian Birth Chart{" — " + title if title else ""}">',
        f'<title>South Indian Birth Chart{" — " + title if title else ""}</title>',
        f'<rect width="{svg_w}" height="{svg_h}" fill="{bg}"/>',
    ]

    cs = 130  # cell size
    ox, oy = 30, 30  # origin offset

    for si in range(12):
        col, row = sign_positions[si]
        x, y = ox + col * cs, oy + row * cs
        is_lagna = (si == lagna_si)
        fill = lagna_fill if is_lagna else bg

        lines.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

        house = (si - lagna_si) % 12 + 1
        lines.append(
            f'<text x="{x+5}" y="{y+16}" font-family="Arial" font-size="11" '
            f'fill="{sign_c}" font-weight="bold">{si+1} H{house}</text>'
        )

        for j, pstr in enumerate(sign_planets.get(si, [])):
            py = y + 32 + j * 14
            lines.append(
                f'<text x="{x + cs//2}" y="{py}" text-anchor="middle" '
                f'font-family="Arial" font-size="10" fill="{planet_c}">{pstr}</text>'
            )

    if title:
        ty = oy + 4 * cs + 25
        lines.append(
            f'<text x="{svg_w//2}" y="{ty}" text-anchor="middle" '
            f'font-family="Arial" font-size="13" font-weight="bold" fill="{sign_c}">'
            f'{title}</text>'
        )

    lines.append('</svg>')
    return '\n'.join(lines)
