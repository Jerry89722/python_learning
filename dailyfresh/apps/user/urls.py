from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView

urlpatterns = [
    # re_path(r'register$', views.register),
    # re_path(r'register_handle$', views.register_handle),
    path('register', RegisterView.as_view(), name='register'),
    path('active/<str:token>', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login'),
    path('', UserInfoView.as_view(), name='user'),
    path('order', UserOrderView.as_view(), name='order'),
    path('address', AddressView.as_view(), name='address'),
]
