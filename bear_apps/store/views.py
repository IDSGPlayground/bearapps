# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, Apps

def home(request):
    return render_to_response('index.html')

def browse(request):
    c = {}
    c.update(csrf(request))

    #Form handling
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            uid = form.cleaned_data['uid']
            app = form.cleaned_data['app']
            print user #prints name on command line output for debugging.

            # write to database
            #p = get_object_or_404(Apps, pk=1)
            #try:
            #   p.user_set.create(name=user, SID=uid, state='requested')
            #except (KeyError, User.DoesNotExit):

    return render_to_response('browse.html', c)

def myapps(request):
    return render_to_response('my-apps.html')


# Class to hold form data in browse()
class RequestForm(forms.Form):
    user = forms.CharField()
    uid = forms.CharField()
    app = forms.CharField()
