from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time

app = Celery('celery_task.tasks', broker='redis://127.0.0.1:6379/7')


@app.task
def send_register_active_email(to_email, username, token):
    subject = 'Welcom to Daily Fresh'
    msg = ''
    sender = settings.EMAIL_FROM
    receivers = [to_email]
    html_msg = "<h1>%s, welcom to daily fresh</h1>please click the link to active your account<br/><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (username, token, token)
    send_mail(subject, msg, sender, receivers, html_message=html_msg)
    time.sleep(5)
