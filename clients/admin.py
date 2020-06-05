from django.contrib import admin
from clients.models import Client
# Register your models here.

from import_export import resources
from import_export.admin import ImportExportModelAdmin
class ClientResource(resources.ModelResource, ):
    class Meta:
        model = Client
class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource
    list_display=['name', 'email','tel',]
    list_editable=['email','tel']
    search_fields = ['name','email']
    # list_filter = ['is_staff','client']


admin.site.register(Client, ClientAdmin)
