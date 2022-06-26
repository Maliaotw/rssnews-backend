from django.db import models

class AbstractBaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='修改時間')
    create_by = models.CharField(verbose_name='創建人', max_length=255, blank=True, default='')
    update_time = models.DateTimeField(auto_now=True, verbose_name='創建時間')
    update_by = models.CharField(verbose_name='修改人', max_length=255, blank=True, default='')
    is_deleted = models.BooleanField(verbose_name='是否刪除',default=False)

    class Meta:
        abstract = True