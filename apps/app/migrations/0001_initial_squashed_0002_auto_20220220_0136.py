# Generated by Django 3.0.9 on 2022-02-27 07:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    replaces = [('app', '0001_initial'), ('app', '0002_auto_20220220_0136')]

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=64, verbose_name='暱稱')),
                ('role', models.CharField(max_length=64, verbose_name='角色')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('content', models.TextField()),
                ('published_parsed', models.DateTimeField()),
                ('updated_parsed', models.DateTimeField()),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('reply_count', models.IntegerField(default=0)),
                ('favor_count', models.IntegerField(default=0)),
                ('views_count', models.IntegerField(default=0)),
                ('thumbnail', models.URLField(verbose_name='縮圖網址')),
                ('push_status', models.BooleanField(default=False, verbose_name='發布狀態')),
            ],
            options={
                'ordering': ['-published_parsed'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Telegram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('chat_id', models.CharField(blank=True, max_length=255, verbose_name='chat_id')),
                ('status', models.BooleanField(default=False, verbose_name='綁定狀態')),
                ('username', models.CharField(blank=True, max_length=255, verbose_name='TG暱稱')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(unique=True)),
                ('timezone', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=True)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('thumbnail', models.URLField(null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category')),
            ],
            options={
                'permissions': (('can_change', 'Can change'), ('can_delete', 'Can delete')),
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.News')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Source'),
        ),
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(blank=True, to='app.Tag', verbose_name='標籤'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='news',
            field=models.ManyToManyField(blank=True, to='app.News', verbose_name='收藏文章'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sourse',
            field=models.ManyToManyField(blank=True, related_name='userprofile', to='app.Source', verbose_name='訂閱來源'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telegram',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Telegram'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
