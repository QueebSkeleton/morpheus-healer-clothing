from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'clothingstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
