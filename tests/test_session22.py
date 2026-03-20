"""tests/test_session22.py — Session 22 JWT auth tests."""
from __future__ import annotations
import pytest

def _f(tmp_path):
    import src.auth as a
    db = str(tmp_path / "u.db"); a.init_user_db(path=db); return a, db

class TestReg:
    def test_ok(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("alice","a@x.com","password123",path=db)
        assert u.username=="alice" and u.id>=1
    def test_dup_username(self, tmp_path):
        a,db=_f(tmp_path); a.register_user("bob","b@x.com","password123",path=db)
        with pytest.raises(ValueError,match="taken"):
            a.register_user("bob","b2@x.com","password123",path=db)
    def test_dup_email(self, tmp_path):
        a,db=_f(tmp_path); a.register_user("c","c@x.com","password123",path=db)
        with pytest.raises(ValueError,match="registered"):
            a.register_user("c2","c@x.com","password123",path=db)
    def test_short_pw(self, tmp_path):
        a,db=_f(tmp_path)
        with pytest.raises(ValueError,match="8 characters"):
            a.register_user("d","d@x.com","short",path=db)
    def test_email_lower(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("e","E@X.COM","password123",path=db)
        assert u.email=="e@x.com"
    def test_distinct_ids(self, tmp_path):
        a,db=_f(tmp_path)
        u1=a.register_user("u1","u1@x.com","password123",path=db)
        u2=a.register_user("u2","u2@x.com","password123",path=db)
        assert u1.id!=u2.id

class TestAuth:
    def test_correct(self, tmp_path):
        a,db=_f(tmp_path); a.register_user("f","f@x.com","horse123",path=db)
        assert a.authenticate_user("f","horse123",path=db) is not None
    def test_wrong_pw(self, tmp_path):
        a,db=_f(tmp_path); a.register_user("g","g@x.com","horse123",path=db)
        assert a.authenticate_user("g","wrong",path=db) is None
    def test_unknown(self, tmp_path):
        a,db=_f(tmp_path); assert a.authenticate_user("nobody","any",path=db) is None
    def test_case_insensitive(self, tmp_path):
        a,db=_f(tmp_path); a.register_user("Henry","h@x.com","password123",path=db)
        assert a.authenticate_user("henry","password123",path=db) is not None
    def test_deactivated(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("i","i@x.com","password123",path=db)
        a.deactivate_user(u.id,path=db)
        assert a.authenticate_user("i","password123",path=db) is None

class TestTok:
    @pytest.fixture(autouse=True)
    def need_jwt(self):
        pytest.importorskip("jwt", reason="pyjwt not installed")
    def test_pair(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("j","j@x.com","password123",path=db)
        p=a.create_token_pair(u.id); assert p.access_token and p.refresh_token
    def test_access_decode(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("k","k@x.com","password123",path=db)
        p=a.create_token_pair(u.id); assert a.verify_access_token(p.access_token)==u.id
    def test_refresh_decode(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("l","l@x.com","password123",path=db)
        p=a.create_token_pair(u.id); assert a.verify_refresh_token(p.refresh_token)==u.id
    def test_cross_reject(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("m","m@x.com","password123",path=db)
        p=a.create_token_pair(u.id)
        with pytest.raises(ValueError): a.verify_refresh_token(p.access_token)
    def test_tamper(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("n","n@x.com","password123",path=db)
        p=a.create_token_pair(u.id)
        with pytest.raises(ValueError): a.verify_access_token(p.access_token[:-4]+"XXXX")
    def test_ttl_order(self, tmp_path):
        a,db=_f(tmp_path); u=a.register_user("o","o@x.com","password123",path=db)
        p=a.create_token_pair(u.id); assert p.access_expires_in<p.refresh_expires_in

class TestRouter:
    @pytest.fixture(autouse=True)
    def need_jwt(self): pytest.importorskip("jwt", reason="pyjwt not installed")
    @pytest.fixture
    def client(self, tmp_path):
        import src.auth as a; a.USER_DB_PATH=str(tmp_path/"u.db"); a.init_user_db()
        from fastapi import FastAPI; from fastapi.testclient import TestClient
        from src.api.auth_router import router
        app=FastAPI(); app.include_router(router); return TestClient(app)
    def test_register_201(self, client):
        assert client.post("/auth/register",json={"username":"sam","email":"s@x.com","password":"password123"}).status_code==201
    def test_conflict_409(self, client):
        client.post("/auth/register",json={"username":"tim","email":"t@x.com","password":"password123"})
        assert client.post("/auth/register",json={"username":"tim","email":"t2@x.com","password":"password123"}).status_code==409
    def test_login_tokens(self, client):
        client.post("/auth/register",json={"username":"uma","email":"u@x.com","password":"password123"})
        r=client.post("/auth/login",json={"username":"uma","password":"password123"})
        assert r.status_code==200 and "access_token" in r.json()
    def test_login_wrong_401(self, client):
        client.post("/auth/register",json={"username":"vic","email":"v@x.com","password":"password123"})
        assert client.post("/auth/login",json={"username":"vic","password":"wrong"}).status_code==401
    def test_me(self, client):
        client.post("/auth/register",json={"username":"wes","email":"w@x.com","password":"password123"})
        tok=client.post("/auth/login",json={"username":"wes","password":"password123"}).json()["access_token"]
        r=client.get("/auth/me",headers={"Authorization":f"Bearer {tok}"})
        assert r.status_code==200 and r.json()["username"]=="wes"
    def test_me_no_token_401(self, client):
        assert client.get("/auth/me").status_code==401
    def test_refresh(self, client):
        client.post("/auth/register",json={"username":"xan","email":"x@x.com","password":"password123"})
        rt=client.post("/auth/login",json={"username":"xan","password":"password123"}).json()["refresh_token"]
        r=client.post("/auth/refresh",json={"refresh_token":rt})
        assert r.status_code==200 and "access_token" in r.json()
    def test_logout_204(self, client):
        assert client.post("/auth/logout").status_code==204
