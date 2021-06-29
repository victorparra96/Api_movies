# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
# from movies import views
from .views import movies as movies_views

router = DefaultRouter()
router.register(r'movies', movies_views.MoviesViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls))
]