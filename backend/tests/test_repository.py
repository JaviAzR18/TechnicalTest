import json

from app.models import TodoCreate, TodoUpdate
from app.repository import TodoRepository


def test_get_all_returns_empty_list_when_file_does_not_exist(data_file):
    data_file.unlink()
    assert TodoRepository().get_all() == []


def test_add_assigns_incremental_ids_and_defaults(repo):
    first = repo.add(TodoCreate(title="A"))
    second = repo.add(TodoCreate(title="B", description="desc"))

    assert (first.id, second.id) == (1, 2)
    assert first.description == ""
    assert first.completed is False
    assert first.favorite is False
    assert second.description == "desc"


def test_add_persists_to_json_file(repo, data_file):
    repo.add(TodoCreate(title="Persisted"))

    saved = json.loads(data_file.read_text(encoding="utf-8"))
    assert len(saved) == 1
    assert saved[0]["title"] == "Persisted"


def test_get_by_id(repo):
    created = repo.add(TodoCreate(title="Find me"))

    assert repo.get_by_id(created.id).title == "Find me"
    assert repo.get_by_id(999) is None


def test_update_changes_only_the_given_fields(repo):
    created = repo.add(TodoCreate(title="Keep", description="keep too"))

    updated = repo.update(created.id, TodoUpdate(completed=True))

    assert updated.completed is True
    assert updated.title == "Keep"
    assert updated.description == "keep too"
    assert updated.favorite is False
    assert repo.get_by_id(created.id).completed is True


def test_update_unknown_id_returns_none(repo):
    assert repo.update(999, TodoUpdate(completed=True)) is None


def test_delete_removes_the_todo(repo):
    keep = repo.add(TodoCreate(title="Keep"))
    remove = repo.add(TodoCreate(title="Remove"))

    assert repo.delete(remove.id) is True
    assert [t.id for t in repo.get_all()] == [keep.id]


def test_delete_unknown_id_returns_false(repo):
    repo.add(TodoCreate(title="Only one"))

    assert repo.delete(999) is False
    assert len(repo.get_all()) == 1


def test_ids_are_not_reused_after_deleting_a_middle_todo(repo):
    repo.add(TodoCreate(title="1"))
    middle = repo.add(TodoCreate(title="2"))
    repo.add(TodoCreate(title="3"))
    repo.delete(middle.id)

    new = repo.add(TodoCreate(title="4"))

    assert new.id == 4
