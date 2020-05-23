from django.contrib import admin
from .models import User
# Register your models here.

class UseAdmin(admin.ModelAdmin):
    #fields=['titre', 'created_at','user','priorite','status']
    list_display=['username', 'email','client','is_staff',]
    list_editable=['client','is_staff']
    search_fields = ['username','email']
    list_filter = ['is_staff','client']
admin.site.register(User, UseAdmin)
