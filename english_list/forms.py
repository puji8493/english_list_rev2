from django import forms
from .models import WordLists

class UserForm(forms.ModelForm):
    class Meta():
        model = WordLists
        fields = '__all__'

    def save(self,*args,**kwargs):
        obj = super().save(commit=False)
        obj.save()

        return obj

# Updateするためのフォーム
class WordUpdateForm(forms.ModelForm):
    class Meta():
        model = WordLists
        fields = '__all__'

    def save(self,*args,**kwargs):
        obj = super().save(commit=False)
        obj.save()
        return obj
