# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
# from movies import views
from .views import movies as movies_views
from .views import rankings as ranking_views
from .views import list_movies as list_movies_views

router = DefaultRouter()
router.register(r'movies', movies_views.MoviesViewSet, basename='movies')
router.register(
    r'movies/(?P<slug_name>[a-zA-Z0-9_-]+)/rankings',
    ranking_views.RankingViewSet,
    basename='rankings'
)
router.register(
    r'movies/(?P<slug_name>[a-zA-Z0-9_-]+)/list_movies',
    list_movies_views.ListMovieViewSet,
    basename='list_movies'
)

urlpatterns = [
    path('', include(router.urls))
]