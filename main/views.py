from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.models import User,Group
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404

from social.apps.django_app.default.models import UserSocialAuth

from django.http import JsonResponse

from rest_framework import generics
from celery import chain

import requests
import json

from rest_framework.decorators import detail_route, list_route

import wdwe.settings as env

from rest_framework import viewsets

from models import *
from serializers import *
from utils import *

from main.tasks import task_update_yp_op_information,task_send_pusher_event

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
    queryset            = User.objects.all()
    serializer_class    = UserSerializer

class TagFeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the image_feed from a tag to be viewed.
    """
    queryset            = TagFeed.objects.all()
    serializer_class    = TagFeedSerializer

    def list(self,request,**kwargs):

        tags = self.get_queryset()
        images_data = {}
        media_feed = []

        #Initial access -> Update the feed_tag
        for tag in tags:
            tag_data = tag.update_tag_data(self.request)

            for media in tag_data.data['data']:

                #Only append the media with a location tagged.
                if not media['location'] == None:
                    try:
                        media_location = Location.objects.get(insta_id = media['location']['id'])
                    except ObjectDoesNotExist:
                        media_location = Location.objects.create(insta_id = media['location']['id'],
                                                longitude =  media['location']['longitude'],
                                                latitude = media['location']['latitude'],
                                                insta_name = media['location']['name'])
                        media_location.save()

                    #START UPDATE/CREATE TASK TO COLLECT LOCATION INFORMATION
                    task_update_yp_op_information.delay(media_location.pk)

                    #Update the list of images in the session.
                    try:
                        existing_media = images_data[media['id']]
                    except:
                        images_data[media['id']] = media

                    media_feed.append(media)

        #append images_data to user session -> used to deDup the existing loaded images after a pusher event is captured.
        request.session['images_data'] = images_data
        request.session.save()

        return JsonResponse(media_feed,safe=False)

class InstaFeedUpdate(generics.ListCreateAPIView):
    queryset            = TagFeed.objects.all()
    serializer_class    = TagFeed

    def list(self,request,**kwargs):

        insta_user = UserSocialAuth.objects.get(user = request.user)

        tag_endpoint_param = {}
        tag_endpoint_param['access_token'] = insta_user.extra_data['access_token']

        tags = self.get_queryset()

        for tag in tags:
            #THIS IS A LOT OF INSTAGRAM API CALL -> TODO: IMPROVE!
            print('Instagram_API_Call')
            updated_tag = tag.update_tag_data(self.request)

            for media in updated_tag.data['data']:

                #Update the list of images in the session.
                try:
                    existing_media = request.session['images_data'][media['id']]
                except:
                    request.session['images_data'][media['id']] = media

                    #CHECKI IF LOCATION ON THE MEDIA
                    if media['location']:
                        try:
                            media_location = Location.objects.get(insta_id = media['location']['id'])
                        except ObjectDoesNotExist:
                            media_location = Location.objects.create(insta_id = media['location']['id'],
                                                    longitude =  media['location']['longitude'],
                                                    latitude = media['location']['latitude'],
                                                    insta_name = media['location']['name'])
                            media_location.save()

                        #START UPDATE/CREATE TASK TO COLLECT LOCATION INFORMATION and send the pusher event when done.
                        task_update_yp_op_information.apply_async((media_location.pk,),link=task_send_pusher_event.si(media,))

                       #task_update_yp_op_information.apply_async(media_location.pk,link=task_send_pusher_event(media))

                request.session.save()

        return JsonResponse({'success':'Check out your new view feed.'})

class InstaPostInfo(View):

    def get(self,*args,**kwargs):
        """
        Return instaPost complete information
        """
        try:
            media_data = self.request.session['images_data'][self.kwargs['post_id']]
            try:
                media_location = Location.objects.get(insta_id = media_data['location']['id'])

                if media_location.opentable_data:
                    media_data['location']['open_table'] = media_location.opentable_data
                else:
                     media_data['location']['open_table'] = 'None'

                if media_location.yelp_data:
                    media_data['location']['yp_table'] = media_location.yelp_data
                else:
                    media_data['location']['yp_table'] = 'None'
            except:
                media_data['location']['open_table'] = 'None'
                media_data['location']['yp_table'] = 'None'

        except:
            raise Http404("Media does not exist")

        return JsonResponse({'data': media_data})