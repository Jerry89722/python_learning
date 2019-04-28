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

    type = models.ForeignKey('GoodsType', verbose_name='goods_type', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', verbose_name='GoodsSPU', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='goods_name')
    desc = models.CharField(max_length=256, verbose_name='goods_description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='goods_price')
    unite = models.CharField(max_length=20, verbose_name='goods_unite')
    image = models.ImageField(upload_to='goods', verbose_name='goods_image')
    stock = models.IntegerField(default=1, verbose_name='goods_stock')
    sales = models.IntegerField(default=0, verbose_name='goods_sales')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='goods_status')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = 'goods'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    name = models.CharField(max_length=20, verbose_name='goods_sku_name')
    detail = HTMLField(blank=True, name='goods_details')

    class Meta:
        db_table = 'df_goods'
        verbose_name = 'goods_spu'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    sku = models.ForeignKey('GoodsSKU', verbose_name='goods', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods', verbose_name='image_path')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = 'goods_images'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    sku = models.ForeignKey('GoodsSKU', verbose_name='Goods', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='image')
    index = models.SmallIntegerField(default=0, verbose_name='goods_banner')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = 'Goods_banner'
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    DISPLAY_TYPE_CHOICES = (
        (0, 'title'),
        (1, 'image'),
    )

    type = models.ForeignKey('GoodsType', verbose_name='goods_type', on_delete=models.CASCADE)
    sku = models.ForeignKey('GoodsSKU', verbose_name='goods_sku', on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='display_type')
    index = models.SmallIntegerField(default=0, verbose_name='show_index')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = 'main_page_goods_show'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    name = models.CharField(max_length=20, verbose_name='promotion_name')
    url = models.URLField(verbose_name='promotion_link')
    image = models.ImageField(upload_to='banner', verbose_name='promotion_image')
    index = models.SmallIntegerField(default=0, verbose_name='show_index')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = 'main_page_promotion'
        verbose_name_plural = verbose_name