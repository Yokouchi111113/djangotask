import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time



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
