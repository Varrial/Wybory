from django import forms

from .models import Wybory


class newWybory(forms.ModelForm):
    class Meta:
        model = Wybory
        fields = ['nazwa', 'typ', 'data_rozpoczecia', 'data_zakonczenia']