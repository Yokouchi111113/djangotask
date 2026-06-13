import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from task.models import Task
from datetime import date
from freezegun import freeze_time


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

