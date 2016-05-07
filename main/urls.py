from django.conf.urls import patterns, url, include

from rest_framework import routers

from views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tag_feed', TagFeedViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),

    url(r'^$',
        IndexView.as_view(),
        name='home')
]