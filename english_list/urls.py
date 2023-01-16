from django.urls import path
from . import views
from .views import IndexView,FormView


app_name = 'english_list'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('input_form/',FormView.as_view() , name='form_create_view'),
]

