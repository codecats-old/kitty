from django.conf.urls import patterns, url, include
from pdf import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^test$', views.generate, name='view'),
   url(r'^(?P<rhyme_id>\d+)$', views.ExporterPDFView.as_view(), name='index'),
   url(r'^$', views.ExporterPDFView.as_view(), name='all'),
)
