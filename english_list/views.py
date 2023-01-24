from django.shortcuts import render
from .models import WordLists
from . import forms
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.db.models import Q
from django.shortcuts import resolve_url

# appフォルダ/templats/english_listにしたので、パスの指定は'english_list/〇〇.html'

class WordListView(ListView):
    model = WordLists
    template_name = 'english_list/list_word.html'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET
        print(type(queryset))
        # print(queryset,";",sep="◎")
        # :=は代入式
        if keyword := query.get('keyword'):
            queryset = queryset.filter(
                Q(ja_word__icontains=keyword)|Q(en_word__icontains=keyword)|Q(memo__icontains=keyword)
            )
        return queryset.order_by('id')

"""WordListViewクラスに変更"""
class IndexView(View):
    def get(self, request, *args, **kwargs):
        data = WordLists.objects.all()
        # データベースに保存した全てのデータを取得する　QuerySetオブジェクト
        # データベース操作に関する機能をもっていることで、取得したデータの絞り込みや並び替え、遅延評価といった高度な機能ももつP85 滝沢さんテキスト
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class WordUpdateView(UpdateView):
    model = WordLists
    template_name = 'english_list/update_word.html'
    form_class = forms.WordUpdateForm

    def get_success_url(self):
        print(self.object)
        # return resolve_url('english_list:index')
        # return reverse_lazy('english_list:edit_word',kwargs={'pk':self.object.id})
        return reverse_lazy('english_list:list_word')

class WordDeleteView(DeleteView):
    model = WordLists
    template_name = 'english_list/delete_word.html'
    success_url = reverse_lazy('english_list:list_word')

