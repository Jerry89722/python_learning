from django.db import models
from db.base_model import BaseModel
# Create your models here.


class OrderInfo(BaseModel):
    PAY_METHOD_CHOICES = (
        (1, 'cash_on_delivery'),
        (2, 'wechat_pay'),
        (3, 'ali_pay'),
        (4, 'union_pay')
    )

    ORDER_STATUS_CHOICE = (
        (1, 'unpaid'),
        (2, 'undelivered'),
        (3, 'unreceived'),
        (4, 'received'),
        (5, 'done')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='order_id')
    user = models.ForeignKey('user.User', verbose_name='user', on_delete=models.CASCADE)
    addr = models.ForeignKey('user.Address', verbose_name='address', on_delete=models.CASCADE)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='pay_method')
    total_count = models.IntegerField(default=1, verbose_name='number')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='total_price')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='transit_price')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICE, default=1, verbose_name='order_status')
    trade_no = models.CharField(max_length=128, verbose_name='payment_id')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = 'orders'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    order = models.ForeignKey('OrderInfo', verbose_name='order', on_delete=models.CASCADE)
    sku = models.ForeignKey('goods.GoodsSKU', verbose_name='goodsSKU', on_delete=models.CASCADE)
    count = models.IntegerField(default=1, verbose_name='number')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    comment = models.CharField(max_length=256, verbose_name='comment')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = 'goods_in_order'
        verbose_name_plural = verbose_name
