from django.urls import path
from .views import LoginTemplateView, SignupTemplateView



urlpatterns = [
    path('signup/', SignupTemplateView.as_view(), name='signup'),
    path('signin/', LoginTemplateView.as_view(), name='signin'),
]