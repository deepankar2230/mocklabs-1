from django import forms
from hr.models import Rating

class RatingForms(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['conducted_by', 'conducted_on', 'student' ]