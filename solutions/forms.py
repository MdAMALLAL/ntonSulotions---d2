from django import forms
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from .models import Reponce, Question, Categorie, SousCategorie

class ReponceForm(forms.ModelForm):

    class Meta:
        model = Reponce
        fields = ( 'description','status','send_mail')

class QuestionForm(forms.ModelForm):

    class Meta:
        fields = ("categorie","souscategorie","objet","priorite","image", "description",'priorite_intern')
        model = Question

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # print('in form')
            self.fields['souscategorie'].queryset = SousCategorie.objects.none()
            if 'categorie' in self.data:
                try:
                    categorie = int(self.data.get('categorie'))
                    self.fields['souscategorie'].queryset = SousCategorie.objects.filter(categorie=categorie).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                categorie = int(self.data.get('categorie'))
                self.fields['souscategorie'].queryset = SousCategorie.objects.filter(categorie=categorie).order_by('name')
    def clean(self):
            self.image = self.cleaned_data['image']
            return
