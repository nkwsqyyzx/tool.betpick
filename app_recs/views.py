from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template


from app_recs.models import Recommend

# Create your views here.
def home(request):
    p = Recommend.objects.filter(Result='-').order_by('-Time2')
    a = [m for m in p]
    c = Context({'Recommends': a})
    t = get_template('app_recs/templates/app_recs/Recommends.html')
    html = t.render(c)
    return HttpResponse(html)

def latest(request):
    p = Recommend.objects.order_by('-Time2')[:100]
    a = [m for m in p]
    c = Context({'Recommends': a})
    t = get_template('app_recs/templates/app_recs/Recommends.html')
    html = t.render(c)
    return HttpResponse(html)
