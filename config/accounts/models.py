from django.db import models
from django.contrib.auth.models import AbstractUser  #AUTH_USER_MODEL = 'アプリ名.CustomUser'　をsettingsに忘れないように


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('メールアドレス', unique=True)
    display_name = models.CharField('表示名', max_length=50, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    @property
    def name(self):

        return self.display_name or self.email.split('@')[0]
    