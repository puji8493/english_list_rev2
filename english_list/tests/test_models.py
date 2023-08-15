from django.test import TestCase
from django.urls import reverse
from english_list.models import WordLists
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

User = get_user_model()


class WordListsModelTest(TestCase):
    """
    WordListsモデルのテスト
    """

    def setUp(self):
        """
        テストメソッド実行前にデータをセットアップする
        User.objects.create_user() で、Userモデルのインスタンスを作成する
        """

        # 作成者用のユーザーを作成
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # 他のユーザーを作成
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )

        # self.userが作成したWordListsモデルを作成
        self.wordlist = WordLists.objects.create(
            user=self.user,
            category='Test Category',
            ja_word='テスト',
            en_word='test',
            memo='This is a test memo'
        )

        # reverse メソッドを使用して、編集用view　'english_list:edit_word' の URL を逆引き（逆解決）
        # このビューには args パラメータとして self.wordlist.pk を渡す。
        # これにより、編集対象の WordLists オブジェクトのプライマリキーが URL に組み込まれる
        self.edit_url = reverse('english_list:edit_word', args=[self.wordlist.pk])
        print(self.edit_url)
        # self.edit_url = resolve_url('english_list:edit_word', args=[self.wordlist.pk])

        # テストユーザーでログイン状態をシミュレート
        self.client.force_login(self.user)

        # ログインしたユーザーのユーザーネームを表示
        print("ログインしたユーザーsetup:", self.client.session['_auth_user_id'])

    def test_edit_word_by_other_user_shows_error_message(self):
        """
        他のユーザーが他のユーザーの投稿を編集しようとした場合に、エラーメッセージが表示されることをテスト
        force_login メソッドを使用して別のユーザーでログインし、self.edit_url に対して GET リクエストを送信し、
        リダイレクトを自動的にたどるオプション follow=True を使用しています。
        通常、ウェブアプリケーションでリダイレクトが発生すると、ブラウザは自動的に新しいURLにアクセスし、
        そのページの内容を表示。follow=True を使用すると、テストクライアントも同様の動作を行い、
        リダイレクト先のページの内容を取得してテストできるようになる
        """

        # ログインしたユーザーのユーザーIDを表示
        print("otheruserを確認するコード　ユーザーbefore:", self.client.session['_auth_user_id'])

        # force_login メソッドは、Djangoのテストクライアントを使用して、指定したユーザーでログイン状態をシミュレート
        self.client.force_login(self.other_user)

        # ログインしたユーザーのユーザーネームを表示
        print("otheruserを確認するコード　ユーザーafter:", self.client.session['_auth_user_id'])

        # テスト対象の投稿を編集しようとするリクエストを送信（follow=True を追加）
        response = self.client.get(self.edit_url, follow=True)

        # エラーメッセージが表示されることを確認
        self.assertContains(response, "他のユーザーの投稿は編集できません")

    def test_edit_word_by_owner_succeeds(self):
        """投稿権限があるユーザのアクセスの確認"""

        # self.client.force_login(self.user)
        # ログインしたユーザーのユーザーネームを表示
        print("ログインしたユーザーtest_edit_word:", self.client.session['_auth_user_id'])

        # テスト対象の投稿を編集するリクエストを送信
        response = self.client.get(self.edit_url)

        # 正常にアクセスできることを確認
        self.assertEqual(response.status_code, 200)

    def test_check_object(self):
        """データベース内にオブジェクトが正しく１つだけ作成されているかを確認する"""
        wordlists = WordLists.objects.all()
        self.assertEqual(len(wordlists),1)

    def test_user_label(self):
        """userフィールドのラベルが'ユーザー'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_category_label(self):
        """categoryフィールドのラベルが'カテゴリー'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'カテゴリー')

    def test_ja_word_label(self):
        """ja_wordフィールドのラベルが'日本語'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('ja_word').verbose_name
        self.assertEqual(field_label, '日本語')

    def test_en_word_label(self):
        """en_wordフィールドのラベルが'英語'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('en_word').verbose_name
        self.assertEqual(field_label, '英語')

    def test_memo_label(self):
        """memoフィールドのラベルが'メモ'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('memo').verbose_name
        self.assertEqual(field_label, 'メモ')

    def test_file_label(self):
        """fileフィールドのラベルが'ファイル'になっているかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('file').verbose_name
        self.assertEqual(field_label, 'file')

    def test_get_absolute_url(self):
        """get_absolute_urlメソッドのテスト"""
        wordlist = WordLists.objects.get(id=1)
        expected_url = reverse('english_list:list_word')
        self.assertEqual(wordlist.get_absolute_url(), expected_url)

    def test_model_str_representation(self):
        """モデルの文字列表現のテスト"""
        wordlist = WordLists.objects.get(id=1)
        expected_str = '<WordLists ☆ id=1,テスト,test,This is a test memo>'
        self.assertEqual(str(wordlist), expected_str)

    def test_wordlist_fields(self):
        """フィールドの値が正しいかをテスト"""
        wordlist = WordLists.objects.get(id=1)
        self.assertEqual(wordlist.user, self.user)
        self.assertEqual(wordlist.category, 'Test Category')
        self.assertEqual(wordlist.ja_word, 'テスト')
        self.assertEqual(wordlist.en_word, 'test')
        self.assertEqual(wordlist.memo, 'This is a test memo')