from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse


User = get_user_model()


# class CustomUserTestCase(TestCase):
#     def setUp(self):
#         self.User = get_user_model()
#
#     def test_create_user(self):
#         user = self.User.objects.create_user(username='testuser', password='testpassword')
#         self.assertEqual(user.username, 'testuser')
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#


# class LoginTestCase(TestCase):
#
#     def setUp(self):
#         self.User = get_user_model()
#
#     def test_create_user(self):
#         user = self.User.objects.create_user(username='testuser', password='testpassword')
#         self.assertEqual(user.username, 'testuser')
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#
#     def test_login_failure_message(self):
#         url = reverse('english_list:login')
#         response = self.client.get(url)
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(len(messages), 0)  # メッセージがないことを確認
#
#         # ログイン失敗時のPOSTリクエストを送信（ユーザー登録をしていないためログイン失敗）
#         response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
#
#         # ログイン失敗時のメッセージが表示されるか確認
#         messages = list(get_messages(response.wsgi_request))
#         # self.assertEqual(len(messages), 1)
#         print(len(messages))
#         # self.assertEqual(str(messages[0]), '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')


class LoginTestCase1(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_login_failure_message(self):
        url = reverse('english_list:login')
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)  # メッセージがないことを確認

        # ログイン失敗時のPOSTリクエストを送信（ユーザー登録をしていないためログイン失敗）
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})

        # ログイン失敗時のメッセージが表示されるか確認
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'ログインに失敗しました。ユーザー名とパスワードを確認してください。')

    def test_login_failure_nonexistent_user(self):
        url = reverse('english_list:login')
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)  # メッセージがないことを確認

        # ログイン失敗時のPOSTリクエストを送信（存在しないユーザーの情報でログイン失敗）
        response = self.client.post(url, {'username': 'nonexistentuser', 'password': 'testpassword'})

        # ログイン失敗時のメッセージが表示されるか確認
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'ログインに失敗しました。ユーザー名とパスワードを確認してください。')
