英文・英単語管理アプリ

[1]登録フォーム　

|項目  | 説明|
|-----------------|----------------------------------------------|
| URL   | /english_list/input_form|
| 内容  | カテゴリー、日本語、英語、メモを入力して、DBに反映するページ                              |
| 備考  | forms.ModelFormクラスを利用。|
| 　　  | 変更　views.py 関数クラスベースビューからクラスベースビューに変更
| 　　  | 一覧ページへのリンクを埋め込み
| 　　  | htmlは、bootstrapを利用


[2]一覧ページ

|項目  | 説明|
|-----------------|----------------------------------------------|
| URL         | /english_list/ |
| 内容  | 登録した内容の一覧ページ|
| 備考  | data（WordLists.objects.all()）を取り出して表示|
| 　　  | 変更　vews.py 関数クラスビューからクラスベースビューに変更
| 　　  | 管理画面・[1]の登録フォームで登録した内容が反映されることを確認済み。
| 　　  | 登録フォームへのリンクを埋め込み
| 　　  | 編集・削除ボタンのリンクの埋め込み
| 　　  | CSSのスタイルシートを活用

[3]更新ページ

|項目  | 説明|
|-----------------|----------------------------------------------|
| URL         | /english_list/edit_word/id番号 |
| 内容  | 更新ページ|

[4]削除ページ

|項目  | 説明|
|-----------------|----------------------------------------------|
| URL         | /english_list/delete_word/id番号 |
| 内容  | 削除ページ|

[5]詳細ページ

|項目  | 説明|
|-----------------|----------------------------------------------|
| URL         | /english_list/detail_word/id番号 |
| 内容  | 更新ページ|
