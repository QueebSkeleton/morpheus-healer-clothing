from django.urls import path

from . import views

app_name = 'clothingstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('store/<slug:stock_keeping_unit>/', views.add_to_cart,
         name='add_to_cart'),
]
