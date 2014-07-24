from django.conf.urls import patterns, url, include
from pdf import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^$', views.generate, name='view'),
   url(r'^(?P<rhyme_id>\d+)$', views.HelloPDFView.as_view(), name='index'),
)
