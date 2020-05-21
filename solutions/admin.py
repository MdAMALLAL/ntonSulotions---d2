from django.contrib import admin
from .models import Question, Reponce, SousCategorie, Categorie

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    #fields=['titre', 'created_at','user','priorite','status']
    list_display=['titre', 'created_at','user','priorite','status']
    list_editable=['priorite','status']
    search_fields = ['titre','description']
    list_filter = ['created_at','user','priorite','status']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Reponce)

class SousCategorieInline(admin.TabularInline):
    model=SousCategorie
    extra=3
admin.site.register(SousCategorie)

class CategorieAdmin(admin.ModelAdmin):
    inlines=[SousCategorieInline]
admin.site.register(Categorie, CategorieAdmin)
