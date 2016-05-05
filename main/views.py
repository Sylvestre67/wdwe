from django.shortcuts import render
from django.views.generic import FormView,TemplateView,ListView,DetailView,View,CreateView,UpdateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

