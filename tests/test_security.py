import pytest
from fastapi.testclient import TestClient

from src.api.security.auth import AdminSecurity, APISecurity, PublicSecurity
from src.api.security.auth_manager import AuthSessionManager
from src.context import ContextManager
from src.server import app

from .mocks.fake_route import router as fake_router


@pytest.fixture
def client():
    # Add test routers
    app.include_router(router=fake_router, prefix="/unittest")

    client = TestClient(app)
    yield client  # Exécuter le test avec le client

    # Cleanup
    app.router.routes = [route for route in app.router.routes if "/unittest/" in route.path]


def test_public_security_should_pass_without_token(client: TestClient):
    app.dependency_overrides[PublicSecurity] = PublicSecurity
    response = client.request("GET", "/unittest/ping/")
    assert response.status_code == 200

def test_user_security_should_fail_without_token(client: TestClient):
    app.dependency_overrides[PublicSecurity] = APISecurity
    response = client.request("GET", "/unittest/ping/")
    assert response.status_code == 401

def test_user_security_should_fail_on_invalid_bearer(client: TestClient):
    app.dependency_overrides[PublicSecurity] = APISecurity
    auth = {"Authorization": "Bearer XXX"}
    response = client.request("GET", "/unittest/ping/", headers=auth)
    assert response.status_code == 401

def test_user_security_should_fail_on_invalid_signature(client: TestClient):
    manager = AuthSessionManager(jwt_secret="myfakesecret")
    token = manager.sign_jwt({"name": "loic", "role": "user"})
    app.dependency_overrides[PublicSecurity] = APISecurity
    auth = {"Authorization": f"Bearer {token}"}
    response = client.request("GET", "/unittest/ping/", headers=auth)
    assert response.status_code == 401

def test_user_security_should_pass_on_valid_token(client: TestClient):
    manager = ContextManager().inject_auth_session_manager()
    token = manager.sign_jwt({"name": "loic", "role": "user"})
    app.dependency_overrides[PublicSecurity] = APISecurity
    auth = {"Authorization": f"Bearer {token}"}
    response = client.request("GET", "/unittest/ping/", headers=auth)
    assert response.status_code == 200

def test_admin_security_should_fail_without_admin_role(client: TestClient):
    manager = ContextManager().inject_auth_session_manager()
    token = manager.sign_jwt({"name": "loic", "role": "user"})
    app.dependency_overrides[PublicSecurity] = AdminSecurity
    auth = {"Authorization": f"Bearer {token}"}
    response = client.request("GET", "/unittest/ping/", headers=auth)
    assert response.status_code == 403

def test_admin_security_should_pass_with_admin_role(client: TestClient):
    manager = ContextManager().inject_auth_session_manager()
    token = manager.sign_jwt({"name": "loic", "role": "admin"})
    app.dependency_overrides[PublicSecurity] = AdminSecurity
    auth = {"Authorization": f"Bearer {token}"}
    response = client.request("GET", "/unittest/ping/", headers=auth)
    assert response.status_code == 200
