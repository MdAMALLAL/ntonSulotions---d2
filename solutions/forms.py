from django import forms
from django.utils.translation import gettext_lazy as _


from .models import Reponce, Question, Categorie, SousCategorie


class ReponceForm(forms.ModelForm):

    class Meta:
        model = Reponce
        fields = ( 'description',)

        # widgets = {
        #     'description': forms.Textarea(attrs={'class': 'wmd-input','id':'ask_question_body'}),
        # }
class QuestionForm(forms.ModelForm):

    class Meta:
        fields = ("categorie","souscategorie","titre","priorite","image", "description")
        model = Question

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['souscategorie'].queryset = SousCategorie.objects.none()
            if 'categorie' in self.data:
                try:
                    categorie = int(self.data.get('categorie'))
                    self.fields['souscategorie'].queryset = SousCategorie.objects.filter(categorie=categorie).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                pass #self.fields['categorie'].queryset = self.instance.country.city_set.order_by('name')

    def form_valid(self, form):
        try:

            self.object = form.save(commit=False)
            self.object.user = self.request.user
            #self.object.image = form.cleaned_data['image']
            if self.request.FILES:
                self.object.image = self.request.FILES['image']
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Question has been saved."))
            return redirect('solutions:questiondetail', pk=self.object.pk)

        return super().form_valid(form)
