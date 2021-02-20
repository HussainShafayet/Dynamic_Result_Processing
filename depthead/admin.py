from django.contrib import admin
from .models import Course_list,Dept,Batch,Session,batch_result,Student_Sessions
from .models import Dept, Syllabus, Course_Semester_List, Course_List_All, Sessions, Result_Semester_List, Result_Table
# Register your models here.
admin.site.register(Course_list),
admin.site.register(Batch),
admin.site.register(Session),
#admin.site.register(Dept),
admin.site.register(batch_result),
admin.site.register(Student_Sessions),

admin.site.register(Dept),
admin.site.register(Syllabus),
admin.site.register(Course_Semester_List),
admin.site.register(Course_List_All),
admin.site.register(Sessions),
admin.site.register(Result_Semester_List),
admin.site.register(Result_Table),
