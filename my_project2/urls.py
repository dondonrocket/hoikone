"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings #2023年5月5日追記static設定のため
from django.conf.urls.static import static #2023年5月5日追記static設定のため

from django.views.generic import TemplateView

from hoikone.views import UserViewSet, user_add_1, ContactCreateView 
#2023年6月3日ユーザー登録のため、2023年7月10日問い合わせフォーム追記

from rest_framework.urls import * #2023年6月7日ログイン状態保持のため

from django.contrib.auth import views as auth_views #パスワード差一定のため2023年7月2日
#from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from hoikone import views

from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticViewSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('hoikone-auth/', include('rest_framework.urls')),
    #パスワードリセットからのログインのためinclude追記
    path('hoikone/v1/', include('hoikone.urls')),
    path('users/register/', UserViewSet.as_view({'post': 'register', 'get': 'register'}), name='register'),
    #path('user-add-1/', user_add_1, name='user-add-1'),
    #パスワードリセット
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #問い合わせフォーム
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    #パスワード変更
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    #ユーザー情報、保育園情報消去のため2023年7月12日
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('google205e2704f12a467c.html/', views.google, name='google'),
]

#2023年5月5日追記static設定のため
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 開発環境でのみメディアファイルを提供する
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

