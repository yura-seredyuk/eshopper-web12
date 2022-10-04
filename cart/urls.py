from . import views
from django.urls import path, include


urlpatterns = [
    path('cart/', views.shop_cart, name='shop_cart')
]