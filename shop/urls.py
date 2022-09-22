from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('shop/', views.shop_page, name='shop_page'),
    path('product/<int:pk>', views.product_detail_page, name='detail_page')
]