from django.db import models
from accounts.models import Teacher
#from depthead.models import Course_List
# Create your models here.


class Teachers(models.Model):
    objects = models.Manager()
    Name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.Name

class Course(models.Model):
    objects = models.Manager()
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    Session = models.CharField(max_length=20, null=True, blank=True)
    Course = models.CharField(max_length=10, null=True, blank=True)
    Active = models.BooleanField(default=True, null=True, blank=True)
    Batch = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.Course

class Course_Result(models.Model):
    objects = models.Manager()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20, null=True, blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Term_test = models.IntegerField(default=0, null=True, blank=True)
    Attendence = models.IntegerField(default=0, null=True, blank=True)
    Exam_Part_A = models.IntegerField(default=0, null=True, blank=True)
    Exam_Part_B = models.IntegerField(default=0, null=True, blank=True)
    Total_mark = models.IntegerField(default=0, null=True, blank=True)
    Grade_point = models.FloatField(
        default=0, max_length=10, null=True, blank=True)
    Letter_grade = models.CharField(max_length=10, default=' ', blank=True)

    def __str__(self):
        return self.Reg_No
