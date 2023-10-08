from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# 静的クラスサイトマップを定義。パラメータは動的クラスのものと同じ。
class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
       # [ ]の左側は urls.py (setting.py側) のnamespace、右側は urls.py(アプリ側)のnameを設定する。
        return ['register',
                'privacypolicy', 
                'hoikone:user-add-1', 
                'contact-create', 
                'password_change',# パスワード変更ページ
                'password_change_done',  # パスワード変更完了ページ
                'email_change',  # メールアドレス変更ページ
                'email_change_done',  # メールアドレス変更完了ページ
                'hoikone:index',
                'hoikone:login',
                'hoikone:signup',
                'hoikone:change',
        ]
    
    def location(self, item):
        return reverse(item)