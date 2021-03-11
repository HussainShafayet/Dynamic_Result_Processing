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
class Course_list(models.Model):
    objects = models.Manager()
    course_code = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=100)
    credit = models.FloatField(max_length=10)
    course_type = models.CharField(max_length=15)
    semester = models.CharField(max_length=10)

    def __str__(self):
        return self.course_code


class Student_Sessions(models.Model):
    objects = models.Manager()
    Batch = models.CharField(max_length=20, primary_key=True)
    Session = models.CharField(max_length=20)

    def __str__(self):
        return self.Batch+' '+self.Session


class Batch(models.Model):
    batch = models.CharField(max_length=50)

    def __str__(self):
        return self.batch


class Session(models.Model):
    session = models.CharField(max_length=50)

    def __str__(self):
        return self.session


class batch_result(models.Model):
    objects = models.Manager()
    Result_Session = models.ForeignKey(
        Student_Sessions, on_delete=models.CASCADE)
    Reg_No = models.CharField(max_length=50, primary_key=True)
    Name = models.CharField(max_length=100)
    # 1ST_SEMESTER
    CSE_101_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_101_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_102_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_102_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_105_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_105_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_106_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_106_LG = models.CharField(max_length=50, null=True, blank=True)
    ME_100_GP = models.FloatField(max_length=10, null=True, blank=True)
    ME_100_LG = models.CharField(max_length=50, null=True, blank=True)
    ME_101_GP = models.FloatField(max_length=10, null=True, blank=True)
    ME_101_LG = models.CharField(max_length=50, null=True, blank=True)
    ME_102_GP = models.FloatField(max_length=10, null=True, blank=True)
    ME_102_LG = models.CharField(max_length=50, null=True, blank=True)
    MATH_101_GP = models.FloatField(max_length=10, null=True, blank=True)
    MATH_101_LG = models.CharField(max_length=50, null=True, blank=True)
    PHY_101_GP = models.FloatField(max_length=10, null=True, blank=True)
    PHY_101_LG = models.CharField(max_length=50, null=True, blank=True)
    PHY_102_GP = models.FloatField(max_length=10, null=True, blank=True)
    PHY_102_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_101_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_101_LG = models.CharField(max_length=50, null=True, blank=True)
    Sem_01_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_01_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_01_LG = models.CharField(max_length=10, null=True, blank=True)
    # 2ND SEMESTER
    CSE_201_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_201_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_202_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_202_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_203_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_203_LG = models.CharField(max_length=50, null=True, blank=True)
    MATH_201_GP = models.FloatField(max_length=10, null=True, blank=True)
    MATH_201_LG = models.CharField(max_length=50, null=True, blank=True)
    CHEM_201_GP = models.FloatField(max_length=10, null=True, blank=True)
    CHEM_201_LG = models.CharField(max_length=50, null=True, blank=True)
    CHEM_202_GP = models.FloatField(max_length=10, null=True, blank=True)
    CHEM_202_LG = models.CharField(max_length=50, null=True, blank=True)
    ENG_201_GP = models.FloatField(max_length=10, null=True, blank=True)
    ENG_201_LG = models.CharField(max_length=50, null=True, blank=True)
    ENG_202_GP = models.FloatField(max_length=10, null=True, blank=True)
    ENG_202_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_201_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_201_LG = models.CharField(max_length=50, null=True, blank=True)
    Sem_02_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_02_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_02_LG = models.CharField(max_length=10, null=True, blank=True)
    Total_Credit_Till_Sem_02 = models.FloatField(
        max_length=10, null=True, blank=True)
    Grade_Point_Till_Sem_02 = models.FloatField(
        max_length=10, null=True, blank=True)
    Letter_Grade_Till_Sem_02 = models.CharField(
        max_length=10, null=True, blank=True)
    # 3RD SEMESTER
    CSE_301_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_301_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_302_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_302_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_303_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_303_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_304_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_304_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_305_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_305_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_306_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_306_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_309_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_309_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_310_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_310_LG = models.CharField(max_length=50, null=True, blank=True)
    MATH_301_GP = models.FloatField(max_length=10, null=True, blank=True)
    MATH_301_LG = models.CharField(max_length=50, null=True, blank=True)
    Sem_03_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_03_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_03_LG = models.CharField(max_length=10, null=True, blank=True)
    Total_Credit_Till_Sem_03 = models.FloatField(
        max_length=10, null=True, blank=True)
    Grade_Point_Till_Sem_03 = models.FloatField(
        max_length=10, null=True, blank=True)
    Letter_Grade_Till_Sem_03 = models.CharField(
        max_length=10, null=True, blank=True)
    # 4TH SEMESTER
    CSE_401_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_401_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_402_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_402_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_403_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_403_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_404_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_404_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_405_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_405_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_407_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_407_LG = models.CharField(max_length=50, null=True, blank=True)
    EEE_408_GP = models.FloatField(max_length=10, null=True, blank=True)
    EEE_408_LG = models.CharField(max_length=50, null=True, blank=True)
    MATH_401_GP = models.FloatField(max_length=10, null=True, blank=True)
    MATH_401_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_401_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_401_LG = models.CharField(max_length=10, null=True, blank=True)
    Sem_04_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_04_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Sem_04_LG = models.CharField(max_length=10, null=True, blank=True)
    Total_Credit_Till_Sem_04 = models.FloatField(
        max_length=10, null=True, blank=True)
    Grade_Point_Till_Sem_04 = models.FloatField(
        max_length=10, null=True, blank=True)
    Letter_Grade_Till_Sem_04 = models.CharField(
        max_length=10, null=True, blank=True)
    # 5TH SEMESTER
    CSE_501_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_501_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_502_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_502_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_503_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_503_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_505_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_505_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_506_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_506_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_507_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_507_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_508_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_508_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_509_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_509_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_501_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_501_LG = models.CharField(max_length=50, null=True, blank=True)
    Z1_Sem_05_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Z2_Sem_05_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Z3_Sem_05_LG = models.CharField(max_length=10, null=True, blank=True)
    Z4_Total_Credit_Till_Sem_05 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z5_Grade_Point_Till_Sem_05 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z6_Letter_Grade_Till_Sem_05 = models.CharField(
        max_length=10, null=True, blank=True)
    # 6TH SEMESTER
    CSE_601_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_601_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_603_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_603_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_604_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_604_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_605_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_605_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_607_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_607_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_608_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_608_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_609_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_609_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_610_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_610_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_612_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_612_LG = models.CharField(max_length=50, null=True, blank=True)
    Z1_Sem_06_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Z2_Sem_06_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Z3_Sem_06_LG = models.CharField(max_length=10, null=True, blank=True)
    Z4_Total_Credit_Till_Sem_06 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z5_Grade_Point_Till_Sem_06 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z6_Letter_Grade_Till_Sem_06 = models.CharField(
        max_length=10, null=True, blank=True)
    # 7TH SEMESTER
    CSE_700_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_700_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_701_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_701_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_702_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_702_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_703_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_703_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_704_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_704_LG = models.CharField(max_length=50, null=True, blank=True)
    IPE_701_GP = models.FloatField(max_length=10, null=True, blank=True)
    IPE_701_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_703_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_703_LG = models.CharField(max_length=50, null=True, blank=True)
    SS_705_GP = models.FloatField(max_length=10, null=True, blank=True)
    SS_705_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_705_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_705_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_707_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_707_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_709_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_709_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_711_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_711_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_713_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_713_LG = models.CharField(max_length=50, null=True, blank=True)
    Z1_Sem_07_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Z2_Sem_07_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Z3_Sem_07_LG = models.CharField(max_length=10, null=True, blank=True)
    Z4_Total_Credit_Till_Sem_07 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z5_Grade_Point_Till_Sem_07 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z6_Letter_Grade_Till_Sem_07 = models.CharField(
        max_length=10, null=True, blank=True)
    # 8TH SEMESTER
    CSE_800_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_800_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_801_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_801_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_802_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_802_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_803_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_803_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_807_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_807_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_808_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_808_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_809_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_809_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_810_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_810_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_811_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_811_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_812_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_812_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_813_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_813_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_814_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_814_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_815_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_815_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_816_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_816_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_817_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_817_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_818_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_818_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_819_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_819_LG = models.CharField(max_length=50, null=True, blank=True)
    CSE_820_GP = models.FloatField(max_length=10, null=True, blank=True)
    CSE_820_LG = models.CharField(max_length=50, null=True, blank=True)
    Z1_Sem_08_Total_Credit = models.FloatField(
        max_length=10, null=True, blank=True)
    Z2_Sem_08_Grade_Point = models.FloatField(
        max_length=10, null=True, blank=True)
    Z3_Sem_08_LG = models.CharField(max_length=10, null=True, blank=True)
    Z4_Total_Credit_Till_Sem_08 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z5_Grade_Point_Till_Sem_08 = models.FloatField(
        max_length=10, null=True, blank=True)
    Z6_Letter_Grade_Till_Sem_08 = models.CharField(
        max_length=10, null=True, blank=True)
