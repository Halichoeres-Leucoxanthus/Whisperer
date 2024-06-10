"""
URL configuration for Whisperer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from userprofile.views import *
from chat.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    path('check-login/', check_login, name='check_login'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('get-available-users/', get_available_users, name='get_available_users'),

    # Profiles URLs
    path('profile/', UserProfileListCreateView.as_view(), name='userprofile-list-create'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/<int:pk>/', UserProfileRetrieveUpdateDestroyView.as_view(),
         name='userprofile-retrieve-update-destroy'),


    # Chatroom URLs
    path('chatroom/<int:chatroom_id>/', chatroom, name='chatroom'),
    path('send_message/<int:chatroom_id>/', send_message, name='send_message'),
    path('delete_chatroom/<int:chatroom_id>/', delete_chatroom, name='delete_chatroom'),
    path('create_chatroom/', create_chatroom, name='create_chatroom'),
    path('chatroom_list/', chatroom_list, name='chatroom_list'),
    # Chat URLs
    path('send_message/<int:chatroom_id>/', send_message, name='send_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
