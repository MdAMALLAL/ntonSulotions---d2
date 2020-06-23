from modeltranslation.translator import TranslationOptions, register
from .models import Notification

@register(Notification)
class CategorieTranslationOptions(TranslationOptions):
    fields = ('description',)
    required_languages = ('en', 'fr')
