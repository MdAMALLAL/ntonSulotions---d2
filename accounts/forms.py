from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from django import forms
from .models import User
from clients.models import Client


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2",'first_name','last_name','is_staff','client','supervisor')
        model = User

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        if self.client:
            try:
                self.fields['client'].initial = Client.objects.get(slug=self.client)
            except (ValueError, TypeError):
                pass
        self.fields['supervisor'].queryset = User.objects.filter(is_staff = True)
