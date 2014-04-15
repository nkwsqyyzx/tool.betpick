from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

# Create your views here.
def stat_home(request):
    return HttpResponse('hello,world')

def stat_match(mid):
    return HttpResponse(mid)
