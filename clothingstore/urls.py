from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

from . import views

app_name = 'clothingstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('store/<slug:stock_keeping_unit>/', views.add_to_cart,
         name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

    # Auth
    path('login/',
         auth_views.LoginView.as_view(
             template_name='clothingstore/login.html',
             next_page=reverse_lazy('clothingstore:index')),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(
             template_name='clothingstore/logout.html'),
         name='logout'),
]
