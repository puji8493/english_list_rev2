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
    paginate_by = 10

    def get_queryset(self):
        """
        ListViewで表示するオブジェクトのクエリセットを取得する
        user_ids:リクエストのクエリパラメータからusersという名前のリストを取得
        :return: user_idsでクエリをフィルタリングしてqueryset変数に代入。
        """

        queryset = super().get_queryset().select_related('user')
        user_ids = self.request.GET.getlist('users')
        if user_ids:
            queryset = queryset.filter(user__in=user_ids).select_related('users')
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
        context['paginator'] = context['paginator']
        context['is_paginated'] = context['is_paginated']
        context['object_list'] = context['wordlists']
        print(context, '〇context〇')
        return context

    def post(self, request, *args, **kwargs):
        """
        ユーザーがフォームで選択したユーザーIDを使用してWordListsオブジェクトをフィルタリング
        ページネーションされたリストを作成しコンテキスト変数に追加
        renderを使用して、HTMLテンプレートにコンテキスト変数を渡してレスポンスを返す。

        queryset:user__in=user_idsでフィルタリングされたオブジェクトのクエリセット
        paginator:ページネーションするために、querysetをpaginate_byの数でページに分割
        page_number:現在のページ番号を取得
        page_obj:現在のページのオブジェクト

        ページネーションされたオブジェクトのページ番号をURLのクエリパラメータに追加する
        query_params:現在のGETパラメーターをコピー
                    　元のQueryDictオブジェクトのコピーを作成し、変更を加えることができる
        query_params['page']:現在のページ番号を設定
                    ページ番号をクエリパラメータに追加するために、query_paramsオブジェクトの'page'キーにpage_obj.numberを代入
        query_string: query_paramsをURLエンコード
                    　オブジェクトをエンコードされた文字列に変換。クエリパラメータがURLに追加。
                    　この文字列は、テンプレートのページネーションリンクなどに使用される

        context: ページネーションされたオブジェクトと関連する情報を含むコンテキスト辞書を作成します。
        :return:contextを使って、list_users.htmlテンプレートを描画
                usersの値が存在しない場合は、getメソッドを呼び出して通常の処理を実行
        """

        user_ids = self.request.POST.getlist('users')
        if user_ids:
            queryset = WordLists.objects.filter(user__in=user_ids).select_related('user')
            paginator = Paginator(queryset, self.paginate_by)
            page_number = self.request.GET.get('page') or 1
            page_obj = paginator.get_page(page_number)

            # ページネーションされたオブジェクトのページ番号をURLのクエリパラメータに追加する
            query_params = self.request.GET.copy()
            query_params['page'] = page_obj.number
            query_string = urlencode(query_params)

            context = {
                'wordlists_list': page_obj,
                'query_string': query_string,
                'form': self.form_class(self.request.GET),
                'is_paginated': True,
                'paginator': paginator,
                'page_obj': page_obj,
                'object_list': page_obj.object_list,
            }
            print(context, '■context■')
            return render(request, 'english_list/list_users.html', context)
        else:
            return self.get(request, *args, **kwargs)


    # def paginate_queryset(self, queryset, page_size):
    #     paginator = Paginator(queryset, page_size)
    #     page_number = self.request.GET.get('page')
    #     return paginator.get_page(page_number)

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


# class CheckUserListView(ListView):
#
#     model = WordLists
#     template_name = 'english_list/list_users.html'
#     context_object_name = 'wordlists'
#     form_class = forms.WordListForm
#     paginate_by = 10
#
#     def get_queryset(self):
#         user_ids = self.request.GET.getlist('users')
#         queryset = WordLists.objects.filter(user__in=user_ids) #if user_ids else WordLists.objects.none()
#         return queryset
#
#     def get_context_data(self, **kwargs):
#
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.form_class()
#
#         # Add pagination parameters to URL
#         query_params = self.request.GET.copy()
#         print(query_params,'☆get_context_query_params☆')
#         context['query_string'] = urlencode(query_params)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         user_ids = self.request.POST.getlist('users')
#
#         if user_ids:
#             queryset = WordLists.objects.filter(user__in=user_ids).select_related('user')
#             paginator = Paginator(queryset, self.paginate_by)
#             page_number = self.request.GET.get('page') or 1  #None
#             print(page_number,"☆")
#             page_obj = paginator.get_page(page_number)#1of4
#
#             # Add pagination parameters to URL
#             query_params = self.request.GET.copy()
#             query_params['page'] = page_obj.number
#             query_string = urlencode(query_params)
#
#             context = {
#                 'wordlists_list': page_obj,
#                 'query_string': query_string,
#             }
#             print(context,"〇〇")
#             return render(request, 'english_list/list_users.html', context)
#             # return render(request, 'english_list/list_word.html', context)
#             # return redirect('english_list:list_word')
#             # return redirect('english_list:list_word', user_ids=user_ids)
#
#         else:
#             return self.get(request, *args, **kwargs)
