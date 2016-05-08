from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
import requests
import json

class TagFeed(models.Model):
    name = models.CharField(max_length=256)
    data = JSONField(blank=True, null=True)

    def update_tag_data(self,tag_endpoint_param):
        tag_endpoint_param['COUNT'] = 20
        url = "https://api.instagram.com/v1/tags/%s/media/recent" % self.name
        tag_req = requests.get(url, params=tag_endpoint_param)
        self.data = json.loads(tag_req.content)
        self.save()

        return self