from .models import CustomUser
from rest_framework import viewsets
from rest_framework import generics
from .Signupserializer import SignupSerializer
from .Signinserializer import SigninSerializer



class SignupView(generics.CreateAPIView):

    serializer_class = SignupSerializer

