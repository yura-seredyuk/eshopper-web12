from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.shop_cart, name='shop_cart'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('add/<product_id>', views.cart_add, name='cart_add'),
    path('clear/', views.cart_clear, name='cart_clear')
]