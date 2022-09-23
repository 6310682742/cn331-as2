from dataclasses import field
import imp
from django.forms import ModelForm
from django import forms
from .models import Course
class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ['teacher']
        fields = '__all__'
        widgets = {
            'student': forms.CheckboxSelectMultiple
        }