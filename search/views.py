from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from search_engine.search_engine import SearchEngine
from search.models import Word, Page, Match
from forms import NewUrlForm, LoadUrlsFromFileForm, SearchForm, RecursiveTraversalForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from web_crawler.crawler import WebCrawler

def index(request):
    form = SearchForm()
    return render(request, 'search/index.html', {'form': form})


def urlsControl(request):
    pages = Page.objects.all()
    form = NewUrlForm()
    file_form = LoadUrlsFromFileForm()
    traversal_form = RecursiveTraversalForm()
    return render(request, 'search/urlsControl.html', { 'form': form,
                                                        'file_form': file_form,
                                                        'traversal_form': traversal_form,
                                                        'pages': pages })
def add_url(request):
    if request.method == 'POST':
        form = NewUrlForm(request.POST)
        if form.is_valid():
            s = SearchEngine()
            s.create_index(form.cleaned_data['url'])
    return HttpResponseRedirect(reverse('urls_control'))
 

def load_urls_from_file(request):
    if request.method == 'POST':
        form = LoadUrlsFromFileForm(request.POST, request.FILES)
        if form.is_valid():
            urls = request.FILES['file'].readlines()
            s = SearchEngine()
            for url in urls:
                s.create_index(url)
    return HttpResponseRedirect(reverse('urls_control'))


def delete_url(request, pk):
    try:
        page = Page.objects.get(pk=pk)
        s = SearchEngine()
        s.delete_index(page.url)
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(reverse('urls_control'))


def update_url(request, pk):
    try:
        page = Page.objects.get(pk=pk)
        s = SearchEngine()
        s.create_index(page.url)
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(reverse('urls_control'))

def search_for_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            s = SearchEngine()
            res = s.search_text(form.cleaned_data['text'])
            f = SearchForm()
            return render(request, 'search/show_results.html', { 'urls': res,
                                                                 'form': f })
    return HttpResponseRedirect(reverse('index'))

def traverse_site(request):
    if request.method == 'POST':
        form = RecursiveTraversalForm(request.POST)
        if form.is_valid():
            start_url = form.cleaned_data['start_url']
            crawler = WebCrawler(limit_width=2, limit_depth=3)
            urls = crawler.traverse(start_url)
            s = SearchEngine()
            for url in urls:
                s.create_index(url)
    return HttpResponseRedirect(reverse('urls_control'))
