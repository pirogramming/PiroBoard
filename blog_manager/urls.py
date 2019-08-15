from django.urls import path
from blog import views as blogviews
from . import views

urlpatterns = [
    path('', views.group_manage, name='group_manage')
    ]