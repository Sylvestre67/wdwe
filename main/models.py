from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField

class TagFeed(models.Model):
    name = models.CharField(max_length=256)
    data = JSONField(blank=True, null=True)