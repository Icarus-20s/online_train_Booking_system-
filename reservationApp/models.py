from django.db import models

from django.contrib.auth.hashers import make_password
from django.conf import settings

def hash_raw_password(password: str) -> str:
    return make_password(password, settings.SALT_KEY)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

# Create your models here.
class User (BaseModel):
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        user = User.objects.filter(pk=self.pk).first()
        if not user:
            self.password = hash_raw_password(self.password)
            return super().save(*args, **kwargs)
        password_changed = self.password != user.password
        if not password_changed:
            return super().save(*args, **kwargs)
        self.password = hash_raw_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username






