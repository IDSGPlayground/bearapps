from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App, Notification, Chartstring, Group

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

def register(request):
    return render_to_response('register.html')

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
                temp_app = User_Apps(app_name=temp_app.app_name, href_name=temp_app.href_name, status="AVAILABLE")
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
        app.status="REQUESTED"
        app.save()

    # Browse page for viewing (non-POST requests)
    if 'uid' not in request.session:
        request.session['uid'] = 000000

    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            state = user.user_apps_set.get(href_name=href_name).status
            if state.lower()=="available":
                app_states.append("app-btn-" + href_name)
            elif state.lower()=="requested":
                app_states.append("requested-btn-" + href_name)
            elif state.lower()=="downloadable":
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
            state = user.user_apps_set.get(href_name=href_name).status
            if state.lower()=="requested":
                app_states.append("requested-btn-" + href_name)
            elif state.lower()=="downloadable":
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
    groups = user.groups.all()
    all_users = User.objects.all()

    # Sorts all groups & all users in alphabetical order.
    groups = sorted(groups, key=lambda group: group.name)
    all_users = sorted(all_users, key=lambda user: user.name)

    if request.method == 'POST':
        if "approve" in request.POST:
            app = request.POST['app']
            #price = app.price
            price = App.objects.get(href_name=app).price
            chartstring = Chartstring.objects.get(chartstring = request.POST['chartstring'])
            user_requested = User.objects.get(SID=request.POST['user'])

            # Write change to database.
            app = user_requested.user_apps_set.get(href_name=app)
            app.chartstring = chartstring
            chartstring.budget = chartstring.budget - price
            chartstring.save()
            app.status = "DOWNLOADABLE"
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
            app.status="AVAILABLE"
            app.save()

            message = "Your license for " + app.app_name + " has been revoked."
            notification = Notification(user=user_requested, message=message)
            notification.user = user_requested
            notification.save()

            user_requested.notifications += 1
            user_requested.save()

        elif "new" in request.POST:
            new_chartstring = Chartstring(nickname=request.POST['nickname'], chartstring=request.POST['chartstring'])
            new_chartstring.group = Group.objects.get(name=request.POST['group'])
            new_chartstring.save()

    users_of_app = {}

    for app in App.objects.all():
        # Generates a list of all members in all groups associated with the user.
        members = []
        for group in groups:
            for u in all_users:
                for user_group in u.groups.all():
                    if user_group == group and u != user:
                        members.append(u)

        for member in members:
            href_name = app.href_name
            requested, downloadable = False, False
            status = User_Apps.objects.get(href_name=href_name, user=member).status

            if status == "REQUESTED":
                requested = True
            elif status == "DOWNLOADABLE":
                downloadable = True

            chartstrings = []
            for group in member.groups.all():
                for chartstring in group.chartstring_set.all():
                    chartstrings.append(chartstring)

            users_of_app[app] = [(member, requested, downloadable, chartstrings,)]

    all_chartstrings, all_members = {}, {}

    for group in groups:
        chartstrings = group.chartstring_set.all()
        chartstrings = sorted(chartstrings, key=lambda chartstring: chartstring.nickname)
        all_chartstrings[group] = [(group.name, chartstrings,)]

        members = []
        for u in all_users:
            for user_group in u.groups.all():
                if user_group == group and u != user:
                    members.append(u)

        all_members[group] = [(group.name, members,)]

    c = Context({
        'username': request.session['user'],
        'groups': groups,
        'users_of_app' : users_of_app,
        'all_members': all_members,
        'all_chartstrings': all_chartstrings,
        'all_users': all_users,
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
