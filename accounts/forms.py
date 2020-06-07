from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from .models import User
from clients.models import Client
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2",'is_staff','client')
        model = User

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)

        super().__init__(*args, **kwargs)
        print(self.client)
        if self.client:
            try:
                self.fields['client'].initial = Client.objects.get(slug=self.client)
            except (ValueError, TypeError):
                pass

class PasswordSetForm(forms.Form):
    print('inForm')
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError(_('The new passwords must be same'))
        else:
            return self.cleaned_data
