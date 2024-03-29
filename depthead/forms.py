from django import forms
from django.forms import ModelForm
from .models import Batch, Session, Syllabus, Course_Semester_List, Course_List_All, Sessions,Dept
from accounts.models import Depthead


class AddSyllabus(forms.ModelForm):
    class Meta():
        model = Syllabus
        fields = '__all__'
        labels = {
            'dept': 'Department'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddSyllabus, self).__init__(*args, **kwargs)
        depthead = Depthead.objects.get(user=user)
        dept = depthead.dept
        if user:
           self.fields['dept'].queryset = Dept.objects.filter(
               dept=dept)
    def clean(self):
        cleaned_data = super(AddSyllabus, self).clean()
        syllabus = cleaned_data.get('Syllabus_Name')
        if Syllabus.objects.filter(Syllabus_Name=syllabus):
            raise forms.ValidationError('Syllabus already Exists!')
        return self.cleaned_data


class Add_Semester(forms.ModelForm):
    class Meta():
        model = Course_Semester_List
        fields = [
            'Semester'
        ]


class AddCourse(forms.ModelForm):
    class Meta():
        model = Course_List_All
        fields = [
            'course_code', 'title', 'course_type', 'credit'
        ]

    """ def clean(self):
        cleaned_data = super(AddCourse, self).clean()
        course_code = cleaned_data.get('course_code')
        course = Course_List_All.objects.get(course_code=course_code)
        print(course)
        if course:
            raise forms.ValidationError('Course code already Exists!')
        return self.cleaned_data """


class Create_batch(forms.ModelForm):
    class Meta():
        model = Sessions
        fields = [
            'syllabus', 'Batch', 'Session'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Create_batch, self).__init__(*args, **kwargs)
        depthead = Depthead.objects.get(user=user)
        dept = depthead.dept
        if user:
           self.fields['syllabus'].queryset = Syllabus.objects.filter(dept=dept)

    def clean(self):
        cleaned_data = super(Create_batch, self).clean()
        batch = cleaned_data.get('Batch')
        session = cleaned_data.get('Session')
        if Sessions.objects.filter(Batch=batch):
            raise forms.ValidationError('Batch already Exists!')
        return self.cleaned_data
