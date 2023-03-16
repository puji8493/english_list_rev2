from django.shortcuts import render
from .models import WordLists
from . import forms
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator


class MyDispatchMixin:

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != self.request.user:
            messages.error(request, '他のユーザーの投稿は編集できません')
            return HttpResponseRedirect(reverse_lazy('english_list:login'))
        return super().dispatch(request, *args, **kwargs)


class CheckMyPostMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        post = WordLists.objects.get(id=self.kwargs["pk"])
        return post.user == self.request.user


class WordListView(ListView):
    """一覧表示"""
    model = WordLists
    template_name = 'english_list/list_word.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        query = self.request.GET
        category = query.get('category')
        keyword = query.get('keyword')

        if category or keyword:
            filters = Q()
            if category:
                filters &= Q(category=category)
            if keyword:
                filters &= Q(ja_word__icontains=keyword) | Q(en_word__icontains=keyword) | Q(memo__icontains=keyword)
            queryset = queryset.filter(filters)

        return queryset.order_by('id')

    """
    しかし、ここでの&=は、DjangoのQオブジェクトを使ったクエリビルダーで、ビット演算子の代わりに論理演算子（AND）を表します。
    &=を使うことで、複数の検索条件を持つフィルターを作成できます。左辺のfiltersオブジェクトに、右辺の検索条件が追加され、その結果がfiltersに代入されます。&=を使わない場合、別々のQオブジェクトを作成して、|演算子で結合する必要があります。
    上記のコードでは、categoryの値が存在する場合、categoryでフィルタリングされたクエリセットを返します。keywordの値が存在する場合は、ja_word、en_word、memoのいずれかがkeywordを含むものでフィルタリングされたクエリセット
    """

    def get_context_data(self, **kwargs):
        """テンプレートに渡すコンテキストデータを返すメソッド
           context['category'] , context['keyword']でテキスボックスの値を表示できる"""

        context = super().get_context_data(**kwargs)
        query = self.request.GET
        context['category'] = query.get('category', '')
        context['keyword'] = query.get('keyword', '')
        return context


class CreateWordView(LoginRequiredMixin, CreateView):
    """新規登録"""

    model = WordLists
    template_name = 'english_list/form_create_view.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('english_list:form_create_view')

    def form_valid(self, form):
        """
        フォームのバリデーション
        ファイル名はフォームにいれた文字をfile_name 属性に格納する
        :param form:　upload.htmlのテンプレートフォーム
            　　 instance:データベースへ保存する前のモデルインスタンス
        :return:指定されたURLにリダイレクト
        """
        form.instance.user_id = self.request.user.id
        messages.success(self.request, "新規登録しました")
        return super().form_valid(form)


class WordDetailView(DetailView):
    """詳細表示"""

    model = WordLists
    template_name = 'english_list/word.html'

    def get_queryset(self):
        return WordLists.objects.select_related('user')

class WordUpdateView(MyDispatchMixin, UpdateView):
    """編集のビュー"""

    model = WordLists
    template_name = 'english_list/update_word.html'
    form_class = forms.WordUpdateForm

    def get_queryset(self):
        return WordLists.objects.select_related('user')

    def get_success_url(self):
        print(self.object)
        return reverse_lazy('english_list:list_word')

    def form_valid(self, form):
        """フォームのバリデーションが成功したときに呼ばれるメソッド
           このメソッドをいれないと画像が保存されなかった"""

        form.save()
        return super().form_valid(form)


class WordDeleteView(MyDispatchMixin, DeleteView):
    """削除するためのView"""

    model = WordLists
    template_name = 'english_list/delete_word.html'
    success_url = reverse_lazy('english_list:list_word')

    def get_queryset(self):
        return WordLists.objects.select_related('user')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        data = WordLists.objects.all()
        # データベースに保存した全てのデータを取得する　QuerySetオブジェクト
        # データベース操作に関する機能をもっていることで、取得したデータの絞り込みや並び替え、遅延評価といった高度な機能も持つ P85 滝沢さんテキスト
        return render(request, 'english_list/index.html', context={'wordlists': data})


class FormView(LoginRequiredMixin, View):
    """新規登録"""

    def get(self, request, *args, **kwargs):
        form = forms.UserForm()
        return render(request, 'english_list/form_create_view.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = self.request.user.id
            form.save()
            form = forms.UserForm()

        return render(request, 'english_list/form_create_view.html', {'form': form})


class Login(LoginView):
    form_class = forms.LoginForm
    template_name = 'english_list/login.html'


class Logout(LogoutView):
    template_name = 'english_list/logout.html'


class SignUpView(CreateView):
    form_class = forms.SignUpForm
    template_name = 'english_list/signup.html'
    success_url = reverse_lazy('english_list:signup')

    def form_valid(self, form):
        """ユーザー登録"""
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.success(self.request, 'ユーザー登録が完了しました。')
        return HttpResponseRedirect(self.get_success_url())
