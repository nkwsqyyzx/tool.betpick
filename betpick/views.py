from django.http import HttpResponse

def odds(request,mid):
    return HttpResponse("Hello world %s" % mid)
