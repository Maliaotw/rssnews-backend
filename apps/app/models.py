import uuid

# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from src.base.model import AbstractBaseModel

# Create your models here.

class UserProfile(AbstractUser):
    """用戶"""
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name="暱稱")
    telegram = models.OneToOneField("app.Telegram", blank=True, null=True, on_delete=models.SET_NULL)
    sourse = models.ManyToManyField("app.Source", verbose_name="訂閱來源", blank=True, related_name='userprofile')
    news = models.ManyToManyField("app.News", verbose_name="收藏文章", blank=True)
    role = models.CharField(max_length=64, verbose_name='角色')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def access_key(self):
        if self.access_keys:
            return self.access_keys.first()

    @property
    def is_app(self):
        return self.role == 'App'

    @property
    def is_valid(self):
        if self.is_active:
            return True
        return False

    # @property
    # def is_superuser(self):
    #     if self.role == 'Admin':
    #         return True
    #     else:
    #         return False

    def __str__(self):
        return self.name


class Category(AbstractBaseModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Source(AbstractBaseModel):
    """RSS 來源表"""

    choices = {
        'enable': (
            (0, '否'),
            (1, '是')
        )
    }

    name = models.CharField(max_length=255, verbose_name='來源名稱')
    url = models.URLField(unique=True, verbose_name='URL')
    timezone = models.IntegerField(default=0, verbose_name='時區差')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name='分類')
    enable = models.BooleanField(choices=choices['enable'], default=True, verbose_name='啟用狀態')
    remarks = models.CharField(max_length=255, blank=True, verbose_name='備註')
    thumbnail = models.URLField(blank=True, default='', verbose_name='縮圖網址')



    class Meta:
        permissions = ()

    def __str__(self):
        return self.name


class Tag(AbstractBaseModel):
    """標籤表"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Telegram(AbstractBaseModel):
    """TG"""
    token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255, verbose_name="chat_id", blank=True)
    status = models.BooleanField(default=False, verbose_name="綁定狀態")
    username = models.CharField(max_length=255, verbose_name="TG暱稱", blank=True)

    def __str__(self):
        return "%s %s" % (self.chat_id, self.token)


class News(AbstractBaseModel):
    """新聞表"""
    id = models.CharField(max_length=32, primary_key=True)
    source = models.ForeignKey("Source", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()
    published_parsed = models.DateTimeField(db_index=True)
    updated_parsed = models.DateTimeField()
    tag = models.ManyToManyField("Tag", blank=True, verbose_name="標籤")
    reply_count = models.IntegerField(default=0)
    favor_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    thumbnail = models.URLField(max_length=512, verbose_name="縮圖網址")
    push_status = models.BooleanField(default=False, verbose_name='發布狀態')

    class Meta:
        indexes = [
            models.Index(fields=['published_parsed'])
        ]
        ordering = ['-published_parsed']


    def __str__(self):
        return self.name


class Reply(AbstractBaseModel):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    new = models.ForeignKey('News', on_delete=models.CASCADE)


    def __str__(self):
        return self.content
