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
    path("booking/<int:property_id>/<int:user_id>/", views.booking, name="booking"),
    path("rent/<int:property_id>/<int:user_id>/", views.rent_property, name="rent"),
    path('map/<int:property_id>/', views.view_on_map, name='map'), 
    path('<int:property_id>/vr/', views.property_vr_view, name='property_vr_view'),
    path('profile/', views.profile_view, name='profile'),
    path('post-property/', views.post_property, name='post_property'),
    path('explore/', views.property_explore, name='property_explore'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
