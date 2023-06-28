from django.db import models

from banodoco.base_model import BaseModel

# Create your models here.
class Session(BaseModel):
    token = models.TextField()
    refresh_token = models.TextField()
    role_id = models.CharField(max_length=50)
    role_type = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'session'