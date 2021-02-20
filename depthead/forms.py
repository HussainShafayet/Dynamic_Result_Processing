from django import forms
from django.forms import ModelForm
from .models import Course_list, Batch, Student_Sessions, Session, Syllabus, Course_Semester_List


class AddSyllabus(forms.ModelForm):
    class Meta():
        model = Syllabus
        fields = '__all__'


class Add_Semester(forms.ModelForm):
    class Meta():
        model = Course_Semester_List
        fields = [
            'Semester'
        ]

class AddCourse(forms.ModelForm):
    class Meta():
        model = Course_list
        fields = '__all__'

    def clean(self):
        cleaned_data = super(AddCourse, self).clean()
        course_code = cleaned_data.get('course_code')
        if Course_list.objects.filter(course_code=course_code):
            raise forms.ValidationError('Course code already Exists!')
        return self.cleaned_data
class Create_batch(forms.ModelForm):
    class Meta():
        model= Student_Sessions
        fields = '__all__'
    def clean(self):
        cleaned_data = super(Create_batch, self).clean()
        batch = cleaned_data.get('Batch')
        session = cleaned_data.get('Session')
        if Batch.objects.filter(batch=batch):
            raise forms.ValidationError('Batch already Exists!')
        elif Session.objects.filter(session=session):
            raise forms.ValidationError('Session already Exists!')
        return self.cleaned_data
