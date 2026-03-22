"""tests/test_session24.py — Session 24 Kubernetes + Helm chart tests."""

from __future__ import annotations
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent
HELM = ROOT / "helm" / "lagnamaster"


class TestHelmStructure:
    def test_chart_yaml_exists(self):
        assert (HELM / "Chart.yaml").exists()

    def test_values_yaml_exists(self):
        assert (HELM / "values.yaml").exists()

    def test_templates_dir_exists(self):
        assert (HELM / "templates").is_dir()

    def test_api_deployment_exists(self):
        assert (HELM / "templates" / "api-deployment.yaml").exists()

    def test_api_service_exists(self):
        assert (HELM / "templates" / "api-service.yaml").exists()

    def test_ui_deployment_exists(self):
        assert (HELM / "templates" / "ui-deployment.yaml").exists()

    def test_ui_service_exists(self):
        assert (HELM / "templates" / "ui-service.yaml").exists()

    def test_worker_deployment_exists(self):
        assert (HELM / "templates" / "worker-deployment.yaml").exists()

    def test_ingress_exists(self):
        assert (HELM / "templates" / "ingress.yaml").exists()

    def test_hpa_exists(self):
        assert (HELM / "templates" / "api-hpa.yaml").exists()

    def test_helpers_tpl_exists(self):
        assert (HELM / "templates" / "_helpers.tpl").exists()

    def test_notes_exists(self):
        assert (HELM / "templates" / "NOTES.txt").exists()


class TestHelmContent:
    @pytest.fixture(scope="class")
    def values(self):
        pytest.importorskip("yaml")
        import yaml

        return yaml.safe_load((HELM / "values.yaml").read_text())

    @pytest.fixture(autouse=True)
    def need_yaml(self):
        pytest.importorskip("yaml", reason="pyyaml not installed")

    def test_api_port_is_8000(self, values):
        assert values["api"]["port"] == 8000

    def test_ui_port_is_8501(self, values):
        assert values["ui"]["port"] == 8501

    def test_autoscaling_enabled(self, values):
        assert values["api"]["autoscaling"]["enabled"] is True

    def test_min_replicas_ge_2(self, values):
        assert values["api"]["autoscaling"]["minReplicas"] >= 2

    def test_max_replicas_ge_min(self, values):
        hpa = values["api"]["autoscaling"]
        assert hpa["maxReplicas"] >= hpa["minReplicas"]

    def test_image_registry_is_ghcr(self, values):
        assert "ghcr.io" in values["image"]["registry"]

    def test_ingress_enabled(self, values):
        assert values["ingress"]["enabled"] is True

    def test_worker_queues_includes_heavy(self, values):
        assert "heavy" in values["worker"]["queues"]


class TestHelmTemplateSyntax:
    """Validate template file content without running helm."""

    def test_api_deployment_has_liveness(self):
        content = (HELM / "templates" / "api-deployment.yaml").read_text()
        assert "livenessProbe" in content

    def test_api_deployment_has_readiness(self):
        content = (HELM / "templates" / "api-deployment.yaml").read_text()
        assert "readinessProbe" in content

    def test_api_deployment_health_path(self):
        content = (HELM / "templates" / "api-deployment.yaml").read_text()
        assert "/health" in content

    def test_worker_uses_celery_command(self):
        content = (HELM / "templates" / "worker-deployment.yaml").read_text()
        assert "celery" in content

    def test_worker_uses_api_image(self):
        content = (HELM / "templates" / "worker-deployment.yaml").read_text()
        assert "lagnamaster-api" in content

    def test_ingress_references_both_services(self):
        content = (HELM / "templates" / "ingress.yaml").read_text()
        assert "api.name" in content
        assert "ui.name" in content

    def test_helpers_defines_labels(self):
        content = (HELM / "templates" / "_helpers.tpl").read_text()
        assert "lagnamaster.labels" in content

    def test_helpers_defines_secret_env(self):
        content = (HELM / "templates" / "_helpers.tpl").read_text()
        assert "JWT_SECRET" in content
        assert "PG_DSN" in content
        assert "REDIS_URL" in content
