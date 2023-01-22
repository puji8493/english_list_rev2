from django.urls import path
from . import views
from .views import IndexView, FormView, WordDetailView, WordUpdateView, WordDeleteView

app_name = 'english_list'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('input_form/', FormView.as_view(), name='form_create_view'),
    path('detail_word/<int:pk>', WordDetailView.as_view(), name='detail_word'),
    path('edit_word/<int:pk>', WordUpdateView.as_view(), name='edit_word'),
    path('delete_word/<int:pk>', WordDeleteView.as_view(), name='delete_word')

]
