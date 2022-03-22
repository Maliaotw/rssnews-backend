import uuid

# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models



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


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255,blank=True,default='')
    content = models.TextField(blank=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    timezone = models.IntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, blank=True)
    thumbnail = models.URLField(blank=True,default='')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("can_change", "Can change"),
            ("can_delete", "Can delete"),
        )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Telegram(models.Model):
    """TG"""
    token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255, verbose_name="chat_id", blank=True)
    status = models.BooleanField(default=False, verbose_name="綁定狀態")
    username = models.CharField(max_length=255, verbose_name="TG暱稱", blank=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.chat_id, self.token)


class News(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    source = models.ForeignKey("Source", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()
    published_parsed = models.DateTimeField()
    updated_parsed = models.DateTimeField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField("Tag", blank=True, verbose_name="標籤")
    reply_count = models.IntegerField(default=0)
    favor_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    thumbnail = models.URLField(verbose_name="縮圖網址")
    push_status = models.BooleanField(default=False, verbose_name='發布狀態')

    class Meta:
        ordering = ['-published_parsed']

    def __str__(self):
        return self.name


class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    new = models.ForeignKey('News', on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
