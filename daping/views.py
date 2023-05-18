from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import RankingList
from .models import MonthCountAvgm
from .models import MonthCountAvgy

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

def month_countAvgm(request):
    month_countAvgm = MonthCountAvgm.objects.all()
    rl_str = serializers.serialize("json", month_countAvgm)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.month-coutAvgm', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.month-coutAvgm', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countAvgy(request):
    month_countAvgy = MonthCountAvgy.objects.all()
    rl_str = serializers.serialize("json", month_countAvgy)
    rl = json.loads(rl_str)
    print(rl)   
    #[{'model': 'daping.month-coutAvgy', 'pk': '西湖区', 'fields': {'count': 2}}, {'model': 'daping.month-coutAvgy', 'pk': '道里区', 'fields': {'count': 1}}]
    
    return HttpResponse(json.dumps(rl), content_type='application/json')
