from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.profile, name='profile'),
    path('remove_order', views.remove_order_button, name='remove_order'),
    path('order_change', views.order_change_button, name='order_change'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('order_status_edit', views.order_status_edit, name='order_status_edit'),
    path('get_customer', views.get_customer, name='get_customer'),
]