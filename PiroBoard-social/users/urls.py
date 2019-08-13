from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


app_name = "users"

urlpatterns = [
    path('', user_views.profile, name='profile'),
    path('update/', user_views.profile_update, name='profile_update'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
