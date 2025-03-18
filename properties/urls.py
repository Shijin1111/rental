from django.urls import path
from properties import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('detail/<int:property_id>/', views.property_detail, name='property_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
