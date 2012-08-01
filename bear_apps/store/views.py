""" Defines views in the model-view-controller scheme for Django. """
from django.template import Context
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App, Chartstring, Group
from store.notifications import addnotification, getnotifications
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    """ Defines the login page for BearApps.
        Entering valid login credentials will direct user to /browse.
        An invalid password redirects to this page with a blank password field.
        An invalid username redirects the user to /register.
    """
    not_user = False
    logout = False

    # Deletes session if logged in previously.
    try:
        del request.session['user']
        logout = True
    except KeyError:
        print 'No sessions are active yet.'

    if request.method == 'POST':
        try:
            user = request.POST['user']
            if User.objects.get(name=user).password == request.POST['password']:
                request.session['user'] = user
                sid = User.objects.get(name=user).SID
                request.session['sid'] = sid
                return HttpResponseRedirect('/browse/')
            # else:
            #     return render_to_response('index.html', c)
        except ObjectDoesNotExist:
            # Redirects to registration page if username does not exist.
            return HttpResponseRedirect('/register/')

    con = Context({
        'not_user': not_user,
        'logout': logout,
    })

    con.update(csrf(request))
    return render_to_response('index.html', con)


def register(request):
    """ Defines the registration view for first-time users.
        Note: the user will not be registered if they enter
        a username that already exists in our database.
    """
    con = Context ({
    'groups': Group.objects.all(),
    })

    if request.method == 'POST' and "register" in request.POST:
        #Try clause checks if all fields are filled out.
        try:
            username = request.POST['username']
            studentid = request.POST['SID']
            password = request.POST['password']
            verify = request.POST['verify-password']
            group_count = int(request.POST['group_count'])
            groups = []
            for i in range(1, group_count + 1):
                groups.append(request.POST['groups-' + str(i)])
            status = request.POST['status']
        except ObjectDoesNotExist:
            con = Context ({
            'empty_fields': True,
            'groups': Group.objects.all(),
            })
            con.update(csrf(request))
            return render_to_response('register.html', con)

        # Checks if passwords match.
        if password != verify:
            con = Context ({
            'not_match': True,
            'groups': Group.objects.all(),
            })
            con.update(csrf(request))
            return render_to_response('register.html', con)

        # Checks if username is already taken.
        for user in User.objects.all():
            if user.name == username:
                con = Context ({
                'user_taken': True,
                'groups': Group.objects.all(),
                })
                con.update(csrf(request))
                return render_to_response('register.html', con)
        
        # Creates admin functionality if professor or rso is selected.
        user_type = 'GENERAL'
        if (status == 'professor') or (status == 'rso'):
            user_type = 'MANAGER'
        elif (status == 'admin'):
            user_type = 'ADMIN'

        # Initializes the new user.
        new_user = User.objects.create(
            name=username, 
            SID=studentid, password=password, 
            user_type=user_type,
            )

        # Adds the new user to selected group.
        # If group exists, gets Group object, otherwise, creates a new group.
        for group in groups:
            try:
                add_group = Group.objects.get(name=group)
            except ObjectDoesNotExist: 
                add_group = Group.objects.create(name=group)
            new_user.groups.add(add_group)

        # Resets request.method, so that POST data is no longer stored.
        request.method = None

        # Redirects user to the log in page.
        return HttpResponseRedirect('/')

    con.update(csrf(request))
    return render_to_response('register.html', con)

def browse(request):
    """ Defines the view to browse and request applications.
        Users not logged in are redirected to the login page.
    """
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    if User.objects.get(name=request.session['user']).user_type == 'MANAGER':
        return HttpResponseRedirect('/manage/')

    elif User.objects.get(name=request.session['user']).user_type == 'ADMIN':
        return HttpResponseRedirect('/admin/')

    user = User.objects.get(name=request.session['user'])

    # Form handling; for POST requests to this view.
    apps = App.objects.all()
    if request.method == 'POST':
        app = request.POST['app']
        app_object = App.objects.get(href_name=app)

        # Write change to database.
        try:
            new_app = User_Apps.objects.get(app=app_object, user=user)
        except ObjectDoesNotExist:
            new_app = User_Apps.objects.create(user=user, 
                app=app_object, 
                status='AVAILABLE')

        new_app.status = 'REQUESTED'
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
            if status.lower() == 'available':
                app_states.append("app-btn-" + href_name)
            elif status.lower() == 'requested':
                app_states.append('requested-btn-' + href_name)
            elif status.lower() == 'approved':
                app_states.append('downloadable-btn-' + href_name)
        except ObjectDoesNotExist:
            app_states.append("app-btn-" + href_name)

    # Dictionary for displaying applications and their statuses
    # app_display: key = app's href name 
    #              value = 'available' or 'requested'
    # app_info: key = app's href name
    #           value = the app object from App.objects.all()
    app_display = dict([(apps[x].href_name, app_states[x]) 
        for x in range(len(apps))])
    app_info = dict([(apps[x].href_name, apps[x]) 
        for x in range(len(apps))])

    messages = getnotifications(user)

    # Context and set-up
    con = Context({
            'username' : request.session['user'],
            'sid' : request.session['sid'],
            'app_display' : app_display,
            'app_info' : app_info,
            'messages' : getnotifications(user),
            'notifications' : len(messages),
            'groups' : sorted(user.groups.all(), key=lambda group: group.name),
        })

    for message in messages:
        message.delete()
    user.notifications = 0
    user.save()

    # Update context with Security token for html form
    con.update(csrf(request))

    return render_to_response('browse.html', con)

def myapps(request):
    """ Defines the my-apps view for BearApps to display applications
        of interest to a user (requested, approved, etc.)
    """
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
            if status.lower() == 'requested':
                app_states.append('requested-btn-' + href_name)
                temp_app.append(app)
            elif status.lower() == 'approved':
                app_states.append('downloadable-btn-' + href_name)
                temp_app.append(app)
        except ObjectDoesNotExist:
            print 'User browsing my-apps currently has no apps'

    # Dictionary for displaying applications and their statuses.
    # app_display: key = app's href name
    #              value = 'available' or 'requested'
    # app_info: key = app's href name
    #           value = the app object from App.objects.all()
    app_display = dict([(temp_app[x].href_name, app_states[x])
        for x in range(len(app_states))])
    app_info = dict([(temp_app[x].href_name, temp_app[x])
        for x in range(len(app_states))])

    if len(temp_app) == 0:
        no_apps = True
    else:
        no_apps = False

    messages = getnotifications(user)
    notifications = len(messages)

    con = Context({
        'username' : request.session['user'],
        'app_display' : app_display,
        'app_info' : app_info,
        'no_apps' : no_apps,
        'notifications' : notifications,
        'messages' : messages,
        })

    return render_to_response('my-apps.html', con)

def manage(request):
    """ Defines the manager view for BearApps. PIs and RSOs are
        directed to this view to manage their user requests and
        chartstrings/budgets.
    """
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
            chartstring = Chartstring.objects.get(
                chartstring = request.POST['chartstring'])
            user_requested = User.objects.get(SID=request.POST['user'])

            # Write change to database.
            app_object = App.objects.get(href_name=app)
            app = user_requested.user_apps_set.get(app=app_object)
            app.chartstring = chartstring
            chartstring.remaining = chartstring.remaining - price
            chartstring.save()
            app.date = date.today()
            app.status = 'APPROVED'
            app.save()

            addnotification(user = user_requested, 
                            app = app_object, 
                            code = 'approve')

        elif "revoke" in request.POST:
            app = request.POST['app']
            user_requested = User.objects.get(SID=request.POST['user'])
            # Write change to database.
            app_object = App.objects.get(href_name=app)
            app = user_requested.user_apps_set.get(app=app_object)
            app.delete()

            addnotification(user = user_requested, 
                            app = app_object, 
                            code = 'revoke')

        elif "new" in request.POST:
            new_chartstring = Chartstring(
                nickname=request.POST['nickname'], 
                chartstring=request.POST['chartstring'],
                budget=request.POST['amount'], 
                remaining=request.POST['amount'], 
                manager=user)
            new_chartstring.group = Group.objects.get(
                                    name=request.POST['group'])
            new_chartstring.save()

        request.method = None

    users_of_app = {}
    chart_history = {} 
    for chartstring in Chartstring.objects.all():
        chart_history[chartstring] = chartstring.user_apps_set.all()

    for app in App.objects.all():
        # Generates a list of members in all groups associated with the user.
        members = []
        for group in groups:
            for person in all_users:
                if group in person.groups.all() and person != user:
                    members.append(person)

        users_of_app[app] = []
        for member in members:
            try:
                if member.user_apps_set.get(app=app).group in user.groups.all():
                    requested, downloadable = False, False
                    status = User_Apps.objects.get(app=app, user=member).status

                    if status == 'REQUESTED':
                        requested = True
                    elif status == 'APPROVED':
                        downloadable = True

                    chartstrings = []
                    for group in user.groups.all():
                        for chartstring in group.chartstring_set.all():
                            chartstrings.append(chartstring)

                    users_of_app[app].append(
                        (member, requested, downloadable, chartstrings,))
            except ObjectDoesNotExist:
                pass

    all_chartstrings, all_members = {}, {}

    for group in groups:
        chartstrings = group.chartstring_set.all()
        chartstrings = sorted(chartstrings, 
                            key=lambda chartstring: chartstring.nickname)
        all_chartstrings[group] = [(group.name, chartstrings,)]
        print all_chartstrings

        members = []
        for person in all_users:
            if group in person.groups.all() and person != user:
                members.append(person)

        all_members[group] = [(group.name, members,)]

    con = Context({
        'username': request.session['user'],
        'groups': groups,
        'users_of_app' : users_of_app,
        'all_members': all_members,
        'all_chartstrings': all_chartstrings,
        'all_users': all_users,
        'chart_history': chart_history
        })

    con.update(csrf(request))

    return render_to_response('manage.html', con)

def admin(request):
    """ Defines the administrator view for BearApps.
        Helpdesk and Financing officials are directed to this page.
    """
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    user = User.objects.get(name=request.session['user'])
    all_users = User.objects.all()
    user_summary = {}
    count = 0

    for person in all_users:
        if person != user:
            user_summary[count] = []
            user_summary[count].append((person, person.user_apps_set.all()))
            count += 1

    chartstrings = Chartstring.objects.all()

    con = Context({
        'username': user.name,
        'user_summary': user_summary,
        'chartstrings': chartstrings,
        })

    return render_to_response('admin.html', con)

class RequestForm(forms.Form):
    """ RequestForm is used by Django to validate
        fields in application requests.
    """
    app = forms.CharField()
