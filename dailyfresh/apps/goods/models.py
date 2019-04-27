from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField


# Create your models here.
class GoodsType(BaseModel):
    name = models.CharField(max_length=20, verbose_name='type_name')
    logo = models.CharField(max_length=20, verbose_name='logo')
    image = models.ImageField(upload_to='type', verbose_name='image_type')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = 'goods_type'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    status_choices = (
        (0, 'offline'),
        (1, 'online'),
    )

    type = models.ForeignKey('GoodsType', verbose_name='goods_type')
    goods = models.ForeignKey('Goods', verbose_name='GoodsSPU')
    name = models.CharField(max_length=20, verbose_name='goods_name')

