import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser

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