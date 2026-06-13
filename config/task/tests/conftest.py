import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time


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