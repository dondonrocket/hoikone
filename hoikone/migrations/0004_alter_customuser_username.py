# Generated by Django 4.2 on 2023-08-01 14:38

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoikone', '0003_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'このユーザー名は使われています。別のユーザー名を入力して下さい。'}, help_text='必須項目です。半角英数字と@,.,+,-が使用できます。文字数は8文字までです。', max_length=8, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
