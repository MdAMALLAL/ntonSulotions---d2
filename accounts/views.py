from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import CreateView, DetailView, UpdateView,TemplateView,ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from . import forms
from  clients.models import Client
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views

from django.core.exceptions import PermissionDenied

class DoesLoggedInUserOwnThisRowMixin(object):

    def get_object(self):
        '''only allow owner (or superuser) to access the table row'''
        obj = super(DoesLoggedInUserOwnThisRowMixin, self).get_object()
        print(obj)
        if self.request.user.is_superuser:
            pass
        elif obj != self.request.user:
            raise PermissionDenied(
                "Permission Denied -- that's not your record!")
        return obj

#from django.contrib.auth import get_user_model
#User = get_user_model()
from .models import User
active = {}
active['users']='active'

class IsStaffTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

from djqscsv import render_to_csv_response,  write_csv
def csv_view(request):
  qs = User.objects.all()
  with open('User.csv', 'wb') as csv_file:
      write_csv(qs, csv_file)
  return render_to_csv_response(qs)

class NewUser(IsStaffTestMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "registration/signup.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active']=active
        return context

class ProfileView(DetailView):
    model = User
    slug_field='username'
    slug_url_kwarg='username'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.username)
        # print(self.kwargs.get('username'))

        if self.request.user.username == self.kwargs.get('username'):
            active['users']=''
            active['person']='active'

        context['active']=active
        return context

def myProfileView(request):
    return redirect('accounts:profile', username=request.user.username)


class UserListView(IsStaffTestMixin, ListView):
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

        context['active']=active
        context['form'] = forms.UserCreateForm
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        context['clients']=Client.objects.all()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model=User
    fields=['username','first_name','last_name','tel','email','client','is_staff','avatar']
    slug_field='username'
    slug_url_kwarg='username'
    user = "user"
    def get_object(self, *args, **kwargs):
        obj = super(ProfileUpdateView, self).get_object(*args, **kwargs)
        print(obj.username)
        print(self.request.user.username)

        if obj.username != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied() #or Http404
        return obj

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active']=active
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active']=active
        return context


    success_url = '/'

@login_required
def made_consultant(request, username):
    user = get_object_or_404(User, username=username)
    # print(user)
    if request.user.is_staff:
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


class UserPasswordChang( auth_views.PasswordChangeView):
    # def __init__(self, arg):
    #         self.get_object
    #         super(UserPasswordChang, self).__init__()
    def get_object(self,  *args, **kwargs):
        '''only allow owner (or superuser) to access the table row'''
        obj = Users.objects.get(username = self.request.user.username)
        # obj = super(UserPasswordChang, self).get_object()
        # print('''only allow owner (or superuser) to access the table row''')
        # print(obj)
        # if self.request.user.is_superuser:
        #     pass
        # elif obj != self.request.user:
        #     raise PermissionDenied(
        #         "Permission Denied -- that's not your record!")
        return obj
    template_name='accounts/password_change_form.html'
