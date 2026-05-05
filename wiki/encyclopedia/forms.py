from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)

class AddForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    content = forms.CharField(required=False)

class EditForm(forms.Form):
    content = forms.CharField(required=False)
