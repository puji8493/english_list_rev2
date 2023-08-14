from django.test import TestCase
from django.urls import reverse
from english_list.models import WordLists
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

User = get_user_model()


class WordListsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )

        self.wordlist = WordLists.objects.create(
            user=self.user,
            category='Test Category',
            ja_word='テスト',
            en_word='test',
            memo='This is a test memo'
        )

        self.edit_url = reverse('english_list:edit_word', args=[self.wordlist.pk])

    # @classmethod
    # def setUpTestData(cls):
    #     # テストデータをセットアップ
    #     cls.user = User.objects.create_user(
    #         username='testuser',
    #         password='testpassword'
    #     )
    #
    #     cls.other_user = User.objects.create_user(
    #         username='otheruser',
    #         password='otherpassword'
    #     )
    #
    #     cls.wordlist = WordLists.objects.create(
    #         user=cls.user,
    #         category='Test Category',
    #         ja_word='テスト',
    #         en_word='test',
    #         memo='This is a test memo'
    #     )
    #

    def test_edit_word_by_other_user_shows_error_message(self):
        """follow=True は、Djangoのテストクライアントにおいて、リダイレクトを自動的にたどるオプションです。
        通常、ウェブアプリケーションでリダイレクトが発生すると、ブラウザは自動的に新しいURLにアクセスし、そのページの内容を表示します。
        follow=True を使用すると、テストクライアントも同様の動作を行い、リダイレクト先のページの内容を取得してテストできるようになります。"""

        self.client.force_login(self.other_user)

        # テスト対象の投稿を編集しようとするリクエストを送信（follow=True を追加）
        response = self.client.get(self.edit_url, follow=True)

        # エラーメッセージが表示されることを確認
        self.assertContains(response, "他のユーザーの投稿は編集できません")

    def test_edit_word_by_owner_succeeds(self):
        self.client.force_login(self.user)

        # テスト対象の投稿を編集するリクエストを送信
        response = self.client.get(self.edit_url)

        # 正常にアクセスできることを確認
        self.assertEqual(response.status_code, 200)

    def test_check_object(self):
        wordlists = WordLists.objects.all()
        self.assertEqual(len(wordlists),1)

    def test_user_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_category_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'カテゴリー')

    def test_ja_word_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('ja_word').verbose_name
        self.assertEqual(field_label, '日本語')

    def test_en_word_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('en_word').verbose_name
        self.assertEqual(field_label, '英語')

    def test_memo_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('memo').verbose_name
        self.assertEqual(field_label, 'メモ')

    def test_file_label(self):
        wordlist = WordLists.objects.get(id=1)
        field_label = wordlist._meta.get_field('file').verbose_name
        self.assertEqual(field_label, 'file')

    def test_get_absolute_url(self):
        wordlist = WordLists.objects.get(id=1)
        expected_url = reverse('english_list:list_word')
        self.assertEqual(wordlist.get_absolute_url(), expected_url)

    def test_model_str_representation(self):
        wordlist = WordLists.objects.get(id=1)
        expected_str = '<WordLists ☆ id=1,テスト,test,This is a test memo>'
        self.assertEqual(str(wordlist), expected_str)
