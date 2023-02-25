from django.shortcuts import render
from .models import WordLists
from . import forms
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.db.models import Q

# appフォルダ/templats/english_listにしたので、パスの指定は'english_list/〇〇.html'

class WordListView(ListView):
    """一覧表示"""

    model = WordLists
    template_name = 'english_list/list_word.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET
        print(type(queryset))
        # :=は代入式
        if keyword := query.get('keyword'):
            queryset = queryset.filter(
                Q(ja_word__icontains=keyword) | Q(en_word__icontains=keyword) | Q(memo__icontains=keyword)
            )
        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword', '')
        return context


class CreateWordView(CreateView):
    """新規登録"""

    model = WordLists
    template_name = 'english_list/form_create_view.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('english_list:list_word')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WordDetailView(DetailView):
    """詳細表示"""

    model = WordLists
    template_name = 'english_list/word.html'


class WordUpdateView(UpdateView):
    """編集のビュー"""

    model = WordLists
    template_name = 'english_list/update_word.html'
    form_class = forms.WordUpdateForm

    def get_success_url(self):
        print(self.object)
        return reverse_lazy('english_list:list_word')

    def form_valid(self, form):
        """フォームのバリデーションが成功したときに呼ばれるメソッド
           このメソッドをいれないと画像が保存されなかった"""

        form.save()
        return super().form_valid(form)


class WordDeleteView(DeleteView):
    """削除するためのView"""

    model = WordLists
    template_name = 'english_list/delete_word.html'
    success_url = reverse_lazy('english_list:list_word')


"""WordListViewクラスに変更"""
class IndexView(View):
    def get(self, request, *args, **kwargs):
        data = WordLists.objects.all()
        # データベースに保存した全てのデータを取得する　QuerySetオブジェクト
        # データベース操作に関する機能をもっていることで、取得したデータの絞り込みや並び替え、遅延評価といった高度な機能も持つ P85 滝沢さんテキスト
        return render(request, 'english_list/index.html', context={'wordlists': data})


class FormView(View):
    """新規登録"""

    def get(self, request, *args, **kwargs):
        form = forms.UserForm()
        return render(request, 'english_list/form_create_view.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = forms.UserForm()
        return render(request, 'english_list/form_create_view.html', {'form': form})
