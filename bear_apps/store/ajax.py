""" ajax module """
from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from store.models import User, User_Apps, App, Chartstring, Group
from notifications import delete_Notifications


def message_update(request):
    user = User.objects.get(name=request.session['user'])

    # Debugging statements.
    print '====================================='
    print user.name

    delete_Notifications(user)
    return simplejson.dumps({'message': 'Messages cleared!'})

dajaxice_functions.register(message_update)
