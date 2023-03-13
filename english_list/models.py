from django.db import models
from django.urls import reverse_lazy
from django.conf import settings


class WordLists(models.Model):
    # 追加　Metaクラス
    # akiyokoさんP51　モデルクラス内部のMetaクラス属性に対応するテーブル名やインデックスや
    # ユニーク制約などのモデルクラス全体に対する付加情報を記述
    class Meta:
        db_table = 'wordlists'

    def get_absolute_url(self):
        return reverse_lazy('english_list:detail_word', kwargs={'pk': self.pk})

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='words')
    category = models.CharField('カテゴリー', max_length=50)
    ja_word = models.CharField('日本語', max_length=300)
    en_word = models.TextField('英語')
    memo = models.TextField('メモ')
    file = models.ImageField(upload_to='media/images/', blank=True)  # 追加

    def __str__(self):
        return '<WordLists ☆ id=' + str(self.id) + ',' + self.ja_word + ',' + self.en_word + ',' + self.memo + '>'
