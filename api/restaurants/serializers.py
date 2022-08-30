from rest_framework import serializers
from restaurants.models import Restaurant, LANGUAGE_CHOICES, STYLE_CHOICES


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']