from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import SignatureExpired
import re

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
        send_register_active_email.delay(email, username, token)
        # subject = "welcom daily fresh"
        # msg = ''
        # html_msg = "<h1>%s, welcom to daily fresh</h1>please click the link to active your account<br/><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (username, token, token)
        # sender = settings.EMAIL_HOST_USER
        # receivers = [email]
        # send_mail(subject, msg, sender, receivers, html_message=html_msg)

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
        return render(request, 'login.html')


