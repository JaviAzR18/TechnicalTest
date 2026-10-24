import json

import pytest
from fastapi.testclient import TestClient

from app import repository
from app.main import app


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    """Point the repository to a temporary JSON file so the real
    `app/todos.json` is never read or modified by the tests."""
    path = tmp_path / "todos.json"
    path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(repository, "DATA_FILE", path)
    return path


@pytest.fixture
def seeded_data_file(data_file):
    """Temporary JSON file pre-loaded with two tasks."""
    data = [
        {"id": 1, "title": "First", "description": "desc 1", "completed": False, "favorite": False},
        {"id": 2, "title": "Second", "description": "", "completed": True, "favorite": True},
    ]
    data_file.write_text(json.dumps(data), encoding="utf-8")
    return data_file


@pytest.fixture
def repo(data_file):
    return repository.TodoRepository()


@pytest.fixture
def client(data_file):
    return TestClient(app)


@pytest.fixture
def seeded_client(seeded_data_file):
    return TestClient(app)
