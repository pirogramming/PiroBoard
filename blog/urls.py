from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('about/', views.about, name='blog-about'),
    path('post_new/', views.post_new, name='post_new'),
    path('detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
]


