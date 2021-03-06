from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist

from app_recs.models import Recommend

# Create your views here.
def home(request):
    Recommends = Recommend.objects.filter(Result='-').order_by('-Time2')
    return render_to_response('app_recs/templates/app_recs/Recommends.html',locals())

def latest(request):
    Recommends = Recommend.objects.order_by('-Time2')[:100]
    return render_to_response('app_recs/templates/app_recs/Recommends.html',locals())

def person(request,name):
    Recommends = Recommend.objects.filter(Person=name).order_by('-Time2')
    return render_to_response('app_recs/templates/app_recs/Recommends.html',locals())

def delete(request,rid):
    try:
        r = Recommend.objects.get(id=rid)
    except ObjectDoesNotExist:
        r = None
    rs = None
    if r:
        r.delete()
        rs = 'OK'
    else:
        rs = 'ERROR'
    return HttpResponse(rs)
