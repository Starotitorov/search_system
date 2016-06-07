from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from forms import NewUrlForm

def index(request):
	return render(request, 'search/index.html', {})

def urlsControl(request):
	if request.method == 'POST':
		form = NewUrlForm(request.POST)
		if form.is_valid():
			print form.cleaned_data
			# Here you can get data from form and save to DB
			return HttpResponseRedirect('/search')

	else:
		form = NewUrlForm()

		return render(request, 'search/urlsControl.html', {'form': form})
