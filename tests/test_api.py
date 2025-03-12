from fastapi.testclient import TestClient

from src.api.security.auth import AdminSecurity, PublicSecurity
from src.server import app
from src.services.book_service import BookService

from .mocks.book_service import MockBookService

client = TestClient(app)

app.dependency_overrides[BookService] = MockBookService
app.dependency_overrides[AdminSecurity] = PublicSecurity


def test_create_book_no_copy():
    payload = {"title": "title", "author": "author", "published_date": "2015-12-03"}
    response = client.request("POST", "/api/books/", json=payload)
    assert response.status_code == 200

def test_create_book_with_copy():
    payload = {"title": "title", "author": "author", "published_date": "2015-12-03", "copies":[{"condition": "good"}]}
    response = client.request("POST", "/api/books/", json=payload)
    assert response.status_code == 200
