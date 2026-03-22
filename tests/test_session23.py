"""tests/test_session23.py — Session 23 CI/CD + project health tests."""

from __future__ import annotations
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent


class TestCIFile:
    def test_ci_yml_exists(self):
        assert (ROOT / ".github" / "workflows" / "ci.yml").exists()

    def test_ci_yml_has_pytest(self):
        assert "pytest" in (ROOT / ".github" / "workflows" / "ci.yml").read_text()

    def test_ci_yml_has_ghcr(self):
        assert "ghcr.io" in (ROOT / ".github" / "workflows" / "ci.yml").read_text()

    def test_ci_yml_has_python_312(self):
        assert "3.12" in (ROOT / ".github" / "workflows" / "ci.yml").read_text()

    def test_ci_yml_docker_needs_test(self):
        assert "needs: test" in (ROOT / ".github" / "workflows" / "ci.yml").read_text()


class TestHealth:
    def test_ephemeris(self):
        from src.ephemeris import compute_chart

        assert callable(compute_chart)

    def test_scoring(self):
        from src.scoring import score_chart

        assert callable(score_chart)

    def test_db(self):
        from src.db import init_db

        assert callable(init_db)

    def test_db_pg(self):
        from src.db_pg import init_db

        assert callable(init_db)

    def test_cache(self):
        from src.cache import get

        assert callable(get)

    def test_auth(self):
        from src.auth import register_user

        assert callable(register_user)

    def test_worker(self):
        from src.worker import celery_app

        assert celery_app.main == "lagnamaster"

    def test_auth_router(self):
        from src.api.auth_router import get_current_user

        assert callable(get_current_user)


class TestRequirements:
    @pytest.fixture(scope="class")
    def rt(self):
        return (ROOT / "requirements.txt").read_text().lower()

    def test_pyjwt(self, rt):
        assert "pyjwt" in rt

    def test_bcrypt(self, rt):
        assert "bcrypt" in rt

    def test_celery(self, rt):
        assert "celery" in rt

    def test_redis(self, rt):
        assert "redis" in rt

    def test_reportlab(self, rt):
        assert "reportlab" in rt

    def test_alembic(self, rt):
        assert "alembic" in rt


class TestEntryPoint:
    def test_streamlit_app_exists(self):
        assert (ROOT / "streamlit_app.py").exists()

    def test_adds_sys_path(self):
        assert "sys.path" in (ROOT / "streamlit_app.py").read_text()

    def test_src_init(self):
        assert (ROOT / "src" / "__init__.py").exists()

    def test_calc_init(self):
        assert (ROOT / "src" / "calculations" / "__init__.py").exists()
