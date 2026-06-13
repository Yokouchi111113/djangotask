import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time




# 別のユーザーのタスクを取得できるか
def test_user_cannot_access_other_users_task(
    auth_client,
    user,
    user_b,
    task_factory,
):
    task_obj = task_factory(user)

    client = auth_client(user_b, "password147")

    res = client.get(
        f"/api/tasks/{task_obj.id}/"
    )

    assert res.status_code == 404

# 別のユーザーのタスクを編集できるか
def test_user_cannot_patch_other_users_task(
        auth_client,
        user,
        user_b,
        task_factory,
):
    task = task_factory(user)

    client = auth_client(user_b, "password147")

    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"title": "updated"},
        format="json",
    )

    assert res.status_code == 404
    task.refresh_from_db()
    assert task.title != "updated"


def test_user_cannot_delete_other_users_task(
        auth_client,
        user,
        user_b,
        task_factory,
):
    task = task_factory(user)

    client = auth_client(user_b, "password147")

    res = client.delete(
        f"/api/tasks/{task.id}/"
    )

    assert res.status_code == 404
    assert Task.objects.filter(id=task.id).exists()


def test_user_can_only_see_own_tasks(
        auth_client,
        user,
        user_b,
        task_factory,
):
    task_factory(user)
    task_factory(user_b)

    client = auth_client(user, "password123")

    res = client.get(
        "/api/tasks/"
    )

    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["title"] == "DRF勉強"