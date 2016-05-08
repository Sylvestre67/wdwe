from rest_framework import serializers
from django.contrib.auth.models import User,Group
from models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class TagFeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagFeed
        fields = ('name', 'data')