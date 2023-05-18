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
    path('rank_list', views.rank_list, name='rank_list'),
    path('month_countall', views.month_countall, name='month_countall'),
    path('region_count', views.region_count, name='region_count'),
    path('events_reason', views.events_reason, name='events_reason'),
    path('month_countavgm', views.month_countavgm, name='month_countavgm'),
    path('month_countavgy', views.month_countavgy, name='month_countavgy')
]