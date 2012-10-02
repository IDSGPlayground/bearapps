""" Defines views in the model-view-controller scheme for Django. """
from django.template import Context
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django import forms
from store.models import User, User_Apps, App, Chartstring, Group
from notifications import add_Notification, get_Notifications
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    """ Defines the login page for BearApps.
        Entering valid login credentials will direct user to /browse.
        An invalid password redirects to this page with a blank password field.
        An invalid username redirects the user to /register.
    """
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
            password = User.objects.get(name=user).password
            if password == request.POST['password']:
                request.session['user'] = user
                sid = User.objects.get(name=user).SID
                request.session['sid'] = sid
                return HttpResponseRedirect('/browse/')
        except ObjectDoesNotExist:
            # Redirects to registration page if username does not exist.
            return HttpResponseRedirect('/register/')

    con = Context({
        'logout': logout,
    })

    con.update(csrf(request))
    return render_to_response('index.html', con)


def register(request):
    """ Defines the registration view for first-time users.
        Note: the user will not be registered if they enter
        a username that already exists in our database.
    """
    con = Context()
    con['groups'] = Group.objects.all()

    if "register" in request.POST:
        # Try clause checks if all fields are filled out.
        try:
            username = request.POST['username']
            studentid = request.POST['SID']
            password = request.POST['password']
            verify = request.POST['verify-password']
            status = request.POST['status']
            group_count = int(request.POST['group_count'])
            groups = []
            for i in range(1, group_count + 1):
                groups.append(request.POST['groups-' + str(i)])
        except (MultiValueDictKeyError, ObjectDoesNotExist):
            con['empty_fields'] = True
            con.update(csrf(request))
            return render_to_response('register.html', con)

        # Checks if passwords match.
        if password != verify:
            con['not_match'] = True
            con.update(csrf(request))
            return render_to_response('register.html', con)

        # Checks if username is already taken.
        for user in User.objects.all():
            if user.name == username:
                con['user_taken'] = True
                con.update(csrf(request))
                return render_to_response('register.html', con)
            if user.SID == studentid:
                con['sid_taken'] = True
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
            SID=studentid,
            password=password,
            user_type=user_type,
            )

        # Adds the new user to selected groups.
        # If group exists, gets Group object, otherwise, creates a new group.
        for group in groups:
            try:
                add_group = Group.objects.get(name=group)
                new_user.groups.add(add_group)
            except ObjectDoesNotExist:
                if user_type == "GENERAL":
                    new_user.delete()
                    con['does_not_exist'] = True
                    con.update(csrf(request))
                    return render_to_response('register.html', con)
                    # if group == '':
                    #     con['blank_group'] = True
                    #     new_user.delete()
                    #     con.update(csrf(request))
                    #     return render_to_response('register.html', con)
                if user_type == "MANAGER" and group != '':
                    add_group = Group.objects.create(name=group)
                    new_user.groups.add(add_group)

            if new_user.user_type == "GENERAL" and add_group != None:
                managers = User.objects.filter(
                    groups=add_group,
                    user_type="MANAGER")
                for manager in managers:
                    add_Notification(
                        user=manager,
                        code="new_user",
                        info={'group': add_group, 'requestor': new_user})

        # Resets request.method, so that POST data is no longer stored.
        request.method = None
        # if len(new_user.groups.filter(name='')) > 0:
        new_user.groups.filter(name='').delete()
        if len(new_user.groups.all()) == 0:
            con['empty_fields'] = True
            new_user.delete()
            con.update(csrf(request))
            return render_to_response('register.html', con)
        # Redirects user to the log in page.
        return HttpResponseRedirect('/')
    elif "cancel" in request.POST:
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
            new_app = User_Apps.objects.create(
                user=user,
                app=app_object,
                status='AVAILABLE')

        new_app.status = 'REQUESTED'
        new_app.group = Group.objects.get(name=request.POST['mygroup'])
        new_app.save()

        managers = User.objects.filter(
                    groups=new_app.group,
                    user_type="MANAGER")
        for manager in managers:
            add_Notification(
                user=manager,
                code="request",
                info={'app': app_object, 'requestor': user})

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

    messages = get_Notifications(user)

    # Context and set-up
    con = Context({
            'username': request.session['user'],
            'sid': request.session['sid'],
            'app_display': app_display,
            'app_info': app_info,
            'messages': messages,
            'notifications': len(messages),
            'groups': sorted(user.groups.all(), key=lambda group: group.name),
        })

    """
    for message in messages:
        message.delete()
    user.notifications = 0
    user.save()"""

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
    if user.user_type != "GENERAL":
        if user.user_type == "ADMIN":
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect('/manage/')
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

    messages = get_Notifications(user)
    notifications = len(messages)

    con = Context({
        'username': request.session['user'],
        'app_display': app_display,
        'app_info': app_info,
        'no_apps': no_apps,
        'notifications': notifications,
        'messages': messages,
        })
    # return HttpResponseRedirect('/manage/')

    return render_to_response('my-apps.html', con)


def manage(request):
    """ Defines the manager view for BearApps. PIs and RSOs are
        directed to this view to manage their user requests and
        chartstrings/budgets.
    """
    if 'user' not in request.session:
        return HttpResponseRedirect('/')

    user = User.objects.get(name=request.session['user'])
    if user.user_type != "MANAGER":
        if user.user_type == "GENERAL":
            return HttpResponseRedirect('/browse/')
        return HttpResponseRedirect('/admin/')
    # Sorts all groups & all users in alphabetical order.
    groups = sorted(user.groups.all(), key=lambda group: group.name)
    all_users = sorted(User.objects.all(), key=lambda user: user.name)
    all_users.remove(user)

    # groups contains all of the manager's groups
    # all_users contains all of the users in the manager's groups excluding the manager
    if request.method == 'POST':
        if "approve" in request.POST:
            app = request.POST['app']
            price = App.objects.get(href_name=app).price
            chartstring = Chartstring.objects.get(
                chartstring=request.POST['chartstring'])
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

            add_Notification(user=user_requested,
                            info={'app': app_object},
                            code='approve')

        elif "revoke" in request.POST:
            app = request.POST['app']
            user_requested = User.objects.get(SID=request.POST['user'])
            # Write change to database.
            app_object = App.objects.get(href_name=app)
            app = user_requested.user_apps_set.get(app=app_object)
            app.delete()

            add_Notification(user=user_requested,
                            info={'app': app_object},
                            code='revoke')
        elif "reject" in request.POST:
            app = request.POST['app']
            app_object = App.objects.get(href_name=app)
            user_requested = User.objects.get(SID=request.POST['user'])
            app = user_requested.user_apps_set.get(app=app_object)
            app.delete()
            add_Notification(user=user_requested,
                            info={'app': app_object},
                            code='reject')
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

        return HttpResponseRedirect('manage')

    chart_history = {chartstring: chartstring.user_apps_set.all() for chartstring in Chartstring.objects.all()}

    members = filter(lambda member: len(set(member.groups.all()).intersection(set(groups))) > 0, all_users)

    users_of_app = {}
    for member in members:
        chartstrings = filter(lambda chartstring: chartstring.group in user.groups.all() and chartstring.group in member.groups.all(), Chartstring.objects.all())
        user_apps = filter(lambda user_app: user_app.group in user.groups.all(), member.user_apps_set.all())

        for user_app in user_apps:
            if user_app.app in users_of_app:
                users_of_app[user_app.app].append((member, user_app.status, chartstrings))
            else:
                users_of_app[user_app.app] = [(member, user_app.status, chartstrings)]

    temp_chartstrings = []
    chartstrings = []

    for group in groups:
        temp_chartstrings = sorted(Chartstring.objects.filter(group=group),
                        key=lambda chartstring: chartstring.nickname.lower())
        for chartstring in temp_chartstrings:
            [chartstrings.append(chartstring) for chartstring in temp_chartstrings if not chartstrings.count(chartstring)]

    members_by_group = {group: [member for member in
                        User.objects.filter(groups=group)
                        if member != user] for group in groups}

    messages = get_Notifications(user)

    con = Context({
        'username': request.session['user'],
        'groups': groups,
        'users_of_app': users_of_app,
        'members_by_group': members_by_group,
        'chartstrings': chartstrings,
        'chart_history': chart_history,
        'messages': messages,
        'notifications': len(messages),
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
    if user.user_type != "ADMIN":
        if user.user_type == "GENERAL":
            return HttpResponseRedirect('/browse/')
        return HttpResponseRedirect('/manage/')

    #don't paste any code above here!
    if request.method == 'POST':
        if "new" in request.POST:
            new_chartstring = Chartstring(
                nickname=request.POST['nickname'],
                chartstring=request.POST['chartstring'],
                budget=request.POST['amount'],
                remaining=request.POST['amount'],
                manager=user)
            new_chartstring.group = Group.objects.get(
                                    name=request.POST['group'])
            new_chartstring.save()

    all_users = User.objects.all()

    groups = Group.objects.all()
    user_groups = user.groups.all()
    # If an admin isn't in every group, add them.
    for group in groups:
        if group not in user_groups:
            user.groups.add(group)

    user_summary = [(member, member.user_apps_set.all())
                        for member in all_users if member != user]

    chartstrings = Chartstring.objects.all()

    messages = get_Notifications(user)

    con = Context({
        'username': user.name,
        'user_summary': user_summary,
        'chartstrings': chartstrings,
        'groups': groups,
        'messages': messages,
        'notifications': len(messages),
        })
    con.update(csrf(request))
    return render_to_response('admin.html', con)


class RequestForm(forms.Form):
    """ RequestForm is used by Django to validate
        fields in application requests.
    """
    app = forms.CharField()
