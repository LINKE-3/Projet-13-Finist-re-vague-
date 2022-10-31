from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class PhotoForm(forms.ModelForm):
  
    class Meta:
        model = Spot
        fields = ['name', 'photo'] #['name', 'photo']



class ContactUsForm(forms.Form):
    #name = forms.CharField(required=True)
    photo = forms.ImageField(required=True)
"""
    def save2(self, commit=True):
        photo = super(PhotoForm, self).save(commit=False)
        if commit:
            photo.save()
        return photo
"""
