from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.signup_url = reverse('english_list:signup')
        self.login_url = reverse('english_list:login')

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})

        # ログインに成功すると、ステータスコードが "english_list:list_word"のページに遷移する
        # 302 (リダイレクト) になるか確認
        self.assertEqual(response.status_code, 302)

        # リダイレクト先のURLが予想通りか確認
        self.assertRedirects(response, expected_url=reverse('english_list:list_word'), fetch_redirect_response=False)

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

