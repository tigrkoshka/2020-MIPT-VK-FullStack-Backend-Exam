from django.contrib import admin
from django.urls import path

from groups import views

urlpatterns = [
    path('create_group/', views.create_group),
    path('join_group/', views.join_group),
    path('leave_group/', views.leave_group),
    path('group_list/', views.group_list),
]
