from django import forms

class NewUrlForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


class LoadUrlsFromFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}),
                           label="File to load urls from")


class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search'}),
                          label='')


class RecursiveTraversalForm(forms.Form):
    start_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
                                label="Url to start from")
