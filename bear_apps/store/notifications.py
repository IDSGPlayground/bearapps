from store.models import User, User_Apps, App, Notification, Chartstring, Group
from django.utils import timezone

messages = {
    'request': ' has requested a license for ',
    'approve': 'Your request has been approved for ',
    'reject': 'Your request has been denied for ',
    'revoke': 'Your license has been revoked for ',
}

"""
    addNotification adds a new message to a User in the database.
    Args:
        user = a User object
        app = an App object (NOT a UserApp object)
        code = a key to one of the predefined message above.
"""
def addNotification(user, app, code):
    if code == 'request':
        message = user.Name + messages[code] + app.app_name
    elif code == 'approve' or code == 'reject' or code == 'revoke':
        message = messages[code] + app.app_name

    notification = Notification(user=user, message=message, viewed=False)
    notification.user = user
    notification.save()