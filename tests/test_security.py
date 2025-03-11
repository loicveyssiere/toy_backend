import pytest
from fastapi.testclient import TestClient
from src.server import app
from .mocks.services.book_service import MockBookService
from src.services.book_service import BookService

client = TestClient(app)


identified_endpoints = []

app.dependency_overrides[BookService] = MockBookService


def test_create_book():
    response = client.request("POST", "api/books/", json={"title": "title", "author": "author"})
    print(response.content)
    assert response.status_code == 200
    

def test_endpoints():
    response = client.request("GET", "/api/books/12")
    assert response.status_code == 200


def test_nb_endpoints():
    print([(route.path, route.methods) for route in app.routes])
    assert 1 ==1 