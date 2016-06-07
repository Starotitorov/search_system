from django import forms

class NewUrlForm(forms.Form):
	url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
