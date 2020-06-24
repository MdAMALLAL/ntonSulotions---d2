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
from djqscsv import render_to_csv_response,  write_csv
from django.contrib.auth.mixins import UserPassesTestMixin


class IsStaffTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
def csv_view(request):
  qs = Client.objects.all()
  with open('Client.csv', 'wb') as csv_file:
      write_csv(qs, csv_file)
  return render_to_csv_response(qs)

class ClientsCreate(LoginRequiredMixin, IsStaffTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_list.html'
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Client has been saved."))
        return super().form_valid(form)

class ClientsDetail(LoginRequiredMixin, IsStaffTestMixin, DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_detail.html'
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Client has been saved."))

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ClientsDetail, self).get_context_data(**kwargs)
        context['form'] = ClientForm
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        context['activePage']= 'clientActive'
        return context


class ClientsUpdate(LoginRequiredMixin, IsStaffTestMixin,  UpdateView):
    model= Client
    #fields=['name','email','tel','url','address','signed','comment']
    template_name = 'clients/client_detail.html'
    form_class = ClientForm
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Client has been saved."))


        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ClientsUpdate, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        context['activePage']= 'clientActive'
        return context

class ClientsList(LoginRequiredMixin, IsStaffTestMixin, ListView):
    model = Client

    def get_queryset(self):
        # self.paginate_by =  int(self.request.GET.get('paginate_by', 10))
        if self.request.user.is_staff:
            clientlist =  Client.objects.all()
        else:
            raise Http404
        return clientlist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientForm
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        context['activePage']= 'clientActive'
        return context

class ClientsDelete(LoginRequiredMixin, IsStaffTestMixin,  DeleteView):
    model= Client
    success_url=reverse_lazy('clients:list')
    def get_context_data(self, **kwargs):
        context = super(ClientsDelete, self).get_context_data(**kwargs)
        context['activePage']= 'clientActive'
        return context

@login_required
def add_user(request, slug):
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
        return reverse_lazy("clients:detail", kwargs={"slug": slug})

    else:
        return reverse_lazy("clients:detail", kwargs={"slug": slug})
