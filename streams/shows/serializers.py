from rest_framework import serializers
from .models import Series, Episode

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'rating', 'comment']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'season', 'episode_number', 'title', 'description', 'duration']

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