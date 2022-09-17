# -*- coding: utf-8 -*-
#

from rest_framework import serializers
from authentication.models import AccessKey
from django.contrib.auth import get_user_model

User = get_user_model()

from . import models

__all__ = ['NewsListSerializer']


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["name"]


class NewsCreateSerializer(serializers.ModelSerializer):
    publish = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=['%Y/%m/%d %H:%M:%S'], read_only=True)
    published_parsed = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=['%Y/%m/%d %H:%M:%S'])
    updated_parsed = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=['%Y/%m/%d %H:%M:%S'])

    class Meta:
        model = models.News
        fields = "__all__"


class NewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        # fields = "__all__"
        fields = ["push_status"]


class NewsListSerializer(serializers.ModelSerializer):
    tag = TagListSerializer(read_only=True, many=True)
    source = serializers.ReadOnlyField(source='source.name')
    published_parsed = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    updated_parsed = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return obj.content[:100]

    class Meta:
        model = models.News
        fields = "__all__"


class NewsDetailSerializer(serializers.ModelSerializer):
    tag = TagListSerializer(read_only=True, many=True)
    source = serializers.ReadOnlyField(source='source.name')
    publish = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    telegram = serializers.SerializerMethodField()

    def get_telegram(self, obj):
        # print(obj)
        userprofile_objs = obj.source.userprofile.all()
        return [i.telegram.chat_id for i in userprofile_objs] if userprofile_objs else []

    class Meta:
        model = models.News
        fields = "__all__"


class SourceTreeListSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return f"{obj.name} {obj.url}"

    class Meta:
        model = models.Source
        fields = ["id", "label"]


class TelegramListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Telegram
        fields = ["status", "token"]


class UserprofileSerializer(serializers.ModelSerializer):
    telegram = serializers.SerializerMethodField()

    def get_telegram(self, obj):
        if obj.telegram:
            return obj.telegram.status
        else:
            return False

    class Meta:
        model = User
        fields = ["name", "email", 'telegram']
        read_only_fields = ["last_login"]


class SourceListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    enable = serializers.CharField(source='get_enable_display')
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    is_subscription = serializers.SerializerMethodField()

    def get_is_subscription(self, obj):
        # self.context['request'].user
        _request = self.context['request']
        _userprofile = _request.user
        if not _userprofile:
            return '否'

        if obj.userprofile.filter(id=_userprofile.id):
            return '是'
        else:
            return '否'

    class Meta:
        model = models.Source
        fields = "__all__"

class SourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = "__all__"

class SourceDetailSerializer(serializers.ModelSerializer):
    enable = serializers.IntegerField()

    class Meta:
        model = models.Source
        fields = "__all__"

class SourceSelectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = "__all__"


class CategorySelectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.name

    def get_children(self, obj):
        return SourceTreeListSerializer(obj.source_set.all(), many=True).data

    class Meta:
        model = models.Category
        fields = ["id", "label", "children"]





class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = ['id', 'secret', 'is_active', 'date_created']
        read_only_fields = ['id', 'secret', 'date_created']


class ServiceAccountSerializer(serializers.ModelSerializer):
    access_key = AccessKeySerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'access_key']
        read_only_fields = ['access_key']

    def get_username(self):
        return self.initial_data.get('name')

    def get_email(self):
        name = self.initial_data.get('name')
        return '{}@serviceaccount.local'.format(name)


class UserAKSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", 'telegram']
        read_only_fields = ["last_login"]


class TerminalRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    comment = serializers.CharField(max_length=128)
    service_account = ServiceAccountSerializer(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
