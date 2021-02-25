from django.contrib import admin
from .models import Course_Result_Sessional,Course_Result_Theory,Course,Teacher_name
# Register your models here.
admin.site.register(Course_Result_Theory)
admin.site.register(Course_Result_Sessional)
admin.site.register(Course)
admin.site.register(Teacher_name)