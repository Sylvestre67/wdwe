from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

from social.apps.django_app.default.models import UserSocialAuth

import requests
import json

class TagFeed(models.Model):
    name = models.CharField(max_length=256)
    data = JSONField(blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def update_tag_data(self,request):

        insta_user = UserSocialAuth.objects.get(user = request.user)

        tag_endpoint_param = {}
        tag_endpoint_param['access_token'] = insta_user.extra_data['access_token']

        tag_endpoint_param['COUNT'] = 20
        url = "https://api.instagram.com/v1/tags/%s/media/recent" % self.name
        tag_req = requests.get(url, params=tag_endpoint_param)

        self.data = json.loads(tag_req.content)
        self.save()

        return self


class Location(models.Model):
    insta_id = models.CharField(max_length=256,null=True,blank=True)
    insta_name = models.CharField(max_length=256,null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    yelp_data = JSONField(null=True,blank=True)
    opentable_data = JSONField(null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.insta_name
