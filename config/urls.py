from django.contrib import admin
from django.urls import path,include
# include関数を追加する

urlpatterns = [
    path('admin/', admin.site.urls),
    path('english_list/',include('english_list.urls'),name="english_list"),
 ]
