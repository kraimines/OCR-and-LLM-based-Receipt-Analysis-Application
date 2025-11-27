from django import forms
from .models import ExtractionHistory

class TicketUploadForm(forms.ModelForm):
    class Meta:
        model = ExtractionHistory
        fields = ['image']
