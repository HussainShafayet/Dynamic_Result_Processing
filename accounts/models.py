from django.db import models
from django.contrib.auth.models import AbstractUser
from depthead.models import Dept,Batch,Session

# Create your models here.
class User(AbstractUser):
    is_depthead=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_none = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Depthead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=1)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/profile', default='images/profile.png')

    def __str__(self):
        return self.user.username
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact = models.CharField(max_length=15)
    designation = models.CharField(max_length=20)
    teach_fields = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/profile', default='images/profile.png')

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class Student(models.Model):
    Gender = (
        ('male','Male'),
        ('female','Female'),
        ('eunuch','Eunuch'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE,default=1)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,default=1)
    session = models.ForeignKey(Session,on_delete=models.CASCADE,default=1)
    reg_no = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=Gender)
    image = models.ImageField(upload_to='images/profile', default='images/profile.png')

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name
