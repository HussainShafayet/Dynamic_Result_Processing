from django.db import models
from depthead.models import Sessions ,Dept
# Create your models here.


class Student_data(models.Model):
    objects = models.Manager()
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20, primary_key=True)
    Name = models.CharField(max_length=100)
    dept = models.CharField(max_length=50)

    def __str__(self):
        return self.Reg_No
