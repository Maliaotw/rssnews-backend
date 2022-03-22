from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.UserLoginLog)


@admin.register(models.AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'secret', 'user', 'is_active', 'date_created'
    ]
