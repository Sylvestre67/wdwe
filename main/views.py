from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.models import User,Group

from social.apps.django_app.default.models import UserSocialAuth

from django.http import JsonResponse

from rest_framework import generics

from rest_framework.decorators import detail_route, list_route

import wdwe.settings as env

from rest_framework import viewsets

from models import *
from serializers import *
from pusher import Pusher

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context(self,*args,**kwargs):
        context            = super(IndexView, self).get_context(*args,**kwargs)
        context['request'] = self.request
        context['user']    = self.request.user

        return context

######################
#
#    REST API
#
######################
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TagFeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proposal campaign to be viewed or edited.
    """
    queryset = TagFeed.objects.all()
    serializer_class = TagFeedSerializer

    def list(self,request,**kwargs):

        #pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
        #pusher.trigger('tag_feed', 'feed_update', {'some': "data"})

        return super(TagFeedViewSet,self).list(request,**kwargs)

class InstaFeedUpdate(generics.ListCreateAPIView):
    queryset = TagFeed.objects.all()
    serializer_class = TagFeed

    def list(self,request,**kwargs):

        insta_user = UserSocialAuth.objects.get(user = request.user)

        tag_endpoint_param = {}
        tag_endpoint_param['access_token'] = insta_user.extra_data['access_token']

        #update tag infomation
        url = "https://api.instagram.com/v1/tags/%s" % tag
        tag_req = requests.get(url, params=tag_endpoint_param)
        tag_object.tag_data = json.loads(tag_req.content)

        #pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
        #pusher.trigger('tag_feed', 'feed_update', {'some': "data"})

        return JsonResponse({'success':'Check out your new view feed.'})

