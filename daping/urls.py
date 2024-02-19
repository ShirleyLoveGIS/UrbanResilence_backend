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
    path('ranking_list2', views.rank_list2, name='ranking_list2'),
    path('ranking_list3', views.rank_list3, name='ranking_list3'),

    path('month_countall', views.month_countall, name='month_countall'),
    path('month_countavgm', views.month_countavgm, name='month_countavgm'),
    path('month_countavgy', views.month_countavgy, name='month_countavgy'),
    path('month_countly', views.month_countly, name='month_countly'),
    path('region_count', views.region_count, name='region_count'),
    path('region_count2', views.region_count2, name='region_count2'),

    path('events_reason', views.events_reason, name='events_reason'),
    path('month_count', views.month_count, name='month_count'),
    path('getmonth', views.getmonth, name='getmonth'),
    path('region_dengjiange', views.region_dengjiange, name='region_dengjiange'),
    path('region_genweifa', views.region_genweifa, name='region_genweifa'),
    path('region_ziranfa', views.region_ziranfa, name='region_ziranfa'),
    path('factor_detec', views.factor_detec, name='factor_detec'),
    path('interaction_detec', views.interaction_detec, name='interaction_detec'),
    path('interaction_rela', views.interaction_rela, name='interaction_rela'),
    path('ecological_detec', views.ecological_detec, name='ecological_detec'),
    path('original_events', views.original_events, name='original_events'),
    path('risk_value', views.risk_value, name='risk_value'),
    # path('post', views.post, name='post'),
    path('post', views.post, name='post'),
    path('post2', views.post2, name='post2'),
    path('news_list', views.news_list , name='news_list')
]
