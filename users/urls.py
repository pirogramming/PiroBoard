from django.urls import path
from . import views

urlpatterns = [
    path('/users/<int:id>?query=kor')
]
