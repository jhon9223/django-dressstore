from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    img1 = models.ImageField(upload_to='product')
    cat = models.ForeignKey(
        category, on_delete=models.CASCADE,)
    us = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
