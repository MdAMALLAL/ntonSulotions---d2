from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, DetailView, UpdateView,TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from . import forms
#from django.contrib.auth import get_user_model
#User = get_user_model()
from .models import User

class NewUser(CreateView):
    model = User
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

class ProfileView(DetailView):
    model = User
    slug_field='username'
    slug_url_kwarg='username'
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model=User
    fields=['username','first_name','last_name','email','client']
    slug_field='username'
    slug_url_kwarg='username'
    user = "user"
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            user = self.request.user
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,"Warning, Profile n'est pas enregistre")
        else:
            messages.success(self.request,"Profile est enregistre.")
        return super().form_valid(form)



    success_url = '/'
