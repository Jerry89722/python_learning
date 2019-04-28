from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db.base_model import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    def generate_active_token(self):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': self.id}
        token = serializer.dump(info)
        return token

    class Meta:
        db_table = 'df_user'
        verbose_name = 'user'
        verbose_name_plural = verbose_name


class Address(BaseModel):
    user = models.ForeignKey('user', on_delete=models.CASCADE, verbose_name='acc_belong_to')
    receiver = models.CharField(max_length=20, verbose_name='receiver')
    addr = models.CharField(max_length=256, verbose_name='receiver_addr')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='post_code')
    phone = models.CharField(max_length=11, verbose_name='phone_number')
    is_default = models.BooleanField(default=False, verbose_name='is_default')

    class Meta:
        db_table = 'df_address'
        verbose_name = 'address'
        verbose_name_plural = verbose_name

