from django.shortcuts import render, HttpResponse, redirect
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
from urllib.parse import urlencode
import csv


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
        """
        WordListsモデルに対応するクエリセットを取得
        リクエストセッションを使用してチェックボックスの状態を取得
        フィルタリングには、&=演算子を使って複数のフィルターを結合
        :return:フィルタリング、検索、ソートしたクエリセット
        """

        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        query = self.request.GET
        category = query.get('category')
        keyword = query.get('keyword')
        my_list = self.request.session.get('my_list') == 'on'

        if my_list and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        if category or keyword:
            filters = Q()
            if category:
                filters &= Q(category=category)
            if keyword:
                filters &= Q(ja_word__icontains=keyword) | Q(en_word__icontains=keyword) | Q(memo__icontains=keyword)
            queryset = queryset.filter(filters)

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストを返す
        :param カテゴリ、検索フォーム、チェックボックスの値を含める
        :return:コンテキスト
        """

        context = super().get_context_data(**kwargs)
        query = self.request.GET
        context['category'] = query.get('category', '')
        context['keyword'] = query.get('keyword', '')
        context['my_list'] = self.request.session.get('my_list') == 'on'

        return context

    def post(self, request, *args, **kwargs):
        """チェックボックスの状態をsession属性に保存"""

        my_list = request.POST.get('my_list')
        if my_list:
            request.session['my_list'] = my_list
        else:
            request.session.pop('my_list', None)

        return super().get(request, *args, **kwargs)


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


class CheckUserListView(ListView):
    model = WordLists
    template_name = 'english_list/list_users.html'
    context_object_name = 'wordlists'
    form_class = forms.WordListForm
    paginate_by = 3

    def get_queryset(self):
        """
        ListViewで表示するオブジェクトのクエリセットを取得する
         user_ids:リクエストのクエリパラメータからusersという名前のリストを取得
        :return: user_idsでクエリをフィルタリングしてqueryset変数に代入。
        """

        queryset = super().get_queryset().select_related('user')
        user_ids = self.request.GET.getlist('user_id')
        print('■user_id■',user_ids,sep=":")
        if user_ids:
            queryset = queryset.filter(user__in=user_ids).select_related('user')
            print('■queryset■',queryset,sep=":")
        return queryset

    def get_context_data(self, **kwargs):
        """
        ページネーションされたWordListsオブジェクトのリストやページネーション関連のオブジェクトをコンテキスト変数に追加

        :form: リクエストのGETパラメーターを含むself.form_classのインスタンスをコンテキスト変数として追加
        :page_obj: ページネーションされたオブジェクトのリスト　 <Page 1 of 1>など
        :paginator: Paginatorオブジェクト
        :is_paginated: ページネーションが有効かどうか
        :object_list: ページネーションされたオブジェクトのリスト（QuerySet）
        :return:form、page_obj、paginator、is_paginated、object_listというキーを持つディクショナリー
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)

        context['page_obj'] = context['page_obj']
        print("■page_obj■",context['page_obj'],sep="")
        context['paginator'] = context['paginator']
        print("■pagenator■",context['paginator'],sep="")
        context['is_paginated'] = context['is_paginated']
        print("■is_paginated■",context['is_paginated'],sep="")
        context['object_list'] = context['wordlists']
        print("■object_list■",context['wordlists'],sep="")

        # print('■context■',context,sep="")
        return context


class GenerateCsvView(LoginRequiredMixin, WordListView):
    """リストをCSVファイルにダウンロードする
        チェックボックスONの場合はログインユーザーの単語リストをダウンロードする
        チェックボックスOFFの場合はログインユーザーの単語リストをダウンロードする
        ユーザーログインしていない場合は、ログイン画面へ遷移する
    """

    def get_queryset(self):

        queryset = super().get_queryset()
        my_list = self.request.session.get('my_list') == 'on'

        if my_list and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def post(self, request):

        response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="wordlist.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'カテゴリ', '英単語', '日本語訳', 'メモ', 'ユーザー名'])

        queryset = self.get_queryset()
        for obj in queryset:
            writer.writerow([obj.id, obj.category, obj.en_word, obj.ja_word, obj.memo, obj.user.username])

        return response


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

