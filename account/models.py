from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid

# Create your models here.
class regUsers(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=254, null=False, unique=True)
    contactno = models.BigIntegerField()
    userType = models.CharField(max_length=25, default="Customer")
    is_active = models.BooleanField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class credentials(AbstractUser):
    regUser = models.OneToOneField(regUsers, on_delete=models.CASCADE, related_name='regUsers')


class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField()