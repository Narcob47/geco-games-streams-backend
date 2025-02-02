from django.db import models
from django.utils import timezone
from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from azure.storage.blob import BlobServiceClient
import datetime

azure_storage = AzureStorage()

class Series(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    age_rating = models.CharField(max_length=10)
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("TV Show", "TV Show")])
    stream_file = models.FileField(upload_to="series/", storage=azure_storage, null=True, blank=True)
    genres = models.CharField(max_length=50)
    cast = models.CharField(max_length=50)
    seasons = models.PositiveIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=20)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def generate_signed_url(self, expiration_time=3600):
        """Generate a signed URL for accessing the video file."""
        blob_service_client = BlobServiceClient(
            account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=settings.AZURE_ACCOUNT_KEY
        )
        blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=f"series/{self.stream_file.name}")

        sas_token = blob_client.generate_blob_sas(
            account_name=settings.AZURE_ACCOUNT_NAME,
            container_name=settings.AZURE_CONTAINER,
            blob_name=f"series/{self.stream_file.name}",
            permission="r",  # Read permission
            expiry=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
        )
        
        return f"{blob_client.url}?{sas_token}"

    def log_play_event(self):
        """Log when the video is played."""
        print(f"Video {self.title} is being played at {timezone.now()}")

    def __str__(self):
        return self.title


class Episode(models.Model):
    series = models.ForeignKey(Series, related_name="episodes", on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=20)
    stream_file = models.FileField(upload_to="episodes/", storage=azure_storage, null=True, blank=True)

    def generate_signed_url(self, expiration_time=3600):
        """Generate a signed URL for accessing the episode file."""
        blob_service_client = BlobServiceClient(
            account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=settings.AZURE_ACCOUNT_KEY
        )
        blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=f"episodes/{self.stream_file.name}")

        sas_token = blob_client.generate_blob_sas(
            account_name=settings.AZURE_ACCOUNT_NAME,
            container_name=settings.AZURE_CONTAINER,
            blob_name=f"episodes/{self.stream_file.name}",
            permission="r",
            expiry=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
        )

        return f"{blob_client.url}?{sas_token}"

    def __str__(self):
        return f"{self.title} (Episode {self.episode_number})"