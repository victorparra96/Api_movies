from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('movies.urls', 'movies'), namespace='movies')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)