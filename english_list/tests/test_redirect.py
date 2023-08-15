from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

User = get_user_model()

class TestCreateViewRedirect(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_path = resolve_url('english_list:form_create_view')
        cls.redirect_path = resolve_url('english_list:list_word')
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.post_data = { 'category': 'testcategory', 'ja_word': 'test日本語', 'en_word': 'testeng','memo': 'testmemo' }


    def test_get_success(self):
        # self.client.force_login(self.user)
        # response = self.client.get(self.request_path)
        # self.assertEqual(response.status_code, 200)

        result = self.client.login(username=self.user.username, password='testpassword')
        self.assertTrue(result)
        response = self.client.get(self.request_path)
        self.assertEqual(response.status_code, 200)

    def test_get_success_follow_false(self):
        """
        302リダイレクトが発生することをテスト
        follow=False を指定すると、これ以上追及しない
        success_url = reverse_lazy('english_list:form_create_view')
        viewはフォームのバリデーションが成功した後に、指定された URL にリダイレクトする処理を含んでいます。
        """
        result = self.client.login(username=self.user.username, password='testpassword')
        self.assertTrue(result)
        response = self.client.post(self.request_path, data=self.post_data, follow=False)
        self.assertEqual(response.status_code, 302)




    def test_get_success_follow_true(self):
        """
        follow=Trueの場合は、転送先までの処理をみるため、レスポンスコードは200になる
        messagesを取得する場合は、follow=Trueを指定する必要がある
        """
        result = self.client.login(username=self.user.username, password='testpassword')
        self.assertTrue(result)
        response = self.client.post(self.request_path, data=self.post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # messagesを取得する場合は、follow=Trueを指定する必要がある
        # 理由は、messagesはHttpResponseRedirectオブジェクトに含まれているため
        # リダイレクト先のビューが実行され、そのビュー内で行われる処理やコンテキスト変数（この場合はメッセージ）にアクセスできるようになります。
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '新規登録しました')