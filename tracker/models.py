from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TrackedCoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_name = models.CharField(max_length=100)
    coin_id = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name
