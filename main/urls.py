from django.conf.urls import patterns, url, include

from rest_framework import routers

from views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tag_feed', TagFeedViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),

     url(r'^api/insta_feed_update/$',
        InstaFeedUpdate.as_view(),
        name='insta_feed_update'),

    url(r'^api/insta_post_information/(?P<post_id>\w+)/$',
        InstaPostInfo.as_view(),
        name='insta_post_information'),

    url(r'^$',
        IndexView.as_view(),
        name='home')

]