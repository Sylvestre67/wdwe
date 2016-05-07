from django.contrib.auth.signals import user_logged_in
import requests

def updateUserInstagramFeed(sender, user, request, **kwargs):

    print('########################')
    pass

user_logged_in.connect(updateUserInstagramFeed)
