from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date
from django.conf import settings


STATUS_CHOICES = [
    ("todo", "未着手"),
    ("doing", "進行中"),
    ("done", "完了"),
]


class Task(models.Model):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[
            ("todo", "未着手"),
            ("doing", "進行中"),
            ("done", "完了"),
        ],
        default="todo"
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def days_until_due(self):
        if not self.due_date:
            return None
        
        delta = self.due_date - date.today()
        return delta.days
    
    def __str__(self):
        return self.title


