from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path('group_find/', views.group_find , name='group_find'),

]
