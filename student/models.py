from django.db import models
from depthead.models import Student_Sessions 
# Create your models here.


class Students(models.Model):
    objects = models.Manager()
    session = models.ForeignKey(Student_Sessions, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20, primary_key=True)
    Name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    Dept = models.CharField(max_length=10)
    Phone = models.CharField(max_length=20)
