# forms.py

from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TaskForm(forms.ModelForm):
    context_object_name = 'task'
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'deadline','deadline_time']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
           'deadline_time': forms.TimeInput(attrs={'type': 'time'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.deadline_time:
            self.initial['deadline_time'] = self.instance.deadline_time
# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]