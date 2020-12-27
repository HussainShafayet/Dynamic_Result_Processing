from django.contrib import admin
from .models import Course_list,Dept,Batch,Session,batch_result,Student_Sessions
# Register your models here.
admin.site.register(Course_list),
admin.site.register(Batch),
admin.site.register(Session),
admin.site.register(Dept),
admin.site.register(batch_result),
admin.site.register(Student_Sessions),