from abc import ABC

from rest_framework import serializers
from user import models as UserModels


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels.User
        fields = ('username', 'email', 'password')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels.Country
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels.City
        fields = ('id', 'name')


class ForecastQuerySerializer(serializers.Serializer, ABC):
    city = serializers.IntegerField()
    days = serializers.IntegerField()
    user_id = serializers.IntegerField()
