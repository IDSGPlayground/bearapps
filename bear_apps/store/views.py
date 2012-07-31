from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.utils import timezone
from django import forms
from store.models import User, User_Apps, App, Notification, Chartstring, Group
from django.contrib import messages
from store.notifications import addNotification, getNotifications
from datetime import date
from operator import attrgetter

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
                request.session['user'] = user
                sid = User.objects.get(name=user).SID
                request.session['sid'] = sid
                return HttpResponseRedirect('/browse/')
            else:
                return render_to_response('index.html', c)
        except:
            # Redirects to registration page if username does not exist.
            return HttpResponseRedirect('/register/')

    c = Context({
        'not_user': not_user,
        'logout': logout,
    })

    c.update(csrf(request))
    return render_to_response('index.html', c)

def register(request):
    all_groups = Group.objects.all()
    c = Context ({
    'groups': all_groups,
    })

    if request.method == 'POST' and "register" in request.POST:
        #Try clause checks if all fields are filled out.
        try:
            username = request.POST['username']
            SID = request.POST['SID']
            password = request.POST['password']
            verify = request.POST['verify-password']
            group_count = int(request.POST['group_count'])
            groups = []
            for i in range(1, group_count + 1):
                groups.append(request.POST['groups-' + str(i)])
            status = request.POST['status']
        except:
            c = Context ({
            'empty_fields': True,
            'groups': all_groups,
            })
            c.update(csrf(request))
            return render_to_response('register.html', c)

        # Checks if passwords match.
        if password != verify:
            c = Context ({
            'not_match': True,
            'groups': all_groups,
            })
            c.update(csrf(request))
            return render_to_response('register.html', c)

        # Checks if username is already taken.
        for user in User.objects.all():
            if user.name == username:
                c = Context ({
                'user_taken': True,
                'groups': all_groups,
                })
                c.update(csrf(request))
                return render_to_response('register.html', c)
        
        # Creates admin functionality if professor or rso is selected.
        user_type = "GENERAL"
        if (status == "professor") or (status == "rso"):
            user_type = "MANAGER"
        elif (status == "admin"):
            user_type = "ADMIN"

        # Initializes the new user.
        new_user = User.objects.create(name=username, SID=SID, password=password, user_type=user_type)

        # Adds the new user to selected group.
        # If group exists, gets Group object, otherwise, creates a new group.
        for group in groups:
            try:
                add_group = Group.objects.get(name=group)
            except: 
                add_group = Group.objects.create(name=group)
            new_user.groups.add(add_group)

        # Resets request.method, so that POST data is no longer stored.
        request.method = None

        # Redirects user to the log in page.
        return HttpResponseRedirect('/')

    c.update(csrf(request))
    return render_to_response('register.html', c)

def browse(request):
    #If user is not logged in redirects to log in page.
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    if User.objects.get(name=request.session['user']).user_type == "MANAGER":
        return HttpResponseRedirect('/manage/')

    elif User.objects.get(name=request.session['user']).user_type == "ADMIN":
        return HttpResponseRedirect('/admin/')

    user = User.objects.get(name=request.session['user'])

    # Form handling; for POST requests to this view.
    apps = App.objects.all()
    if request.method == 'POST':
        form = RequestForm(request.POST)
        app = request.POST['app']
        app_object = App.objects.get(href_name=app)

        # Write change to database.
        try:
            new_app = User_Apps.objects.get(app=app_object, user=user)
        except:
            new_app = User_Apps.objects.create(user=user, app=app_object, status="AVAILABLE")

        new_app.status="REQUESTED"
        new_app.group = Group.objects.get(name=request.POST['mygroup'])
        new_app.save()
        
        request.method = None

        # Resets request.method, so that POST data is no longer stored.
        request.method = None

    app_states = []
    for app in apps:
        href_name = app.href_name
        try:
            status = User_Apps.objects.get(app=app, user=user).status
            if status.lower()=="available":
                app_states.append("app-btn-" + href_name)
            elif status.lower()=="requested":
                app_states.append("requested-btn-" + href_name)
            elif status.lower()=="approved":
                app_states.append("downloadable-btn-" + href_name)
        except:
            app_states.append("app-btn-" + href_name)

    messages = getNotifications(user)
    notifications = len(messages)

    # Dictionary for displaying applications and their statuses.
    # app_display: key = app's href name and value = 'available' or 'requested'
    # app_info: key = app's href name and value = the app object from App.objects.all()
    app_display = dict([(apps[x].href_name,app_states[x]) for x in range(len(apps))])
    app_info = dict([(apps[x].href_name, apps[x]) for x in range(len(apps))])

    groups = user.groups.all()
    groups = sorted(groups, key=lambda group: group.name)

    # Context and set-up
    c = Context({
            'username' : request.session['user'],
            'sid' : request.session['sid'],
            'app_display' : app_display,
            'app_info' : app_info,
            'messages' : messages,
            'notifications' : notifications,
            'groups' : groups,
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
    temp_app = []
    for app in apps:
        href_name = app.href_name
        try:
            status = User_Apps.objects.get(app=app, user=user).status
            if status.lower() == "requested":
                app_states.append("requested-btn-" + href_name)
                temp_app.append(app)
            elif status.lower() == "approved":
                app_states.append("downloadable-btn-" + href_name)
                temp_app.append(app)
        except:
            pass

    # Dictionary for displaying applications and their statuses.
    # app_display: key = app's href name and value = 'available' or 'requested'
    # app_info: key = app's href name and value = the app object from App.objects.all()
    app_display = dict([(temp_app[x].href_name,app_states[x]) for x in range(len(app_states))])
    app_info = dict([(temp_app[x].href_name, temp_app[x]) for x in range(len(app_states))])

    if len(temp_app) == 0:
        no_apps = True
    else:
        no_apps = False

    messages = ["None"]
    notifications = 0
    try:
        messages = user.notification_set.all()
        notifications = len(messages)
    except:
        pass

    c = Context({
        'username' : request.session['user'],
        'app_display' : app_display,
        'app_info' : app_info,
        'no_apps' : no_apps,
        'notifications' : notifications,
        'messages' : messages,
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
            price = App.objects.get(href_name=app).price
            chartstring = Chartstring.objects.get(chartstring = request.POST['chartstring'])
            print "HFASFSDFSDFSDF"
            print request.POST['user']
            user_requested = User.objects.get(SID=request.POST['user'])

            # Write change to database.
            app_object = App.objects.get(href_name=app)
            app = user_requested.user_apps_set.get(app=app_object)
            app.chartstring = chartstring
            chartstring.remaining = chartstring.remaining - price
            chartstring.save()
            app.date= date.today()
            print app.date
            app.status = "APPROVED"
            app.save()

            addNotification(user = user_requested, app = app_object, code = 'approve')

        elif "revoke" in request.POST:
            app = request.POST['app']
            user_requested = User.objects.get(SID=request.POST['user'])
            # Write change to database.
            app_object = App.objects.get(href_name=app)
            app = user_requested.user_apps_set.get(app=app_object)
            app.delete()

            addNotification(user = user_requested, app = app_object, code = 'revoke')

        elif "new" in request.POST:
            new_chartstring = Chartstring(
                nickname=request.POST['nickname'], 
                chartstring=request.POST['chartstring'],
                budget=request.POST['amount'], 
                remaining=request.POST['amount'], 
                manager=user)
            new_chartstring.group = Group.objects.get(name=request.POST['group'])
            new_chartstring.save()

        request.method = None

    users_of_app = {}
    chart_history = {} 
    for chartstring in Chartstring.objects.all():
        chart_history[chartstring] = chartstring.user_apps_set.all()

    for app in App.objects.all():
        # Generates a list of all members in all groups associated with the user.
        members = []
        for group in groups:
            for u in all_users:
                if group in u.groups.all() and u != user:
                    members.append(u)

        users_of_app[app] = []
        for member in members:
            try:
                if member.user_apps_set.get(app=app).group in user.groups.all():
                    href_name = app.href_name
                    requested, downloadable = False, False
                    status = User_Apps.objects.get(app=app, user=member).status

                    if status == "REQUESTED":
                        requested = True
                    elif status == "APPROVED":
                        downloadable = True

                    chartstrings = []
                    for group in user.groups.all():
                        for chartstring in group.chartstring_set.all():
                            chartstrings.append(chartstring)

                    users_of_app[app].append((member, requested, downloadable, chartstrings,))
            except:
                pass

    all_chartstrings, all_members = {}, {}

    for group in groups:
        chartstrings = group.chartstring_set.all()
        chartstrings = sorted(chartstrings, key=lambda chartstring: chartstring.nickname)
        all_chartstrings[group] = [(group.name, chartstrings,)]
        print all_chartstrings

        members = []
        for u in all_users:
            if group in u.groups.all() and u != user:
                members.append(u)

        all_members[group] = [(group.name, members,)]

    c = Context({
        'username': request.session['user'],
        'groups': groups,
        'users_of_app' : users_of_app,
        'all_members': all_members,
        'all_chartstrings': all_chartstrings,
        'all_users': all_users,
        'chart_history': chart_history
        })

    c.update(csrf(request))

    return render_to_response('manage.html', c)

def admin(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    user = User.objects.get(name=request.session['user'])
    all_users = User.objects.all()
    all_user_apps = User_Apps.objects.all()
    all_accepted_apps=[]
    for app in all_user_apps:
        if app.status=="APPROVED":
            all_accepted_apps.append(app)
    sorted_by_chartstring = sorted(all_accepted_apps, key=attrgetter('chartstring.nickname'))
    sorted_by_group = sorted(Group.objects.all(), key=attrgetter('name'))
    user_summary = {}
    count = 0

    for u in all_users:
        if u != user:
            user_summary[count] = []
            user_summary[count].append((u, u.user_apps_set.all()))
            count += 1

    chartstrings = Chartstring.objects.all()

    c = Context({
        'username': user.name,
        'user_summary': user_summary,
        'chartstrings': chartstrings,
        'sorted_by_chartstring' : sorted_by_chartstring,
        'sorted_by_group' : sorted_by_group,
        })

    return render_to_response('admin.html', c)

class RequestForm(forms.Form):
    app = forms.CharField()

