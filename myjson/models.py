from django.db import models

# Create your models here.
class Securities(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return str(self.username) + str(self.password)
