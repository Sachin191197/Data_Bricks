from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.serializers import UserSerializer, CountrySerializer, CitySerializer, ForecastQuerySerializer
from user import models as UserModels
from user import utils as UserUtils


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "successfully signup"}, status=201)
        return Response(serializer.errors, status=400)


class CountryView(APIView):
    def get(self, request):
        countries = UserModels.Country.objects.values("id", "name")
        serializer = CountrySerializer(countries, many=True)
        return Response(data=serializer.data, status=200)


class CityView(APIView):
    def get(self, request, country_id):
        cities = UserModels.City.objects.filter(country_id=country_id).values("id", "name")
        serializer = CitySerializer(cities, many=True)
        return Response(data=serializer.data, status=200)


class ForcastView(APIView):
    def get(self, request):
        serializer = ForecastQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        days = serializer.validated_data.get('days')
        city = UserModels.City.objects.get(pk=serializer.validated_data.get('city_id'))
        forecast_data = UserUtils.fetch_forcast(
            city=city.name,
            days=days
        )
        forecasts = UserUtils.normalize_forecast_details(forecast_data["forecast"])
        UserUtils.create_user_forecast_query(
            city_id=serializer.validated_data.get('city_id'),
            user_id=serializer.validated_data.get('user_id'),
        )
        return Response(data={"forecasts": forecasts}, status=200)


class AnalyticsApi(APIView):
    def get(self, request, n):
        top_user_json, top_city_json = [], []
        query_logs = UserModels.UserQueryLog.objects.annotate(
            user_count=Count('user_id')
        ).order_by('-user_count')[:-1 * n]
        for query_log in query_logs:
            user = UserModels.User.objects.pk(id=query_log.user_id)
            top_user_json.append({
                "user": UserSerializer(user, many=False),
                "count": query_log.user_count
            })

        query_logs = UserModels.UserQueryLog.objects.annotate(
            city_count=Count('city_id')
        ).order_by('-city_count')[:-1 * n]
        for query_log in query_logs:
            city = UserModels.City.objects.pk(id=query_log.city_id)
            top_city_json.append({
                "user": CitySerializer(city, many=False),
                "count": query_log.user_count
            })

        return Response(data={
            "top_user_json": top_user_json,
            "top_city_json": top_city_json
        }, status=200)


