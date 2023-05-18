from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import RankingList
from .models import Monthcountall
from .models import RegionCount
from .models import EventsReason

def index(request):
    
    return render(request, 'index.html')

from django.core import serializers
import json
from django.http import JsonResponse


def rank_list(request):
    ranking_list = RankingList.objects.all()
    rl_str = serializers.serialize("json", ranking_list)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.rankinglist', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.rankinglist', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countall(request):
    monthcountall = Monthcountall.objects.all()
    rl_str = serializers.serialize("json", monthcountall)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.rankinglist', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.rankinglist', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

def region_count(request):
    region_counting = RegionCount.objects.all()
    rl_str = serializers.serialize("json", region_counting)
    rl = json.loads(rl_str)
    print(rl)

    return HttpResponse(json.dumps(rl), content_type='application/json')

def events_reason(request):
    events_reasoning = EventsReason.objects.all()
    rl_str = serializers.serialize("json", events_reasoning)
    rl = json.loads(rl_str)
    print(rl)

    return HttpResponse(json.dumps(rl), content_type='application/json')