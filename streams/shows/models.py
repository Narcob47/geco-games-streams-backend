from django.db import models
from django.utils import timezone
from google.cloud import storage
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage

gcs_storage = GoogleCloudStorage()

class Series(models.Model):
    title = models.CharField(max_length=255)
    # trailer_url = models.URLField(null=True, blank=True)
    descriptions = models.TextField()
    age_rating = models.CharField(max_length=10)
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("TV Show", "TV Show")])
    stream_file = models.FileField(upload_to='series/', storage=gcs_storage, null=True, blank=True)
    genres = models.CharField(max_length=50)
    cast = models.CharField(max_length=50)
    seasons = models.PositiveIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=20)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def generate_signed_url(self, expiration_time=3600):
        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_PROJECT_ID)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'series/{self.stream_file.name}')
        signed_url = blob.generate_signed_url(expiration=expiration_time)
        return signed_url

    def __str__(self):
        return self.title

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes', on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=20)
    stream_file = models.FileField(upload_to='episodes/', storage=gcs_storage, null=True, blank=True)

    def generate_signed_url(self, expiration_time=3600):
        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_PROJECT_ID)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'episodes/{self.stream_file.name}')
        signed_url = blob.generate_signed_url(expiration=expiration_time)
        return signed_url

    def __str__(self):
        return f'{self.title} (Episode {self.episode_number})'