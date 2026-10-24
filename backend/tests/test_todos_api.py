import json


# ---------- GET /todos ----------

def test_list_todos_empty(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_returns_existing_tasks(seeded_client):
    response = seeded_client.get("/todos")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["First", "Second"]

# ---------- POST /todos ----------

def test_create_todo_with_defaults(client):
    response = client.post("/todos", json={"title": "Learn JavaScript"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn JavaScript",
        "description": "",
        "completed": False,
        "favorite": False,
    }

def test_create_todo_with_description(client):
    response = client.post("/todos", json={"title": "Learn JavaScript", "description": "Fundamentals"})

    assert response.status_code == 201
    assert response.json()["description"] == "Fundamentals"


def test_create_todo_is_saved_in_json_file(client, data_file):
    client.post("/todos", json={"title": "Learn JavaScript"})

    saved = json.loads(data_file.read_text(encoding="utf-8"))
    assert [t["title"] for t in saved] == ["Learn JavaScript"]


def test_create_todo_without_title_returns_422(client):
    response = client.post("/todos", json={"description": "no title"})

    assert response.status_code == 422
    assert client.get("/todos").json() == []

# ---------- PATCH /todos/{id} (completed / favorite) ----------

def test_mark_todo_as_completed(seeded_client):
    response = seeded_client.patch("/todos/1", json={"completed": True})

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_unmark_completed_todo(seeded_client):
    response = seeded_client.patch("/todos/2", json={"completed": False})

    assert response.json()["completed"] is False


def test_mark_and_unmark_favorite(seeded_client):
    on = seeded_client.patch("/todos/1", json={"favorite": True})
    assert on.json()["favorite"] is True

    off = seeded_client.patch("/todos/1", json={"favorite": False})
    assert off.json()["favorite"] is False


def test_patch_does_not_modify_other_fields(seeded_client):
    response = seeded_client.patch("/todos/1", json={"favorite": True})

    body = response.json()
    assert body["title"] == "First"
    assert body["description"] == "desc 1"
    assert body["completed"] is False


def test_patch_status_is_persisted(seeded_client):
    seeded_client.patch("/todos/1", json={"completed": True, "favorite": True})

    todo = next(t for t in seeded_client.get("/todos").json() if t["id"] == 1)
    assert todo["completed"] is True
    assert todo["favorite"] is True


def test_patch_unknown_todo_returns_404(seeded_client):
    response = seeded_client.patch("/todos/999", json={"completed": True})

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

# ---------- DELETE /todos/{id} ----------

def test_delete_todo(seeded_client):
    response = seeded_client.delete("/todos/1")

    assert response.status_code == 204
    assert response.content == b""
    assert [t["id"] for t in seeded_client.get("/todos").json()] == [2]


def test_delete_unknown_todo_returns_404(seeded_client):
    response = seeded_client.delete("/todos/999")

    assert response.status_code == 404
    assert len(seeded_client.get("/todos").json()) == 2


def test_delete_twice_returns_404_the_second_time(seeded_client):
    assert seeded_client.delete("/todos/1").status_code == 204
    assert seeded_client.delete("/todos/1").status_code == 404
