from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2",'client')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
