from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

import product.views
import category.views


class CustomRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = super().get_redirect_url(*args, **kwargs)
        return url

    def post(self, request, *args, **kwargs):
        self.url = self.get_redirect_url(*args, **kwargs)
        return HttpResponseRedirect(self.url, status=307)  # 使用307保持POST请求


def login_to_user_redirect(request, subpath=None):
    # 构建新的 URL
    target_url = f'/user/{subpath}' if subpath else '/user/'

    # 获取查询参数并附加到目标 URL
    query_string = request.META.get('QUERY_STRING', '')
    if query_string:
        target_url += f'?{query_string}' if '?' not in target_url else f'&{query_string}'

    # 保留 POST 请求的数据
    if request.method == 'POST':
        return HttpResponseRedirect(target_url, status=307)
    else:
        return redirect(target_url)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/category/head', category.views.get_response_data, name='category'),

    path('home/new', category.views.get_new_books, name='new_books'),
    path('home/banner', product.views.banner_view, name='banner'),

    # 获取商品库存
    re_path(r'^goods/stock/(?P<id>\d+)$', RedirectView.as_view(url='/product/stock/%(id)s', query_string=True)),
    # 匹配 /goods?id=1 的格式，重定向到 /products/?id=1，查询商品详情
    re_path(r'^goods$', RedirectView.as_view(url='/product/', query_string=True)),

    path('home/brand', RedirectView.as_view(url='/product/brand', query_string=True)),
    path('product/', include('product.urls')),

    re_path(r'^login(?:/(.*))?$', login_to_user_redirect),
    path('user/', include('user.urls')),

    # path('login', CustomRedirectView.as_view(url='/user/', query_string=True)),
    # path('user/', include('user.urls')),

    # 购物车
    path('member/cart', include('cart.urls')),

    path('member/', include('user.urls')),

    path('member/order', include('order.urls')),


    path('category',include('category.urls'),name='category'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)