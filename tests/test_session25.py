"""tests/test_session25.py — Session 25 Next.js frontend structure tests."""

from __future__ import annotations
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent
FE = ROOT / "frontend"


class TestFrontendStructure:
    def test_package_json_exists(self):
        assert (FE / "package.json").exists()

    def test_next_config_exists(self):
        assert (FE / "next.config.js").exists()

    def test_tsconfig_exists(self):
        assert (FE / "tsconfig.json").exists()

    def test_tailwind_config_exists(self):
        assert (FE / "tailwind.config.ts").exists()

    def test_app_page_exists(self):
        assert (FE / "src" / "app" / "page.tsx").exists()

    def test_app_layout_exists(self):
        assert (FE / "src" / "app" / "layout.tsx").exists()

    def test_api_client_exists(self):
        assert (FE / "src" / "lib" / "api.ts").exists()

    def test_api_tests_exist(self):
        assert (FE / "src" / "lib" / "api.test.ts").exists()

    def test_frontend_readme_exists(self):
        assert (FE / "README.md").exists()


class TestPackageJson:
    @pytest.fixture(scope="class")
    def pkg(self):
        import json

        return json.loads((FE / "package.json").read_text())

    def test_name(self, pkg):
        assert pkg["name"] == "lagnamaster-frontend"

    def test_has_next(self, pkg):
        assert "next" in pkg["dependencies"]

    def test_has_react(self, pkg):
        assert "react" in pkg["dependencies"]

    def test_has_recharts(self, pkg):
        assert "recharts" in pkg["dependencies"]

    def test_has_typescript(self, pkg):
        assert "typescript" in pkg["devDependencies"]

    def test_has_tailwind(self, pkg):
        assert "tailwindcss" in pkg["devDependencies"]

    def test_has_jest(self, pkg):
        assert "jest" in pkg["devDependencies"]

    def test_dev_script(self, pkg):
        assert "dev" in pkg["scripts"]

    def test_build_script(self, pkg):
        assert "build" in pkg["scripts"]

    def test_test_script(self, pkg):
        assert "test" in pkg["scripts"]


class TestApiClient:
    @pytest.fixture(scope="class")
    def api_ts(self):
        return (FE / "src" / "lib" / "api.ts").read_text()

    def test_has_birth_data_interface(self, api_ts):
        assert "BirthDataRequest" in api_ts

    def test_has_chart_out_interface(self, api_ts):
        assert "ChartOut" in api_ts

    def test_has_token_out_interface(self, api_ts):
        assert "TokenOut" in api_ts

    def test_has_auth_module(self, api_ts):
        assert "export const auth" in api_ts

    def test_has_charts_module(self, api_ts):
        assert "export const charts" in api_ts

    def test_has_health_module(self, api_ts):
        assert "export const health" in api_ts

    def test_auth_has_login(self, api_ts):
        assert "login:" in api_ts

    def test_auth_has_register(self, api_ts):
        assert "register:" in api_ts

    def test_auth_has_refresh(self, api_ts):
        assert "refresh:" in api_ts

    def test_sets_bearer_token(self, api_ts):
        assert "Authorization" in api_ts
        assert "Bearer" in api_ts


class TestNextConfig:
    @pytest.fixture(scope="class")
    def config(self):
        return (FE / "next.config.js").read_text()

    def test_has_rewrites(self, config):
        assert "rewrites" in config

    def test_proxies_api(self, config):
        assert "/api/:path*" in config

    def test_standalone_output(self, config):
        assert "standalone" in config
