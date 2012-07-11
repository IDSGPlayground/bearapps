# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
def home(request):
    return render_to_response('index.html')

def browse(request):
    return render_to_response('browse.html')

def myapps(request):
    return render_to_response('my-apps.html')
