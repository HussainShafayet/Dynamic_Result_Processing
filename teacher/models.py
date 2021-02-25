from django.db import models
from accounts.models import Teacher
from depthead.models import Sessions
# Create your models here.


class Teacher_name(models.Model):
    objects = models.Manager()
    teacher = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher


class Course(models.Model):
    objects = models.Manager()
    teacher = models.ForeignKey(Teacher_name, on_delete=models.CASCADE)
    Course = models.CharField(max_length=20)
    Active = models.BooleanField(default=True)
    Batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Course_type = models.CharField(max_length=20)

    def __str__(self):
        return self.Course


class Course_Result_Theory(models.Model):
    objects = models.Manager()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Term_test = models.IntegerField()
    Attendence = models.IntegerField()
    Exam_Part_A = models.IntegerField()
    Exam_Part_B = models.IntegerField()
    Total_mark = models.IntegerField()
    Grade_point = models.FloatField()
    Letter_grade = models.CharField(max_length=10)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)

    def __str__(self):
        return self.Reg_No


class Course_Result_Sessional(models.Model):
    objects = models.Manager()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Attendence = models.IntegerField()
    Lab_performance = models.IntegerField()
    Exam = models.IntegerField()
    Total_mark = models.IntegerField()
    Grade_point = models.FloatField()
    Letter_grade = models.CharField(max_length=10)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)

    def __str__(self):
        return self.Reg_No
