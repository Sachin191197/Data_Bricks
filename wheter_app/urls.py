"""
URL configuration for wheter_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as UserViews

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/signup", UserViews.UserView.as_view(), name='user/signup'),
    path("api/country", UserViews.CountryView.as_view(), name="List Country"),
    path("api/country/<int:country_id>/cities/", UserViews.CityView.as_view(), name="list cities"),
    path("api/forcast/", UserViews.ForcastView.as_view(), name="forecast details"),
    path("api/<int: n>/analytics/", UserViews.AnalyticsApi.as_view(), name="list analytics"),
]
