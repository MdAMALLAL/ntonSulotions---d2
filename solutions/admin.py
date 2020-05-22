from django.contrib import admin
from .models import Question, Reponce, SousCategorie, Categorie
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    #fields=['titre', 'created_at','user','priorite','status']
    list_display=['titre', 'created_at','user','priorite','status']
    list_editable=['priorite','status']
    search_fields = ['titre','description']
    list_filter = ['created_at','user','priorite','status']

class SousCategorieInline(TranslationTabularInline):
    model=SousCategorie
    extra=3

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines=[SousCategorieInline]

class CategorieTranslatedAdmin(CategorieAdmin, TranslationAdmin):
    model = Categorie

admin.site.register(Question, QuestionAdmin)
admin.site.register(Reponce)
admin.site.register(SousCategorie)
admin.site.register(Categorie, CategorieAdmin)
