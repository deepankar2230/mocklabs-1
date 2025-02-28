from django import forms
from manager.models import *

class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        help_texts = {'username': ''}

roles = [
    ('Trainer', 'Trainer'),
    ('HR', 'HR')
]
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        exclude = ['username']
        widgets = {'role': forms.RadioSelect(choices=roles)}