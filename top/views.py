from django.views.generic.base import TemplateView
from datetime import datetime
from english_list.models import WordLists

class TopView(TemplateView):
    template_name = 'english_list/top.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['time'] = datetime.now()
        context['count'] = WordLists.objects.count()
        return context






from django.shortcuts import render

# Create your views here.
