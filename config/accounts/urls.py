from django.urls import path
from .views import LoginTemplateView, LogoutView, SignupTemplateView



urlpatterns = [
    path('signup/', SignupTemplateView.as_view(), name='signup'),
    path('signin/', LoginTemplateView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
]