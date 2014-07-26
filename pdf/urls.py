from django.conf.urls import patterns, url, include
from pdf import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^test$', views.generate, name='view'),
   url(r'^export/(?P<rhyme_id>\d+)$', views.ExporterPDFView.as_view(), name='index'),
   url(r'^export/(?P<context>all)$', views.ExporterPDFView.as_view(), name='all'),
   url(r'^export/(?P<context>favorite)$', views.ExporterPDFView.as_view(), name='favorite'),
)
