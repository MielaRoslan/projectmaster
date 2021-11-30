from django import forms
from .models import SearchLog, APIKeys


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchLog
        fields = ['term']

class APIKeysForm(forms.ModelForm):
    class Meta:
        model = APIKeys
        fields = ['api_key', 'api_secret_key', 'access_token', 'access_token_secret']
