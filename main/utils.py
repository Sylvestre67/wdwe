import wdwe.settings as env

import requests
import json

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from pusher import Pusher

from models import Location

def update_yp_op_information(location_id):
    """
    Update Location information with Yelp and OpeTable API response.
    """
    try:
        location = Location.objects.get(pk=location_id)
        #Get Yelp information - from https://github.com/Yelp/yelp-python
        auth = Oauth1Authenticator(
            consumer_key    = env.YELP_CONSUMER_KEY,
            consumer_secret = env.YELP_CONSUMER_SECRET,
            token           = env.YELP_TOKEN,
            token_secret    = env.YELP_TOKEN_SECRET
        )

        client = Client(auth)

        params = {
            'term': location.insta_name,
            'radius_filter' : 300
        }

        yelp_response = client.search_by_coordinates(location.latitude,location.longitude,**params)

        place_name = yelp_response.businesses[0].name

        place = yelp_response.businesses[0].__dict__

        place_location = place.pop('location')
        place_location_dict = place_location.__dict__

        place_location_coordinate = place_location_dict.pop('coordinate')
        place_location_coordinate_dict = place_location_coordinate.__dict__

        #Get openTable information
        opentable_param = {}
        opentable_param['name'] = place_name
        opentable_param['address'] = place_location_dict['address']
        opentable_param['zip'] = place_location_dict['postal_code']

        url = "http://opentable.herokuapp.com/api/restaurants"

        opentable_req = requests.get(url, params=opentable_param)

        location.opentable_data = json.loads(opentable_req.content)
        location.yelp_data = { 'places_info' : place,
                  'places_location' : place_location_dict,
                  'places_coordinate' : place_location_coordinate_dict }

        location.save()

    except Exception as e:
        print(e)

    return {'status':'Successfully update media location'}

def send_pusher_event(media):

    pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
    pusher.trigger('tag_feed', 'feed_update', media)

    return media