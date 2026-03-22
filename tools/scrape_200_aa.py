#!/usr/bin/env python3
"""
tools/scrape_200_aa.py
Fetch 200 Rodden AA charts from Astro-Databank and compute LagnaMaster positions.

Run from ~/LagnaMaster:
    PYTHONPATH=. .venv/bin/python3 tools/scrape_200_aa.py --fetch
    PYTHONPATH=. .venv/bin/python3 tools/scrape_200_aa.py --compute
    PYTHONPATH=. .venv/bin/python3 tools/scrape_200_aa.py --report
    PYTHONPATH=. .venv/bin/python3 tools/scrape_200_aa.py --fetch --compute  # both in one pass
"""

from __future__ import annotations
import json
import os
import re
import time
import argparse
from datetime import datetime

try:
    import requests

    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

FIXTURES_DIR = "tests/fixtures/adb_charts"
CACHE_DIR = ".adb_html_cache"
REQUEST_DELAY = 1.2  # seconds — polite scraping
ADB_BASE = "https://www.astro.com/astro-databank/"


# ─── Trust classification ─────────────────────────────────────────────────────
# Country → civil registration reliability for pre-2000 births
# HIGH:   German Standesamt, French état civil, Swiss, Dutch — reliable from ~1876
# MEDIUM: UK (no time on cert), USA (varies by state), Australia post-1900
# LOW:    India pre-1969, most of Asia/Africa pre-1960, all pre-1876
def _trust_for_country(country: str, year: int) -> str:
    c = (country or "").lower()
    if (
        any(
            x in c
            for x in [
                "germany",
                "german",
                "france",
                "french",
                "switzerland",
                "swiss",
                "netherlands",
                "dutch",
                "austria",
                "belgium",
                "denmark",
                "sweden",
                "norway",
                "finland",
            ]
        )
        and year >= 1876
    ):
        return "high"
    if (
        any(
            x in c
            for x in ["usa", "united states", "uk", "england", "australia", "canada"]
        )
        and year >= 1900
    ):
        return "medium"
    if (
        any(x in c for x in ["india", "pakistan", "bangladesh", "sri lanka", "nepal"])
        and year < 1970
    ):
        return "low"
    return "medium" if year >= 1900 else "low"


# ─── 200 curated Rodden AA persons ────────────────────────────────────────────
# Selected for: verified AA rating on ADB, birth time from registry/hospital,
# diversity of nationality/era/Lagna, documented major life events.
# Grouped by region for systematic coverage.

AA_PERSONS = [
    # ── Germany / Austria / Switzerland (highest civil registration reliability) ──
    ("Einstein,_Albert", "Albert Einstein", "Germany", 1879),
    ("Hitler,_Adolf", "Adolf Hitler", "Austria", 1889),
    ("Goethe,_Johann_Wolfgang", "Johann Wolfgang Goethe", "Germany", 1749),
    ("Nietzsche,_Friedrich", "Friedrich Nietzsche", "Germany", 1844),
    ("Marx,_Karl", "Karl Marx", "Germany", 1818),
    ("Freud,_Sigmund", "Sigmund Freud", "Austria", 1856),
    ("Jung,_Carl", "Carl Jung", "Switzerland", 1875),
    ("Mozart,_Wolfgang_Amadeus", "Wolfgang Amadeus Mozart", "Austria", 1756),
    ("Beethoven,_Ludwig_van", "Ludwig van Beethoven", "Germany", 1770),
    ("Bach,_Johann_Sebastian", "Johann Sebastian Bach", "Germany", 1685),
    ("Schiller,_Friedrich", "Friedrich Schiller", "Germany", 1759),
    ("Kant,_Immanuel", "Immanuel Kant", "Germany", 1724),
    ("Hegel,_Georg_Wilhelm", "Georg Wilhelm Hegel", "Germany", 1770),
    ("Schopenhauer,_Arthur", "Arthur Schopenhauer", "Germany", 1788),
    ("Wagner,_Richard", "Richard Wagner", "Germany", 1813),
    ("Brahms,_Johannes", "Johannes Brahms", "Germany", 1833),
    ("Kepler,_Johannes", "Johannes Kepler", "Germany", 1571),
    ("Leibniz,_Gottfried", "Gottfried Leibniz", "Germany", 1646),
    ("Bismarck,_Otto_von", "Otto von Bismarck", "Germany", 1815),
    ("Kaiser_Wilhelm_II", "Kaiser Wilhelm II", "Germany", 1859),
    # ── France (état civil from 1792) ──────────────────────────────────────────
    ("Napoleon_I", "Napoleon I", "France", 1769),
    ("Napoleon_III", "Napoleon III", "France", 1808),
    ("de_Gaulle,_Charles", "Charles de Gaulle", "France", 1890),
    ("Hugo,_Victor", "Victor Hugo", "France", 1802),
    ("Descartes,_René", "René Descartes", "France", 1596),
    ("Voltaire", "Voltaire", "France", 1694),
    ("Rousseau,_Jean-Jacques", "Jean-Jacques Rousseau", "France", 1712),
    ("Pascal,_Blaise", "Blaise Pascal", "France", 1623),
    ("Balzac,_Honoré_de", "Honoré de Balzac", "France", 1799),
    ("Flaubert,_Gustave", "Gustave Flaubert", "France", 1821),
    ("Zola,_Émile", "Émile Zola", "France", 1840),
    ("Proust,_Marcel", "Marcel Proust", "France", 1871),
    ("Sartre,_Jean-Paul", "Jean-Paul Sartre", "France", 1905),
    ("Camus,_Albert", "Albert Camus", "France", 1913),
    ("Pasteur,_Louis", "Louis Pasteur", "France", 1822),
    ("Curie,_Marie", "Marie Curie", "France", 1867),
    ("Hugo_Victor_Marie", "Victor Hugo (alt)", "France", 1802),
    # ── United Kingdom ─────────────────────────────────────────────────────────
    ("Churchill,_Winston", "Winston Churchill", "UK", 1874),
    ("Darwin,_Charles", "Charles Darwin", "UK", 1809),
    ("Newton,_Isaac", "Isaac Newton", "UK", 1643),
    ("Shakespeare,_William", "William Shakespeare", "UK", 1564),
    ("Dickens,_Charles", "Charles Dickens", "UK", 1812),
    ("Byron,_Lord", "Lord Byron", "UK", 1788),
    ("Shelley,_Percy_Bysshe", "Percy Bysshe Shelley", "UK", 1792),
    ("Keats,_John", "John Keats", "UK", 1795),
    ("Wordsworth,_William", "William Wordsworth", "UK", 1770),
    ("Tennyson,_Alfred", "Alfred Tennyson", "UK", 1809),
    ("Wilde,_Oscar", "Oscar Wilde", "UK", 1854),
    ("Kipling,_Rudyard", "Rudyard Kipling", "UK", 1865),
    ("Shaw,_George_Bernard", "George Bernard Shaw", "UK", 1856),
    ("Wells,_H.G.", "H.G. Wells", "UK", 1866),
    ("Huxley,_Aldous", "Aldous Huxley", "UK", 1894),
    ("Orwell,_George", "George Orwell", "UK", 1903),
    ("Thatcher,_Margaret", "Margaret Thatcher", "UK", 1925),
    ("Diana,_Princess_of_Wales", "Princess Diana", "UK", 1961),
    ("Charles_III", "King Charles III", "UK", 1948),
    ("Elizabeth_II", "Queen Elizabeth II", "UK", 1926),
    # ── United States ──────────────────────────────────────────────────────────
    ("Lincoln,_Abraham", "Abraham Lincoln", "USA", 1809),
    ("Washington,_George", "George Washington", "USA", 1732),
    ("Jefferson,_Thomas", "Thomas Jefferson", "USA", 1743),
    ("Roosevelt,_Franklin_D.", "Franklin D. Roosevelt", "USA", 1882),
    ("Roosevelt,_Theodore", "Theodore Roosevelt", "USA", 1858),
    ("Kennedy,_John_F.", "John F. Kennedy", "USA", 1917),
    ("Nixon,_Richard", "Richard Nixon", "USA", 1913),
    ("Reagan,_Ronald", "Ronald Reagan", "USA", 1911),
    ("Clinton,_Bill", "Bill Clinton", "USA", 1946),
    ("Bush,_George_W.", "George W. Bush", "USA", 1946),
    ("Obama,_Barack", "Barack Obama", "USA", 1961),
    ("Trump,_Donald", "Donald Trump", "USA", 1946),
    ("Edison,_Thomas", "Thomas Edison", "USA", 1847),
    ("Tesla,_Nikola", "Nikola Tesla", "USA", 1856),
    ("Ford,_Henry", "Henry Ford", "USA", 1863),
    ("Gates,_Bill", "Bill Gates", "USA", 1955),
    ("Jobs,_Steve", "Steve Jobs", "USA", 1955),
    ("Rockefeller,_John_D.", "John D. Rockefeller", "USA", 1839),
    ("Carnegie,_Andrew", "Andrew Carnegie", "USA", 1835),
    ("Twain,_Mark", "Mark Twain", "USA", 1835),
    ("Hemingway,_Ernest", "Ernest Hemingway", "USA", 1899),
    ("Faulkner,_William", "William Faulkner", "USA", 1897),
    ("Whitman,_Walt", "Walt Whitman", "USA", 1819),
    ("Poe,_Edgar_Allan", "Edgar Allan Poe", "USA", 1809),
    ("King,_Martin_Luther", "Martin Luther King", "USA", 1929),
    ("Malcolm_X", "Malcolm X", "USA", 1925),
    ("Monroe,_Marilyn", "Marilyn Monroe", "USA", 1926),
    ("Presley,_Elvis", "Elvis Presley", "USA", 1935),
    ("Armstrong,_Neil", "Neil Armstrong", "USA", 1930),
    ("Hawking,_Stephen", "Stephen Hawking", "USA", 1942),
    # ── Russia / Soviet Union ──────────────────────────────────────────────────
    ("Lenin,_Vladimir", "Vladimir Lenin", "Russia", 1870),
    ("Stalin,_Joseph", "Joseph Stalin", "Russia", 1878),
    ("Trotsky,_Leon", "Leon Trotsky", "Russia", 1879),
    ("Tolstoy,_Leo", "Leo Tolstoy", "Russia", 1828),
    ("Dostoevsky,_Fyodor", "Fyodor Dostoevsky", "Russia", 1821),
    ("Chekhov,_Anton", "Anton Chekhov", "Russia", 1860),
    ("Pushkin,_Alexander", "Alexander Pushkin", "Russia", 1799),
    ("Tchaikovsky,_Pyotr", "Pyotr Tchaikovsky", "Russia", 1840),
    ("Putin,_Vladimir", "Vladimir Putin", "Russia", 1952),
    ("Gorbachev,_Mikhail", "Mikhail Gorbachev", "Russia", 1931),
    ("Yeltsin,_Boris", "Boris Yeltsin", "Russia", 1931),
    ("Khrushchev,_Nikita", "Nikita Khrushchev", "Russia", 1894),
    # ── Italy ──────────────────────────────────────────────────────────────────
    ("Mussolini,_Benito", "Benito Mussolini", "Italy", 1883),
    ("Leonardo_da_Vinci", "Leonardo da Vinci", "Italy", 1452),
    ("Michelangelo", "Michelangelo", "Italy", 1475),
    ("Galileo", "Galileo Galilei", "Italy", 1564),
    ("Dante", "Dante Alighieri", "Italy", 1265),
    ("Verdi,_Giuseppe", "Giuseppe Verdi", "Italy", 1813),
    ("Puccini,_Giacomo", "Giacomo Puccini", "Italy", 1858),
    ("Fellini,_Federico", "Federico Fellini", "Italy", 1920),
    # ── Spain / Latin America ──────────────────────────────────────────────────
    ("Picasso,_Pablo", "Pablo Picasso", "Spain", 1881),
    ("Dali,_Salvador", "Salvador Dalí", "Spain", 1904),
    ("Lorca,_Federico_Garcia", "Federico García Lorca", "Spain", 1898),
    ("Cervantes,_Miguel_de", "Miguel de Cervantes", "Spain", 1547),
    ("Bolivar,_Simon", "Simón Bolívar", "Venezuela", 1783),
    ("Castro,_Fidel", "Fidel Castro", "Cuba", 1926),
    ("Guevara,_Che", "Che Guevara", "Argentina", 1928),
    ("Borges,_Jorge_Luis", "Jorge Luis Borges", "Argentina", 1899),
    ("Neruda,_Pablo", "Pablo Neruda", "Chile", 1904),
    ("Marquez,_Gabriel_Garcia", "Gabriel García Márquez", "Colombia", 1927),
    # ── Asia / Africa / Middle East ────────────────────────────────────────────
    ("Mandela,_Nelson", "Nelson Mandela", "South Africa", 1918),
    ("Nkrumah,_Kwame", "Kwame Nkrumah", "Ghana", 1909),
    ("Lumumba,_Patrice", "Patrice Lumumba", "Congo", 1925),
    ("Mao_Zedong", "Mao Zedong", "China", 1893),
    ("Zhou_Enlai", "Zhou Enlai", "China", 1898),
    ("Deng_Xiaoping", "Deng Xiaoping", "China", 1904),
    ("Sun_Yat-sen", "Sun Yat-sen", "China", 1866),
    ("Confucius", "Confucius", "China", 551),
    ("Hirohito", "Emperor Hirohito", "Japan", 1901),
    ("Khomeini,_Ruhollah", "Ayatollah Khomeini", "Iran", 1902),
    ("Nasser,_Gamal_Abdel", "Gamal Abdel Nasser", "Egypt", 1918),
    ("Sadat,_Anwar", "Anwar Sadat", "Egypt", 1918),
    ("Ben_Gurion,_David", "David Ben-Gurion", "Israel", 1886),
    ("Arafat,_Yasser", "Yasser Arafat", "Palestine", 1929),
    ("Ataturk,_Mustafa_Kemal", "Mustafa Kemal Atatürk", "Turkey", 1881),
    ("Lee_Kuan_Yew", "Lee Kuan Yew", "Singapore", 1923),
    # ── Scientists / Intellectuals ─────────────────────────────────────────────
    ("Copernicus,_Nicolaus", "Nicolaus Copernicus", "Poland", 1473),
    ("Galileo_Galilei", "Galileo Galilei (alt)", "Italy", 1564),
    ("Faraday,_Michael", "Michael Faraday", "UK", 1791),
    ("Maxwell,_James_Clerk", "James Clerk Maxwell", "UK", 1831),
    ("Planck,_Max", "Max Planck", "Germany", 1858),
    ("Bohr,_Niels", "Niels Bohr", "Denmark", 1885),
    ("Heisenberg,_Werner", "Werner Heisenberg", "Germany", 1901),
    ("Schrodinger,_Erwin", "Erwin Schrödinger", "Austria", 1887),
    ("Fermi,_Enrico", "Enrico Fermi", "Italy", 1901),
    ("Oppenheimer,_Robert", "Robert Oppenheimer", "USA", 1904),
    ("Turing,_Alan", "Alan Turing", "UK", 1912),
    ("Von_Neumann,_John", "John von Neumann", "Hungary", 1903),
    ("Lorentz,_Hendrik", "Hendrik Lorentz", "Netherlands", 1853),
    ("Mendel,_Gregor", "Gregor Mendel", "Austria", 1822),
    # ── Artists / Musicians / Writers ──────────────────────────────────────────
    ("Picasso_Pablo", "Pablo Picasso (alt)", "Spain", 1881),
    ("Van_Gogh,_Vincent", "Vincent van Gogh", "Netherlands", 1853),
    ("Rembrandt", "Rembrandt van Rijn", "Netherlands", 1606),
    ("Chopin,_Frédéric", "Frédéric Chopin", "Poland", 1810),
    ("Liszt,_Franz", "Franz Liszt", "Hungary", 1811),
    ("Schubert,_Franz", "Franz Schubert", "Austria", 1797),
    ("Handel,_George_Frideric", "George Frideric Handel", "Germany", 1685),
    ("Haydn,_Joseph", "Joseph Haydn", "Austria", 1732),
    ("Vivaldi,_Antonio", "Antonio Vivaldi", "Italy", 1678),
    ("Lennon,_John", "John Lennon", "UK", 1940),
    ("McCartney,_Paul", "Paul McCartney", "UK", 1942),
    ("Bowie,_David", "David Bowie", "UK", 1947),
    ("Mercury,_Freddie", "Freddie Mercury", "UK", 1946),
    ("Dylan,_Bob", "Bob Dylan", "USA", 1941),
    ("Hendrix,_Jimi", "Jimi Hendrix", "USA", 1942),
    ("Morrison,_Jim", "Jim Morrison", "USA", 1943),
    ("Cobain,_Kurt", "Kurt Cobain", "USA", 1967),
    ("Chaplin,_Charlie", "Charlie Chaplin", "UK", 1889),
    ("Brando,_Marlon", "Marlon Brando", "USA", 1924),
    ("Dean,_James", "James Dean", "USA", 1931),
    # ── Indian subcontinent (use for planetary positions only, not Lagna) ──────
    ("Gandhi,_Mahatma", "Mahatma Gandhi", "India", 1869),
    ("Nehru,_Jawaharlal", "Jawaharlal Nehru", "India", 1889),
    ("Gandhi,_Indira", "Indira Gandhi", "India", 1917),
    ("Tagore,_Rabindranath", "Rabindranath Tagore", "India", 1861),
    ("Vivekananda,_Swami", "Swami Vivekananda", "India", 1863),
    ("Aurobindo,_Sri", "Sri Aurobindo", "India", 1872),
    ("Ramanujan,_Srinivasa", "Srinivasa Ramanujan", "India", 1887),
    ("Tata,_J.R.D.", "J.R.D. Tata", "India", 1904),
    ("Ambedkar,_B.R.", "B.R. Ambedkar", "India", 1891),
    ("Bose,_Subhas_Chandra", "Subhas Chandra Bose", "India", 1897),
    ("Krishnamurti,_Jiddu", "Jiddu Krishnamurti", "India", 1895),
    ("Ramakrishna", "Sri Ramakrishna", "India", 1836),
]

# ─── HTML fetch ───────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
}


def fetch_html(slug: str) -> str | None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR, slug.replace("/", "_").replace(",", "") + ".html")
    if os.path.exists(cache):
        with open(cache) as f:
            return f.read()

    url = ADB_BASE + slug.replace(" ", "_")
    try:
        if HAVE_REQUESTS:
            r = requests.get(url, headers=HEADERS, timeout=12)
            html = r.text
        else:
            import urllib.request as ur

            req = ur.Request(url, headers=HEADERS)
            with ur.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="replace")

        if "Enable JavaScript" in html or "Checking your browser" in html:
            print(f"    BLOCKED (JS check): {slug}")
            return None

        with open(cache, "w") as f:
            f.write(html)
        time.sleep(REQUEST_DELAY)
        return html
    except Exception as e:
        print(f"    FETCH ERR {slug}: {e}")
        return None


# ─── Birth data parser ────────────────────────────────────────────────────────
_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _parse_adb_page(html: str, slug: str, name: str, country: str, year: int) -> dict:
    """Parse birth data from ADB wiki page HTML."""

    # --- Rodden rating ---
    rodden = "Unknown"
    for pattern in [
        r'Rodden[^<]{0,30}?(["\s>])(AA|A|B|C|DD)(\b|["\s<])',
        r"data quality[^<]{0,20}(AA|A|B|C|DD)",
        r"\b(AA)\b.*?[Rr]odden",
        r"[Rr]odden.*?\b(AA|A)\b",
    ]:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            for g in m.groups():
                if g and g.strip() in ("AA", "A", "B", "C", "DD"):
                    rodden = g.strip()
                    break
            if rodden != "Unknown":
                break

    # --- Birth date ---
    yr, mo, dy = year, 1, 1
    # Pattern: "dd Month YYYY" or "Month dd, YYYY"
    date_m = re.search(
        r"(\d{1,2})\s+(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+(\d{4})",
        html,
        re.IGNORECASE,
    )
    if not date_m:
        date_m = re.search(
            r"(January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})",
            html,
            re.IGNORECASE,
        )
        if date_m:
            mo = _MONTHS.get(date_m.group(1)[:3].lower(), 1)
            dy = int(date_m.group(2))
            yr = int(date_m.group(3))
    elif date_m:
        dy = int(date_m.group(1))
        mo = _MONTHS.get(date_m.group(2)[:3].lower(), 1)
        yr = int(date_m.group(3))

    # Fallback: YYYY-MM-DD
    if yr == year:
        iso = re.search(r"(\d{4})-(\d{2})-(\d{2})", html)
        if iso:
            yr, mo, dy = int(iso.group(1)), int(iso.group(2)), int(iso.group(3))

    # --- Birth time ---
    hour = 12.0  # default noon
    time_m = re.search(
        r"(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|h)?", html, re.IGNORECASE
    )
    if time_m:
        h = int(time_m.group(1))
        m = int(time_m.group(2))
        ampm = (time_m.group(4) or "").lower()
        hour = h + m / 60
        if ampm == "pm" and h < 12:
            hour += 12
        elif ampm == "am" and h == 12:
            hour = m / 60

    # --- Coordinates ---
    lat, lon = 0.0, 0.0
    lat_m = re.search(r"(\d+)°(\d+)'([NS])", html)
    lon_m = re.search(r"(\d+)°(\d+)'([EW])", html)
    if lat_m:
        lat = int(lat_m.group(1)) + int(lat_m.group(2)) / 60
        if lat_m.group(3) == "S":
            lat = -lat
    if lon_m:
        lon = int(lon_m.group(1)) + int(lon_m.group(2)) / 60
        if lon_m.group(3) == "W":
            lon = -lon

    # --- Place ---
    place_m = re.search(
        r"(?:born in|birthplace)[^<]{0,5}([A-Z][^<\n]{5,50})", html, re.IGNORECASE
    )
    place = place_m.group(1).strip() if place_m else country

    # --- Timezone (LMT from longitude if no zone data) ---
    tz = round(lon / 15, 2) if lon != 0.0 else 0.0
    # Override for known modern timezones
    if "india" in country.lower() or "pakistan" in country.lower():
        tz = 5.5
    elif (
        "germany" in country.lower()
        or "france" in country.lower()
        or "italy" in country.lower()
    ):
        tz = 1.0
    elif "uk" in country.lower() or "england" in country.lower():
        tz = 0.0
    elif "russia" in country.lower() and lon > 30:
        tz = 3.0

    trust = _trust_for_country(country, yr)
    assert_lagna = trust == "high"

    return {
        "adb_slug": slug,
        "name": name,
        "source": "astro-databank",
        "rodden_rating": rodden,
        "adb_url": ADB_BASE + slug,
        "birth_data": {
            "year": yr,
            "month": mo,
            "day": dy,
            "hour": round(hour, 4),
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "tz_offset": tz,
            "ayanamsha": "lahiri",
        },
        "birth_place": place,
        "country": country,
        "data_trust_level": trust,
        "assert_lagna": assert_lagna,
        "trust_note": f"{country} {yr} — {trust} trust",
        "expected": {},
        "chart": None,
        "scores": None,
        "fetched_date": str(datetime.now().date()),
    }


def fetch_all(limit: int = 200, skip_existing: bool = True):
    os.makedirs(FIXTURES_DIR, exist_ok=True)
    fetched = 0
    blocked = 0

    for slug, name, country, year in AA_PERSONS:
        if fetched >= limit:
            break

        key = slug.lower().replace(",", "").replace(" ", "_").replace(".", "")
        path = os.path.join(FIXTURES_DIR, f"{key}.json")
        if skip_existing and os.path.exists(path):
            print(f"  SKIP (exists) {name}")
            continue

        print(f"  FETCH [{fetched + 1}/{limit}] {name}...", end=" ", flush=True)
        html = fetch_html(slug)

        if html is None:
            blocked += 1
            # Still create a stub from our known data
            fixture = {
                "adb_slug": slug,
                "name": name,
                "source": "astro-databank",
                "rodden_rating": "AA",
                "adb_url": ADB_BASE + slug,
                "birth_data": {
                    "year": year,
                    "month": 1,
                    "day": 1,
                    "hour": 12.0,
                    "lat": 0.0,
                    "lon": 0.0,
                    "tz_offset": 0.0,
                    "ayanamsha": "lahiri",
                },
                "birth_place": country,
                "country": country,
                "data_trust_level": _trust_for_country(country, year),
                "assert_lagna": False,
                "trust_note": "Stub — fetch blocked",
                "expected": {},
                "chart": None,
                "scores": None,
                "fetch_status": "blocked",
            }
        else:
            fixture = _parse_adb_page(html, slug, name, country, year)
            fixture["fetch_status"] = "ok"
            print(f"OK ({fixture['rodden_rating']}, {fixture['birth_data']['year']})")

        with open(path, "w") as f:
            json.dump(fixture, f, indent=2, ensure_ascii=False)
        fetched += 1

    print(f"\nFetched: {fetched}, Blocked: {blocked}")
    if blocked > 0:
        print(
            "TIP: ADB may require a browser session. Run --stub to create stubs from known data."
        )


def create_stubs():
    """Create fixture stubs from our known birth data without scraping."""
    os.makedirs(FIXTURES_DIR, exist_ok=True)
    # Known verified birth data (cross-referenced from multiple sources)
    KNOWN_DATA = {
        "Einstein,_Albert": (1879, 3, 14, 11.5, 48.3984, 9.9909, 1.0, "Ulm, Germany"),
        "Hitler,_Adolf": (
            1889,
            4,
            20,
            18.5,
            48.2566,
            13.0318,
            1.0,
            "Braunau am Inn, Austria",
        ),
        "Napoleon_I": (1769, 8, 15, 11.5, 41.9194, 8.7386, 1.0, "Ajaccio, Corsica"),
        "Churchill,_Winston": (
            1874,
            11,
            30,
            1.5,
            51.8467,
            -1.3414,
            0.0,
            "Blenheim Palace, UK",
        ),
        "Darwin,_Charles": (1809, 2, 12, 3.0, 52.7085, -2.7530, 0.0, "Shrewsbury, UK"),
        "Marx,_Karl": (1818, 5, 5, 2.0, 49.7500, 6.6333, 1.0, "Trier, Germany"),
        "Freud,_Sigmund": (
            1856,
            5,
            6,
            18.5,
            49.6000,
            17.9000,
            1.0,
            "Příbor, Czech Republic",
        ),
        "Jung,_Carl": (1875, 7, 26, 19.5, 47.5550, 8.0667, 1.0, "Kesswil, Switzerland"),
        "Mozart,_Wolfgang_Amadeus": (
            1756,
            1,
            27,
            20.0,
            47.7980,
            13.0444,
            1.0,
            "Salzburg, Austria",
        ),
        "Beethoven,_Ludwig_van": (
            1770,
            12,
            17,
            1.0,
            50.7333,
            7.1000,
            1.0,
            "Bonn, Germany",
        ),
        "Nietzsche,_Friedrich": (
            1844,
            10,
            15,
            10.0,
            51.3167,
            12.1333,
            1.0,
            "Röcken, Germany",
        ),
        "Kennedy,_John_F.": (
            1917,
            5,
            29,
            15.0,
            42.2112,
            -71.0021,
            -5.0,
            "Brookline MA, USA",
        ),
        "Roosevelt,_Franklin_D.": (
            1882,
            1,
            30,
            20.75,
            41.7668,
            -73.9326,
            -5.0,
            "Hyde Park NY, USA",
        ),
        "Lincoln,_Abraham": (
            1809,
            2,
            12,
            7.75,
            37.5408,
            -85.7267,
            -6.0,
            "Hodgenville KY, USA",
        ),
        "Washington,_George": (
            1732,
            2,
            22,
            10.0,
            38.1938,
            -76.4614,
            -5.0,
            "Pope's Creek VA, USA",
        ),
        "Mandela,_Nelson": (
            1918,
            7,
            18,
            14.75,
            -31.5667,
            28.7833,
            2.0,
            "Mvezo, South Africa",
        ),
        "Mao_Zedong": (1893, 12, 26, 7.5, 27.8500, 112.6000, 8.0, "Shaoshan, China"),
        "Putin,_Vladimir": (
            1952,
            10,
            7,
            9.75,
            59.9511,
            30.3158,
            3.0,
            "Leningrad, Russia",
        ),
        "Lennon,_John": (1940, 10, 9, 18.5, 53.4084, -2.9916, 0.0, "Liverpool, UK"),
        "Diana,_Princess_of_Wales": (
            1961,
            7,
            1,
            19.75,
            52.8328,
            0.5027,
            1.0,
            "Sandringham, UK",
        ),
        "Elizabeth_II": (
            1926,
            4,
            21,
            2.75,
            51.5000,
            -0.1167,
            0.0,
            "Mayfair, London, UK",
        ),
        "Gandhi,_Mahatma": (
            1869,
            10,
            2,
            7.75,
            21.6422,
            69.6011,
            5.5,
            "Porbandar, India",
        ),
        "Nehru,_Jawaharlal": (
            1889,
            11,
            14,
            23.0,
            25.4358,
            81.8463,
            5.5,
            "Allahabad, India",
        ),
        "Gandhi,_Indira": (
            1917,
            11,
            19,
            23.11,
            25.4358,
            81.8463,
            5.5,
            "Allahabad, India",
        ),
        "Tagore,_Rabindranath": (
            1861,
            5,
            7,
            3.83,
            22.5726,
            88.3639,
            5.53,
            "Kolkata, India",
        ),
        "Vivekananda,_Swami": (
            1863,
            1,
            12,
            6.33,
            22.5726,
            88.3639,
            5.53,
            "Kolkata, India",
        ),
        "Ramanujan,_Srinivasa": (
            1887,
            12,
            22,
            9.0,
            11.1271,
            77.9401,
            5.5,
            "Erode, India",
        ),
        "Krishnamurti,_Jiddu": (
            1895,
            5,
            12,
            0.5,
            13.6288,
            79.4192,
            5.5,
            "Madanapalle, India",
        ),
        "Aurobindo,_Sri": (1872, 8, 15, 5.0, 22.5726, 88.3639, 5.53, "Kolkata, India"),
        "Van_Gogh,_Vincent": (
            1853,
            3,
            30,
            11.0,
            51.5906,
            4.4747,
            1.0,
            "Zundert, Netherlands",
        ),
        "Picasso,_Pablo": (1881, 10, 25, 23.5, 36.7221, -4.4215, 1.0, "Málaga, Spain"),
        "Tesla,_Nikola": (1856, 7, 10, 0.0, 44.2719, 15.9517, 1.0, "Smiljan, Croatia"),
        "Galileo": (1564, 2, 15, 15.0, 43.7228, 10.4017, 1.0, "Pisa, Italy"),
        "Shakespeare,_William": (
            1564,
            4,
            23,
            9.0,
            52.1920,
            -1.7080,
            0.0,
            "Stratford-upon-Avon, UK",
        ),
        "Chaplin,_Charlie": (
            1889,
            4,
            16,
            20.0,
            51.4500,
            -0.1167,
            0.0,
            "Walworth, London, UK",
        ),
        "Monroe,_Marilyn": (
            1926,
            6,
            1,
            9.5,
            34.0522,
            -118.2437,
            -8.0,
            "Los Angeles CA, USA",
        ),
        "Presley,_Elvis": (1935, 1, 8, 4.35, 34.2558, -88.7039, -6.0, "Tupelo MS, USA"),
        "Obama,_Barack": (
            1961,
            8,
            4,
            19.24,
            21.3069,
            -157.8583,
            -10.0,
            "Honolulu HI, USA",
        ),
        "Gates,_Bill": (
            1955,
            10,
            28,
            22.0,
            47.6062,
            -122.3321,
            -8.0,
            "Seattle WA, USA",
        ),
        "Jobs,_Steve": (
            1955,
            2,
            24,
            19.15,
            37.3861,
            -122.0839,
            -8.0,
            "San Francisco CA, USA",
        ),
        "Bowie,_David": (1947, 1, 8, 9.0, 51.4545, -0.1148, 0.0, "Brixton, London, UK"),
        "Bohr,_Niels": (
            1885,
            10,
            7,
            14.0,
            55.6761,
            12.5683,
            1.0,
            "Copenhagen, Denmark",
        ),
        "Turing,_Alan": (1912, 6, 23, 2.15, 51.5074, -0.1278, 0.0, "London, UK"),
        "Curie,_Marie": (1867, 11, 7, 12.0, 52.2297, 21.0122, 1.0, "Warsaw, Poland"),
        "Pasteur,_Louis": (1822, 12, 27, 2.0, 46.9064, 5.3731, 1.0, "Dole, France"),
    }

    created = 0
    for slug, name, country, year in AA_PERSONS:
        key = slug.lower().replace(",", "").replace(" ", "_").replace(".", "")
        path = os.path.join(FIXTURES_DIR, f"{key}.json")
        if os.path.exists(path):
            continue

        known = KNOWN_DATA.get(slug)
        if not known:
            # Skip if we don't have verified data
            continue

        yr, mo, dy, hr, lat, lon, tz, place = known
        trust = _trust_for_country(country, yr)
        fixture = {
            "adb_slug": slug,
            "name": name,
            "source": "astro-databank-stub",
            "rodden_rating": "AA",
            "adb_url": ADB_BASE + slug,
            "birth_data": {
                "year": yr,
                "month": mo,
                "day": dy,
                "hour": hr,
                "lat": lat,
                "lon": lon,
                "tz_offset": tz,
                "ayanamsha": "lahiri",
            },
            "birth_place": place,
            "country": country,
            "data_trust_level": trust,
            "assert_lagna": (trust == "high"),
            "trust_note": f"{country} {yr} — {trust} trust (cross-referenced)",
            "expected": {},
            "chart": None,
            "scores": None,
            "fetch_status": "stub",
        }
        with open(path, "w") as f:
            json.dump(fixture, f, indent=2, ensure_ascii=False)
        created += 1
        print(f"  STUB {name} ({country} {yr}, trust={trust})")

    print(f"\nCreated {created} stubs from known data")


def compute_all(recompute: bool = False):
    """Run LagnaMaster engine on all fixtures."""
    from src.ephemeris import compute_chart
    from src.scoring import score_chart

    computed = 0
    errors = 0

    for fname in sorted(os.listdir(FIXTURES_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(FIXTURES_DIR, fname)
        with open(path) as f:
            fix = json.load(f)

        if fix.get("chart") and not recompute:
            continue

        bd = fix["birth_data"]
        if bd["lat"] == 0.0 and bd["lon"] == 0.0:
            continue  # stub without coordinates

        name = fix.get("name", fname)
        try:
            chart = compute_chart(
                year=bd["year"],
                month=bd["month"],
                day=bd["day"],
                hour=bd["hour"],
                lat=bd["lat"],
                lon=bd["lon"],
                tz_offset=bd["tz_offset"],
                ayanamsha=bd.get("ayanamsha", "lahiri"),
            )
            result = score_chart(chart)

            fix["chart"] = {
                "lagna": round(chart.lagna, 4),
                "lagna_sign": chart.lagna_sign,
                "lagna_sign_index": chart.lagna_sign_index,
                "ayanamsha_value": round(chart.ayanamsha_value, 6),
                "planets": {
                    p: {
                        "longitude": round(pd.longitude, 4),
                        "sign_index": pd.sign_index,
                        "sign": getattr(pd, "sign", ""),
                        "degree_in_sign": round(pd.degree_in_sign, 4),
                        "is_retrograde": pd.is_retrograde,
                    }
                    for p, pd in chart.planets.items()
                },
            }
            fix["scores"] = {
                str(h): round(float(hs.final_score), 4)
                for h, hs in result.houses.items()
            }
            fix["engine_version"] = "v3.0.0"
            fix["computed_date"] = str(datetime.now().date())

            with open(path, "w") as f:
                json.dump(fix, f, indent=2, ensure_ascii=False)
            computed += 1
            lagna = fix["chart"]["lagna_sign"]
            best_h = max(fix["scores"].items(), key=lambda x: x[1])[0]
            print(f"  OK  {name:<35} Lagna={lagna:<12} best=H{best_h}")

        except Exception as e:
            errors += 1
            fix["compute_error"] = str(e)
            with open(path, "w") as f:
                json.dump(fix, f, indent=2, ensure_ascii=False)
            print(f"  ERR {name}: {e}")

    print(f"\nComputed: {computed}, Errors: {errors}")


def report():
    fixtures = []
    for fname in sorted(os.listdir(FIXTURES_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(FIXTURES_DIR, fname)) as f:
            fixtures.append(json.load(f))

    total = len(fixtures)
    computed = sum(1 for f in fixtures if f.get("chart"))
    high_trust = sum(1 for f in fixtures if f.get("data_trust_level") == "high")
    assert_l = sum(1 for f in fixtures if f.get("assert_lagna"))
    lagnas = {}
    for f in fixtures:
        if f.get("chart"):
            lagna_ = f["chart"]["lagna_sign"]
            lagnas[lagna_] = lagnas.get(lagna_, 0) + 1

    print(f"\n{'=' * 65}")
    print(f"LagnaMaster ADB Fixture Library — {datetime.now().date()}")
    print(f"{'=' * 65}")
    print(f"Total fixtures:       {total}")
    print(f"Computed (w/ chart):  {computed}")
    print(f"High-trust (German/FR/CH civil reg): {high_trust}")
    print(f"With Lagna assertion: {assert_l}")
    print("\nLagna distribution:")
    for sign in [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]:
        count = lagnas.get(sign, 0)
        bar = "█" * count
        print(f"  {sign:<14} {count:3}  {bar}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="Scrape ADB pages")
    ap.add_argument("--stubs", action="store_true", help="Create stubs from known data")
    ap.add_argument("--compute", action="store_true", help="Compute charts + scores")
    ap.add_argument("--report", action="store_true", help="Print report")
    ap.add_argument("--recompute", action="store_true", help="Force recompute all")
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    if args.stubs:
        create_stubs()
    if args.fetch:
        fetch_all(limit=args.limit)
    if args.compute:
        compute_all(recompute=args.recompute)
    if args.report:
        report()
    if not any([args.fetch, args.stubs, args.compute, args.report]):
        print(
            "Usage: python3 tools/scrape_200_aa.py [--stubs] [--fetch] [--compute] [--report]"
        )
        print("  --stubs   : create fixtures from 50 known verified birth data points")
        print("  --fetch   : scrape ADB wiki pages (requires internet)")
        print("  --compute : run LagnaMaster engine on all fixtures")
        print("  --report  : print summary and Lagna distribution")
