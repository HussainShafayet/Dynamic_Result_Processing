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
    semester = models.CharField(max_length=20)
    Course_type = models.CharField(max_length=20)

    def __str__(self):
        return self.Course


class Course_Khata(models.Model):
    objects = models.Manager()
    teacher = models.ForeignKey(Teacher_name, on_delete=models.CASCADE)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    Course_Code = models.CharField(max_length=20)
    Exam_Part = models.CharField(max_length=20)
    Active = models.BooleanField(default=True)

    def __str__(self):
        return self.Course_Code+' '+str(self.batch)


class Course_Result_Theory(models.Model):
    objects = models.Manager()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Attendence = models.IntegerField(default=0)
    Term_Test_01 = models.IntegerField(default=0)
    Term_Test_02 = models.IntegerField(default=0)
    Term_Test_03 = models.IntegerField(default=0)
    Term_Test_Total = models.IntegerField(default=0)
    Pre_Final_Total = models.IntegerField(default=0)
    Exam_Part_A_Code = models.CharField(max_length=20, null=True, blank=True)
    Exam_Part_A = models.IntegerField(default=0)
    Exam_Part_B_Code = models.CharField(max_length=20, null=True, blank=True)
    Exam_Part_B = models.IntegerField(default=0)
    Total_mark = models.IntegerField(default=0)
    Grade_point = models.FloatField(default=0)
    Letter_grade = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(
        max_length=20, null=True, blank=True, default=' ')

    def __str__(self):
        return self.Reg_No


class Course_Result_Sessional(models.Model):
    objects = models.Manager()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Attendence = models.IntegerField(default=0)
    Lab_performance = models.IntegerField(default=0)
    Project_mark = models.IntegerField(default=0)
    Exam = models.IntegerField(default=0)
    Total_mark = models.IntegerField(default=0)
    Grade_point = models.FloatField(default=0)
    Letter_grade = models.CharField(max_length=10, null=True, blank=True)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    semester = models.CharField(
        max_length=20, null=True, blank=True, default=' ')

    def __str__(self):
        return self.Reg_No
