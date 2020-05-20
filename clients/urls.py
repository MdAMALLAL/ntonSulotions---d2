from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path("", views.ClientsList.as_view(),name='list'),
    path("add/", views.ClientsCreate.as_view(), name="new"),
    path("<slug>/", views.ClientsDetail.as_view(), name="detail"),
    path("<slug>/delete", views.ClientsDelete.as_view(), name="delete"),
    path("<slug>/edit", views.ClientsUpdate.as_view(), name="edit"),


]
