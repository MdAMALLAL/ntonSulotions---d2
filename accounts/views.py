from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import CreateView, DetailView, UpdateView,TemplateView,ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from . import forms
from  clients.models import Client
from django.http import Http404
from django.utils.translation import gettext_lazy as _


#from django.contrib.auth import get_user_model
#User = get_user_model()
from .models import User

from djqscsv import render_to_csv_response,  write_csv
def csv_view(request):
  qs = User.objects.all()
  with open('User.csv', 'wb') as csv_file:
      write_csv(qs, csv_file)
  return render_to_csv_response(qs)

class NewUser(CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "registration/signup.html"

    def get_form_kwargs(self):
        kwargs = super(NewUser, self).get_form_kwargs()
        kwargs['client'] = self.request.GET.get('client')
        return kwargs

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("User has been saved."))
            return redirect('accounts:profile', username=self.object.username)

        return super().form_valid(form)

class ProfileView(DetailView):
    model = User
    slug_field='username'
    slug_url_kwarg='username'

class UserListView(ListView):
    model = User

    def get_queryset(self):
        self.paginate_by =  int(self.request.GET.get('paginate_by', 4))

        if self.request.user.is_staff:
            userlist =  User.objects.all()
        else:
            raise Http404

        if self.request.GET.get('client'):
            userlist =  User.objects.filter(client = self.request.GET.get('client'))

        return userlist

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['form'] = forms.UserCreateForm
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        context['clients']=Client.objects.all()
        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model=User
    fields=['username','first_name','last_name','tel','email','client']
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


@login_required
def made_consultant(request, username):
    user = get_object_or_404(User, username=username)
    print(user)

    if request.method == "POST":
        try:
            if user.is_staff:
                user.is_staff = False
                messages_text = _("{0} is removed from consultant list".format(user))
            else:
                user.is_staff = True
                messages_text = _("{0} is added to consultant list".format(user))

            user.save()
        except IntegrityError:
            messages.warning(request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(request,messages_text)
    return redirect('accounts:profile', username=user.username)
