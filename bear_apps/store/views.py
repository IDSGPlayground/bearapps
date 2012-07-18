# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App

def home(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        # request.session['user'] = form.user
        if form.is_valid():
        #     # request.session['user'] = request.POST['user']
            request.session['user'] = form.user
        #     request.Update()
        #     # print request.session['user']
        #     c = Context({'user':form.user})
        #     c.update(csrf(request))
        #     return render_to_response('index.html', c)
    c = Context({})
    c.update(csrf(request))
    # print request.session['user']
    return render_to_response('index.html', c)  

def browse(request):
    #Form handling; for POST requests to this view.
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            uid = form.cleaned_data['uid']
            app = form.cleaned_data['app']
            print user #prints name on command line output for debugging.

            # Write change to database.
            try:
                p=get_object_or_404(User, pk=User.objects.get(SID__startswith=int(uid)).id)
                try:
                    p.user_apps_set.get(name=app).change_state()
                except (KeyError, User_Apps.DoesNotExist):
                    p.user_apps_set.create(name=app, state="requested")
            except (KeyError, User.DoesNotExist):
                p = User(name=user, SID=uid)
                p.save()
                p.user_apps_set.create(name=app, state="requested")

    # Access db and check if app is already requested.
    uid = 12345678 # hardcoded because minimum viable product and stuff
    # Initial access to database, which allows us to check for a request.
    Matlab_obj=get_object_or_404(App, pk=App.objects.get(app_name='MatLab').id)
    Matlab_decrip=Matlab_obj.description
    Matlab_sysreq=Matlab_obj.Sysreq_windows+"\n\n"+Matlab_obj.Sysreq_linux+"\n\n"+Matlab_obj.Sysreq_mac
    Matlab_obtain=Matlab_obj.obtain
    Toolbox_obj=get_object_or_404(App, pk=App.objects.get(app_name='MatLab + Toolboxes').id)
    Toolbox_decrip=Toolbox_obj.description
    Toolbox_sysreq=Toolbox_obj.Sysreq_windows+"\n\n"+Matlab_obj.Sysreq_linux+"\n\n"+Matlab_obj.Sysreq_mac
    Toolbox_obtain=Toolbox_obj.obtain
    try:
        p=get_object_or_404(User, pk=User.objects.get(SID__startswith=(uid)).id)
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

    # Context and set-up
    c = Context({
            'Matlab_decrip': Matlab_decrip,
            'Matlab_sysreq': Matlab_sysreq,
            'Matlab_obtain': Matlab_obtain,
            'Toolbox_decrip': Toolbox_decrip,
            'Toolbox_sysreq': Toolbox_sysreq,
            'Toolbox_obtain': Toolbox_obtain,
            'button_value' : button_value,
            'button_value4': button_value4,
            'form_value' : form_value,
            'form_value4': form_value4,
            'icon_state' : icon,
            'icon_state2': icon2,
            'username' : request.POST['user']
            })

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    return render_to_response('my-apps.html', {'username' : request.session['user']})


# Class to hold form data in browse()
class RequestForm(forms.Form):
    user = forms.CharField()
    uid = forms.CharField()
    app = forms.CharField()

# Log In Form
class LogInForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()