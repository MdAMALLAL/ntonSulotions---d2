from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from .models import User
from clients.models import Client


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2",'is_staff','client')
        model = User

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)

        super().__init__(*args, **kwargs)
        if self.client:
            try:
                self.fields['client'].initial = Client.objects.get(slug=self.client)
            except (ValueError, TypeError):
                pass
