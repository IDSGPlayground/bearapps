# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App

def home(request):
    c = Context({})
    c.update(csrf(request))
    if request.method == 'POST':
        form = LogInForm(request.POST)
        #if form.is_valid():
        try: 
            user = request.POST['user']
            if User.objects.get(name=user) != None:
                request.session['user'] = user
                uid = User.objects.get(name=user).SID
                request.session['uid'] = uid
                return HttpResponseRedirect('/browse/')
        except: 
            return render_to_response('index.html', c)
    else:
        return render_to_response('index.html', c)

def browse(request):
    #Form handling; for POST requests to this view.
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            app = form.cleaned_data['app']

            # Write change to database.
            try:
                p = User.objects.get(name=request.session['user'])
                try:
                    p.user_apps_set.get(name=app).change_state()
                except (KeyError, User_Apps.DoesNotExist):
                    p.user_apps_set.create(name=app, state="requested")
            except (KeyError, User.DoesNotExist):
                p = User(name=user, SID=uid)
                p.save()
                p.user_apps_set.create(name=app, state="requested")

    # Access db and check if app is already requested.

    try:
        p = User.objects.get(name=request.session['user'])
    except (KeyError, User.DoesNotExist):
        p = None

    # Check if the app has been requested
    # In this case, it check specifically for one user, Elvis.
    request_status = False # default value
    try:
        p.user_apps_set.get(name='Matlab')
        request_status = True
    except (KeyError, User_Apps.DoesNotExist):
        request_status = False
    except AttributeError:
        request_status = False

    # control flow for disabling the html form in browse.html
    if request_status:
        button_value = 'ALREADY REQUESTED'
        form_value = 'DISABLED'
        icon = 'requested-btn-matlab'
    else:
        button_value = 'REQUEST'
        form_value = ''
        icon = 'app-btn-matlab'
    
    try:
        p.user_apps_set.get(name='Matlab + Toolbox')
        request_status = True
    except (KeyError, User_Apps.DoesNotExist):
        request_status = False
    except AttributeError:
        request_status = False

    # control flow for disabling the html form in browse.html
    if request_status:
        button_value4 = 'ALREADY REQUESTED'
        form_value4 = 'DISABLED'
        icon2 = 'requested-btn-matlab'
    else:
        button_value4 = 'REQUEST'
        form_value4 = ''
        icon2 = 'app-btn-matlab'

    if 'uid' not in request.session:
        request.session['uid'] = "Not set"

    apps = App.objects.all()
    for app in apps:
        name = app.app_name
    #user_apps =  p.user_apps_set.get(name='Matlab')

    # Context and set-up
    c = Context({
            'button_value' : button_value,
            'button_value4': button_value4,
            'form_value' : form_value,
            'form_value4': form_value4,
            'icon_state' : icon,
            'icon_state2': icon2,
            'username' : request.session['user'],
            'uid' : request.session['uid'],
            'apps' : apps,
            
            })

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    return render_to_response('my-apps.html', {'username' : request.session['user'],})


# Class to hold form data in browse()
class RequestForm(forms.Form):
    user = forms.CharField()
    uid = forms.CharField()
    app = forms.CharField()

# Log In Form
class LogInForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()