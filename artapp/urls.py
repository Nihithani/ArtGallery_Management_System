from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('Home/', views.home, name='home'),
    path('Login/', views.Login, name='Login'),
    path('Logout/', views.Logout, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register', views.register, name='register'),

    path('artapp/art/<slug:url>', views.theart, name='theart'),
    path('paintings/', views.Paintings, name='paintings'),

    path('all_artist/', views.Artistss, name='artists'),
    path('artist/<str:url>/', views.view_artist, name='view_artist'),
    
    path('about/', views.About),

    path('add_to_cart/<int:art_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('view_art/<str:url>/', views.view_art, name='view_art'),
    

]
