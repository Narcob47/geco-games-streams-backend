from django.contrib import admin
from .models import Series, Episode

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'seasons')
    search_fields = ('title',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('series', 'episode_number', 'title')
    search_fields = ('series__title', 'title')
