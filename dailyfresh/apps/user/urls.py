from django.urls import path, re_path
from user.views import RegisterView, ActiveView, LoginView

urlpatterns = [
    # re_path(r'register$', views.register),
    # re_path(r'register_handle$', views.register_handle),
    path('register', RegisterView.as_view(), name='register'),
    path('active/<str:token>', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login')
]
