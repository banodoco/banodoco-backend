from django.db import models

from banodoco.base_model import BaseModel

# Create your models here.

class User(BaseModel):
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255)
    password = models.TextField(default=None, null=True)
    type = models.CharField(max_length=50, default="user")
    third_party_id = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        app_label = 'backend'
        db_table = 'user'

