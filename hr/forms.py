from django import forms
from hr.models import *

class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Schedulings
        exclude = ['slot_id']

    trainer = forms.ModelChoiceField(
        queryset=User.objects.filter(employees__role__iexact = 'trainer'),
        empty_label='Trainer'
    )