from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('top.urls'), name="top"),
    path('english_list/',include('english_list.urls'),name="english_list"),
 ]
