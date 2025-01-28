from django.db import models
from django.contrib.auth import get_user_model

class Content(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    age_rating = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("TV Show", "TV Show")])
    duration = models.CharField(max_length=20, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    trailer_url = models.URLField(null=True, blank=True)
    stream_url = models.URLField(null=True, blank=True)
    genres = models.JSONField(default=list)
    cast = models.JSONField(default=list)
    seasons = models.PositiveIntegerField(null=True, blank=True)
    episodes = models.PositiveIntegerField(null=True, blank=True)

class Review(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="reviews")
    user = models.CharField(max_length=255)
    rating = models.FloatField()
    comment = models.TextField()

class Episode(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="episodes")
    season = models.PositiveIntegerField()
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=20)

User = get_user_model()

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='views')
    watched_duration = models.IntegerField(default=0)  # Duration watched in seconds
    last_watched = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-last_watched']