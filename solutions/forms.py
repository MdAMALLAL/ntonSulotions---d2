from django import forms

from .models import Reponce


class ReponceForm(forms.ModelForm):

    class Meta:
        model = Reponce
        fields = ( 'description',)

        # widgets = {
        #     'description': forms.Textarea(attrs={'class': 'wmd-input','id':'ask_question_body'}),
        # }
