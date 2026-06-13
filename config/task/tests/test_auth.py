import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time



# 認証なし
def test_task_create_requires_authentication():
    client = APIClient()

    res = client.post(
        "/api/tasks/",
        {"title": "task", 
         "status": "todo"},
        format="json",
    )

    assert res.status_code == 401


def test_task_list_requires_authentication():
    client = APIClient()

    res = client.get(
        "/api/tasks/"
    )

    assert res.status_code == 401


def test_task_detail_requires_authentication(task_factory, user):
    client = APIClient()

    task = task_factory(user)

    res = client.get(
        f"/api/tasks/{task.id}/"
    )

    assert res.status_code == 401


def test_task_patch_requires_authentication(task_factory, user):
    client = APIClient()

    task = task_factory(user)

    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"title": "updated"},
        format="json",
    )

    assert res.status_code == 401


def test_task_delete_requires_authentication(task_factory, user):
    client = APIClient()

    task = task_factory(user)

    res = client.delete(
        f"/api/tasks/{task.id}/"
    )

    assert res.status_code == 401