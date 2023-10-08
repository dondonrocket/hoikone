import re

#ログイン認証のための追記2023年6月7日
from django.contrib.auth import authenticate
#ここまで
from rest_framework import serializers
from .models import Nursery
#ユーザー登録機能登録のため追記2023年6月3日
#from django.contrib.auth.models import User
#ここまで
#ご入力を防ぐため2023年7月2日追記
from .models import TemporaryNursery
#customユーザー作成のため
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
#お問い合わせフォーム作成
from .models import Contact

#数字のみのバリデーションエラーのため追記2023年8月9日
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
#バリデーションエラーのため
from django.db import IntegrityError

class NurserySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        user = self.context['request'].user
        if self.instance is None and Nursery.objects.filter(user=user).exists():
            # ユーザーは既に保育園情報を作成済みの場合にエラーメッセージを設定
            raise serializers.ValidationError("ユーザーは既に保育園情報を作成済みです。")
        return attrs

    class Meta:
        model = Nursery
        fields = ['nursery_number', 'key_field', 'name', 'user', 'type', 'feature', 'feature_image', 'feature_image2', 'description', 'future', 'experience', 'experience_image', 'experience_image2', 'phone_number', 'email', 'address', 'capacity_0', 'capacity_1', 'capacity_2', 'capacity_3', 'capacity_4', 'capacity_5', 'open_hours', 'extension_time', 'holidays', 'url', 'image', 'image2', 'created_at', 'updated_at', 'playground']
        extra_kwargs = {
            'name': {
                'error_messages':{
                    'blank': '保育園名は空にできません。'
                }
            }
        }
            
#ユーザー登録機能登録のため追記2023年6月3日customuserに変更7月6日
#class UserSerializer(serializers.ModelSerializer):
#    password = serializers.CharField(write_only=True)

#    class Meta:
#        model = User
#        fields = ( 'username', 'password', 'email')

#    def create(self, validated_data):
#        password = validated_data.pop('password')
#        user = User(**validated_data)
#        user.set_password(password)
#        user.save()
#        return user
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        errors = {}

        # ユーザー名の重複チェック
        if User.objects.filter(username=username).exists():
            if 'username' not in errors:
                errors['username'] = []
            errors['username'].append('ユーザー名は既に使用されています。別のユーザー名を選択してください.')

        # Emailの重複チェック
        if User.objects.filter(email=email).exists():
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append('メールアドレスは既に使用されています。別のメールアドレスを入力してください.')

        # パスワードが8文字未満の場合のエラーチェック
        if len(password) < 8:
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('パスワードは8文字以上で入力してください.')

        # ユーザー名の正規表現チェック
        regex = r'^[\w.@+-]+$'
        if not re.match(regex, username):
            if 'username' not in errors:
                errors['username'] = []
            errors['username'].append('ユーザー名は英数字と @/./+/-/_ の記号のみ使用できます.')
        # Djangoのデフォルトのバリデーションを適用
        try:
            validate_password(password)
        except ValidationError as e:
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].extend(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

#ここまで

#ログイン認証のため追記2023年6月7日
class LoginSerializer(serializers.Serializer):
    """ログインAPI用のシリアライザ"""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if user is None or not user.is_active:
                raise serializers.ValidationError("ログインが失敗しました")
            data['user'] = user
        return data
#ここまで

#ご入力を防ぐため
class TemporaryNurserySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryNursery
        fields = '__all__'

#問い合わせフォーム
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')