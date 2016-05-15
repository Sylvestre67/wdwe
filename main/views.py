from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.models import User,Group
from django.forms.models import model_to_dict

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
        images_data = []

        #TODO: Need to set_up the initial API call to retrieve the post from tag at first load.

        for tag in tags:
            for media in tag.data['data']:
                if not any(img['id'] == media['id'] for img in images_data):
                    new_media = {'id':media['id'],'href':media['images']['thumbnail']['url'],'tags':media['tags']}
                    images_data.append(new_media)

        request.session['images_data'] = images_data

        return JsonResponse(images_data,safe=False)

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
            updated_tag = tag.update_tag_data(tag_endpoint_param)

            for media in updated_tag.data['data']:
                if not any(img['id'] == media['id'] for img in request.session['images_data']):
                    new_media = {'id':media['id'],'href':media['images']['thumbnail']['url'],'tags':media['tags']}
                    request.session['images_data'].append(new_media)
                    request.session.save()

                    pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
                    pusher.trigger('tag_feed', 'feed_update', new_media)

        return JsonResponse({'success':'Check out your new view feed.'})

class InstaPostInfo(View):

    def get(self,*args,**kwargs):
        """
        Makes an API call to instagram API and return the information about the media and the location, if media has one.
        """
        insta_user = UserSocialAuth.objects.get(user = self.request.user)
        tag_endpoint_param = {}
        tag_endpoint_param['access_token'] = insta_user.extra_data['access_token']

        #Do we need to update the image information ?
        for index,image in enumerate(self.request.session['images_data']):
            #Image is here and does not have extra_data -> Let's Update
            if image['id'] == self.kwargs['post_id'] and not 'extra_data' in image.keys():
                #Get media information
                url = "https://api.instagram.com/v1/media/%s" % self.kwargs['post_id']
                media_req = requests.get(url, params=tag_endpoint_param)
                media_data = json.loads(media_req.content)

                if media_data['data']['location']:
                    #make API call to retrieve Location Information
                    url = "https://api.instagram.com/v1/locations/%s/media/recent" % media_data['data']['location']['id']
                    location_req = requests.get(url, params=tag_endpoint_param)
                    location_data = json.loads(location_req.content)

                    #add location_data to media_data
                    media_data['location_info'] = location_data

                    try:
                        #Get Yelp information - from https://github.com/Yelp/yelp-python
                        from yelp.client import Client
                        from yelp.oauth1_authenticator import Oauth1Authenticator

                        auth = Oauth1Authenticator(
                            consumer_key    = env.YELP_CONSUMER_KEY,
                            consumer_secret = env.YELP_CONSUMER_SECRET,
                            token           = env.YELP_TOKEN,
                            token_secret    = env.YELP_TOKEN_SECRET
                        )

                        client = Client(auth)

                        params = {
                            'term': media_data['data']['location']['name'],
                            'radius_filter' : 300
                        }

                        location_longitude = media_data['data']['location']['longitude']
                        location_latitude = media_data['data']['location']['latitude']

                        yelp_response = client.search_by_coordinates(location_latitude,location_longitude,**params)

                        place_name = yelp_response.businesses[0].name

                        place = yelp_response.businesses[0].__dict__

                        place_location = place.pop('location')
                        place_location_dict = place_location.__dict__

                        place_location_coordinate = place_location_dict.pop('coordinate')
                        place_location_coordinate_dict = place_location_coordinate.__dict__

                        media_data['yelp_info'] = { 'places_info' : place,
                                                    'places_location' : place_location_dict,
                                                    'places_coordinate' : place_location_coordinate_dict}

                        #Get openTable information
                        opentable_param = {}
                        opentable_param['name'] = place_name
                        opentable_param['address'] = place_location_dict['address']
                        opentable_param['zip'] = place_location_dict['postal_code']

                        url = "http://opentable.herokuapp.com/api/restaurants"

                        opentable_req = requests.get(url, params=opentable_param)

                        media_data['opentable_info'] = json.loads(opentable_req.content)

                    except:
                        media_data = {}

                    self.request.session['images_data'][index]['extra_data'] = media_data
                    self.request.session.save()

            #Already have the extra_data ->  No Need for update
            elif image['id'] == self.kwargs['post_id'] and 'extra_data' in image.keys():
                media_data = image['extra_data']

        return JsonResponse({'data': media_data})

