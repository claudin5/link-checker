from django import forms

class Url(forms.Form):
    url = forms.URLField(label='Please Enter URL', widget=forms.TextInput(attrs={'class':'form-control'}))
    