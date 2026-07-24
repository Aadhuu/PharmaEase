from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields=['prescription']

        widgets = {'prescription': forms.FileInput(attrs={'class': 'form-control'})
        }