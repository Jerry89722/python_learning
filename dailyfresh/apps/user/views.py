from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate, login
import re

from utils.mixin import LoginRequiredMixin
from user.models import User
from celery_tasks.tasks import send_register_active_email
# Create your views here.


# /user/register
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 1. data receive
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2. data validate
        if not all([username, pwd, cpwd, email]):
            return render(request, 'register.html', {'errmsg': "the number of parameters is incorrect"})

        # 2.1 email validate
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': "the format of email is incorrect"})

        # 2.2 allow validate
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': "please check the agreement"})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': "user name exist"})

        user = User.objects.create_user(username, email, pwd)
        user.is_active = 0
        user.save()

        return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 1. data receive
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2. data validate
        if not all([username, pwd, cpwd, email]):
            return render(request, 'register.html', {'errmsg': "the number of parameters is incorrect"})

        # 2.1 email validate
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': "the format of email is incorrect"})

        # 2.2 allow validate
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': "please check the agreement"})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': "user name exist"})

        user = User.objects.create_user(username, email, pwd)
        user.is_active = 0
        user.save()

        # encode user's identify info
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()

        # send active email
        # send_register_active_email.delay(email, username, token)
        subject = "welcom daily fresh"
        msg = ''
        html_msg = "<h1>%s, welcom to daily fresh</h1>please click the link to active your account<br/><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (username, token, token)
        sender = settings.EMAIL_HOST_USER
        receivers = [email]
        send_mail(subject, msg, sender, receivers, html_message=html_msg)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self, request, token):

        serializer = Serializer(settings.SECRET_KEY, 3600)


        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as se:
            return HttpResponse("active link expired")


class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # 接收数据
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        remember = request.POST.get('remember')

        # 校验数据
        if not all([username, pwd]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        # 业务处理
        user = authenticate(username=username, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                response = redirect(reverse('goods:index'))
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, 7*24*3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'login.html', {'errmsg': '账号未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '账号或密码不正确'})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_info.html')

    # @classmethod
    # def as_view(cls, **initkwargs):
    #     view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    #     return login_required(view)


class UserOrderView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_order.html')


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_site.html')

