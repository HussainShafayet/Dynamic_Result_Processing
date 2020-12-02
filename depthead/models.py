from django.db import models



# Create your models here.


class Course_List(models.Model):
    #id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    credit = models.FloatField(max_length=10)
    course_type = models.CharField(max_length=15)
    semester = models.CharField(max_length=10)

    def __str__(self):
        return self.course_code


    
class Batch(models.Model):
    batch = models.CharField(max_length=20)

    def __str__(self):
        return self.batch


class Session(models.Model):
    session = models.CharField(max_length=20)

    def __str__(self):
        return self.session


class Dept(models.Model):
    dept = models.CharField(max_length=20)

    def __str__(self):
        return self.dept

