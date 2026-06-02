from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} form-control'

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser

        fields = ['email', 'display_name', 'password1', 'password2']