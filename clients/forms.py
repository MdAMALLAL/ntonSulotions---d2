from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['signed'].widget.attrs.update({'class': 'dateField'})
    #

    class Meta:
        model = Client
        fields=['name','email','tel','url','address','signed','comment']
        widgets = {
            'signed': forms.DateInput(attrs={'class': 'dateField'}),
        }
