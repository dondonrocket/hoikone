from multiprocessing import context
from rest_framework import generics, views
from rest_framework.filters import SearchFilter
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from .models import Nursery, TemporaryNursery

from .serializers import NurserySerializer

from django.shortcuts import render
from django.template import loader

#ユーザー登録機能登録のため追記2023年6月3日
#from django.contrib.auth.models import User
#from .serializers import UserSerializer
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
#7月4日追記
from rest_framework.exceptions import ValidationError
#ここまで

#ログイン認証のため追記2023年6月7日
from .serializers import LoginSerializer
#ここまで
#登録後のメッセージの追記2023年6月7日
from django.contrib import messages
#ここまで
#ページネーション組み込みのため追記2023年6月10日
from rest_framework.pagination import PageNumberPagination
from django.core import paginator
from django.core.paginator import Paginator
#ここまで
#検索機能追加のため追記2023年6月11日
from django.db.models import Q
#ここまで

from django.shortcuts import get_object_or_404, resolve_url
#住所をエンコードするため
from urllib.parse import quote
#登録後、email送信
from django.core.mail import EmailMessage
#一時保持用のモデルのシリアライザー
from .serializers import TemporaryNurserySerializer

from django.contrib.auth import views as auth_views

#パスワード再設定に使用
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .forms import NewPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
#from .models import CustomUser

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
)

from .forms import (
    MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm, EmailChangeForm
)
#問い合わせフォーム
from .models import Contact
from .serializers import ContactSerializer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps

from django.views import View

#古い画像の消去のため2023年7月15日
import os

CustomUser = get_user_model()

#python正規表現を使うため
import re

# Create your views here.

def index(request):        
    return render(request, 'index.html')

def httplogin(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def user_add_1(request):
    return render(request, 'user-add-1.html')

def nursery_list(request):
    return render(request, 'nursery-list.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def password_reset_invalid_token(request):
    return render(request, 'password_reset_invalid_token.html')

def google(request):
    return render(request, 'google205e2704f12a467c.html')

class NurseryViewSet(viewsets.ModelViewSet):
    queryset = Nursery.objects.all()
    serializer_class = NurserySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'feature', 'address']
#    pagination_class = PageNumberPagination()

    # 追加された部分
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        self.perform_create(serializer)
        feature_image = serializer.validated_data.get('feature_image')
        experience_image = serializer.validated_data.get('experience_image')
        image = serializer.validated_data.get('image')
        serializer.validated_data['feature_image2'] = feature_image
        serializer.validated_data['experience_image2'] = experience_image
        serializer.validated_data['image2'] = image

        # ログインしているユーザー名を取得し、それをNurseryインスタンスのuserフィールドに設定
        serializer.save(user=self.request.user)

        # 一時保存用のモデル情報を取得
        temporary_nursery = TemporaryNursery.objects.get(user=request.user)

        # 新規登録が完了したので、一時保存用のモデル情報を削除。
        temporary_nursery.delete()

        headers = self.get_success_headers(serializer.data)

        messages.success(request, '保育園情報の登録が完了しました。')

        #情報をクライアント側に返す必要がある時に使用　return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return redirect('/')

    # ここまで

    #検索機能、ページネーション追加2023年6月9日
    def list(self, request, *args, **kwargs):

        query = request.GET.get('query')
        queryset = self.queryset  # 初期化
        if query:
            keywords = query.split()  # キーワードをスペースで分割
            q_objects = Q()  # 空のQオブジェクトを作成

            for keyword in keywords:
                q_objects &= Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(feature__icontains=keyword)

            queryset = self.queryset.filter(q_objects)

            request.session['search_query'] = query

        else:
            query = request.session.get('search_query')
            if query:
                keywords = query.split()
                q_objects = Q()

                for keyword in keywords:
                    q_objects &= Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(feature__icontains=keyword)

                queryset = self.queryset.filter(q_objects)
            else:
                queryset = self.queryset
                request.session.pop('search_query', None)
        if not queryset.exists():  # クエリセットにデータが存在しない場合の処理
            context = {
                'count': '0'
            }
            return render(request, 'nursery-list.html', context)
#        pagination_class = PageNumberPagination()
        paginator = Paginator(queryset, 6)
        page_number = request.GET.get('page')
        NurseryDatafinal = paginator.get_page(page_number)
        totalpage=NurseryDatafinal.paginator.num_pages

        paginated_queryset = self.paginate_queryset(queryset.order_by('name'))



        serializer = NurserySerializer(paginated_queryset, many=True)

        # シリアライザーのデータとページネーションの情報をテンプレートに渡す
        context = {
            'search': serializer.data,
            'result_count': len(queryset),
            'pagination': NurseryDatafinal,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'current_page_number':page_number,
        }

        return render(request, 'nursery-list.html', context)


    #詳細情報2023年6月18日
    def retrieve(self, request, *args, **kwargs):

        nursery_number = self.kwargs.get('pk')  # nursery_numberを取得する

        # nursery_numberを使用してオブジェクトを取得する
        instance = get_object_or_404(Nursery, nursery_number=nursery_number)

        serializer = NurserySerializer(instance)  # NurserySerializerを適切にインスタンス化する
        # セッションから最初の検索条件を取得する

        query = request.session.get('search_query')
        if query:
            keywords = query.split()
            q_objects = Q()

            for keyword in keywords:
                q_objects &= Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(feature__icontains=keyword)

            other_nursery = self.queryset.filter(q_objects).exclude(key_field=instance.key_field)

            # other_nurseryをシリアライズする
            serializer_other_nursery = NurserySerializer(other_nursery, many=True)
            serialized_other_nursery = serializer_other_nursery.data
        else:
            serialized_other_nursery = []

        address = (serializer.data['address'])
        context = {
            'nursery': serializer.data,
            'address': address,
            'other_nursery': serialized_other_nursery
        }

        return render(request, 'nursery-info.html', context)


    #更新処理のため2023年6月26日
    def change(self, request, *args, **kwargs):
        # ログインしているユーザーに関連付けられたNursery情報を取得
        user = request.user
        try:            
            temporary_nursery = TemporaryNursery.objects.get(user=request.user)
            return redirect('user-add-1')
        except TemporaryNursery.DoesNotExist:

            nursery = get_object_or_404(Nursery, user=user)

            if request.method == 'GET':
                # テンプレートにNursery情報を送る
                serializer = NurserySerializer(nursery)
                context = {'nursery': serializer.data}
                return render(request, 'change.html', context)
            elif request.method == 'POST':
                serializer = NurserySerializer(nursery, data=request.data, partial=True,  context={'request': request})
                if serializer.is_valid():
                        # フォームから送信された画像の値を受け取る
                    feature_image = serializer.validated_data.get('feature_image')
                    experience_image = serializer.validated_data.get('experience_image')
                    image = serializer.validated_data.get('image')
                    # 画像を他のフィールドに代入する
                    if not feature_image:
                        serializer.validated_data['feature_image'] = nursery.feature_image2
                    else:
                        serializer.validated_data['feature_image2'] = serializer.validated_data['feature_image']
                    if not experience_image:
                        serializer.validated_data['experience_image'] = nursery.experience_image2
                    else:
                        serializer.validated_data['experience_image2'] = serializer.validated_data['experience_image']
                    if not image:
                        serializer.validated_data['image'] = nursery.image2
                    else:
                        serializer.validated_data['image2'] = serializer.validated_data['image']

                    serializer.save()

                    messages.success(request, '更新が完了しました')
                    return redirect('/')
                else:
                    # バリデーションエラーがある場合はエラーメッセージを表示
                    context = {'nursery': serializer.data, 'errors': serializer.errors}
                    return render(request, 'change.html', context)


#ユーザー登録機能登録のため追記2023年6月3日
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def register(self, request, *args, **kwargs):

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            # カスタムバリデーションエラーを一元化するためのリスト
            errors = {}
            if not serializer.is_valid():
                field_errors = {}
                for field, field_error_list in serializer.errors.items():
                    field_errors[field] = field_error_list

                    username = request.data.get('username')
                    email = request.data.get('email')
                    password = request.data.get('password')
                # field_errors ディクショナリーには各フィールドのエラーリストが含まれる
                return render(request, 'signup.html', {'field_errors': field_errors, 'username': username, 'email': email, 'password': password})


            # カスタムバリデーションエラーがある場合、エラーレスポンスを返す
#                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            # カスタムバリデーションエラーがない場合、ユーザーを作成
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = serializer.save()

            # ユーザー名とパスワードでログインを試行
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # ログインに成功した場合、セッションにユーザー情報を保存
                login(request, user)
                #一時保存用の情報を保持。Nursery登録後消去
                temporary_nursery = TemporaryNursery(user=user)
                temporary_nursery.save()
                # メール送信
                subject = '【ユーザー登録完了のお知らせ】ホイコネ！'
                message = f'ご登録頂きましてありがとうございました！ユーザー登録が完了しましたのでご連絡申し上げます。\n\n●登録内容●\nユーザーID:{user.username}\nメールアドレス:{user.email}\n\n本メールにはパスワードの記載はありません。パスワードを忘れた方はログイン画面から、パスワードを設定することができます。\nご不明な点やご質問などがありましたら、下記までお気軽にお問い合わせ下さい。\n本メールにお心当たりのない方は、お手数ではございますが、下記のメールへの返信でお知らせください。\nホイコネ！\nhoikone1108@gmail.com'
                from_email = 'hoikone1108@gmail.com'  # 送信元メールアドレスを指定
                to_email = [user.email]  # ユーザーのメールアドレスを取得
                email = EmailMessage(subject, message, from_email, to_email)
                email.send()

                messages.success(request, 'ユーザー情報の登録が完了しました。登録したメールアドレスに登録完了のお知らせを送信しました。ご確認下さい。')

                            # ユーザー登録が成功した場合の処理
                return redirect('hoikone:user-add-1')

            # バリデーションエラーが発生した場合の処理
            return Response({'error': 'エラーが発生しました。もう一度ユーザーを登録して下さい。'}, status=status.HTTP_400_BAD_REQUEST)
            #return render(request,'register.html', {'errors':serializer.errors})
        else:
            # GETリクエストの場合、ユーザー登録ページを表示
            return render(request, 'signup.html')
        
    #削除のためユーザー情報を取得2023年7月13日
class UserDetailView(View):
    def get(self, request, username):
        instance = self.get_object(username)
        nursery_info = instance.nursery_set.filter(user__username=username)
        context = {
            'user': instance,
            'nursery_info': nursery_info,
        }
        return render(request, 'user_detail.html', context)

    def post(self, request, username):
        instance = self.get_object(username)
        # ユーザーと関連する保育園情報の削除処理
        instance.nursery_set.all().delete()
        # ユーザーの削除処理
        instance.delete()
        messages.success(request, 'ユーザーと関連する保育園情報を削除しました。ご利用ありがとうございました。')
        return redirect('/')

    def get_object(self, username):
        return get_object_or_404(CustomUser, username=username)

#ここまで


#ログイン認証のため追記2023年6月7日
class LoginView(generics.GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            error_message = "ログインが失敗しました。ユーザー名とパスワードを確認してもう一度ログインしてください。"
            return render(request, 'login.html', {'error_message': error_message})
       
        user = serializer.validated_data['user']

        login(request, user)

            # ユーザーモデルのemail_changeを確認してリダイレクト先を決定
        if user.email_change:
            user.email_change = False  # 変更完了後にリセット
            user.save()
            token = kwargs.get('token')
            return redirect('email_change_complete', token=user.email_change_token)

        return redirect('/')
            
#        return redirect('/')
class LogoutView(views.APIView):
    """ログアウトAPIクラス"""

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail':"ログアウトが成功しました。"})

#ここまで

#パスワード再設定のため2023年7月9日
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    template_name = 'registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #問い合わせ内容をメールで送信
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        message = serializer.validated_data['message']
        email_body = f"お名前：{name}\n\nメールアドレス：{email}\n\nお問い合わせ内容：{message}" 

        send_mail(subject='お問い合わせがありました', message=email_body, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list= ['hoikone1108@gmail.com'])
        # リダイレクトとメッセージの表示
        messages.success(request, 'お問い合わせありがとうございました。')  # メッセージの内容を適宜変更してください
        return redirect('/')  # トップページのURLに適切な値を指定してください
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return render(request, self.template_name, {'contacts': serializer.data})


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'registration/email_change.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # ユーザーモデルのemail_changeをTrueに設定
        user.email_change = True
        # トークンを生成
        token = dumps(new_email)
        # トークンを保持
        user.email_change_token = token
        user.save()

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': token,
            'user': user,
        }

        subject = render_to_string('registration/email_change/subject.txt', context)
        message = render_to_string('registration/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'registration/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'registration/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            CustomUser.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()

            # 状態とトークンをリセット
            request.user.email_change_token = ''
            request.user.email_change = False  # 状態をリセット
            request.user.save()

            return super().get(request,**kwargs)
        
