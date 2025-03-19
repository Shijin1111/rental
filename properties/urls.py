from django.urls import path
from properties import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "properties"

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('property_detail/<int:property_id>/', views.property_detail, name='property_detail'),
    path('chat/<int:property_id>/<int:receiver_id>/', views.chat_view, name="chat_view"),
    path('owner_chat/', views.owner_chat, name="owner_chat"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
