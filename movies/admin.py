# Django
from django.contrib import admin

# Models
from movies.models import Movies
from movies.models.rankings import Ranking
from movies.models.list_movies import List_movie
from movies.models.comments import Comment
from movies.models.like import Like


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    """Movies admin."""

    list_display = ('pk', 'name', 'gender',)
    list_display_links = ('pk', 'name', 'gender',)

    search_fields = (
        'gender',
        'production',
        'duration',
        'author',
    )

    list_filter = (
        'date_launch',
    )

    readonly_fields = ('date_launch',)

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    """Ranking admin."""

@admin.register(List_movie)
class ListMovieAdmin(admin.ModelAdmin):
    """List_movie admin."""

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin."""

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Like admin."""
