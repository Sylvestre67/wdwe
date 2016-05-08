from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.models import User,Group
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
        import pdb;pdb.set_trace()

        pusher = Pusher(env.PUSHER_APP_ID, env.PUSHER_APP_KEY, env.PUSHER_APP_SECRET)
        pusher.trigger('a_channel', 'an_event', {'some': "data"})

        return super(TagFeedViewSet,self).list(request,**kwargs)

    def update(self,*args,**kwargs):
        tag_feed = ''
        user = ''

        #UPDATE THE TAG_FEED BY MAKING INSTAGRAM API CALL

        #TRIGGER A PUSHER EVENT TO NOTIFY THE FEED OF THIS TAG HAS BEEN UPDATED

        pass