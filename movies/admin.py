# Django
from django.contrib import admin

# Models
from movies.models import Movies


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