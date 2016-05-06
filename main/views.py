from django.shortcuts import render
from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context(self,*args,**kwargs):
        context            = super(IndexView, self).get_context(*args,**kwargs)
        context['request'] = self.request
        context['user']    = self.request.user

        return context

