from django import forms
from .models import Client
from accounts.models import User


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields=['name','email','tel','url','address','contact','contact_tel','contact_email','charged_by']
        # widgets = {
        #     'url': forms.TextInput(attrs={'placeholder': 'http://'})
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charged_by'].queryset = User.objects.filter(is_staff = True)
