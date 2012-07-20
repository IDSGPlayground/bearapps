from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App, Notification, Chartstring

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
            if User.objects.get(name=user).password == request.POST['password']:
            # User.objects.get(name=user)
                request.session['user'] = user
                uid = User.objects.get(name=user).SID
                request.session['uid'] = uid
                return HttpResponseRedirect('/browse/')
            else:
                return render_to_response('index.html', c)
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

    if User.objects.get(name=request.session['user']).owner:
        return HttpResponseRedirect('/manage/')

    user = User.objects.get(name=request.session['user'])
    notifications = user.notifications

    #Form handling; for POST requests to this view.
    apps = App.objects.all()
    if request.method == 'POST':
        for temp_app in apps:
            try:
                user.user_apps_set.get(href_name=temp_app.href_name)
            except:
                temp_app = User_Apps(app_name=temp_app.app_name, href_name=temp_app.href_name, available=True, requested=False, downloadable=False)
                chartstring = Chartstring()
                chartstring.group = user.groups
                chartstring.save()
                temp_app.chartstring = chartstring
                temp_app.user = user
                temp_app.save()

        form = RequestForm(request.POST)
        app = request.POST['app']

        # Write change to database.
        app = User_Apps.objects.get(href_name=app, user=user)
        app.requested = True
        app.available = False
        app.save()

    # Browse page for viewing (non-POST requests)

    if 'uid' not in request.session:
        request.session['uid'] = 000000

    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name)
            if state.available:
                app_states.append("app-btn-" + href_name)
            elif state.requested:
                app_states.append("requested-btn-" + href_name)
            elif state.downloadable:
                app_states.append("downloadable-btn-" + href_name)
        except:
            app_states.append("app-btn-" + href_name)
    print app_states

    try: 
        messages = user.notification_set.all()
    except:
        messages = ["None"]


    # Dictionary for displaying applications and their statuses.
    # app_display: key = app's href name and value = 'available' or 'requested'
    # app_info: key = app's href name and value = the app object from App.objects.all()
    app_display = dict([(apps[x].href_name,app_states[x]) for x in range(len(apps))])
    app_info = dict([(apps[x].href_name, apps[x]) for x in range(len(apps))])


    # Context and set-up
    c = Context({
            'username' : request.session['user'],
            'uid' : request.session['uid'],
            'apps' : apps,
            'app_states' : app_states,
            'app_display' : app_display,
            'app_info' : app_info,
            'notifications' : notifications,
            'messages' : messages,
            })
    try:
        for message in messages:
            message.delete()
        user.notifications = 0
        user.save()
    except:
        pass

    # Update context with Security token for html form
    c.update(csrf(request))

    return render_to_response('browse.html', c)

def myapps(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    user = User.objects.get(name=request.session['user'])

    apps = App.objects.all()
    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name)
            if state.requested:
                app_states.append("requested-btn-" + href_name)
            elif state.downloadable:
                app_states.append("downloadable-btn-" + href_name)
        except:
            app_states.append('none')

    c = Context({
        'username' : request.session['user'],
        'apps' : apps,
        'app_states' : app_states,
        })

    return render_to_response('my-apps.html', c)

def manage(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    user = User.objects.get(name=request.session['user'])
    group = user.groups
    all_users = User.objects.all()
    members = []

    if request.method == 'POST':
        if "approve" in request.POST:
            app = request.POST['app']
            chartstring = Chartstring.objects.get(chartstring = request.POST['chartstring'])
            user_requested = User.objects.get(SID=request.POST['user'])

            # Write change to database.
            app = user_requested.user_apps_set.get(href_name=app)
            app.chartstring = chartstring
            app.requested = False
            app.downloadable = True
            app.save()

            message = "You have been approved to download " + app.app_name
            notification = Notification(user=user_requested, message=message)
            notification.user = user_requested
            notification.save()

            user_requested.notifications += 1
            user_requested.save()


        elif "revoke" in request.POST:
            app = request.POST['app']
            user_requested = User.objects.get(SID=request.POST['user'])

            # Write change to database.
            app = user_requested.user_apps_set.get(href_name=app)
            app.requested = False
            app.available = True
            app.downloadable = False
            app.save()

            message = "Your license for " + app.app_name + " has been revoked."
            notification = Notification(user=user_requested, message=message)
            notification.user = user_requested
            notification.save()

            user_requested.notifications += 1
            user_requested.save()

        elif "new" in request.POST:
            nickname = request.POST['nickname']
            chartstring = request.POST['chartstring']
            new_chartstring = Chartstring(nickname=nickname, chartstring=chartstring)
            new_chartstring.group = group
            new_chartstring.save()


    for u in all_users:
        if u.groups == group and u != user:
            members.append(u)

    members = sorted(members, key=lambda member: member.name)


    users_of_app = {}
    apps = App.objects.all()

    for app in apps:
        users_of_app[app] = []

        for member in members:
            href_name = app.href_name
            try:
                requested = User_Apps.objects.get(href_name=href_name, user=member).requested
                downloadable = User_Apps.objects.get(href_name=href_name, user=member).downloadable
                chartstring = User_Apps.objects.get(href_name=href_name, user=member).chartstring
                users_of_app[app].append((member, requested, downloadable, chartstring,))
            except:
                pass

    chartstrings = group.chartstring_set.all()

    edited_chartstrings = []
    for chartstring in chartstrings:
        if chartstring.nickname != "":
            edited_chartstrings.append(chartstring)

    c = Context({
        'username': request.session['user'],
        'group': group,
        'members': members,
        'users_of_app' : users_of_app,
        'chartstrings': edited_chartstrings,
        })

    c.update(csrf(request))

    return render_to_response('manage.html', c)


# Class to hold form data in browse()
class RequestForm(forms.Form):
    app = forms.CharField()

# Log In Form
class LogInForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()
