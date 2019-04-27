from django.db import models


class BaseModel(models.Model):

    """base model abstract"""
    create_time = models.DateField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateField(auto_now=True, verbose_name="update_time")
    is_delete = models.BooleanField(default=False, verbose_name="del_flag")

    class Meta:
        # to flag this is a abstract class
        abstract = True

