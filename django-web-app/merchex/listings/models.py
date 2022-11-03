from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=155, unique=True)
    photo = models.ImageField(upload_to='images/')
    time = models.CharField(max_length=155, default=0)

    def __str__(self):
        return self.name

class Userphoto(models.Model):
    photo = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name