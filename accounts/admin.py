from django.contrib import admin
from .models import User,Depthead,Teacher,Student

# Register your models here.
admin.site.register(User)
admin.site.register(Depthead)
admin.site.register(Teacher)
admin.site.register(Student)