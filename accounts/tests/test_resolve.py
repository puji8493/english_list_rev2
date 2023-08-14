from django.shortcuts import resolve_url
from django.test import TestCase
from django.contrib.auth import get_user_model
from english_list.models import WordLists

User = get_user_model()

class TestSample(TestCase):

    def setUp(self):
        self.category = WordLists.objects.create()


    # category = models.CharField('カテゴリー', max_length=50)
    # ja_word = models.CharField('日本語', max_length=300)
    # en_word = models.TextField('英語')
    # memo = models.TextField('メモ')
    # file = models.ImageField(upload_to='media/images/', blank=True)  # 追加

