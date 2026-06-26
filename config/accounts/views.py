from rest_framework import generics
from .Signupserializer import SignupSerializer
from django.views.generic import TemplateView



class SignupView(generics.CreateAPIView):

    serializer_class = SignupSerializer



class LoginTemplateView(TemplateView):
    template_name = "accounts/signin.html"


class SignupTemplateView(TemplateView):
    template_name = "accounts/signup.html"


