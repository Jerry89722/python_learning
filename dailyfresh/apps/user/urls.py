from django.urls import path, re_path
from user import views

urlpatterns = [
    re_path(r'register$', views.register),
    re_path(r'register_handle$', views.register_handle),
]
