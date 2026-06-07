import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser

# 認証なし
def test_task_create_requires_authentication():
    client = APIClient()

    res = client.post(
        "/api/tasks/",
        {"title": "task", "status": "todo"},
        format="json",
    )

    assert res.status_code == 401


def test_task_get_requires_authentication():
    client = APIClient()

    res = client.get(
        "/api/tasks/"
    )

    assert res.status_code == 401


def test_task_delete_requires_authentication():
    client = APIClient()

    res = client.delete(
        "/api/tasks/2/"
    )

    assert res.status_code == 401



#　user登録
@pytest.mark.django_db
def test_signup_success():
    client = APIClient()

    res = client.post(
        "/api/signup/",
        {"email": "test@example01.com", "display_name": "test01", 
         "password1": "password147", "password2": "password147"},
        format="json",
    )

    assert res.status_code == 201

#　ログイン
@pytest.mark.django_db
def test_signin_success():
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

    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data

#　task作成
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