from . import views

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from django.contrib.admin import site as admin_site

app_name = 'clothingstore'
urlpatterns = [
    # Index page
    path('',
         views.index,
         name='index'),
    # Main Store pages
    path('store/',
         views.store,
         name='store'),
    path('store/<slug:category_slug>/',
         views.store,
         name='store'),

    # Cart pages
    path('cart/',
         views.cart,
         name='cart'),
    path('cart/<slug:product_stock_keeping_unit>/add/',
         views.add_to_cart,
         name='add_to_cart'),
    path('cart/<slug:product_stock_keeping_unit>/remove/',
         views.remove_from_cart,
         name='remove_from_cart'),
    path('cart/remove-everything/',
         views.remove_all_from_cart,
         name='remove_everything_from_cart'),

    # Checkout pages
    path('checkout/',
         views.checkout,
         name='checkout'),
    path('thank-you/',
         views.thank_you,
         name='thank_you'),

    # Auth
    path('login/',
         auth_views.LoginView.as_view(
             template_name='clothingstore/login.html',
             next_page=reverse_lazy('clothingstore:index')),
         name='login'),
    path('profile/',
         views.profile_change,
         name='profile_change'),
    path('profile/orders/',
         views.order_history,
         name='order_history'),
    path('profile/orders/<int:order_id>/',
         views.order_details,
         name='order_details'),
    path('profile/orders/<int:order_id>/invoice/',
         views.invoice,
         name='invoice'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='clothingstore/logout.html'),
         name='logout'),

    # Charts
    path('charts/sales-last2weeks/',
         views.sales_last2weeks_chartjs,
         name='sales_last2weeks'),
]

admin_site.site_header = 'Morpheus Healer Clothing Store'
admin_site.index_title = 'Dashboard'
