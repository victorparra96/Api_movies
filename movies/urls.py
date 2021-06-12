# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from movies import views

router = DefaultRouter()
router.register(r'movies', views.MoviesViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls))
]