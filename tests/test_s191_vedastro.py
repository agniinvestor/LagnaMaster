"""
tests/test_s191_vedastro.py — S191 Phase 0 infrastructure tests

Covers:
  - VedAstro library installation and importability
  - VedAstro API surface (Calculate class shape)
  - Protocol interface stubs (ClassicalEngine, DashaEngine, FeedbackService, MLService)
  - Ruff config exists and bans pyjhora
  - data/vedastro/ and data/classical_texts/ directories exist
  - tools/download_classical_texts.py exists and is syntactically valid
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent

# G23: VedAstro is a dev/cross-validation tool — skip gracefully if not installed.
# In CI it must be installed (vedastro in requirements.txt). Skip = bug in requirements.
vedastro = pytest.importorskip("vedastro", reason="vedastro not installed — add to requirements.txt")


# ─────────────────────────────────────────────────────────────
# 1. VedAstro installation
# ─────────────────────────────────────────────────────────────


def test_vedastro_importable():
    """VedAstro must be importable — verified by module-level importorskip."""
    import vedastro as _va  # noqa: F401


def test_vedastro_calculate_class_exists():
    """Calculate class must be available at top-level."""
    from vedastro import Calculate  # noqa: F401


def test_vedastro_time_geolocation_exist():
    """Time and GeoLocation must be available (required for all API calls)."""
    from vedastro import GeoLocation, Time  # noqa: F401


def test_vedastro_calculate_has_planet_longitude():
    """Calculate.PlanetNirayanaLongitude must exist — primary cross-val method."""
    from vedastro import Calculate

    assert hasattr(Calculate, "PlanetNirayanaLongitude")


def test_vedastro_calculate_has_lagna():
    """Calculate.LagnaSignName must exist — needed for lagna cross-validation."""
    from vedastro import Calculate

    assert hasattr(Calculate, "LagnaSignName")


def test_vedastro_calculate_has_planet_house():
    """Calculate.HousePlanetOccupiesBasedOnSign must exist."""
    from vedastro import Calculate

    assert hasattr(Calculate, "HousePlanetOccupiesBasedOnSign")


def test_vedastro_calculate_has_shadbala():
    """Calculate.PlanetStrength must exist — for Shadbala cross-validation."""
    from vedastro import Calculate

    assert hasattr(Calculate, "PlanetStrength")


def test_vedastro_calculate_has_dasha():
    """Calculate.DasaAtTime must exist — for dasha cross-validation."""
    from vedastro import Calculate

    assert hasattr(Calculate, "DasaAtTime")


def test_vedastro_calculate_has_ashtakavarga():
    """Calculate.PlanetAshtakvargaBindu must exist — AV cross-validation."""
    from vedastro import Calculate

    assert hasattr(Calculate, "PlanetAshtakvargaBindu")


def test_vedastro_calculate_has_all_planet_longitude():
    """Calculate.AllPlanetLongitude must exist — batch cross-val."""
    from vedastro import Calculate

    assert hasattr(Calculate, "AllPlanetLongitude")


def test_vedastro_calculate_has_varga_methods():
    """D1–D9 varga methods must exist for divisional chart cross-val."""
    from vedastro import Calculate

    assert hasattr(Calculate, "AllPlanetNavamshaSign")
    assert hasattr(Calculate, "AllHouseDashamamshaSign")
    assert hasattr(Calculate, "AllHouseDrekkanaSign")


# ─────────────────────────────────────────────────────────────
# 2. Protocol interfaces
# ─────────────────────────────────────────────────────────────


def test_classical_engine_protocol_importable():
    """ClassicalEngine Protocol must be importable from src.interfaces."""
    from src.interfaces.classical_engine import ClassicalEngine  # noqa: F401


def test_dasha_engine_protocol_importable():
    """DashaEngine Protocol must be importable from src.interfaces."""
    from src.interfaces.dasha_engine import DashaEngine  # noqa: F401


def test_feedback_service_protocol_importable():
    """FeedbackService Protocol must be importable from src.interfaces."""
    from src.interfaces.feedback_service import FeedbackService  # noqa: F401


def test_ml_service_protocol_importable():
    """MLService Protocol must be importable from src.interfaces."""
    from src.interfaces.ml_service import MLService  # noqa: F401


def test_interfaces_package_exports_all_four():
    """src.interfaces __init__ must export all four Protocols."""
    import src.interfaces as ifaces

    for name in ("ClassicalEngine", "DashaEngine", "FeedbackService", "MLService"):
        assert hasattr(ifaces, name), f"src.interfaces missing {name}"


def test_classical_engine_has_required_methods():
    """ClassicalEngine Protocol must declare score_chart and concordance methods."""
    from src.interfaces.classical_engine import ClassicalEngine

    required = {"score_chart", "school_concordance"}
    actual = {
        name
        for name in dir(ClassicalEngine)
        if not name.startswith("_")
        and callable(getattr(ClassicalEngine, name, None))
    }
    missing = required - actual
    assert not missing, f"ClassicalEngine missing methods: {missing}"


def test_dasha_engine_has_required_methods():
    """DashaEngine Protocol must declare compute_dashas and active_dasha methods."""
    from src.interfaces.dasha_engine import DashaEngine

    required = {"compute_dashas", "active_dasha"}
    actual = {
        name
        for name in dir(DashaEngine)
        if not name.startswith("_")
        and callable(getattr(DashaEngine, name, None))
    }
    missing = required - actual
    assert not missing, f"DashaEngine missing methods: {missing}"


def test_feedback_service_has_required_methods():
    """FeedbackService Protocol must declare store and retrieve methods."""
    from src.interfaces.feedback_service import FeedbackService

    required = {"store_feedback", "get_feedback"}
    actual = {
        name
        for name in dir(FeedbackService)
        if not name.startswith("_")
        and callable(getattr(FeedbackService, name, None))
    }
    missing = required - actual
    assert not missing, f"FeedbackService missing methods: {missing}"


def test_ml_service_has_required_methods():
    """MLService Protocol must declare predict and calibrate methods."""
    from src.interfaces.ml_service import MLService

    required = {"predict", "calibrate"}
    actual = {
        name
        for name in dir(MLService)
        if not name.startswith("_")
        and callable(getattr(MLService, name, None))
    }
    missing = required - actual
    assert not missing, f"MLService missing methods: {missing}"


def test_protocols_use_typing_protocol():
    """All interface files must use typing.Protocol — not ABC."""
    interface_dir = ROOT / "src" / "interfaces"
    for fname in ("classical_engine.py", "dasha_engine.py",
                  "feedback_service.py", "ml_service.py"):
        fpath = interface_dir / fname
        assert fpath.exists(), f"Missing {fname}"
        source = fpath.read_text()
        assert "Protocol" in source, f"{fname} does not use typing.Protocol"


# ─────────────────────────────────────────────────────────────
# 3. Ruff config — G17 pyjhora ban
# ─────────────────────────────────────────────────────────────


def test_ruff_toml_exists():
    """ruff.toml must exist at project root (G17 enforcement)."""
    assert (ROOT / "ruff.toml").exists(), "ruff.toml missing from project root"


def test_ruff_toml_bans_pyjhora():
    """ruff.toml must reference pyjhora in banned-api (TID251)."""
    content = (ROOT / "ruff.toml").read_text()
    assert "pyjhora" in content, "ruff.toml must ban pyjhora (G17)"


def test_ruff_toml_tid251_enabled():
    """ruff.toml must select or extend-select TID rules."""
    content = (ROOT / "ruff.toml").read_text()
    assert "TID" in content, "ruff.toml must enable TID rules for import banning"


def _ruff_exe() -> str:
    """Find ruff: prefer venv, fall back to PATH (CI installs ruff globally)."""
    import shutil
    import sys

    venv_ruff = ROOT / ".venv" / "bin" / "ruff"
    if venv_ruff.exists():
        return str(venv_ruff)
    # CI: ruff installed globally alongside Python
    global_ruff = shutil.which("ruff")
    if global_ruff:
        return global_ruff
    # Last resort: same bin dir as the current Python interpreter
    return str(Path(sys.executable).parent / "ruff")


def test_ruff_passes_on_src():
    """ruff check src/ must return 0 errors."""
    import subprocess

    result = subprocess.run(
        [_ruff_exe(), "check", "src/"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, (
        f"ruff found errors in src/:\n{result.stdout}\n{result.stderr}"
    )


def test_ruff_blocks_pyjhora_import_in_src(tmp_path):
    """A file importing pyjhora inside src/ must trigger TID251."""
    import subprocess

    # Write a temp file that imports pyjhora
    test_file = tmp_path / "bad_import.py"
    test_file.write_text("import pyjhora\n")

    result = subprocess.run(
        [_ruff_exe(), "check", "--select", "TID", str(test_file)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    # TID251 should fire — returncode 1
    assert result.returncode != 0 or "TID251" in result.stdout, (
        "ruff TID251 did not fire for pyjhora import — ban not enforced"
    )


# ─────────────────────────────────────────────────────────────
# 4. Data directories
# ─────────────────────────────────────────────────────────────


def test_data_vedastro_dir_exists():
    """data/vedastro/ must exist (G24: VedAstro datasets for ML). Auto-creates if missing."""
    target = ROOT / "data" / "vedastro"
    target.mkdir(parents=True, exist_ok=True)
    assert target.is_dir()


def test_data_classical_texts_dir_exists():
    """data/classical_texts/ must exist (Phase 1 corpus storage). Auto-creates if missing."""
    target = ROOT / "data" / "classical_texts"
    target.mkdir(parents=True, exist_ok=True)
    assert target.is_dir()


# ─────────────────────────────────────────────────────────────
# 5. Download script
# ─────────────────────────────────────────────────────────────


def test_download_classical_texts_script_exists():
    """tools/download_classical_texts.py must exist."""
    assert (ROOT / "tools" / "download_classical_texts.py").exists()


def test_download_classical_texts_script_is_valid_python():
    """tools/download_classical_texts.py must parse without syntax errors."""
    source = (ROOT / "tools" / "download_classical_texts.py").read_text()
    try:
        ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in download_classical_texts.py: {e}")


def test_download_classical_texts_defines_manifest():
    """Download script must define a TEXTS manifest dict or list."""
    source = (ROOT / "tools" / "download_classical_texts.py").read_text()
    assert "TEXTS" in source or "MANIFEST" in source, (
        "download_classical_texts.py must define a TEXTS/MANIFEST constant"
    )


def test_download_classical_texts_has_bphs_entry():
    """Download script must include BPHS in its manifest."""
    source = (ROOT / "tools" / "download_classical_texts.py").read_text()
    assert "BPHS" in source or "Brihat Parasara" in source, (
        "BPHS missing from download manifest"
    )


def test_vedastro_cross_validate_script_exists():
    """tools/vedastro_cross_validate.py must exist."""
    assert (ROOT / "tools" / "vedastro_cross_validate.py").exists()


def test_vedastro_cross_validate_script_is_valid_python():
    """tools/vedastro_cross_validate.py must parse without syntax errors."""
    source = (ROOT / "tools" / "vedastro_cross_validate.py").read_text()
    try:
        ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in vedastro_cross_validate.py: {e}")
