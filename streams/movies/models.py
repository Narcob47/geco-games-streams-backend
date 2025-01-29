from django.db import models
from django.utils import timezone
from google.cloud import storage
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage

gcs_storage = GoogleCloudStorage()

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_rating = models.CharField(max_length=10)
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("TV Show", "TV Show")])
    duration = models.CharField(max_length=20, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    genre = models.CharField(max_length=50)
    release_date = models.DateField(default=timezone.now)
    movie_upload = models.FileField(upload_to='movies/', storage=gcs_storage, null=True, blank=True)
    image = models.ImageField(upload_to='movies/images/', null=True, blank=True)

    def generate_signed_url(self, expiration_time=3600):
        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_PROJECT_ID)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'movies/{self.movie_upload.name}')

        signed_url = blob.generate_signed_url(expiration=expiration_time)
        return signed_url

    def generate_upload_signed_url(self, expiration_time=3600):
        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_PROJECT_ID)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'movies/{self.movie_upload.name}')

        upload_signed_url = blob.generate_signed_url(
            expiration=expiration_time,
            method='PUT',
            content_type='application/octet-stream'
        )
        return upload_signed_url

    def __str__(self):
        return self.title
