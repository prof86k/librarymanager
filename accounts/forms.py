from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from . import models as mdl 


class AdministratorRegisterationForm(UserCreationForm):
    GENDER = (('','...'),('male','Male'),('female','Female'))
    email = forms.EmailField(label="Email",max_length=255,widget=forms.EmailInput(attrs={
        'class':'form-control','required':True,
        'placeholder':'Enter email...'
    }))
    full_name = forms.CharField(label='Fullname:',widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter fullname ...',
        'required':False,
    }))
    gender = forms.CharField(label='Gender:',widget=forms.Select(attrs={
        'class':'form-control', 'required':True,
    }))
    class Meta(UserCreationForm.Meta):
        model = mdl.User
        fields = ['username', 'password1','password2']
        widgets ={
            'username':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter Username...',
                'required':True,
            }),
            'password1':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter password ...',
                'type':'password','required':True,
            }),
            'password2':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Confirm password ...',
                'type':'password','required':True,
            })
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.gender = self.cleaned_data.get('gender')
        user.username = self.cleaned_data.get('username')
        user.password1 = self.cleaned_data.get('password1')
        user.password2 = self.cleaned_data.get('password2')
        user.is_administrator = True
        user.save(commit=True)

        administrator = mdl.Administrator.create(user=user)
        return user

class StudentRegisterationForm(UserCreationForm):
    GENDER = (('','...'),('male','Male'),('female','Female'))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={
        'class':'form-control','required':True,
        'placeholder':'Enter email...'
    }))
    full_name = forms.CharField(label='Fullname:',widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter fullname ...',
        'required':False,
    }))
    gender = forms.CharField(label='Gender:',widget=forms.Select(attrs={
        'class':'form-control', 'required':True,
    }))
    class Meta(UserCreationForm.Meta):
        model = mdl.User
        fields = ['username', 'password1','password2']
        widgets ={
            'username':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter Student ID...',
                'required':True,
            }),
            'password1':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter password ...',
                'type':'password','required':True,
            }),
            'password2':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Confirm password ...',
                'type':'password','required':True,
            })
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.gender = self.cleaned_data.get('gender')
        user.username = self.cleaned_data.get('username')
        user.password1 = self.cleaned_data.get('password1')
        user.password2 = self.cleaned_data.get('password2')
        user.is_student = True
        user.save(commit=True)

        student = mdl.Student.create(user=user)
        return user

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username:',widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter Username/Student ID...',
        'required':True,
    }))
    password = forms.CharField(label='Password:',widget=forms.TextInput(attrs={
        'type':'password','class':'form-control','placeholder':'Enter Password...',
        'required':True,
    }))


    