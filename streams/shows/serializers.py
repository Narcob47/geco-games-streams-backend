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
    # reviews = ReviewSerializer(many=True, read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = [
            'id', 'title', 'descriptions', 'age_rating', 'category', 'duration', 
            'likes', 'dislikes', 'trailer_url', 'stream_url', 'genres', 'cast', 
            'seasons', 'episodes', 'reviews'
        ]
