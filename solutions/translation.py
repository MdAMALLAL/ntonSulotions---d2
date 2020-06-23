from modeltranslation.translator import translator, TranslationOptions, register
from .models import Categorie, SousCategorie

@register(Categorie)
class CategorieTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'fr')



@register(SousCategorie)
class SousCategorieTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'fr')
