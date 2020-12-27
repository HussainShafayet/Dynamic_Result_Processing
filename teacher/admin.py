from django.contrib import admin
from .models import Course_Result,Teachers,Course
# Register your models here.
admin.site.register(Course_Result)
admin.site.register(Course)
admin.site.register(Teachers)