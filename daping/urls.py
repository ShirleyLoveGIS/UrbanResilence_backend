"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path

from . import views

urlpatterns = [
    path('ranking_list', views.rank_list, name='ranking_list'),
    path('month_countall', views.month_countall, name='month_countall'),
    path('month_countavgm', views.month_countavgm, name='month_countavgm'),
    path('month_countavgy', views.month_countavgy, name='month_countavgy'),
    path('month_countly', views.month_countly, name='month_countly'),
    path('region_count', views.region_count, name='region_count'),
    path('events_reason', views.events_reason, name='events_reason'),
    path('month_count', views.month_count, name='month_count'),
    path('getmonth', views.getmonth, name='getmonth'),
    path('region_dengjiange', views.region_dengjiange, name='region_dengjiange')
]