from django.shortcuts import render
from .models import WordLists
from . import forms
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


# appフォルダ/templats/english_listにしたので、パスの指定は'english_list/〇●.html'

class IndexView(View):
    def get(self, request, *args, **kwargs):
        data = WordLists.objects.all()
        return render(request, 'english_list/index.html', context={'wordlists': data})


class FormView(View):
    def get(self, request, *args, **kwargs):
        form = forms.UserForm()
        return render(request, 'english_list/form_create_view.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = forms.UserForm()
        return render(request, 'english_list/form_create_view.html', {'form': form})


class WordDetailView(DetailView):
    model = WordLists
    template_name = 'english_list/word.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    #   objectは<WordLists:
    #   {'object': <WordLists: <WordLists ☆ id=9,例外　除外,exception,名詞>>, 'wordlists': <WordLists: <WordLists ☆ id=9,例外　除外,exception,名詞>>, 'view': <english_list.views.WordDetailView object at 0x00000217F48AD840>}

class WordUpdateView(UpdateView):
    model = WordLists
    template_name = 'english_list/update_word.html'
    form_class = forms.WordUpdateForm

    def save(self, *args, **kwargs):
        obj = super().save()
        obj.save()
        return obj

    def get_success_url(self):
        print(self.object)
        # return reverse_lazy('english_list:edit_word',kwargs={'pk':self.object.id})
        return reverse_lazy('english_list:index')

class WordDeleteView(DeleteView):
    model = WordLists
    template_name = 'english_list/delete_word.html'
    success_url = reverse_lazy('english_list:index')

