from django import forms
from .models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields=['name','email','tel','url','address','contact','contact_tel','contact_email',]
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'http://'})
        }
