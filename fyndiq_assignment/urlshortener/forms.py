from django import forms

class URLInputForm(forms.Form):
    url_input = forms.URLField(required=True,label='URL Here:')