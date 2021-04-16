from django.db import models
#from accounts.models import Teacher
# Create your models here.


class Dept(models.Model):
    dept = models.CharField(max_length=50)

    def __str__(self):
        return self.dept


class Syllabus(models.Model):
    objects = models.Manager()
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    Syllabus_Name = models.CharField(max_length=100)
    Year_created = models.CharField(max_length=20)

    def __str__(self):
        return self.Syllabus_Name


class Course_Semester_List(models.Model):
    objects = models.Manager()
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    Semester = models.CharField(max_length=20)

    def __str__(self):
        return self.Semester


class Course_List_All(models.Model):
    objects = models.Manager()
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        Course_Semester_List, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    credit = models.FloatField(max_length=10)
    course_type = models.CharField(max_length=20)

    def __str__(self):
        return self.course_code


class Sessions(models.Model):
    objects = models.Manager()
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    Batch = models.CharField(max_length=40)
    Session = models.CharField(max_length=20)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)

    def __str__(self):
        return self.Batch


class Result_Semester_List(models.Model):
    objects = models.Manager()
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Semester = models.CharField(max_length=20)

    def __str__(self):
        return self.Semester


class Result_Table(models.Model):
    objects = models.Manager()
    result_semester = models.ForeignKey(
        Result_Semester_List, on_delete=models.CASCADE)
    batch = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Reg = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Column_01 = models.CharField(max_length=50, null=True, blank=True)
    Column_02 = models.CharField(max_length=50, null=True, blank=True)
    Column_03 = models.CharField(max_length=50, null=True, blank=True)
    Column_04 = models.CharField(max_length=50, null=True, blank=True)
    Column_05 = models.CharField(max_length=50, null=True, blank=True)
    Column_06 = models.CharField(max_length=50, null=True, blank=True)
    Column_07 = models.CharField(max_length=50, null=True, blank=True)
    Column_08 = models.CharField(max_length=50, null=True, blank=True)
    Column_09 = models.CharField(max_length=50, null=True, blank=True)
    Column_10 = models.CharField(max_length=50, null=True, blank=True)
    Column_11 = models.CharField(max_length=50, null=True, blank=True)
    Column_12 = models.CharField(max_length=50, null=True, blank=True)
    Column_13 = models.CharField(max_length=50, null=True, blank=True)
    Column_14 = models.CharField(max_length=50, null=True, blank=True)
    Column_15 = models.CharField(max_length=50, null=True, blank=True)
    Column_16 = models.CharField(max_length=50, null=True, blank=True)
    Column_17 = models.CharField(max_length=50, null=True, blank=True)
    Column_18 = models.CharField(max_length=50, null=True, blank=True)
    Column_19 = models.CharField(max_length=50, null=True, blank=True)
    Column_20 = models.CharField(max_length=50, null=True, blank=True)
    Column_21 = models.CharField(max_length=50, null=True, blank=True)
    Column_22 = models.CharField(max_length=50, null=True, blank=True)
    Column_23 = models.CharField(max_length=50, null=True, blank=True)
    Column_24 = models.CharField(max_length=50, null=True, blank=True)
    Column_25 = models.CharField(max_length=50, null=True, blank=True)
    Column_26 = models.CharField(max_length=50, null=True, blank=True)
    Column_27 = models.CharField(max_length=50, null=True, blank=True)
    Column_28 = models.CharField(max_length=50, null=True, blank=True)
    Column_29 = models.CharField(max_length=50, null=True, blank=True)
    Column_30 = models.CharField(max_length=50, null=True, blank=True)
    Column_31 = models.CharField(max_length=50, null=True, blank=True)
    Column_32 = models.CharField(max_length=50, null=True, blank=True)
    Column_33 = models.CharField(max_length=50, null=True, blank=True)
    Column_34 = models.CharField(max_length=50, null=True, blank=True)
    Column_35 = models.CharField(max_length=50, null=True, blank=True)
    Column_36 = models.CharField(max_length=50, null=True, blank=True)
    Column_37 = models.CharField(max_length=50, null=True, blank=True)
    Column_38 = models.CharField(max_length=50, null=True, blank=True)
    Column_39 = models.CharField(max_length=50, null=True, blank=True)
    Column_40 = models.CharField(max_length=50, null=True, blank=True)
    Column_41 = models.CharField(max_length=50, null=True, blank=True)
    Column_42 = models.CharField(max_length=50, null=True, blank=True)
    Column_43 = models.CharField(max_length=50, null=True, blank=True)
    Column_44 = models.CharField(max_length=50, null=True, blank=True)
    Column_45 = models.CharField(max_length=50, null=True, blank=True)
    Column_46 = models.CharField(max_length=50, null=True, blank=True)
    Column_47 = models.CharField(max_length=50, null=True, blank=True)
    Column_48 = models.CharField(max_length=50, null=True, blank=True)
    Column_49 = models.CharField(max_length=50, null=True, blank=True)
    Column_50 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Reg+' '+str(self.result_semester)


# previous model

class Batch(models.Model):
    batch = models.CharField(max_length=50)

    def __str__(self):
        return self.batch


class Session(models.Model):
    session = models.CharField(max_length=50)

    def __str__(self):
        return self.session
