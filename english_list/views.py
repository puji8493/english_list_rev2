from django.shortcuts import render
from .models import WordLists
from . import forms
from django.views.generic.base import View

class IndexView(View):
    def get(self,request,*args,**kwargs):
        data = WordLists.objects.all()
        return render(request,'english_list/index.html',context={'wordlists':data})

class FormView(View):
    def get(self,request,*args,**kwargs):
        form = forms.UserForm()
        return render(request,'english_list/form_create_view.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = forms.UserForm()
        return render(request,'english_list/form_create_view.html',{'form':form})


# def form_create_view(request):
#     form = forms.UserForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = forms.UserForm()#初期化
#     return render(request,'english_list/form_create_view.html',{'form':form})
