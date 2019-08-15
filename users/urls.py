from django.urls import path

from . import views


app_name = "users"

urlpatterns = [

    path('password/', views.change_password, name='change_password'),
    path('password_reset_form/', views.password_reset_form, name='password_reset_form'),

]
