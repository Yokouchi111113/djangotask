import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser

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
