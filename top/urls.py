from django.urls import path
from .views import TopView

app_name = 'top'
urlpatterns = [
    path('', TopView.as_view(), name='top'),
]
