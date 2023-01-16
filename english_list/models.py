from django.db import models


class WordLists(models.Model):
    # 追加　Metaクラス
    # akiyokoさんP51　モデルクラス内部のMetaクラス属性に対応するテーブル名やインデックスや
    # ユニーク制約などのモデルクラス全体に対する付加情報を記述
    class Meta:
        db_table = 'wordlists'

    category = models.CharField('カテゴリー', max_length=50)
    ja_word = models.CharField('日本語', max_length=300)
    en_word = models.TextField('英語')
    memo = models.TextField('メモ')

    def __str__(self):
        return '<WordLists ☆ id=' + str(self.id) + ',' + self.ja_word + ',' + self.en_word + ',' + self.memo + '>'
