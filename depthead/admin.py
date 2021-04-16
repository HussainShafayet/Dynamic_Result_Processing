from django.contrib import admin
from .models import Dept, Batch, Session
from .models import Dept, Syllabus, Course_Semester_List, Course_List_All, Sessions, Result_Semester_List, Result_Table
# Register your models here.

admin.site.register(Batch),
admin.site.register(Session),
admin.site.register(Dept),
admin.site.register(Syllabus),
admin.site.register(Course_Semester_List),
admin.site.register(Course_List_All),
admin.site.register(Sessions),
admin.site.register(Result_Semester_List),
admin.site.register(Result_Table),
