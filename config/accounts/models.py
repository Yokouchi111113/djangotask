from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager  #AUTH_USER_MODEL = 'アプリ名.CustomUser'　をsettingsに忘れないように

    

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("メールアドレスは必須です")
        
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('メールアドレス', unique=True)
    display_name = models.CharField('表示名', max_length=50, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    @property
    def name(self):

        return self.display_name or self.email.split('@')[0]