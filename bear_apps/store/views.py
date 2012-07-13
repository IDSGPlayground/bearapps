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

    #Form handling
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
                    p.apps_set.get(name=app).change_state()
                except (KeyError, Apps.DoesNotExist):
                    p.apps_set.create(name=app, state="requested")
            except (KeyError, User.DoesNotExist):
                p = User(name=user, SID=uid)
                p.save()
                p.apps_set.create(name=app, state="requested")

    # Access db and check if app is already requested.
    uid = 12345678 # hardcoded because minimum viable product and stuff

    # Initial access to database, which allows us to check for a request.
    try:
        p=get_object_or_404(User, pk=User.objects.get(SID__startswith=(uid)).id)
    except (KeyError, User.DoesNotExist):
        p = None

    request_status = False

    # Check if the app has been requested
    # In this case, it check specifically for one user, Elvis.
    try:
        p.apps_set.get(name='Matlab')
        request_status = True
    except (KeyError, Apps.DoesNotExist):
        request_status = False
    except AttributeError:
        request_status = False

    # control flow for disabling the html form in browse.html
    if request_status:
        button_value = 'ALREADY REQUESTED'
        form_value = 'DISABLED'
        icon = 'requested-btn'
    else:
        button_value = 'REQUEST'
        form_value = ''
        icon = 'app-btn'

    # Context and template set-up
    c = Context({
            'button_value' : button_value,
            'form_value' : form_value,
            'icon_state' : icon,
            'username' : 'Elvis'
            })

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    return render_to_response('my-apps.html', {'username' : 'Elvis'})


# Class to hold form data in browse()
class RequestForm(forms.Form):
    user = forms.CharField()
    uid = forms.CharField()
    app = forms.CharField()
