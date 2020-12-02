from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,Teacher,Student,Depthead
from django.db import transaction
from depthead.models import Dept, Batch, Session

class TeacherRegForm(UserCreationForm):
    contact = forms.CharField(max_length=15,required=True)
    designation = forms.CharField(max_length=20,required=True)
    location = forms.CharField(max_length=30,required=True)
    image = forms.ImageField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name','last_name','username','email','password1','password2'
        ]
        labels = {
            'email':'Email*'
        }
    def __init__(self, *args, **kwargs):
        super(TeacherRegForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'required': True,
            'autofocus': True,
            'placeholder':'first name'
        })
        self.fields['last_name'].widget.attrs.update({
            'required': True,
            'placeholder':'last name'
        })
        self.fields['username'].widget.attrs.update({
            'required': True,
            'placeholder': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'required': True,
            'placeholder': '***@gmail.com'
        })
        self.fields['password1'].widget.attrs.update({
            'required': True,
            'placeholder': '********'
        })
        self.fields['password2'].widget.attrs.update({
            'required': True,
            'placeholder': '********'
        })
        self.fields['designation'].widget.attrs.update({
            'required': True,
            'placeholder': 'designation'
        })
        self.fields['contact'].widget.attrs.update({
            'placeholder':'01***-******'
        })
        self.fields['location'].widget.attrs.update({
            'required': True,
            'placeholder': 'location'
        })
    @transaction.atomic
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_none=True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.contact = self.cleaned_data.get('contact')
        teacher.designation=self.cleaned_data.get('designation')
        teacher.location = self.cleaned_data.get('location')
        teacher.image = self.cleaned_data.get('image')
        teacher.save()
        return user



class StudentRegForm(UserCreationForm):
    Gender = (
        ('male','Male'),
        ('female','Female'),
        ('eunuch','Eunuch'),
    )

    dept = forms.ModelChoiceField(queryset=Dept.objects.all(), label='Department', empty_label="Choose your Department")
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Choose your Batch")
    session = forms.ModelChoiceField(queryset=Session.objects.all(),empty_label="Choose your Session")
    reg_no = forms.IntegerField(required=True,label='Registration No')
    mobile = forms.CharField(max_length=15, required=True)
    gender=forms.ChoiceField(widget=forms.RadioSelect(),choices=Gender,required=True)
    image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'
        ]
        labels = {
            'email':'Email*'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dept'].queryset=Dept.objects.none()
    def __init__(self, *args, **kwargs):
        super(StudentRegForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'required': True,
            'autofocus': True,
            'placeholder': 'first name'
        })
        self.fields['last_name'].widget.attrs.update({
            'required': True,
            'placeholder': 'last name'
        })
        self.fields['username'].widget.attrs.update({
            'required': True,
            'placeholder': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'required': True,
            'placeholder': '***@gmail.com'
        })
        self.fields['password1'].widget.attrs.update({
            'required': True,
            'placeholder': '********'
        })
        self.fields['password2'].widget.attrs.update({
            'required': True,
            'placeholder': '********'
        })
        
        
        self.fields['reg_no'].widget.attrs.update({
            'required': True,
            'placeholder': 'reg_no'
        })
        self.fields['mobile'].widget.attrs.update({
            'placeholder': '01***-******'
        })
        self.fields['dept'].queryset = Dept.objects.none()
        if 'dept' in self.data:
            self.fields['dept'].queryset = Dept.objects.all()
        elif self.instance.pk:
            self.fields['dept'].queryset = Dept.objects.all().filter(pk=self.instance.dept.pk)

        
        self.fields['batch'].queryset = Batch.objects.none()
        if 'batch' in self.data:
            self.fields['batch'].queryset = Batch.objects.all()
        elif self.instance.pk:
            self.fields['batch'].queryset = Batch.objects.all().filter(
                pk=self.instance.batch.pk)

        self.fields['session'].queryset = Session.objects.none()
        if 'session' in self.data:
            self.fields['session'].queryset = Session.objects.all()
        elif self.instance.pk:
            self.fields['session'].queryset = Session.objects.all().filter(
                pk=self.instance.session.pk)
    @transaction.atomic
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_none=True
        user.save()
        student = Student.objects.create(user=user)
        student.dept = self.cleaned_data.get('dept')
        student.batch = self.cleaned_data.get('batch')
        student.session = self.cleaned_data.get('session')
        student.reg_no = self.cleaned_data.get('reg_no')
        student.mobile = self.cleaned_data.get('mobile')
        student.gender = self.cleaned_data.get('gender')
        student.image = self.cleaned_data.get('image')
        student.save()
        return user
