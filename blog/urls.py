from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='blog-home'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/<int:pk>/head/', include('blog_manager.urls')),
    path('about/', views.about, name='blog-about'),     # 그룹생성
    path('group/<int:pk>/post_new/', views.post_new, name='post_new'),
    path('detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
]