from django.contrib import admin
from .models import Course_List, Batch, Session, Dept
# Register your models here.
admin.site.register(Course_List),
admin.site.register(Batch),
admin.site.register(Session),
admin.site.register(Dept),
