from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name='profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('auth/', views.user_auth, name='auth'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('update-user', views.updateUser, name='update-user'),
    path('likes', views.likes, name='likes'),
    path('unlikes', views.unlikes, name='unlikes'),
] 


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)