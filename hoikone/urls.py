from django.urls import path, include
from rest_framework import routers

from . import views
#ユーザー登録機能登録のため追記2023年6月3日,#2023年6月4日追記ユーザー紐づけのため
from .views import UserViewSet, NurseryViewSet, UserDetailView
#ここまで
#キャッシュの無効化
from django.views.decorators.cache import cache_page


router = routers.DefaultRouter()
router.register('nursery', views.NurseryViewSet)
router.register('users', UserViewSet)

app_name = 'hoikone'

urlpatterns = [
    path('', include(router.urls)),
    path('', views.index, name='index'),
    path('login/', views.httplogin, name='login'),
    #ログインのため追記2023年6月8日追記
    path('login_user/', views.LoginView.as_view(), name='login_user'),
    path('signup/', views.signup, name='signup'),
    path('user-add-1/', views.user_add_1, name='user-add-1'),
    #ユーザー登録機能登録のため追記2023年6月3日
    #path('users/register/', views.UserViewSet.as_view({'post': 'create'}), name='register'),
    #2023年6月4日追記ユーザー紐づけのため
    path('nurseries/', views.NurseryViewSet.as_view({'post': 'create'}), name='create_nursery'),
    path('nurseries/<uuid:key_field>/', NurseryViewSet.as_view({'get': 'retrieve'}), name='retrieve_nursery'),
    #ここまで
    #検索ページ追加2023年6月10日
    path('nursery-list/', NurseryViewSet.as_view({'get': 'list'}), name='nursery-list'),
    #詳細ページ追加2023年6月18日
    path('nursery-info/<int:pk>/', NurseryViewSet.as_view({'get': 'retrieve'}), name='nursery-info'),
    #更新ページ追加2023年6月24日
    path('change/', NurseryViewSet.as_view({'get': 'change', 'post': 'change'}), name='change'),

]