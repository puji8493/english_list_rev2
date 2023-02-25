from django import forms
from .models import WordLists

class BaseForm(forms.ModelForm):
    en_word = forms.CharField(label='英語', widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
    memo = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))

    class Meta:
        model = WordLists
        fields = '__all__'

    def save(self, *args, **kwargs):
        obj = super().save(commit=False)
        obj.save()
        return obj

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError('ファイルサイズは500KB以下にしてください。')
        return file


class UserForm(BaseForm):
    """新規登録するためのフォーム BaseFormを継承
       重複をチェックするメソッドだけ追加"""
    def clean_en_word(self):
        en_word = self.cleaned_data['en_word']
        if WordLists.objects.filter(en_word__iexact=en_word).exists():
            raise forms.ValidationError('この単語は既に登録されています。')
        return en_word


class WordUpdateForm(BaseForm):
    """編集するためのフォーム　BaseFormを継承"""
    pass


# class CategoryFilterForm(forms.Form):
#     CATEGORY_CHOICES = [
#         ('', 'カテゴリー'),
#         ('IT', 'IT'),
#         ('仕事', '仕事'),
#         ]
#     category = forms.ChoiceField(label='カテゴリー', choices=CATEGORY_CHOICES, required=False)

#
# class UserForm(forms.ModelForm):
#     """新規登録するためのフォーム"""
#
#     en_word = forms.CharField(label='英語', widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
#     memo = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
#
#     class Meta:
#         model = WordLists
#         fields = '__all__'
#
#     def save(self, *args, **kwargs):
#         obj = super().save(commit=False)
#         obj.save()
#         return obj
#
#     def clean_file(self):
#         """fileサイズが500KB以下かどうかをチェックする"""
#
#         file = self.cleaned_data['file']
#         if file:
#             if file.size > 5 * 1024:
#                 raise forms.ValidationError('ファイルサイズは500KB以下にしてください。')
#         return file
#
#     def clean_en_word(self):
#         """en_wordが重複していないかチェックする
#            完全一致（大文字小文字区別無し） 　　
#             Sample.objects.filter(field__iexact='条件')
#         """
#
#         en_word = self.cleaned_data['en_word']
#         if WordLists.objects.filter(en_word__iexact=en_word).exists():
#             raise forms.ValidationError('この単語は既に登録されています。')
#         return en_word
#
#
# class WordUpdateForm(forms.ModelForm):
#     """編集するためのフォーム"""
#
#     en_word = forms.CharField(label='英語', widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
#     memo = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
#
#     class Meta:
#         model = WordLists
#         fields = '__all__'
#
#     def save(self, *args, **kwargs):
#         obj = super().save(commit=False)
#         # commit=Falseは、データベースに保存しない
#         # 上書きする条件を書いて、obj.save()で保存する
#         obj.save()
#         # インスタンスを返す
#         return obj
#
#     def clean_file(self):
#         """fileサイズが500KB以下かどうかをチェックする"""
#
#         file = self.cleaned_data['file']
#         if file:
#             if file.size > 5 * 1024:
#                 raise forms.ValidationError('ファイルサイズは500KB以下にしてください。')
#         return file
#
#     def clean_en_word(self):
#         """en_wordが重複していないかチェックする
#            完全一致（大文字小文字区別無し） 　　
#             Sample.objects.filter(field__iexact='条件')
#         """
#
#         en_word = self.cleaned_data['en_word']
#         if WordLists.objects.filter(en_word__iexact=en_word).exists():
#             raise forms.ValidationError('この単語は既に登録されています。')
#         return en_word
#

# class UpdatePictureForm(forms.ModelForm):
#     """画像をアップロードするフォーム"""
#
#     class Meta:
#         model = WordLists
#         fields = ['file']
#
#     def save(self, *args, **kwargs):
#         obj = super().save(commit=False)
#         obj.save()
#         return obj
#
#     def clean_file(self):
#         file = self.cleaned_data['file']
#         if file:
#             if file.size > 5 * 1024:
#                 raise forms.ValidationError('ファイルサイズは500KB以下にしてください。')
#         return file
