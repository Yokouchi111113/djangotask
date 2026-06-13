import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time


#　認証あり・task作成・DBの状態確認
@pytest.mark.django_db
def test_authenticated_user_can_create_task():
    client = APIClient()
    
    user = CustomUser.objects.create_user(
        email="test@example01.com",
        password="password147",
        display_name="test01"
    )

    res = client.post(
        "/api/signin/",
        {
            "email": "test@example01.com",
            "password": "password147"
        },
        format="json"
    )

    token = res.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    res = client.post(
        "/api/tasks/",
        {
            "title": "DRF勉強",
            "status": "doing"
        },
        format="json"
    )

    assert res.status_code == 201

    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert res.data["title"] == "DRF勉強"
    assert res.data["status"] == "doing"
    assert task.user == user



def test_user_can_get_own_task(
    auth_client,
    user,
    task_factory,
):
    task = task_factory(user)

    client = auth_client(user, "password123")

    res = client.get(
        f"/api/tasks/{task.id}/"
    )

    assert res.status_code == 200
    assert res.data["title"] == "DRF勉強"
    assert res.data["status"] == "doing"


def test_user_can_patch_own_task(
    auth_client,
    user,
    task_factory,
):
    task = task_factory(user)

    client = auth_client(user, "password123")

    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"title": "updated"},
        format="json",
    )

    assert res.status_code == 200
    assert res.data["title"] == "updated"
    task.refresh_from_db()
    assert task.title == "updated"


def test_user_can_delete_own_task(
    auth_client,
    user,
    task_factory,
):
    task = task_factory(user)

    client = auth_client(user, "password123")

    res = client.delete(
        f"/api/tasks/{task.id}/"
    )

    assert res.status_code == 204
    assert not Task.objects.filter(id=task.id).exists()