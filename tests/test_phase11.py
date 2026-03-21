"""tests/test_phase11.py — Phase 11: Privacy & Legal (S76–78)"""
from __future__ import annotations
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def tmp_db(tmp_path):
    return str(tmp_path / "test.db")

class TestConsentEngine:
    def test_grant_consent(self, tmp_db):
        from src.privacy.consent_engine import grant_consent, has_active_consent
        grant_consent("user1", "core", db_path=tmp_db)
        assert has_active_consent("user1", "core", db_path=tmp_db)

    def test_withdraw_consent(self, tmp_db):
        from src.privacy.consent_engine import grant_consent, withdraw_consent, has_active_consent
        grant_consent("user2", "core", db_path=tmp_db)
        withdraw_consent("user2", "core", db_path=tmp_db)
        assert not has_active_consent("user2", "core", db_path=tmp_db)

    def test_right_to_erasure(self, tmp_db):
        from src.privacy.consent_engine import grant_consent, right_to_erasure
        grant_consent("user3", "core", db_path=tmp_db)
        result = right_to_erasure("user3", db_path=tmp_db)
        assert result["erased"] is True
        assert result["tombstone"] is True

    def test_age_gate_under_18(self):
        from src.privacy.consent_engine import check_age_eligibility
        ok, reason = check_age_eligibility(2020)
        assert not ok
        assert "18" in reason

    def test_age_gate_adult(self):
        from src.privacy.consent_engine import check_age_eligibility
        ok, _ = check_age_eligibility(1990)
        assert ok

class TestFamilyConsent:
    def test_add_member_with_consent(self, tmp_db):
        from src.privacy.family_consent import add_family_member, has_family_consent
        add_family_member("owner1", "member1", "spouse", True, db_path=tmp_db)
        assert has_family_consent("member1", db_path=tmp_db)

    def test_add_member_no_consent(self, tmp_db):
        from src.privacy.family_consent import add_family_member, has_family_consent
        add_family_member("owner1", "member2", "parent", False, db_path=tmp_db)
        assert not has_family_consent("member2", db_path=tmp_db)

    def test_revoke_consent(self, tmp_db):
        from src.privacy.family_consent import add_family_member, revoke_family_consent, has_family_consent
        add_family_member("owner1", "member3", "sibling", True, db_path=tmp_db)
        revoke_family_consent("member3", db_path=tmp_db)
        assert not has_family_consent("member3", db_path=tmp_db)

    def test_compatibility_requires_both(self, tmp_db):
        from src.privacy.consent_engine import grant_consent
        from src.privacy.family_consent import add_family_member, can_run_compatibility
        grant_consent("owner2", "core", db_path=tmp_db)
        add_family_member("owner2", "partner1", "spouse", False, db_path=tmp_db)
        ok, reason = can_run_compatibility("owner2", "partner1", db_path=tmp_db)
        assert not ok
        assert "consented" in reason.lower()

    def test_delete_member(self, tmp_db):
        from src.privacy.family_consent import add_family_member, delete_family_member, has_family_consent
        add_family_member("owner3", "member4", "child", True, db_path=tmp_db)
        delete_family_member("member4", db_path=tmp_db)
        assert not has_family_consent("member4", db_path=tmp_db)

class TestDataMinimisation:
    def test_minimise_birth_time(self):
        from src.privacy.data_minimisation import minimise_birth_time
        h = minimise_birth_time(10.5833)  # 10h35m
        assert abs(h - 10.5833) < 0.02

    def test_hash_ip(self):
        from src.privacy.data_minimisation import hash_ip
        h = hash_ip("192.168.1.1")
        assert len(h) == 16
        assert h == hash_ip("192.168.1.1")
        assert h != hash_ip("10.0.0.1")

    def test_minimise_location(self):
        from src.privacy.data_minimisation import minimise_location
        r = minimise_location(city="Mumbai", state="Maharashtra",
                               country="India", street="123 MG Road", postcode="400001")
        assert "street" not in r
        assert "postcode" not in r
        assert r["city"] == "Mumbai"

    def test_retention_dry_run(self, tmp_db):
        from src.privacy.data_minimisation import apply_retention_policy
        report = apply_retention_policy(db_path=tmp_db, dry_run=True)
        assert "birth_data_eligible" in report
        assert "deleted" in report

    def test_audit_stored_fields(self, tmp_db):
        from src.privacy.data_minimisation import audit_stored_fields
        from src.privacy.consent_engine import ensure_consent_tables
        ensure_consent_tables(tmp_db)
        report = audit_stored_fields(tmp_db)
        assert isinstance(report, list)
