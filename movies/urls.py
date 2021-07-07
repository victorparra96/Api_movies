# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
# from movies import views
from .views import movies as movies_views
from .views import rankings as ranking_views
from .views import list_movies as list_movies_views
from .views import comment as comment_views
from .views import like as like_views

router = DefaultRouter()
router.register(r'movies', movies_views.MoviesViewSet, basename='movies')
router.register(
    r'movies/(?P<slug_name>[a-zA-Z0-9_-]+)/rankings',
    ranking_views.RankingViewSet,
    basename='rankings'
)
router.register(r'list_movies', list_movies_views.ListMovieViewSet, basename='list_movies')
router.register(
    r'movies/(?P<slug_name>[a-zA-Z0-9_-]+)/comment',
    comment_views.CommentViewSet,
    basename='comment'
)
router.register(
    r'comment/(?P<slug_name>[a-zA-Z0-9_-]+)/like',
    like_views.LikeViewSet,
    basename='like'
)

urlpatterns = [
    path('', include(router.urls))
]