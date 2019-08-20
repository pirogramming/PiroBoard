from django.urls import path
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


app_name = "users"

urlpatterns = [

    path('password/', views.change_password, name='change_password'),
    path('password_reset_form/', views.password_reset_form, name='password_reset_form'),
    path('group_find/', views.group_find, name='group_find'),
    path('requests_manage/', views.requests_manage, name='group_manage'),
    path('', views.profile, name='profile'),
    path('update/', views.profile_update, name='profile_update'),
    path('request_cancel/', views.request_cancel, name='request_cancel'),
    path('request_accept/', views.request_accept, name='request_accept'),


]
