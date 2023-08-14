from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

User = get_user_model()

class TestAuthentication(TestCase):

    def setUp(self):
        """ すべてのテストメソッドに共通の準備 """
        self.signup_url = resolve_url('english_list:signup')
        self.login_url = resolve_url('english_list:login')
        self.english_list_url = resolve_url('english_list:list_word')

    def test_anonymous(self):
        """未ログインユーザーとしてgetリクエストを行う"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """
        ユーザー登録を行い、ログインに成功することを確認する
        ログインに成功すると、"english_list:list_word"のページに遷移する
        302 (リダイレクト) になるか確認
        """
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})

        login_result = self.client.login(username=user.username, password='testpassword')

        # login_result = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_result)

        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # ログインに成功すると、ステータスコードが "english_list:list_word"のページに遷移する
        # 302 (リダイレクト) になるか確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のURLが予想通りか確認
        self.assertRedirects(response, expected_url=self.english_list_url, fetch_redirect_response=True)
        # self.assertRedirects(response, expected_url=self.english_list_url, fetch_redirect_response=False)

    def test_login_with_invalid_user(self):
        # 存在しないユーザーでログイン
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'testpassword',
        }, follow=True)

        # ステータスコードが正しいか確認
        self.assertEqual(response.status_code, 200)

        # ログインに失敗した場合、適切なメッセージが表示されるか確認
        expected_content = '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。'
        self.assertContains(response, expected_content)


