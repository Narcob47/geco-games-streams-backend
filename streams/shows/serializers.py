from rest_framework import serializers
from .models import Series, Episode

class EpisodeSerializer(serializers.ModelSerializer):
    stream_url = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Episode
        fields = ['id', 'series', 'episode_number', 'title', 'description', 'duration', 'stream_url']

    def get_stream_url(self, obj):
        # Generate the signed URL dynamically
        return obj.generate_signed_url()  # Assuming `generate_signed_url` is a method in the `Episode` model

class SeriesSerializer(serializers.ModelSerializer):
    stream_url = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Series
        fields = [
            'id', 'title', 'descriptions', 'age_rating', 'category', 'duration',
            'likes', 'dislikes', 'genres', 'stream_url'  # Include stream_url here
        ]

    def get_stream_url(self, obj):
        # Generate the signed URL dynamically
        return obj.generate_signed_url()  # Assuming `generate_signed_url` is a method in the `Series` model