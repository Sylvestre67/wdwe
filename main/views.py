from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.models import User,Group

from social.apps.django_app.default.models import UserSocialAuth

from django.http import JsonResponse

from rest_framework import generics

import requests
import json

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

        tags = self.get_queryset()
        images_data = []

        for tag in tags:
            for media in tag.data['data']:
                if not any(img['id'] == media['id'] for img in images_data):
                    new_media = {'id':media['id'],'href':media['images']['thumbnail']['url'],'tags':media['tags']}
                    images_data.append(new_media)

        request.session['images_data'] = images_data

        return JsonResponse(images_data,safe=False)

class InstaFeedUpdate(generics.ListCreateAPIView):
    queryset = TagFeed.objects.all()
    serializer_class = TagFeed

    def list(self,request,**kwargs):

        insta_user = UserSocialAuth.objects.get(user = request.user)

        tag_endpoint_param = {}
        tag_endpoint_param['access_token'] = insta_user.extra_data['access_token']

        tags = self.get_queryset()

        for tag in tags:
            #THIS IS A LOT OF INSTAGRAM API CALL -> TODO: IMPROVE!
            print('Instagram_API_Call')
            updated_tag = tag.update_tag_data(tag_endpoint_param)

            for media in updated_tag.data['data']:
                if not any(img['id'] == media['id'] for img in request.session['images_data']):
                    new_media = {'id':media['id'],'href':media['images']['thumbnail']['url'],'tags':media['tags']}
                    request.session['images_data'].append(new_media)
                    request.session.save()
            
                    pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
                    pusher.trigger('tag_feed', 'feed_update', new_media)

        return JsonResponse({'success':'Check out your new view feed.'})
