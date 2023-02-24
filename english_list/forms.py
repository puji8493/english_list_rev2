from django import forms
from .models import WordLists

class UserForm(forms.ModelForm):
    """新規登録するためのフォーム"""
    class Meta:
        model = WordLists
        fields = '__all__'

    def save(self,*args,**kwargs):
        obj = super().save(commit=False)
        obj.save()

        return obj

# Updateするためのフォーム
class WordUpdateForm(forms.ModelForm):
    """編集ページ"""
    class Meta:
        model = WordLists
        fields = '__all__'

    def save(self,*args,**kwargs):
        obj = super().save(commit=False)
        obj.save()
        return obj

class UpdatePictureForm(forms.ModelForm):
    """画像をアップロードするフォーム"""
    class Meta:
        model = WordLists
        fields = ['file']

    def save(self,*args,**kwargs):
        obj = super().save(commit=False)
        obj.save()
        return obj