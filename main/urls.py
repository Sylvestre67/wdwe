from django.conf.urls import patterns, url
from views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home')
]