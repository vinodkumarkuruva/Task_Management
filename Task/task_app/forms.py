from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'priority', 'file']


class TaskFilterForm(forms.Form):
    name = forms.CharField(required=False, max_length=255, label='Task Name')
    description = forms.CharField(required=False, label='Task Description')
    status = forms.ChoiceField(required=False, choices=[('', 'All')] + Task.STATUS_CHOICES, label='Status')
    start_date = forms.DateField(required=False, label='From Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, label='To Date', widget=forms.DateInput(attrs={'type': 'date'}))
