from django.shortcuts import render
import json
import numpy as np
import math
# Create your views here.
from django.http import HttpResponse
from collections import defaultdict
from itertools import chain
from django.forms.models import model_to_dict


import sys
print(sys.path)

from .models import RankingList
from .models import Monthcountall
from .models import Monthcountly
from .models import RegionCount
from .models import EventsReason
from .models import MonthCountavgm
from .models import MonthCountavgy
from .models import MonthCount

def index(request):
    
    return render(request, 'index.html')

from django.core import serializers
import json
from django.http import JsonResponse

def merge_dict(d1, d2):
    d = defaultdict(list)

    for dd in (d1, d2):
        for key, value in d.items():
            if isinstance(value, list):
                dd[key].extend(value)
            else:
                dd[key].append(value)
    return dict(dd)



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

def month_countly(request):
    monthcountly = Monthcountly.objects.all()
    rl_str = serializers.serialize("json", monthcountly)
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

def month_countavgm(request):
    month_countavgm = MonthCountavgm.objects.all()
    rl_str = serializers.serialize("json", month_countavgm)
    rl = json.loads(rl_str)
    print(rl)   

    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_countavgy(request):
    month_countavgy = MonthCountavgy.objects.all()
    rl_str = serializers.serialize("json", month_countavgy)
    rl = json.loads(rl_str)
    print(rl)   

    return HttpResponse(json.dumps(rl), content_type='application/json')

def month_count(request):
    month_count = MonthCount.objects.all()
    rl_str = serializers.serialize("json", month_count)
    print(rl_str)
    rl = json.loads(rl_str)
    print(rl)
    return HttpResponse(json.dumps(rl), content_type='application/json')

def getmonth(request):
    monthcountavgm = MonthCountavgm.objects.all()
    monthcountly = Monthcountly.objects.all()
    monthcountall = Monthcountall.objects.all()
    r2_str = serializers.serialize("json", monthcountavgm)
    r2 = json.loads(r2_str)
    r3_str = serializers.serialize("json", monthcountly)
    r3 = json.loads(r3_str)
    r4_str = serializers.serialize("json", monthcountall)
    r4 = json.loads(r4_str)   
    r5 = r2+r3+r4


    return HttpResponse(json.dumps(r5), content_type='application/json')


def myview(_request):
    response = HttpResponse(json.dumps({"key": "value","key2":"value"}))
    response["Access-Control-Allow-Origin"] ="*"
    response["Access-Control-Alow-Methods"] ="POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] ="1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#等间隔法
def region_dengjiange(request):
    adict = {"南通市":0,"南京市":0,"扬州市":0,"无锡市":0,"泰州市":0,"盐城市":0,"徐州市":0,"常州市":0,"宿迁市":0,"淮安市":0,"镇江市":0,"连云港市":0,"苏州市":0}
    region_counting = RegionCount.objects.all()

    
    dic = RegionCount.objects.values("city","regioncounts")
    for i in dic:
        cit = i["city"]+"市"
        adict[cit] = i["regioncounts"]
        
    print(adict)
    #{'南通': 4, '南京': 11, '扬州': 1, '无锡': 2, '泰州': 2, '盐城': 3, '徐州': 2, '常州': 1, '宿迁': 0, '淮安': 0, '镇江': 0, '连云港': 0, '苏州': 0}
    
    #分成五级
    n = 5
    #取出字典中值进行排序
    list= sorted(adict.values())
    
#最大值
    maxi = max(list)
#最小值
    mini = min(list)
#间隔值
    nn = (maxi-mini) / n
    
#分等间隔区间
    for key,value in adict.items():
        for x in range(n):
            ma = mini + nn*(x+1)
            mi = ma - nn
#mi-ma
            if value>=mi and value<ma:
                adict[key] = (x+1)
        if value == maxi:
            adict[key] = n
            
    print(adict)
    dd = json.dumps(adict, ensure_ascii=False)
    
    return HttpResponse(dd, content_type='application/json')