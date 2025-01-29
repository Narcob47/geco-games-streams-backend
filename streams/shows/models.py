from django.db import models
from django.contrib.auth import get_user_model
from storages.backends.gcloud import GoogleCloudStorage

# Use GCS as the default storage backend
gcs_storage = GoogleCloudStorage()

class Series(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    age_rating = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("TV Show", "TV Show")])
    duration = models.CharField(max_length=20, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    trailer_url = models.URLField(null=True, blank=True)
    stream_file = models.FileField(upload_to='series/', storage=gcs_storage, null=True, blank=True)
    genres = models.CharField(max_length=50)
    cast = models.CharField(max_length=50)
    seasons = models.PositiveIntegerField(null=True, blank=True)
    
    def generate_signed_url(self):
        # Replace this with your logic to generate a signed URL
        return f"gs://wach-1/series/V1.mp4/{self.id}"  # Example URL

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes', on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=20)
    stream_file = models.FileField(upload_to='episodes/', storage=gcs_storage, null=True, blank=True)  # Store video file in GCS