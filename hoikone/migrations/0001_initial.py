# Generated by Django 4.2 on 2023-07-07 15:37

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hoikone.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', hoikone.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryNursery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nursery',
            fields=[
                ('key_field', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nursery_number', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=255, verbose_name='保育園名')),
                ('type', models.CharField(max_length=255, verbose_name='種類')),
                ('feature', models.TextField(null=True, verbose_name='特色')),
                ('feature_image', models.ImageField(null=True, upload_to=hoikone.models.user_directory_path, verbose_name='特色を表現している画像')),
                ('feature_image2', models.ImageField(blank=True, null=True, upload_to=hoikone.models.user_directory_path, verbose_name='保持用')),
                ('description', models.TextField(null=True, verbose_name='特色を活かすためにどのように保育をしていますか？')),
                ('future', models.TextField(null=True, verbose_name='子どもたちにどのように育ってもらいたいか')),
                ('experience', models.TextField(null=True, verbose_name='子どもが体験できる経験')),
                ('experience_image', models.ImageField(null=True, upload_to=hoikone.models.user_directory_path, verbose_name='子どが体験できる経験の画像')),
                ('experience_image2', models.ImageField(null=True, upload_to=hoikone.models.user_directory_path, verbose_name='保持用')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='電話番号')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='住所')),
                ('capacity_0', models.IntegerField(blank=True, null=True, verbose_name='定員数…0歳')),
                ('capacity_1', models.IntegerField(blank=True, null=True, verbose_name='定員数…1歳')),
                ('capacity_2', models.IntegerField(blank=True, null=True, verbose_name='定員数…2歳')),
                ('capacity_3', models.IntegerField(blank=True, null=True, verbose_name='定員数…3歳')),
                ('capacity_4', models.IntegerField(blank=True, null=True, verbose_name='定員数…4歳')),
                ('capacity_5', models.IntegerField(blank=True, null=True, verbose_name='定員数…5歳')),
                ('open_hours', models.CharField(blank=True, max_length=255, verbose_name='開所時間')),
                ('extension_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='延長保育時間')),
                ('holidays', models.CharField(blank=True, max_length=255, verbose_name='休園日')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('image', models.ImageField(null=True, upload_to=hoikone.models.user_directory_path, verbose_name='園の画像')),
                ('image2', models.ImageField(null=True, upload_to=hoikone.models.user_directory_path, verbose_name='保持用')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nursery',
            },
        ),
    ]
