from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from .models import Filter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class PropertiesForm(forms.ModelForm):
    property = forms.ChoiceField(choices=[(x, x) for x in ['Wiazowna', 'Legionowo']], label=False, required=False)
    #max_price = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'style': 'width: 60px'}))
    min_size = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '950'}))
    #max_size = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'none'}))
    #min_price = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'none'}))
    max_price = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '200 000'}))

    class Meta:
        model = Filter
        fields = ['property', 'min_size', 'max_price']


class PrecisePropertiesForm(forms.ModelForm):
    property = forms.ChoiceField(required=True, widget=forms.TextInput(attrs={'placeholder': '950'}))
    min_size = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '950'}))
    max_price = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '200 000'}))

    class Meta:
        model = Filter
        fields = ['property', 'min_size', 'max_price']
