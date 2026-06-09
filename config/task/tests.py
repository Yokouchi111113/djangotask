import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task

# 認証なし
def test_task_create_requires_authentication():
    client = APIClient()

    res = client.post(
        "/api/tasks/",
        {"title": "task", "status": "todo"},
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



@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="test@example.com",
        password="password123",
        display_name="test"
    )

@pytest.fixture
def user_b(db):
    return CustomUser.objects.create_user(
        email="testb@example.com",
        password="password147",
        display_name="test01"
    )

#タスク作成
@pytest.fixture
def task_factory():
    def _task(user):
        return Task.objects.create(
            title="DRF",
            status="doing",
            user=user
        )
    return _task


# 認証済みclientをuser指定で作る
@pytest.fixture
def auth_client():
    def _auth_client(user, password):
        client = APIClient()

        res = client.post(
            "/api/signin/",
            {
                "email": user.email,
                "password": password
            },
            format="json"
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}"
        )

        return client
    
    return _auth_client

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

