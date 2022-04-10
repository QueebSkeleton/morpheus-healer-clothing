from django.urls import path

from . import views

app_name = 'clothingstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
]
