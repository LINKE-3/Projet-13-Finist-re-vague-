from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=100,
    	                   widget=forms.TextInput(attrs={'placeholder': 'Chercher'}))