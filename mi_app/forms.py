from django import forms
from .models import Player, TierEntry


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nombre', 'apodo', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre real'}),
            'apodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apodo'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
        }


class TierEntryForm(forms.ModelForm):
    class Meta:
        model = TierEntry
        fields = ['category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
