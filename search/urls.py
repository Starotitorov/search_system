from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results$', views.search_for_results, name='search_for_results'),
    url(r'^urlsControl$', views.urlsControl, name='urls_control'),
    url(r'^add_url$', views.add_url, name='add_url'),
    url(r'^traverse$', views.traverse_site, name='traverse_site'),
    url(r'^load_urls_from_file$', views.load_urls_from_file, name='load_urls_from_file'),
    url(r'^delete_url/(?P<pk>\d+)/$', views.delete_url, name='delete_url'),
    url(r'^update_url/(?P<pk>\d+)/$', views.update_url, name='update_url')
]
