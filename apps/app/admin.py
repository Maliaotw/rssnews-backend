from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import (
    ugettext, gettext_lazy as _, pgettext_lazy as p,
)
from . import models

admin.site.register(models.Tag)
# admin.site.register(models.UserProfile)
# admin.site.register(models.News)
admin.site.register(models.Reply)


# admin.site.register(models.PushNews)
# admin.site.register(models.TelegramMaster)

@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'url', 'timezone', 'category', 'enable', 'remarks', 'thumbnail', 'update_time', 'create_time'
    ]
    list_filter = ['category', 'enable']
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'content', 'get_source', 'update_time', 'create_time'
    ]
    fields = [
        'name', 'content'
    ]
    search_fields = ['name']

    def get_source(self, instance):
        return format_html(
            '{name}',
            name=', '.join(instance.source_set.values_list('name', flat=True))
        )


@admin.register(models.Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = [
        'token', 'chat_id', 'status', 'username', 'userprofile'
    ]
    fields = [
        'chat_id', 'status', 'username'
    ]


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'url', 'source', 'get_category', 'published_parsed', 'updated_parsed'
    ]
    list_filter = ['source', 'source__category']
    search_fields = ['name']

    def get_category(self, instance):
        return instance.source.category
