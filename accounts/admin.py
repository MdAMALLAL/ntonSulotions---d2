from django.contrib import admin
from .models import User, Notification
# Register your models here.
from import_export import resources
from import_export.admin import  ImportExportModelAdmin
class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UseAdmin(ImportExportModelAdmin):
    #fields=['objet', 'created_at','user','priorite','status']
    list_display=['username', 'email','client','is_staff',]
    list_editable=['client','is_staff']
    search_fields = ['username','email']
    list_filter = ['is_staff','client']
    resource_class = UserResource
admin.site.register(User, UseAdmin)
admin.site.register(Notification)
