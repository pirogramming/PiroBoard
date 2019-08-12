from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('about/', views.about, name='blog-about'),
]
