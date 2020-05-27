from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, DetailView, UpdateView,TemplateView,ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from . import forms
from django.http import Http404

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
bypage = 1
class UserListView(ListView):
    model = User
    pagecounter = 0
    page = 0
    def get_queryset(self):
        if self.request.user.is_staff:
            userlist =  User.objects.all()
        else:
            raise Http404

        if self.request.GET.get('page'):
            self.page = int(self.request.GET.get('page'))
        self.pagecounter = int((userlist.count()-1 )/ bypage)

        if self.page <= self.pagecounter:
            return userlist[self.page * bypage :(self.page + 1) * bypage]
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['form'] = forms.UserCreateForm
        context['inpage']=self.page
        context['pagecounter']=self.pagecounter
        context['preview']=0
        if self.page: context['preview']= self.page - 1
        context['next']=self.pagecounter
        if not self.page == self.pagecounter: context['next']=self.page + 1
        return context



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
