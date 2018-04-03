from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class MyUser(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    nric = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now())
    photo1 = models.FileField(upload_to="userimage", null=True)
    photo2 = models.FileField(upload_to="userimage", null=True)
    photo3 = models.FileField(upload_to="userimage", null=True)
    complete = models.BooleanField(default=False)
    photoverify = models.BooleanField(default=False)
    digicard = models.CharField(max_length=200, null=True, blank=True)
    randomcode = models.CharField(max_length=200, default="")
    def __str__(self):
        return str(self.username)