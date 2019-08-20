from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_manage, name='group_manage'),
    path('info_update/', views.group_info_update, name='group_info_update'),
    path('manage_member/', views.group_member_manage, name='group_member_manage'),
    path('byebye_manager/', views.byebye_manager, name='byebye_manager'),
    path('welcome_manager/', views.welcome_manager, name='welcome_manager'),
    path('baton/', views.baton_touch, name='baton_touch'),
    path('refuse/', views.user_request_refuse, name='user_request_refuse'), # 차단

    path('manage_member/chadan_member/', views.chadan_member_manage, name='chadan_member_manage'),
    path('manage_member/chadan_member/unblock/', views.unblock, name='unblock'),

    path('invite_member/', views.invite_member_page, name='invite_member_page'),
    path('invite/', views.invite, name='invite'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),

    path('request_accept/', views.user_request_accept, name='user_request_accept'),
    path('request_delete/', views.request_refuse, name='group_request_delete'), # 삭제
]
