from django.contrib import admin
from .models import Question, Reponce, SousCategorie, Categorie
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from import_export import resources
from import_export.admin import  ImportExportMixin, ImportExportModelAdmin


# Register your models here.
class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
class SousCategorieResource(resources.ModelResource):
    class Meta:
        model = SousCategorie

class QuestionAdmin(ImportExportModelAdmin):
    #fields=['titre', 'created_at','user','priorite','status']
    list_display=['titre', 'created_at','user','priorite','status']
    list_editable=['priorite','status']
    search_fields = ['titre','description']
    list_filter = ['created_at','user','priorite','status']
    resource_class = QuestionResource

class CategorieResource(resources.ModelResource):
    class Meta:
        model = Categorie
        fields = ('id', 'name', 'name_en', 'name_fr',)
class SousCategorieInline(ImportExportMixin, TranslationTabularInline):
    model=SousCategorie
    resource_class = SousCategorieResource
    extra=3

class CategorieAdmin(ImportExportMixin, admin.ModelAdmin):
    model = Categorie
    resource_class = CategorieResource
    list_display=['name_en','name_fr']

    inlines=[SousCategorieInline]

class CategorieTranslatedAdmin(CategorieAdmin, TranslationAdmin):
    model = Categorie




admin.site.register(Question, QuestionAdmin)
admin.site.register(Reponce)
admin.site.register(SousCategorie)
admin.site.register(Categorie, CategorieAdmin)
