from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),
    path('view/', views.cart_view, name='cart_view'),
    path('add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
