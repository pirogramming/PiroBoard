from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_manage, name='group_manage'),
    path('info_update/', views.group_info_update, name='group_info_update'),
    path('manage_member/', views.group_member_manage, name='group_member_manage'),
    path('invite_member/', views.invite_member, name='invite_member'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
]
