from django.urls import path
from . import views
from accounts.views import NewUser as new_user

app_name = 'clients'

urlpatterns = [
    path("", views.ClientsList.as_view(),name='list'),
    path("new/", views.ClientsCreate.as_view(), name="new"),
    path("new_user/", new_user.as_view(), name="new_user"),
    
    #path("new/", views.clientsCreate, name="new"),

    #path("<slug>/", views.ClientsDetail.as_view(), name="detail"),
    path("<slug>/", views.ClientsUpdate.as_view(), name="detail"),

    path("<slug>/delete", views.ClientsDelete.as_view(), name="delete"),
    path("<slug>/edit", views.ClientsUpdate.as_view(), name="edit"),




]
