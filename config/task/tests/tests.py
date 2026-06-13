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
    def _task(
        user,
        title="DRF勉強",
        description="",
        status="doing",
        due_date=None,
    ):
        return Task.objects.create(
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            user=user,
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


def test_task_create_requires_title(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "", 
         "status": "todo"},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_requires_status(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": ""},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_requires_title_status_none(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "", 
         "status": ""},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_due_date(
        auth_client,
        user
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": "doing",
         "due_date": "2000-01-01"},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_due_date_success(
        auth_client,
        user
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": "doing",
         "due_date": "2111-01-01"},
        format="json",
    )

    assert res.status_code == 201


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


def test_task_detail_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.get(
        "/api/tasks/99999/"
     )

    assert res.status_code == 404

def test_task_patch_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.patch(
        "/api/tasks/99999/",
        {"title": "updated"},
        format="json",
        )

    assert res.status_code == 404

def test_task_delete_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.delete(
        "/api/tasks/99999/"
        )

    assert res.status_code == 404


def test_task_status_choice_no_exists(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {
            "title": "DRF",
            "status": "complete"
        },
        format="json",
        )

    assert res.status_code == 400


@freeze_time("2026-06-11")
def test_filter_due_within_7_days(auth_client, user):
    client = auth_client(user, "password123")

    client.post(
        "/api/tasks/",
        {
            "title": "today",
            "status": "doing",
            "due_date": "2026-06-11",
        },
        format="json",
    )

    client.post(
        "/api/tasks/",
        {
            "title": "limit",
            "status": "doing",
            "due_date": "2026-06-18",
        },
        format="json",
    )

    client.post(
        "/api/tasks/",
        {
            "title": "over",
            "status": "doing",
            "due_date": "2026-06-19",
        },
        format="json",
    )

    res = client.get(
        "/api/tasks/?due_within=7"
        )

    assert res.status_code == 200
    assert len(res.data) == 2

    titles = [task["title"] for task in res.data]

    assert "today" in titles
    assert "limit" in titles
    assert "over" not in titles


# 検索 title
def test_search_by_title(
    auth_client,
    user,
    task_factory,
):
    task_factory(
        user, 
        title="DRF勉強"
        )
    task_factory(
        user, 
        title="Python勉強"
        )

    client = auth_client(user, "password123")

    res = client.get(
        "/api/tasks/?q=DRF"
        )

    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["title"] == "DRF勉強"

# 検索 description
def test_search_by_description(
    auth_client,
    user,
    task_factory,
):
    task_factory(
        user, 
        title="テスト1",
        description="Django REST Framework"
        )
    task_factory(
        user, 
        title="タスク2",
        description="Playwright"
        )

    client = auth_client(user, "password123")

    res = client.get(
        "/api/tasks/?q=Django"
        )
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["description"] == "Django REST Framework"

# &検索
def test_search_by_multiple_words(
    auth_client,
    user,
    task_factory,
):
    task_factory(
        user, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    task_factory(
        user, 
        title="DRF勉強",
        description="Playwright"
        )
    
    client = auth_client(user, "password123")
    
    res = client.get(
        "/api/tasks/?q=DRF REST"
    )

    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]["description"] == "Django REST Framework"


def test_search_by_q_none(
    auth_client,
    user,
    task_factory,
):
    task_factory(
        user, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    task_factory(
        user, 
        title="DRF勉強",
        description="Playwright"
        )
    
    client = auth_client(user, "password123")
    
    res = client.get(
        "/api/tasks/?q="
    )

    assert res.status_code == 200
    assert len(res.data) == 2

def test_search_by_q_none(
    auth_client,
    user,
    user_b,
    task_factory,
):
    task_factory(
        user, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    task_factory(
        user_b, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    
    client = auth_client(user, "password123")
    
    res = client.get(
        "/api/tasks/?q=DRF"
    )

    assert res.status_code == 200
    assert len(res.data) == 1

def test_search_by_pointless_word(
    auth_client,
    user,
    user_b,
    task_factory,
):
    task_factory(
        user, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    task_factory(
        user_b, 
        title="DRF勉強",
        description="Django REST Framework"
        )
    
    client = auth_client(user, "password123")
    
    res = client.get(
        "/api/tasks/?q=54782514567"
    )

    assert res.status_code == 200
    assert len(res.data) == 0



def test_task_patch_invalid_status(
    auth_client,
    user,
    task_factory,
):
    task = task_factory(user)

    client = auth_client(user, "password123")

    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"status": "complete"},
        format="json",
    )
    
    assert res.status_code == 400
    task.refresh_from_db()
    assert task.status != "complete"


def test_task_str(
    task_factory, 
    user
):
    task = task_factory(user, title="DRF勉強")

    assert str(task) == "DRF勉強"


@freeze_time("2026-06-11")
def test_days_until_due(
    user, 
    task_factory
):
    task = task_factory(
        user,
        due_date=date(2026, 6, 18)
    )

    assert task.days_until_due == 7


def test_days_until_due_none(user, task_factory):
    task = task_factory(
        user,
        due_date=None
    )

    assert task.days_until_due is None

