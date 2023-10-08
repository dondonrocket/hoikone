import os
import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.apps import apps


def user_directory_path(instance, filename):
    # アップロード先のディレクトリパスを生成する関数
    # ユーザーごとにフォルダを作成する

    # ファイル名を取得
    base_filename = os.path.basename(filename)

    # ユーザーごとのフォルダ名を生成（例: user_id/）
    folder_name = str(instance.nursery_number)

    # ファイルパスを生成して返す（例: 'upload_img/user_id/filename'）
    return os.path.join('upload_img', folder_name, base_filename)

class Nursery(models.Model):

    class Meta:
        db_table = 'nursery'
    #キーの設定
    key_field = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #作成順のidを登録
    nursery_number = models.IntegerField(default=0)
    #userとの紐づけ2023年6月4日
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #保育園名
    name = models.CharField('保育園名', max_length=255)
    #保育園の種類
    type = models.CharField('種類', max_length=255)
    #特色
    feature = models.TextField('特色', null=True, max_length=80)
    #特色を表している画像
    feature_image = models.ImageField('特色を表現している画像', upload_to=user_directory_path, null=True)
    #保持用
    feature_image2 = models.ImageField('保持用', upload_to=user_directory_path, blank=True, null=True)
    #特色を活かすためにどのように保育をしているか
    description = models.TextField('特色を活かすためにどのように保育をしていますか？', null=True)
    #子どもと接するときに何を大事にしているか
    future = models.TextField('子どもと接するときに何を大事にしているか', null=True)
    #あなたの保育園で子どもが体験できる経験を1つ教えてください。
    experience = models.TextField('子どもが体験できる経験', null=True)
    #子どもが体験できる経験の画像
    experience_image = models.ImageField('子どが体験できる経験の画像', upload_to=user_directory_path, null=True)
    #保持用
    experience_image2 = models.ImageField('保持用', upload_to=user_directory_path, null=True)
    #電話番号
    phone_number = models.CharField('電話番号', max_length=20,  blank=True, null=True)
    #Email
    email = models.EmailField('Email', blank=True, null=True)
    #住所
    address = models.CharField('住所', max_length=255, blank=True,  null=True)
    #園庭
    playground = models.CharField('園庭', max_length=255, blank=True,  null=True)
    #定員数0歳
    capacity_0 = models.IntegerField('定員数…0歳', blank=True, null=True)
    #定員数1歳
    capacity_1 = models.IntegerField('定員数…1歳', blank=True, null=True)
    #定員数2歳
    capacity_2 = models.IntegerField('定員数…2歳', blank=True, null=True)
    #定員数3歳
    capacity_3 = models.IntegerField('定員数…3歳', blank=True, null=True)
    #定員数4歳
    capacity_4 = models.IntegerField('定員数…4歳', blank=True, null=True)
    #定員数5歳
    capacity_5 = models.IntegerField('定員数…5歳', blank=True, null=True)
    #開所時間
    open_hours = models.CharField('開所時間', max_length=255, blank=True)
    #延長保育の時間
    extension_time = models.CharField('延長保育時間', max_length=255, blank=True, null=True)
    #休園日
    holidays = models.CharField('休園日', max_length=255, blank=True)
    #url
    url = models.URLField('url', blank=True, null=True)
    #園の画像
    image = models.ImageField('園の画像', upload_to=user_directory_path, null=True)
    #保持用
    image2 = models.ImageField('保持用', upload_to=user_directory_path, null=True)

    #作成日
    created_at = models.DateTimeField(auto_now_add=True)
    #更新日
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.nursery_number:
        # 新規作成時にnursery_numberを自動的に割り当てる
            max_nursery_number = Nursery.objects.aggregate(models.Max('nursery_number'))['nursery_number__max']
            self.nursery_number = max_nursery_number + 1 if max_nursery_number else 1

        # フォルダを作成するパスを設定
        folder_path = os.path.join(settings.MEDIA_ROOT, 'upload_img', str(self.nursery_number))
        # フォルダが存在しない場合は作成する
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        super().save(*args, **kwargs)  # 親クラスのsaveメソッドを呼び出す

    def __str__(self):
        return self.name

#パスワード形成のため追加2023年6月3日
    def set_password(self, raw_password):
        # パスワードをハッシュ化して保存
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # 入力されたパスワードが正しいかをチェック
        return check_password(raw_password, self.password)
#ここまで


#一時保存用のモデルを作成
class TemporaryNursery(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,  # ユニークキーに設定
        help_text=_('必須項目です。半角英数字と@,.,+,-が使用できます。文字数は15文字以下までです。'),
        validators=[username_validator],
        error_messages={
            'unique': _("このユーザー名は使われています。別のユーザー名を入力して下さい。"),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    email_change = models.BooleanField(default=False)  # メールアドレス変更の状態
    email_change_token = models.CharField(max_length=255, blank=True) #メールアドレス変更のトークン

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

