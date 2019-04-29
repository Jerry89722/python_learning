from django.urls import path, re_path
from cart import views

urlpatterns = [
    path('test/<str:token>', views.test, name='test'),
]