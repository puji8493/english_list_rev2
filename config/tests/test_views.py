from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.contrib.messages import get_messages
from django.contrib.auth.models import User

"""
テストコード内でURLを指定する際には、reverse関数を使用してURLを生成するのが一般的です。
"""

class MyTestCase(TestCase):

    def test_login(self):
        url = reverse('english_list:login')  # テンプレートの対応するビュー名を指定
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_login_html(self):
        url = reverse('english_list:login')  # テンプレートの対応するビュー名を指定
        response = self.client.get(url)
        expected_content = 'ログイン'
        self.assertContains(response, expected_content)

    # def test_login_html_massages(self):
    #     url = reverse('english_list:login')
    #     response = self.client.get(url)
    #     messages = list(response.context['messages'])
    #     print(len(messages))
    #     self.assertEqual(len(messages), 0)


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        response = self.client.post(reverse('english_list:login'), {'username': 'testuser', 'password': 'testpassword'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)


class TestLogin(TestCase):

    def test_login(self):
        url = reverse('english_list:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_html(self):
        url = reverse('english_list:login')
        response = self.client.get(url)
        expected_content = 'ログイン'
        self.assertContains(response, expected_content)

    def test_login_failure_message(self):
        url = reverse('english_list:login')
        data = {
            'username': 'invalid_user',
            'password': 'invalid_password'
        }
        response = self.client.post(url, data)

        # ログイン失敗時のメッセージが表示されるか確認
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        # self.assertEqual(str(messages[0]), 'ユーザー名またはパスワードが正しくありません。')



class TestLogin1(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


        url = reverse('english_list:login')
        data = {
            'username': 'invalid_user',  # 存在しないユーザー名
            'password': 'invalid_password'  # 不正なパスワード
        }
        # response = self.client.post(url, data)

        # セッションをシミュレートするためにClientを使用
        response = self.client.post(url, data, follow=True)


        # ログイン失敗時のメッセージが表示されるか確認
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), 'ユーザー名またはパスワードが正しくありません。')
