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
            if User.objects.get(name=user).password==request.POST['password']:
            # User.objects.get(name=user)
                request.session['user'] = user
                uid = User.objects.get(name=user).SID
                request.session['uid'] = uid
                return HttpResponseRedirect('/browse/')
            else:
            #     user = User(name=user, SID=uid)
            #     user.save()
            #     # user.user_apps_set.create(name=app, state="requested")
            #     user.user_apps_set.create(app_name=app, )
                return render_to_response('index.html', c)
        except: 
            return render_to_response('index.html', c)
    else:
        return render_to_response('index.html', c)

def browse(request):
    #Form handling; for POST requests to this view.
    if request.method == 'POST':
        form = RequestForm(request.POST)
        app = request.POST['app']
        # Write change to database.
        # try:
        user = User.objects.get(name=request.session['user'])
        app = User_Apps.objects.get(pk=1)
        # app.state = "requested"
        app.requested=True
        app.available=False
        app.downloadable=False
        app.user = user
        app.save()
        # except (KeyError, User.DoesNotExist):
        #     user.user_apps_set.create(href_name=app, state="requested")
    try:
        user = User.objects.get(name=request.session['user'])
    except (KeyError, User.DoesNotExist):
        user = None

    if 'uid' not in request.session:
        request.session['uid'] = 000000

    apps = App.objects.all()

    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name)
            # if state == "available":
            if state.available:
                app_states.append("app-btn-" + href_name)
            # elif state == "requested":
            elif state.requested:
                app_states.append("requested-btn-" + href_name)
        except:
            app_states.append('none')



    # Context and set-up
    c = Context({
            # 'button_value' : button_value,
            'form_value' : '',
            # 'icon_state' : icon,
            'username' : request.session['user'],
            'uid' : request.session['uid'],
            'apps' : apps,
            'app_states' : app_states,
            })

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    
    return render_to_response('my-apps.html', {'username' : request.session['user'],})

def manage(request):
    return render_to_response('manage.html', {'username' : request.session['user'],})


# Class to hold form data in browse()
class RequestForm(forms.Form):
    app = forms.CharField()

# Log In Form
class LogInForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()

