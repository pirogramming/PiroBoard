from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_manage, name='group_manage'),
    path('info_update/', views.group_info_update, name='group_info_update'),
    path('manage_member/', views.group_member_manage, name='group_member_manage'),
    path('baton/', views.baton_touch, name='baton_touch'),
    path('refuse/', views.refuse, name='refuse'),

    path('invite_member/', views.invite_member_page, name='invite_member_page'),
    path('invite/', views.invite, name='invite'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),

    path('request_accept/', views.user_request_accept, name='user_request_accept'),
    path('request_cancel/', views.group_request_cancel, name='group_request_cancel'),
]
