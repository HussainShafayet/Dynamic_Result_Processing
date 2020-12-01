from django import forms
from django.forms import ModelForm
from .models import Course_List


class Course(forms.ModelForm):
    class Meta():
        model = Course_List
        fields = '__all__'
