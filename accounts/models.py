from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_administrator = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    full_name = models.CharField(verbose_name="Full Name:",max_length=255,null=True)
    gender = models.CharField(verbose_name='Gender',max_length=25,null=True)



class Administrator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Administrators'


    def __str__(self) -> str:
        return self.user.username



class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username
