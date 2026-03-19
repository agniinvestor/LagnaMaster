"""tests/test_session22.py - LagnaMaster Session 22 tests."""
from __future__ import annotations
import pytest

def _fresh(tmp_path):
    import src.auth as a
    db = str(tmp_path / "users.db")
    a.init_user_db(path=db)
    return a, db

class TestRegistration:
    def test_register_returns_user(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("alice", "alice@x.com", "password123", path=db)
        assert u.username == "alice" and u.id >= 1

    def test_duplicate_username_raises(self, tmp_path):
        a, db = _fresh(tmp_path)
        a.register_user("bob", "bob@x.com", "password123", path=db)
        with pytest.raises(ValueError, match="taken"):
            a.register_user("bob", "bob2@x.com", "password123", path=db)

    def test_duplicate_email_raises(self, tmp_path):
        a, db = _fresh(tmp_path)
        a.register_user("carol", "carol@x.com", "password123", path=db)
        with pytest.raises(ValueError, match="registered"):
            a.register_user("carol2", "carol@x.com", "password123", path=db)

    def test_short_password_raises(self, tmp_path):
        a, db = _fresh(tmp_path)
        with pytest.raises(ValueError, match="8 characters"):
            a.register_user("dave", "d@x.com", "short", path=db)

    def test_email_stored_lowercase(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("eve", "EVE@X.COM", "password123", path=db)
        assert u.email == "eve@x.com"

    def test_distinct_ids(self, tmp_path):
        a, db = _fresh(tmp_path)
        u1 = a.register_user("u1","u1@x.com","password123",path=db)
        u2 = a.register_user("u2","u2@x.com","password123",path=db)
        assert u1.id != u2.id

class TestAuthentication:
    def test_correct_creds(self, tmp_path):
        a, db = _fresh(tmp_path)
        a.register_user("frank","f@x.com","correcthorse",path=db)
        assert a.authenticate_user("frank","correcthorse",path=db) is not None

    def test_wrong_password(self, tmp_path):
        a, db = _fresh(tmp_path)
        a.register_user("grace","g@x.com","correcthorse",path=db)
        assert a.authenticate_user("grace","wrong",path=db) is None

    def test_unknown_user(self, tmp_path):
        a, db = _fresh(tmp_path)
        assert a.authenticate_user("nobody","any",path=db) is None

    def test_case_insensitive(self, tmp_path):
        a, db = _fresh(tmp_path)
        a.register_user("Henry","h@x.com","password123",path=db)
        assert a.authenticate_user("henry","password123",path=db) is not None

    def test_deactivated_cannot_login(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("ivan","i@x.com","password123",path=db)
        a.deactivate_user(u.id, path=db)
        assert a.authenticate_user("ivan","password123",path=db) is None

class TestTokens:
    @pytest.fixture(autouse=True)
    def need_jwt(self):
        try: import jwt
        except ImportError: pytest.skip("PyJWT not installed")

    def test_token_pair(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("j","j@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        assert p.access_token and p.refresh_token

    def test_access_decodes(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("k","k@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        assert a.verify_access_token(p.access_token) == u.id

    def test_refresh_decodes(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("l","l@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        assert a.verify_refresh_token(p.refresh_token) == u.id

    def test_cross_token_rejected(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("m","m@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        with pytest.raises(ValueError): a.verify_refresh_token(p.access_token)

    def test_tampered_raises(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("n","n@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        with pytest.raises(ValueError): a.verify_access_token(p.access_token[:-4]+"XXXX")

    def test_access_ttl_shorter(self, tmp_path):
        a, db = _fresh(tmp_path)
        u = a.register_user("o","o@x.com","password123",path=db)
        p = a.create_token_pair(u.id)
        assert p.access_expires_in < p.refresh_expires_in

class TestAuthRouter:
    @pytest.fixture(autouse=True)
    def need_jwt(self):
        try: import jwt
        except ImportError: pytest.skip("PyJWT not installed")

    @pytest.fixture
    def client(self, tmp_path):
        import src.auth as a
        a.USER_DB_PATH = str(tmp_path / "users.db")
        a.init_user_db()
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from src.api.auth_router import router
        app = FastAPI(); app.include_router(router)
        return TestClient(app)

    def test_register_201(self, client):
        r = client.post("/auth/register",json={"username":"sam","email":"s@x.com","password":"password123"})
        assert r.status_code == 201

    def test_duplicate_409(self, client):
        client.post("/auth/register",json={"username":"tim","email":"t@x.com","password":"password123"})
        r = client.post("/auth/register",json={"username":"tim","email":"t2@x.com","password":"password123"})
        assert r.status_code == 409

    def test_login_tokens(self, client):
        client.post("/auth/register",json={"username":"uma","email":"u@x.com","password":"password123"})
        r = client.post("/auth/login",json={"username":"uma","password":"password123"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_401(self, client):
        client.post("/auth/register",json={"username":"v","email":"v@x.com","password":"password123"})
        r = client.post("/auth/login",json={"username":"v","password":"wrong"})
        assert r.status_code == 401

    def test_me_returns_profile(self, client):
        client.post("/auth/register",json={"username":"will","email":"w@x.com","password":"password123"})
        token = client.post("/auth/login",json={"username":"will","password":"password123"}).json()["access_token"]
        r = client.get("/auth/me",headers={"Authorization":f"Bearer {token}"})
        assert r.status_code == 200 and r.json()["username"] == "will"

    def test_me_no_token_401(self, client):
        assert client.get("/auth/me").status_code == 401

    def test_refresh(self, client):
        client.post("/auth/register",json={"username":"xena","email":"x@x.com","password":"password123"})
        rt = client.post("/auth/login",json={"username":"xena","password":"password123"}).json()["refresh_token"]
        r = client.post("/auth/refresh",json={"refresh_token":rt})
        assert r.status_code == 200 and "access_token" in r.json()

    def test_logout_204(self, client):
        assert client.post("/auth/logout").status_code == 204
