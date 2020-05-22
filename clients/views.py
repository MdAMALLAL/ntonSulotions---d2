
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import  Client
from django.utils.translation import gettext_lazy as _



class ClientsCreate(LoginRequiredMixin,CreateView):
    fields=['name','email','tel','url','address','signed','comment']
    model = Client

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Client has been saved."))
            #success_url=reverse_lazy('clients:detail', slug=self.object.slug)
        return super().form_valid(form)

class ClientsDetail(LoginRequiredMixin,DetailView):
    model = Client
class ClientsUpdate(LoginRequiredMixin, UpdateView):
    model= Client
    fields=['name','email','tel','url','address','signed','comment']

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Client has been saved."))
            success_url = reverse_lazy('clients:detail', slug=self.object.slug)

        return super().form_valid(form)

class ClientsList(LoginRequiredMixin,ListView):
    model = Client




class ClientsDelete(LoginRequiredMixin, DeleteView):
    model= Client
    success_url=reverse_lazy('clients:list')


@login_required
def add_user(request, slug, username):
    client = get_object_or_404(Client, slug=slug)
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        try:
            user.client = client
            user.save()
        except IntegrityError:
            messages.warning(request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(request,_("ticket has been resolved, thanks for using owr platform."))
        return redirect('clients:detail', slug=self.object.slug)

    else:
        return redirect('clients:detail', slug=self.object.slug)
