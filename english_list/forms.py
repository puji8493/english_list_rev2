from django import forms
from .models import WordLists

class UserForm(forms.ModelForm):
    class Meta():
        model = WordLists
        fields = '__all__'

    def save(self,*args,**kwargs):
        obj = super(UserForm,self).save(commit=False)
        obj.save()

        return obj

