from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App

def home(request):
    not_user = False
    logout = False
    # Deletes session if logged in previously.
    try:
        del request.session['user']
        logout = True
    except:
        pass

    if request.method == 'POST':
        try: 
            user = request.POST['user']
            if User.objects.get(name=user) != None:
                request.session['user'] = user
                uid = User.objects.get(name=user).SID
                request.session['uid'] = uid
                return HttpResponseRedirect('/browse/')
        except: 
            # Errors if user does not exist.
            not_user = True

    c = Context({
        'not_user': not_user,
        'logout': logout,
    })
    c.update(csrf(request))
    return render_to_response('index.html', c)

def browse(request):
    #If user is not logged in redirects to log in page.
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    #Form handling; for POST requests to this view.
    if request.method == 'POST':
        form = RequestForm(request.POST)
        app = request.POST['app']

        # Write change to database.
        try:
            user = User.objects.get(name=request.session['user'])
            app = User_Apps.objects.get(user=user, href_name=app)
            app.state = "REQUESTED"
            app.save()
        except (KeyError, User.DoesNotExist):
            user.user_apps_set.create(href_name=app, state="REQUESTED")

    user = User.objects.get(name=request.session['user'])

    if 'uid' not in request.session:
        request.session['uid'] = 000000

    apps = App.objects.all()

    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name).state
            if state == "AVAILABLE":
                app_states.append("app-btn-" + href_name)
            elif state == "REQUESTED":
                app_states.append("requested-btn-" + href_name)
        except:
            app_states.append("app-btn" + href_name)



    # Context and set-up
    c = Context({
            'form_value' : '',
            'username' : request.session['user'],
            'uid' : request.session['uid'],
            'apps' : apps,
            'app_states' : app_states,
            })

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    try:
        user = User.objects.get(name=request.session['user'])
    except (KeyError, User.DoesNotExist):
        user = None

    apps = App.objects.all()
    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name).state
            if state == "REQUESTED":
                app_states.append("requested-btn-" + href_name)
        except:
            app_states.append('none')

    c = Context({
        'username' : request.session['user'],
        'apps' : apps,
        'app_states' : app_states,
        })

    return render_to_response('my-apps.html', c)

def manage(request):
    return render_to_response('manage.html', {'username' : request.session['user'],})


# Class to hold form data in browse()
class RequestForm(forms.Form):
    app = forms.CharField()

# Log In Form
class LogInForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()