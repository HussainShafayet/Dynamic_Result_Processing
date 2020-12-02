from django import forms
from django.forms import ModelForm
from .models import Course_List,Batch


class Course(forms.ModelForm):
    class Meta():
        model = Course_List
        fields = '__all__'

    def clean(self):
        cleaned_data = super(Course, self).clean()
        course_code = cleaned_data.get('course_code')
        if Course_List.objects.filter(course_code=course_code):
            raise forms.ValidationError('Course code already Exists!')
        return self.cleaned_data
class Create_batch(forms.ModelForm):
    class Meta():
        model= Batch
        fields = '__all__'
    def clean(self):
        cleaned_data = super(Create_batch, self).clean()
        batch = cleaned_data.get('batch')
        if Batch.objects.filter(batch=batch):
            raise forms.ValidationError('Batch already Exists!')
        return self.cleaned_data
