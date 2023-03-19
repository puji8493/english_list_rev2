from django.urls import path
from .views import (IndexView, FormView, WordDetailView, WordUpdateView, WordDeleteView,
                    WordListView,CreateWordView,Login,Logout,SignUpView,GenerateCsvView)


app_name = 'english_list'
urlpatterns = [
    path('', WordListView.as_view(), name='list_word'),
    path('input_form/', CreateWordView.as_view(), name='form_create_view'),
    path('detail_word/<int:pk>/', WordDetailView.as_view(), name='detail_word'),
    path('edit_word/<int:pk>/', WordUpdateView.as_view(), name='edit_word'),
    path('delete_word/<int:pk>/', WordDeleteView.as_view(), name='delete_word'),
    path('test/', IndexView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('export/', GenerateCsvView.as_view(), name='export'),
]
