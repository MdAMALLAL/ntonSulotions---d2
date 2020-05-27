from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView,ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import  Client
from .forms import ClientForm



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

bypage = 1
class ClientsList(LoginRequiredMixin,ListView):
    model = Client
    pagecounter = 0
    page = 0

    def get_queryset(self):
        if self.request.user.is_staff:
            clientlist =  Client.objects.all()
        else:
            raise Http404

        if self.request.GET.get('page'):
            self.page = int(self.request.GET.get('page'))
        self.pagecounter = int((clientlist.count()-1 )/ bypage)

        if self.page <= self.pagecounter:
            #print(self.page)
            return clientlist[self.page * bypage :(self.page + 1) * bypage]
        else:
            #self.page = self.pagecounter
            raise Http404






    def get_context_data(self, **kwargs):
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['form'] = ClientForm
        context['inpage']=self.page
        context['pagecounter']=self.pagecounter
        context['preview']=0
        if self.page: context['preview']= self.page - 1
        context['next']=self.pagecounter
        if not self.page == self.pagecounter: context['next']=self.page + 1
        return context





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
