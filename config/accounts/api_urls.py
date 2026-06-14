from django.urls import path
from . import views
from .views import SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', TokenObtainPairView.as_view(), name="api_signin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

