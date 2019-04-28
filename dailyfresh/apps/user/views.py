from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
import re

# Create your views here.


# /user/register
def register(request):
    return render(request, 'register.html')


def register_handle(request):
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

    User.objects.create_user(username, email, pwd)
    return redirect(reverse('goods:index'))
