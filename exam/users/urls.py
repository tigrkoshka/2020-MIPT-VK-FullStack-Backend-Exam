from django.urls import path
from .views import create_user, user_list, user_info

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('user_list/', user_list, name='user_list'),
    path('user_info/', user_info, name='user_info'),
]